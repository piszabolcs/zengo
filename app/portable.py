"""Hordozható mód: minden adat az app mappájában, és egyszeri átköltöztetés a régi telepítésből.

Mappaszerkezet (gyökér = a Zengo.exe mappája):
    data\\            adatbázis, beállítások, projektek, gyorsítótár, hangok, modellek
    Hangoskönyvek\\   kész MP3 / M4B
    runtime\\ffmpeg\\  ffmpeg.exe
"""

from __future__ import annotations

import logging
import os
import shutil
import sqlite3
import tomllib
from pathlib import Path

import tomli_w

log = logging.getLogger(__name__)

OUTPUT_DIR_NAME = "Hangoskönyvek"
MIGRATED_FLAG = ".migrated"


def data_dir(root: Path) -> Path:
    return root / "data"


def output_dir(root: Path) -> Path:
    return root / OUTPUT_DIR_NAME


def setup_env(root: Path) -> None:
    """A meglévő FELOLVASO_* környezeti változókkal a mappán belüli útvonalakra állítja az appot."""
    os.environ["FELOLVASO_DATA_DIR"] = str(data_dir(root))
    os.environ["FELOLVASO_CONFIG_DIR"] = str(data_dir(root))
    os.environ["FELOLVASO_OUTPUT_ROOT"] = str(output_dir(root))
    ff = root / "runtime" / "ffmpeg"
    if ff.is_dir():
        os.environ["PATH"] = f"{ff}{os.pathsep}{os.environ.get('PATH', '')}"


def legacy_dirs() -> tuple[Path, Path]:
    """A régi (Felolvasó) telepítés adatmappája és kimeneti mappája."""
    local = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    old_data = local / "Felolvaso"
    old_out = Path(os.environ.get("USERPROFILE", Path.home())) / "Music" / "Felolvaso"
    cfg = old_data / "config.toml"
    if cfg.exists():
        try:
            old_out = Path(tomllib.loads(cfg.read_text(encoding="utf-8")).get("output_root") or old_out)
        except (OSError, tomllib.TOMLDecodeError):
            pass
    return old_data, old_out


def _replace_prefix(value: str, pairs: list[tuple[str, str]]) -> str:
    for old, new in pairs:
        for o, n in ((old, new), (old.replace("\\", "/"), new.replace("\\", "/"))):
            if value[: len(o)].lower() == o.lower():
                return n + value[len(o):]
    return value


def rewrite_db_paths(db_file: Path, pairs: list[tuple[str, str]]) -> int:
    """Minden szöveges oszlopban a régi útvonal-előtagot az újra cseréli. Visszaadja a módosított cellák számát."""
    con = sqlite3.connect(db_file)
    changed = 0
    try:
        tables = [r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")]
        for t in tables:
            cols = [r[1] for r in con.execute(f'PRAGMA table_info("{t}")') if (r[2] or "").upper() in ("TEXT", "")]
            for c in cols:
                rows = con.execute(f'SELECT rowid, "{c}" FROM "{t}" WHERE typeof("{c}") = \'text\'').fetchall()
                for rowid, val in rows:
                    new = _replace_prefix(val, pairs)
                    if new != val:
                        con.execute(f'UPDATE "{t}" SET "{c}" = ? WHERE rowid = ?', (new, rowid))
                        changed += 1
        con.commit()
    finally:
        con.close()
    return changed


def _copy_db(src: Path, dst: Path) -> None:
    """Konzisztens másolat akkor is, ha a régi app éppen fut (SQLite backup API, WAL-lal együtt)."""
    s = sqlite3.connect(f"file:{src}?mode=ro", uri=True)
    d = sqlite3.connect(dst)
    try:
        s.backup(d)
    finally:
        d.close()
        s.close()


def migrate(root: Path, old_data: Path | None = None, old_out: Path | None = None) -> bool:
    """Első indításkor átmásolja a régi telepítés adatait. A régi mappákhoz nem nyúl.

    Akkor fut, ha a hordozható adatbázis még nincs meg és a régi létezik. Visszaadja, hogy történt-e költözés.
    """
    new_data, new_out = data_dir(root), output_dir(root)
    if old_data is None or old_out is None:
        lo, lout = legacy_dirs()
        old_data, old_out = old_data or lo, old_out or lout
    new_db, old_db = new_data / "felolvaso.db", old_data / "felolvaso.db"
    if new_db.exists() or not old_db.exists():
        return False
    log.info("Átköltöztetés: %s -> %s", old_data, new_data)
    new_data.mkdir(parents=True, exist_ok=True)
    for name in ("projects", "cache", "voices"):
        if (old_data / name).is_dir():
            shutil.copytree(old_data / name, new_data / name, dirs_exist_ok=True)
    if old_out.is_dir():
        shutil.copytree(old_out, new_out, dirs_exist_ok=True)
    if (old_data / "config.toml").exists():
        cfg = tomllib.loads((old_data / "config.toml").read_text(encoding="utf-8"))
        cfg["output_root"] = str(new_out)
        cfg["ffmpeg_path"] = ""
        for eng in cfg.get("engines", {}).values():
            eng["venv_path"] = ""
            eng["weights_path"] = ""
        cfg.get("engines", {}).pop("xtts", None)
        (new_data / "config.toml").write_text(tomli_w.dumps(cfg), encoding="utf-8")
    tmp = new_db.with_suffix(".db.tmp")
    _copy_db(old_db, tmp)
    n = rewrite_db_paths(tmp, [(str(old_data), str(new_data)), (str(old_out), str(new_out))])
    os.replace(tmp, new_db)
    (new_data / MIGRATED_FLAG).write_text(f"{old_data}\n{old_out}\n", encoding="utf-8")
    log.info("Átköltöztetés kész, %d útvonal átírva.", n)
    return True
