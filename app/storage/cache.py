"""Chunk WAV gyorsítótár: `<data_dir>/cache/<hash[0:2]>/<hash>.wav` (L7, L7-07)."""

from __future__ import annotations

import os
import shutil
from collections.abc import Iterable
from pathlib import Path

from app.storage.db import Database, now_iso


class ChunkCache:
    def __init__(self, db: Database, root: Path):
        self.db = db
        self.root = Path(root)

    def path_for(self, chunk_id: str) -> Path:
        return self.root / chunk_id[:2] / f"{chunk_id}.wav"

    def has(self, chunk_id: str) -> bool:
        p = self.path_for(chunk_id)
        if not p.exists():
            return False
        self.touch(chunk_id)
        return True

    def touch(self, chunk_id: str) -> None:
        self.db.execute(
            "INSERT INTO cache_entries (chunk_id, path, bytes, last_used_at) VALUES (?, ?, ?, ?) "
            "ON CONFLICT(chunk_id) DO UPDATE SET last_used_at = excluded.last_used_at",
            (chunk_id, str(self.path_for(chunk_id)), self._size(chunk_id), now_iso()),
        )

    def _size(self, chunk_id: str) -> int:
        try:
            return self.path_for(chunk_id).stat().st_size
        except OSError:
            return 0

    def put(self, chunk_id: str, src: Path) -> Path:
        dst = self.path_for(chunk_id)
        dst.parent.mkdir(parents=True, exist_ok=True)
        tmp = dst.with_suffix(".wav.tmp")
        shutil.copyfile(src, tmp)
        os.replace(tmp, dst)
        self.db.execute(
            "INSERT INTO cache_entries (chunk_id, path, bytes, last_used_at) VALUES (?, ?, ?, ?) "
            "ON CONFLICT(chunk_id) DO UPDATE SET path = excluded.path, bytes = excluded.bytes, "
            "last_used_at = excluded.last_used_at",
            (chunk_id, str(dst), dst.stat().st_size, now_iso()),
        )
        return dst

    def total_bytes(self) -> int:
        row = self.db.one("SELECT COALESCE(SUM(bytes), 0) AS b FROM cache_entries")
        return int(row["b"])

    def cleanup(self, max_bytes: int, protected: Iterable[str] = ()) -> list[str]:
        """A legrégebben használt bejegyzések törlése a méretkorlátig. A védett chunkok maradnak."""
        protected_set = set(protected)
        total = self.total_bytes()
        removed: list[str] = []
        if total <= max_bytes:
            return removed
        for row in self.db.query("SELECT chunk_id, path, bytes FROM cache_entries ORDER BY last_used_at ASC"):
            if total <= max_bytes:
                break
            if row["chunk_id"] in protected_set:
                continue
            try:
                Path(row["path"]).unlink(missing_ok=True)
            except OSError:
                continue
            self.db.execute("DELETE FROM cache_entries WHERE chunk_id = ?", (row["chunk_id"],))
            total -= int(row["bytes"] or 0)
            removed.append(row["chunk_id"])
        return removed
