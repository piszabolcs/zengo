from __future__ import annotations

import shutil
import subprocess
import sys
from functools import lru_cache

from fastapi import APIRouter, Depends

from app.api.deps import get_state
from app.audio.ffmpeg import Ffmpeg, FfmpegError
from app.config import ENGINE_DIRS
from app.state import AppState

router = APIRouter()


@lru_cache(maxsize=1)
def gpu_info() -> dict:
    exe = shutil.which("nvidia-smi")
    if not exe:
        return {"available": False}
    try:
        flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        out = subprocess.run([exe, "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader"],
                             capture_output=True, text=True, timeout=10, check=False, creationflags=flags).stdout.strip()
        name, mem, driver = [x.strip() for x in out.splitlines()[0].split(",")]
        return {"available": True, "name": name, "memory": mem, "driver": driver}
    except Exception:  # noqa: BLE001
        return {"available": False}


def ffmpeg_status(state: AppState) -> dict:
    try:
        ff = Ffmpeg(state.config["ffmpeg_path"])
        return {"available": True, "path": str(ff.ffmpeg), "version": ff.version()}
    except FfmpegError as e:
        return {"available": False, "error": str(e)}


def engines_status(state: AppState) -> dict:
    out = {}
    for engine_id in ENGINE_DIRS:
        installed = engine_id == "dummy" or state.config.engine_python(engine_id).exists()
        out[engine_id] = {"installed": installed, "loaded": engine_id in state.manager.workers}
    return out


@router.get("/api/health")
def health(state: AppState = Depends(get_state)) -> dict:
    return {"status": "ok", "ffmpeg": ffmpeg_status(state), "gpu": gpu_info(), "engines": engines_status(state),
            "qa": {"enabled": bool(state.config["qa"]["enabled"]), "loaded": state.qa is not None}}
