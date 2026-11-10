"""ffmpeg futtatása, hibakimenet elkapása, verzió ellenőrzés (L6-01)."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


class FfmpegError(RuntimeError):
    pass


class FfmpegNotFound(FfmpegError):
    pass


def _winget_candidates() -> list[Path]:
    base = Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "WinGet"
    found = [base / "Links" / "ffmpeg.exe"]
    found += sorted((base / "Packages").glob("Gyan.FFmpeg*/ffmpeg-*/bin/ffmpeg.exe"), reverse=True)
    return found


def find_ffmpeg(configured: str | None = None) -> Path | None:
    if configured:
        p = Path(configured)
        if p.is_dir():
            p = p / ("ffmpeg.exe" if sys.platform == "win32" else "ffmpeg")
        if p.exists():
            return p
    which = shutil.which("ffmpeg")
    if which:
        return Path(which)
    for c in _winget_candidates():
        if c.exists():
            return c
    return None


class Ffmpeg:
    def __init__(self, configured: str | None = None):
        path = find_ffmpeg(configured)
        if path is None:
            raise FfmpegNotFound("Az ffmpeg nem található. Telepítsd, vagy add meg az útvonalát a beállításokban.")
        self.ffmpeg = path
        probe = path.with_name("ffprobe" + path.suffix)
        self.ffprobe = probe if probe.exists() else Path(shutil.which("ffprobe") or "ffprobe")

    def _run(self, exe: Path, args: list[str], timeout: float | None = None) -> subprocess.CompletedProcess:
        flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        proc = subprocess.run([str(exe), *args], capture_output=True, timeout=timeout, check=False, creationflags=flags)
        if proc.returncode != 0:
            tail = proc.stderr.decode("utf-8", "replace").strip().splitlines()[-15:]
            raise FfmpegError(f"{exe.name} hiba (kód {proc.returncode}):\n" + "\n".join(tail))
        return proc

    def run(self, args: list[str], timeout: float | None = None) -> str:
        """ffmpeg futtatása; visszaadja a stderr szövegét (a loudnorm mérés ott jelenik meg)."""
        proc = self._run(self.ffmpeg, ["-hide_banner", "-nostdin", "-y", *args], timeout)
        return proc.stderr.decode("utf-8", "replace")

    def probe(self, args: list[str]) -> dict:
        proc = self._run(self.ffprobe, ["-v", "error", "-print_format", "json", *args])
        return json.loads(proc.stdout.decode("utf-8", "replace") or "{}")

    def version(self) -> str:
        proc = self._run(self.ffmpeg, ["-version"])
        first = proc.stdout.decode("utf-8", "replace").splitlines()[0]
        m = re.search(r"ffmpeg version (\S+)", first)
        return m.group(1) if m else first

    def duration(self, path: Path) -> float:
        info = self.probe(["-show_entries", "format=duration", str(path)])
        return float(info.get("format", {}).get("duration", 0.0))
