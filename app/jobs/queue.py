"""FIFO feladatsor egyetlen háttérszállal (L7-04, 5.2)."""

from __future__ import annotations

import logging
import threading
from typing import TYPE_CHECKING

from app.jobs.runner import Control, JobStopped
from app.storage.db import now_iso

if TYPE_CHECKING:
    from app.state import AppState

log = logging.getLogger(__name__)


class JobQueue:
    def __init__(self, state: AppState):
        self.state = state
        self.wake = threading.Event()
        self.stopping = threading.Event()
        self.thread: threading.Thread | None = None
        self.current: tuple[str, Control] | None = None
        self.lock = threading.Lock()

    def start(self) -> None:
        # újraindításkor a futó feladatok szüneteltetett állapotba kerülnek
        self.state.db.execute("UPDATE jobs SET status = 'paused' WHERE status = 'running'")
        self.cleanup_cache()
        self.thread = threading.Thread(target=self._loop, name="job-queue", daemon=True)
        self.thread.start()

    def cleanup_cache(self) -> None:
        """L7-07: a méretkorlát fölött a legrégebben használt chunkok törlődnek, az aktív projekteké nem."""
        st = self.state
        max_bytes = int(float(st.config["cache"]["max_gb"]) * 1024**3)
        protected = [r["chunk_id"] for r in st.db.query(
            "SELECT DISTINCT c.chunk_id FROM chunks c JOIN jobs j ON j.id = c.job_id "
            "WHERE j.status IN ('queued', 'running', 'paused')")]
        try:
            removed = st.cache.cleanup(max_bytes, protected)
            if removed:
                log.info("Gyorsítótár takarítás: %d chunk törölve", len(removed))
        except Exception:
            log.exception("Gyorsítótár takarítás sikertelen")

    def stop(self, timeout: float = 30.0) -> None:
        self.stopping.set()
        with self.lock:
            if self.current:
                self.current[1].stop = "pause"
        self.wake.set()
        if self.thread:
            self.thread.join(timeout=timeout)

    def _next_job(self) -> str | None:
        row = self.state.db.one("SELECT id FROM jobs WHERE status = 'queued' ORDER BY created_at, rowid LIMIT 1")
        return row["id"] if row else None

    def _loop(self) -> None:
        while not self.stopping.is_set():
            job_id = self._next_job()
            if job_id is None:
                self.wake.wait(timeout=1.0)
                self.wake.clear()
                continue
            self._run(job_id)

    def _run(self, job_id: str) -> None:
        repo = self.state.repo
        control = Control()
        with self.lock:
            self.current = (job_id, control)
        repo.set_job(job_id, status="running", started_at=now_iso(), finished_at=None)
        status, error = "done", None
        try:
            self.state.runner.run(job_id, control)
        except JobStopped as e:
            status, error = e.status, e.message
        except Exception as e:
            log.exception("Feladat hiba: %s", job_id)
            status, error = "failed", str(e)
        finally:
            with self.lock:
                self.current = None
        if self.stopping.is_set() and status == "paused":
            error = None
        fields = {"status": status, "error": error}
        if status in ("done", "failed", "cancelled"):
            fields["finished_at"] = now_iso()
        repo.set_job(job_id, **fields)
        if status in ("done", "failed", "cancelled"):
            self.cleanup_cache()
        prog = self.state.runner.progress.get(job_id)
        if prog:
            prog.phase = status
        log.info("Feladat %s: %s %s", job_id, status, error or "")

    # --- vezérlés ---
    def pause(self, job_id: str) -> bool:
        with self.lock:
            if self.current and self.current[0] == job_id:
                self.current[1].stop = "pause"
                return True
        return self.state.db.execute("UPDATE jobs SET status = 'paused' WHERE id = ? AND status = 'queued'",
                                     (job_id,)) > 0

    def resume(self, job_id: str) -> bool:
        ok = self.state.db.execute(
            "UPDATE jobs SET status = 'queued', error = NULL WHERE id = ? AND status IN ('paused', 'failed')",
            (job_id,)) > 0
        self.wake.set()
        return ok

    def cancel(self, job_id: str) -> bool:
        with self.lock:
            if self.current and self.current[0] == job_id:
                self.current[1].stop = "cancel"
                return True
        return self.state.db.execute(
            "UPDATE jobs SET status = 'cancelled', finished_at = ? WHERE id = ? AND status IN ('queued', 'paused')",
            (now_iso(), job_id)) > 0

    def notify(self) -> None:
        self.wake.set()
