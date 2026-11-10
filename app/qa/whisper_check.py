"""Visszafelismerés faster-whisperrel (6.5, L5-02).

A modell a GPU workerrel nem fut párhuzamosan: a futó feladat egyetlen szálon, chunkonként
felváltva hívja a motort és az ellenőrzőt. Alapértelmezésben CPU-n, `int8` módban fut.
`qa.device = "cuda"` esetén a cuBLAS / cuDNN DLL-eket a GPU-s motorok PyTorch-ából tölti be
(nem kell külön letölteni); ha a GPU nem használható, CPU-ra vált.
"""

from __future__ import annotations

import logging
import os
import sys
import threading
from pathlib import Path

import numpy as np
import soundfile as sf

from app.config import Config
from app.normalize.hu import normalize
from app.qa.wer import QaResult, evaluate

log = logging.getLogger(__name__)

MODEL_NAME = "large-v3-turbo"
ASR_SR = 16000


class WhisperChecker:
    def __init__(self, config: Config, models_dir: Path | None = None):
        from faster_whisper import WhisperModel

        device = config["qa"].get("device", "cpu")
        local = (models_dir or config.paths.models_dir) / f"whisper-{MODEL_NAME}"
        model_path = str(local) if (local / "model.bin").exists() else MODEL_NAME
        if device == "cuda":
            _expose_cuda_dlls(config)
            try:
                self.model = WhisperModel(model_path, device="cuda", compute_type="int8_float16",
                                          local_files_only=model_path != MODEL_NAME)
                # a CUDA könyvtárak csak az első futtatáskor töltődnek be
                list(self.model.transcribe(np.zeros(ASR_SR, dtype=np.float32), language="hu")[0])
            except (RuntimeError, ValueError) as e:
                log.warning("A QA nem futhat GPU-n (%s), CPU-ra váltok.", e)
                device = "cpu"
        compute = "int8_float16" if device == "cuda" else "int8"
        if device != "cuda":
            self.model = WhisperModel(model_path, device="cpu", compute_type=compute,
                                      local_files_only=model_path != MODEL_NAME)
        self.lock = threading.Lock()
        log.info("QA modell betöltve: %s (%s, %s)", model_path, device, compute)

    @staticmethod
    def load_16k(wav: Path) -> np.ndarray:
        """WAV -> 16 kHz mono float32 (a felismerő bemenete; a PyAV dekódolót megkerüljük)."""
        data, sr = sf.read(str(wav), dtype="float32", always_2d=True)
        mono = data.mean(axis=1)
        if sr == ASR_SR:
            return mono
        n = round(len(mono) * ASR_SR / sr)
        return np.interp(np.linspace(0, len(mono) - 1, n), np.arange(len(mono)), mono).astype(np.float32)

    def transcribe(self, wav: Path) -> str:
        return self.transcribe_words(wav)[0]

    def transcribe_words(self, wav: Path) -> tuple[str, list[tuple[str, float, float]]]:
        audio = self.load_16k(wav)
        with self.lock:
            segments, _ = self.model.transcribe(audio, language="hu", beam_size=1, vad_filter=False,
                                                condition_on_previous_text=False, word_timestamps=True)
            segments = list(segments)
        text = " ".join(s.text.strip() for s in segments).strip()
        words = [(w.word.strip(), float(w.start), float(w.end)) for s in segments for w in (s.words or [])]
        return text, words

    def check(self, wav: Path, expected: str, duration_s: float) -> QaResult:
        recognized, words = self.transcribe_words(wav)
        # a felismerő számjegyeket is írhat: ugyanazzal a normalizálóval hozzuk közös alakra
        recognized_norm, _ = normalize(recognized)
        result = evaluate(expected, recognized_norm, duration_s)
        result.words = words
        if not result.ok:
            log.info("QA eltérés (WER %.2f, arány %.3f): %r -> %r", result.wer, result.ratio, expected, recognized)
        return result


def _expose_cuda_dlls(config: Config) -> None:
    """Windowson a GPU-s motorok PyTorch `lib` mappáját a PATH elejére teszi (cuBLAS 12, cuDNN 9)."""
    if sys.platform != "win32":
        return
    from app.config import ENGINE_DIRS

    root = Path(__file__).resolve().parents[2] / "engines"
    dirs = []
    for engine_id in ("f5_hu", "xtts"):
        venv = config["engines"].get(engine_id, {}).get("venv_path") or root / ENGINE_DIRS[engine_id] / ".venv"
        lib = Path(venv) / "Lib" / "site-packages" / "torch" / "lib"
        if (lib / "cublas64_12.dll").exists():
            dirs.append(str(lib))
    if dirs:
        os.environ["PATH"] = os.pathsep.join(dirs + [os.environ.get("PATH", "")])
