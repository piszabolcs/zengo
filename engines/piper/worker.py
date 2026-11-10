"""Piper worker: magyar hu_HU hangok CPU-n, gyors előnézethez (L4-03)."""

import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from worker_base import ERR_VOICE, ERR_WEIGHTS, RpcError, Worker, base_args, serve, write_wav_int16

DEFAULT_MODEL = "hu_HU-anna-medium"


class PiperWorker(Worker):
    def __init__(self, weights: str):
        import piper

        self.piper = piper
        self.weights = Path(weights)
        if not any(self.weights.glob("*.onnx")):
            raise RpcError(ERR_WEIGHTS, f"Nincs Piper hangmodell itt: {self.weights}. "
                                        "Futtasd: uv run python scripts/download_models.py --only piper")
        self.models: dict[str, object] = {}
        self.voice_models: dict[str, str] = {}
        self.version = getattr(piper, "__version__", "1.8")
        self._load(DEFAULT_MODEL if (self.weights / f"{DEFAULT_MODEL}.onnx").exists()
                   else next(self.weights.glob("*.onnx")).stem)

    def _load(self, model: str):
        if model not in self.models:
            path = self.weights / f"{model}.onnx"
            if not path.exists():
                raise RpcError(ERR_VOICE, f"Ismeretlen Piper hang: {model}")
            self.models[model] = self.piper.PiperVoice.load(str(path))
        return self.models[model]

    def info(self) -> dict:
        sr = next(iter(self.models.values())).config.sample_rate
        return {"engine_id": "piper_hu", "version": str(self.version), "sample_rate": sr, "max_chars": 500,
                "device": "cpu", "supports_reference_audio": False}

    def load_voice(self, voice_id, ref_audio_path, ref_text, params):
        model = params.get("model", DEFAULT_MODEL)
        self._load(model)
        self.voice_models[voice_id] = model
        return {"ok": True}

    def synthesize(self, chunk_id, text, voice_id, params, out_path):
        import numpy as np

        model = params.get("model") or self.voice_models.get(voice_id, DEFAULT_MODEL)
        voice = self._load(model)
        cfg = self.piper.SynthesisConfig(length_scale=float(params.get("length_scale", 1.0)))
        parts = [c.audio_float_array for c in voice.synthesize(text, syn_config=cfg)]
        samples = np.concatenate(parts) if parts else np.zeros(1, dtype=np.float32)
        dur = write_wav_int16(out_path, samples, voice.config.sample_rate)
        return {"ok": True, "out_path": out_path, "duration_s": dur}


if __name__ == "__main__":
    args = base_args()
    serve(lambda: PiperWorker(args.weights))
