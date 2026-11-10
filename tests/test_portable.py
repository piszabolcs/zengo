"""Hordozható mód: egyszeri átköltöztetés a régi adathelyről, útvonalak átírása, a régi adatok érintetlenek."""

import sqlite3
import tomllib

from app import portable


def make_legacy(tmp_path):
    old = tmp_path / "old" / "Felolvaso"
    out = tmp_path / "Music" / "Felolvaso"
    (old / "projects" / "p1").mkdir(parents=True)
    (old / "projects" / "p1" / "script.tts.md").write_text("# Cím\n", encoding="utf-8")
    (old / "voices").mkdir()
    (old / "voices" / "ferfi.wav").write_bytes(b"RIFF")
    (old / "cache" / "ab").mkdir(parents=True)
    (old / "cache" / "ab" / "abc.wav").write_bytes(b"RIFF")
    (out / "Könyv").mkdir(parents=True)
    (out / "Könyv" / "01.mp3").write_bytes(b"ID3")
    (old / "config.toml").write_text(
        f'output_root = "{str(out).replace(chr(92), chr(92) * 2)}"\nffmpeg_path = "C:\\\\x\\\\ffmpeg.exe"\n'
        '[engines.f5_hu]\nvenv_path = "C:\\\\old\\\\venv"\nweights_path = ""\ngpu = true\n'
        '[engines.xtts]\nvenv_path = ""\nweights_path = ""\ngpu = true\n', encoding="utf-8")
    con = sqlite3.connect(old / "felolvaso.db")
    con.execute("CREATE TABLE projects (id TEXT, script_path TEXT, settings_json TEXT)")
    con.execute("CREATE TABLE voices (id TEXT, ref_audio_path TEXT)")
    con.execute("CREATE TABLE cache_entries (chunk_id TEXT, path TEXT, bytes INTEGER)")
    con.execute("INSERT INTO projects VALUES ('p1', ?, '{}')", (str(old / "projects" / "p1" / "script.tts.md"),))
    con.execute("INSERT INTO voices VALUES ('ferfi', ?)", (str(old / "voices" / "ferfi.wav").upper(),))
    con.execute("INSERT INTO cache_entries VALUES ('abc', ?, 4)", (str(old / "cache" / "ab" / "abc.wav"),))
    con.commit()
    con.close()
    return old, out


def test_migrate_copies_and_rewrites_paths(tmp_path):
    old, out = make_legacy(tmp_path)
    root = tmp_path / "Zengo"
    assert portable.migrate(root, old, out) is True
    data, new_out = portable.data_dir(root), portable.output_dir(root)
    assert (data / "projects" / "p1" / "script.tts.md").exists()
    assert (data / "voices" / "ferfi.wav").exists()
    assert (new_out / "Könyv" / "01.mp3").exists()
    con = sqlite3.connect(data / "felolvaso.db")
    assert con.execute("SELECT script_path FROM projects").fetchone()[0] == str(data / "projects" / "p1" / "script.tts.md")
    # kis-nagybetűtől függetlenül felismeri a régi előtagot
    assert con.execute("SELECT ref_audio_path FROM voices").fetchone()[0].lower() == str(
        data / "voices" / "ferfi.wav").lower()
    assert con.execute("SELECT path FROM cache_entries").fetchone()[0].startswith(str(data))
    con.close()
    cfg = tomllib.loads((data / "config.toml").read_text(encoding="utf-8"))
    assert cfg["output_root"] == str(new_out)
    assert cfg["ffmpeg_path"] == "" and cfg["engines"]["f5_hu"]["venv_path"] == ""
    assert "xtts" not in cfg["engines"]
    # a régi adatbázis változatlan
    con = sqlite3.connect(old / "felolvaso.db")
    assert con.execute("SELECT script_path FROM projects").fetchone()[0].startswith(str(old))
    con.close()


def test_migrate_runs_only_once(tmp_path):
    old, out = make_legacy(tmp_path)
    root = tmp_path / "Zengo"
    assert portable.migrate(root, old, out) is True
    assert portable.migrate(root, old, out) is False


def test_migrate_without_legacy_is_noop(tmp_path):
    root = tmp_path / "Zengo"
    assert portable.migrate(root, tmp_path / "nincs", tmp_path / "nincs-out") is False
    assert not (portable.data_dir(root) / "felolvaso.db").exists()


def test_setup_env_points_inside_root(tmp_path, monkeypatch):
    for k in ("FELOLVASO_DATA_DIR", "FELOLVASO_CONFIG_DIR", "FELOLVASO_OUTPUT_ROOT", "PATH"):
        monkeypatch.setenv(k, "")
    (tmp_path / "runtime" / "ffmpeg").mkdir(parents=True)
    portable.setup_env(tmp_path)
    import os

    assert os.environ["FELOLVASO_DATA_DIR"] == str(tmp_path / "data")
    assert os.environ["FELOLVASO_OUTPUT_ROOT"] == str(tmp_path / "Hangoskönyvek")
    assert os.environ["PATH"].startswith(str(tmp_path / "runtime" / "ffmpeg"))
