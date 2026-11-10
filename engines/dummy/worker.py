"""Tesztmotor: szinuszhangot ad, a szöveg hosszával arányos időtartammal (L4-01).

Tesztcélú jelölők a szövegben: `OOMTESZT` (CUDA OOM hiba), `HANGTESZT` (nem válaszol),
`CRASHTESZT` (a folyamat kilép), `FAILONCETESZT` (30 karakternél hosszabb chunkon OOM).
"""

import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from worker_base import ERR_OOM, RpcError, Worker, base_args, serve

SAMPLE_RATE = 24000
SECONDS_PER_CHAR = 0.065


class DummyWorker(Worker):
    def __init__(self) -> None:
        self.voices: dict[str, dict] = {}

    def info(self) -> dict:
        return {"engine_id": "dummy", "version": "1.0", "sample_rate": SAMPLE_RATE, "max_chars": 300,
                "device": "cpu", "supports_reference_audio": False}

    def load_voice(self, voice_id, ref_audio_path, ref_text, params):
        self.voices[voice_id] = params
        return {"ok": True}

    def synthesize(self, chunk_id, text, voice_id, params, out_path):
        if "OOMTESZT" in text:
            raise RpcError(ERR_OOM, "CUDA out of memory (szimulált)")
        if "FAILONCETESZT" in text and len(text) > 30:
            raise RpcError(ERR_OOM, "CUDA out of memory (szimulált, hosszú chunk)")
        if "HANGTESZT" in text:
            time.sleep(3600)
        if "CRASHTESZT" in text:
            os._exit(3)
        if params.get("delay_s"):
            time.sleep(float(params["delay_s"]))
        import numpy as np

        seed = int(params.get("seed", 0))
        freq = 220.0 + (seed % 7) * 30.0
        duration = max(0.3, len(text) * SECONDS_PER_CHAR)
        t = np.arange(int(duration * SAMPLE_RATE)) / SAMPLE_RATE
        env = np.minimum(1.0, np.minimum(t / 0.02, (duration - t) / 0.02))
        samples = 0.3 * np.sin(2 * math.pi * freq * t) * env
        from worker_base import write_wav_int16

        dur = write_wav_int16(out_path, samples, SAMPLE_RATE)
        return {"ok": True, "out_path": out_path, "duration_s": dur}


if __name__ == "__main__":
    base_args()
    serve(DummyWorker)
