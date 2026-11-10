"""Az alkalmazás egyetlen állapotobjektuma: konfiguráció, tárolás, motorok, feladatsor."""

from __future__ import annotations

import logging
import logging.handlers

from app.config import Config
from app.engines.manager import EngineManager
from app.jobs.queue import JobQueue
from app.jobs.runner import GpuGate, JobRunner
from app.storage.cache import ChunkCache
from app.storage.db import Database
from app.storage.repo import Repo

log = logging.getLogger(__name__)

DEFAULT_VOICES = [
    ("piper-anna", "Piper Anna", "piper_hu", {"model": "hu_HU-anna-medium"}),
    ("piper-berta", "Piper Berta", "piper_hu", {"model": "hu_HU-berta-medium"}),
    ("piper-imre", "Piper Imre", "piper_hu", {"model": "hu_HU-imre-medium"}),
]


def setup_logging(config: Config) -> None:
    """NFR-03: forgó napló 5 × 5 MB."""
    root = logging.getLogger()
    if any(getattr(h, "_felolvaso", False) for h in root.handlers):
        return
    handler = logging.handlers.RotatingFileHandler(
        config.paths.logs_dir / "felolvaso.log", maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    handler._felolvaso = True  # type: ignore[attr-defined]
    root.addHandler(handler)
    root.setLevel(getattr(logging, str(config.get("log_level", "INFO")).upper(), logging.INFO))


class AppState:
    def __init__(self, config: Config | None = None, qa=None):
        self.config = config or Config.load()
        self.db = Database(self.config.paths.db_file)
        self.repo = Repo(self.db, self.config)
        self.cache = ChunkCache(self.db, self.config.paths.cache_dir)
        self.manager = EngineManager(self.config)
        self.gate = GpuGate()
        self.runner = JobRunner(self)
        self.queue = JobQueue(self)
        self.qa = qa
        self.ensure_default_voices()

    def ensure_default_voices(self) -> None:
        """Csak az első indításkor (üres hanglista): a törölt alaphangok ne jöjjenek vissza."""
        if self.repo.list_voices():
            return
        for vid, name, engine, params in DEFAULT_VOICES:
            self.repo.upsert_voice(vid, name, engine, None, None, params)

    def init_qa(self) -> None:
        """A faster-whisper ellenőrzőt csak akkor töltjük, ha a QA be van kapcsolva."""
        if self.qa is not None or not self.config["qa"]["enabled"]:
            return
        try:
            from app.qa.whisper_check import WhisperChecker

            self.qa = WhisperChecker(self.config)
        except Exception as e:  # noqa: BLE001
            log.warning("A minőségellenőrzés nem érhető el: %s", e)

    def start(self) -> None:
        self.queue.start()

    def stop(self) -> None:
        self.queue.stop()
        self.manager.shutdown_all()
        self.db.close()
