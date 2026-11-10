"""config.toml betöltése, alapértelmezések és adatkönyvtárak (NFR-05, L7-01)."""

from __future__ import annotations

import copy
import os
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import tomli_w
from platformdirs import user_config_dir, user_data_dir

APP_NAME = "Felolvaso"
REPO_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_PAUSES = {
    "sentence": 350,
    "paragraph": 700,
    "h3_before": 900,
    "h3_after": 600,
    "h2_before": 1200,
    "h2_after": 800,
    "chapter_title_after": 1500,
    "chapter_end": 2000,
    "list_item": 350,
}

DEFAULTS: dict[str, Any] = {
    "output_root": os.environ.get("FELOLVASO_OUTPUT_ROOT")
    or str(Path(os.environ.get("USERPROFILE", Path.home())) / "Music" / "Felolvaso"),
    "ffmpeg_path": "",
    "default_voice": "piper-anna",
    "announce_chapters": True,
    "log_level": "INFO",
    "pauses": dict(DEFAULT_PAUSES),
    "qa": {"enabled": True, "device": "cpu"},
    "export": {"formats": ["mp3", "m4b"], "speed": 1.0},
    "cache": {"max_gb": 20.0},
    # képletek: a szabályalapú olvasó által nem értett képletekhez helyi nyelvi modell (alapból ki)
    "math_llm": {"enabled": False, "provider": "ollama", "url": "http://127.0.0.1:11434", "model": "qwen3:8b",
                 "timeout_s": 60, "max_formulas": 40},
    "engines": {
        "dummy": {"venv_path": "", "weights_path": "", "gpu": False},
        "piper_hu": {"venv_path": "", "weights_path": "", "gpu": False},
        "f5_hu": {"venv_path": "", "weights_path": "", "gpu": True},
        "xtts": {"venv_path": "", "weights_path": "", "gpu": True},
    },
}

# motor azonosító -> worker csomag mappa az `engines/` alatt
ENGINE_DIRS = {"dummy": "dummy", "piper_hu": "piper", "f5_hu": "f5", "xtts": "xtts"}


def _deep_merge(base: dict, override: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


@dataclass
class Paths:
    config_dir: Path
    data_dir: Path

    @property
    def config_file(self) -> Path:
        return self.config_dir / "config.toml"

    @property
    def db_file(self) -> Path:
        return self.data_dir / "felolvaso.db"

    @property
    def projects_dir(self) -> Path:
        return self.data_dir / "projects"

    @property
    def cache_dir(self) -> Path:
        return self.data_dir / "cache"

    @property
    def voices_dir(self) -> Path:
        return self.data_dir / "voices"

    @property
    def models_dir(self) -> Path:
        return self.data_dir / "models"

    @property
    def logs_dir(self) -> Path:
        return self.data_dir / "logs"

    @property
    def tmp_dir(self) -> Path:
        return self.data_dir / "tmp"

    def ensure(self) -> None:
        for d in (self.config_dir, self.data_dir, self.projects_dir, self.cache_dir, self.voices_dir,
                  self.models_dir, self.logs_dir, self.tmp_dir):
            d.mkdir(parents=True, exist_ok=True)


def default_paths() -> Paths:
    cfg = os.environ.get("FELOLVASO_CONFIG_DIR") or user_config_dir(APP_NAME, appauthor=False)
    data = os.environ.get("FELOLVASO_DATA_DIR") or user_data_dir(APP_NAME, appauthor=False)
    return Paths(Path(cfg), Path(data))


class Config:
    """A config.toml tartalma alapértelmezésekkel kiegészítve."""

    def __init__(self, paths: Paths, data: dict[str, Any]):
        self.paths = paths
        self.data = data

    @classmethod
    def load(cls, paths: Paths | None = None) -> Config:
        paths = paths or default_paths()
        paths.ensure()
        if paths.config_file.exists():
            with paths.config_file.open("rb") as f:
                user = tomllib.load(f)
            data = _deep_merge(DEFAULTS, user)
        else:
            data = copy.deepcopy(DEFAULTS)
            cls(paths, data).save()
        return cls(paths, data)

    def save(self) -> None:
        tmp = self.paths.config_file.with_suffix(".toml.tmp")
        tmp.write_text(tomli_w.dumps(self.data), encoding="utf-8")
        os.replace(tmp, self.paths.config_file)

    def update(self, changes: dict[str, Any]) -> None:
        self.data = _deep_merge(self.data, changes)
        self.save()

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    @property
    def output_root(self) -> Path:
        return Path(self.data["output_root"])

    def engine_dir(self, engine_id: str) -> Path:
        return REPO_ROOT / "engines" / ENGINE_DIRS[engine_id]

    def engine_python(self, engine_id: str) -> Path:
        """A motor worker saját venv-jének python.exe-je."""
        venv = self.data["engines"].get(engine_id, {}).get("venv_path") or ""
        venv_path = Path(venv) if venv else self.engine_dir(engine_id) / ".venv"
        exe = venv_path / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        return exe

    def engine_weights(self, engine_id: str) -> Path:
        w = self.data["engines"].get(engine_id, {}).get("weights_path") or ""
        return Path(w) if w else self.paths.models_dir / engine_id

    def engine_is_gpu(self, engine_id: str) -> bool:
        return bool(self.data["engines"].get(engine_id, {}).get("gpu", False))
