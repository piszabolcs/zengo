import os
import shutil
from pathlib import Path

import pytest

from app.config import Config, Paths

FIXTURES = Path(__file__).parent / "fixtures"


def _find_ffmpeg() -> str | None:
    found = shutil.which("ffmpeg")
    if found:
        return found
    base = Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "WinGet" / "Packages"
    for p in base.glob("Gyan.FFmpeg*/ffmpeg-*/bin/ffmpeg.exe"):
        return str(p)
    return None


FFMPEG = _find_ffmpeg()
needs_ffmpeg = pytest.mark.skipif(FFMPEG is None, reason="ffmpeg nem található")


@pytest.fixture
def config(tmp_path: Path) -> Config:
    paths = Paths(tmp_path / "config", tmp_path / "data")
    cfg = Config.load(paths)
    cfg.data["output_root"] = str(tmp_path / "out")
    cfg.data["ffmpeg_path"] = FFMPEG or ""
    cfg.data["qa"]["enabled"] = False
    cfg.data["default_voice"] = "dummy-test"
    cfg.save()
    return cfg
