"""SQLite kapcsolat WAL módban és sémamigráció (L7-02, 8.3)."""

from __future__ import annotations

import re
import sqlite3
import threading
from datetime import UTC, datetime
from pathlib import Path

MIGRATIONS_DIR = Path(__file__).parent / "migrations"


def now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


class Database:
    """Szálanként saját kapcsolat; az írásokat egy zár sorosítja (NFR-04: egy író)."""

    def __init__(self, path: Path):
        self.path = Path(path)
        self._local = threading.local()
        self.write_lock = threading.RLock()
        self.migrate()

    def conn(self) -> sqlite3.Connection:
        c = getattr(self._local, "conn", None)
        if c is None:
            c = sqlite3.connect(self.path, timeout=30, check_same_thread=False)
            c.row_factory = sqlite3.Row
            c.execute("PRAGMA journal_mode=WAL")
            c.execute("PRAGMA foreign_keys=ON")
            c.execute("PRAGMA synchronous=NORMAL")
            self._local.conn = c
        return c

    def close(self) -> None:
        c = getattr(self._local, "conn", None)
        if c is not None:
            c.close()
            self._local.conn = None

    def migrate(self) -> int:
        c = self.conn()
        with self.write_lock:
            c.execute("CREATE TABLE IF NOT EXISTS schema_version (version INTEGER NOT NULL)")
            row = c.execute("SELECT MAX(version) AS v FROM schema_version").fetchone()
            current = row["v"] or 0
            for f in sorted(MIGRATIONS_DIR.glob("*.sql")):
                m = re.match(r"(\d+)_", f.name)
                if not m:
                    continue
                ver = int(m.group(1))
                if ver <= current:
                    continue
                c.executescript(f.read_text(encoding="utf-8"))
                c.execute("INSERT INTO schema_version (version) VALUES (?)", (ver,))
                c.commit()
                current = ver
        return current

    def query(self, sql: str, params: tuple | dict = ()) -> list[sqlite3.Row]:
        return self.conn().execute(sql, params).fetchall()

    def one(self, sql: str, params: tuple | dict = ()) -> sqlite3.Row | None:
        return self.conn().execute(sql, params).fetchone()

    def execute(self, sql: str, params: tuple | dict = ()) -> int:
        with self.write_lock:
            c = self.conn()
            cur = c.execute(sql, params)
            c.commit()
            return cur.rowcount

    def executemany(self, sql: str, rows: list) -> None:
        with self.write_lock:
            c = self.conn()
            c.executemany(sql, rows)
            c.commit()
