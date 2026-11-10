"""Az `EngineWorker` JSON-RPC protokoll üzenetei (6.4, L4-01)."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

ERR_OOM = -32001
ERR_WEIGHTS = -32002
ERR_VOICE = -32003


class EngineInfo(BaseModel):
    engine_id: str
    version: str
    sample_rate: int
    max_chars: int
    device: str
    supports_reference_audio: bool


class LoadVoiceParams(BaseModel):
    voice_id: str
    ref_audio_path: str | None = None
    ref_text: str | None = None
    params: dict[str, Any] = Field(default_factory=dict)


class SynthesizeParams(BaseModel):
    chunk_id: str
    text: str
    voice_id: str
    params: dict[str, Any] = Field(default_factory=dict)
    out_path: str


class SynthesizeResult(BaseModel):
    ok: bool
    out_path: str
    duration_s: float
    rtf: float = 0.0


class EngineError(Exception):
    def __init__(self, code: int, message: str):
        super().__init__(f"[{code}] {message}")
        self.code = code
        self.message = message

    @property
    def is_oom(self) -> bool:
        return self.code == ERR_OOM


class EngineTimeout(EngineError):
    def __init__(self, message: str = "A motor nem válaszolt időben."):
        super().__init__(-32010, message)


class EngineCrashed(EngineError):
    def __init__(self, message: str = "A motor folyamata váratlanul leállt."):
        super().__init__(-32011, message)


# A 6.4 táblázat alapértelmezett paraméterei
DEFAULT_ENGINE_PARAMS: dict[str, dict[str, Any]] = {
    "f5_hu": {"nfe_step": 32, "cfg_strength": 2.0, "speed": 1.0, "seed": 0},
    "xtts": {"language": "hu", "temperature": 0.65, "repetition_penalty": 5.0, "speed": 1.0, "seed": 0},
    "piper_hu": {"length_scale": 1.0, "model": "hu_HU-anna-medium"},
    "dummy": {"seed": 0},
}

DEFAULT_MAX_CHARS = {"f5_hu": 300, "xtts": 200, "piper_hu": 500, "dummy": 300}
