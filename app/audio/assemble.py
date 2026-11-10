"""Chunk előkészítés (újramintavételezés, csendvágás, szünet) és fejezet összefűzés (L6-02, L6-03)."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import soundfile as sf

from app.audio.ffmpeg import Ffmpeg, FfmpegError

TARGET_SR = 24000
SILENCE_DB = -45.0
LOUDNORM = "loudnorm=I=-18:TP=-1.5:LRA=11"


@dataclass
class ChunkAudio:
    wav: Path
    pause_after_ms: int


def trim_silence(samples: np.ndarray, sr: int, threshold_db: float = SILENCE_DB) -> np.ndarray:
    """Eleji és végi csend levágása 10 ms-os ablakok RMS értéke alapján."""
    if samples.size == 0:
        return samples
    win = max(1, sr // 100)
    n = samples.size // win
    if n == 0:
        return samples
    frames = samples[: n * win].reshape(n, win)
    rms = np.sqrt(np.mean(frames.astype(np.float64) ** 2, axis=1) + 1e-12)
    loud = np.where(20 * np.log10(rms) > threshold_db)[0]
    if loud.size == 0:
        return samples[:0]
    start = max(0, loud[0] - 1) * win
    end = min(samples.size, (loud[-1] + 2) * win)
    return samples[start:end]


def load_24k_mono(ff: Ffmpeg, src: Path, tmp_dir: Path) -> np.ndarray:
    data, sr = sf.read(str(src), dtype="float32", always_2d=True)
    if sr == TARGET_SR and data.shape[1] == 1:
        return data[:, 0]
    tmp = tmp_dir / (src.stem + ".24k.wav")
    ff.run(["-i", str(src), "-af", f"aresample={TARGET_SR}", "-ac", "1", "-c:a", "pcm_s16le", str(tmp)])
    data, _ = sf.read(str(tmp), dtype="float32", always_2d=True)
    tmp.unlink(missing_ok=True)
    return data[:, 0]


def prepare_chunk(ff: Ffmpeg, chunk: ChunkAudio, out: Path, tmp_dir: Path) -> float:
    samples = trim_silence(load_24k_mono(ff, chunk.wav, tmp_dir), TARGET_SR)
    pad = np.zeros(int(TARGET_SR * chunk.pause_after_ms / 1000), dtype=np.float32)
    sf.write(str(out), np.concatenate([samples, pad]), TARGET_SR, subtype="PCM_16")
    return (samples.size + pad.size) / TARGET_SR


def concat_wavs(ff: Ffmpeg, parts: list[Path], out: Path, work_dir: Path) -> None:
    """ffmpeg concat demuxer."""
    lst = work_dir / (out.stem + ".concat.txt")
    lines = []
    for p in parts:
        escaped = str(p.resolve()).replace("\\", "/").replace("'", r"'\''")
        lines.append(f"file '{escaped}'")
    lst.write_text("\n".join(lines) + "\n", encoding="utf-8")
    ff.run(["-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(out)])
    lst.unlink(missing_ok=True)


def build_chapter(ff: Ffmpeg, chunks: list[ChunkAudio], out: Path, work_dir: Path) -> list[float]:
    """Chunkokból összefűzött fejezet WAV (még normalizálatlan).

    Visszaadja a chunkok hosszát szünettel együtt (másodperc), ebből készül az olvasónézet időzítése.
    """
    work_dir.mkdir(parents=True, exist_ok=True)
    parts: list[Path] = []
    durations: list[float] = []
    for i, c in enumerate(chunks):
        p = work_dir / f"{out.stem}.part{i:05d}.wav"
        durations.append(prepare_chunk(ff, c, p, work_dir))
        parts.append(p)
    concat_wavs(ff, parts, out, work_dir)
    for p in parts:
        p.unlink(missing_ok=True)
    return durations


def _speed_filter(speed: float) -> str:
    if abs(speed - 1.0) < 1e-6:
        return ""
    if not 0.8 <= speed <= 1.5:
        raise ValueError("A tempó 0.8 és 1.5 között lehet.")
    return f"atempo={speed:.3f},"


def loudnorm(ff: Ffmpeg, src: Path, out: Path, speed: float = 1.0) -> None:
    """Kétmenetes hangerő-normalizálás, opcionális tempóval."""
    pre = _speed_filter(speed)
    stderr = ff.run(["-i", str(src), "-af", f"{pre}{LOUDNORM}:print_format=json", "-f", "null", "-"])
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", stderr, re.DOTALL)
    if not m:
        raise FfmpegError("A loudnorm mérés nem adott eredményt.")
    meas = json.loads(m.group(0))
    af = (f"{pre}{LOUDNORM}:measured_I={meas['input_i']}:measured_TP={meas['input_tp']}"
          f":measured_LRA={meas['input_lra']}:measured_thresh={meas['input_thresh']}"
          f":offset={meas['target_offset']}:linear=true,aresample={TARGET_SR}")
    tmp = out.with_name(out.stem + ".tmp" + out.suffix)
    ff.run(["-i", str(src), "-af", af, "-ac", "1", "-c:a", "pcm_s16le", str(tmp)])
    os.replace(tmp, out)
