"""Hangprofil végpontok (L7-06, FR-04)."""

from __future__ import annotations

import json
import shutil
import uuid
from pathlib import Path

import soundfile as sf
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import Response

from app.api.deps import get_state
from app.api.projects import synthesize_texts
from app.config import ENGINE_DIRS
from app.engines.protocol import DEFAULT_ENGINE_PARAMS, EngineError
from app.normalize.chunker import pack
from app.normalize.hu import Normalizer
from app.state import AppState

router = APIRouter()

TEST_SENTENCE = "Az R ellenállás egyenlő ró szorozva l per A, és ez a harmadik tétel lényege."
REF_MIN_S, REF_MAX_S = 6.0, 30.0
REF_ENGINES = {"f5_hu", "xtts"}


@router.get("/api/voices")
def list_voices(state: AppState = Depends(get_state)) -> list[dict]:
    return state.repo.list_voices()


@router.post("/api/voices")
async def create_voice(request: Request, state: AppState = Depends(get_state)) -> dict:
    form = await request.form()
    name = str(form.get("name") or "").strip()
    engine_id = str(form.get("engine_id") or "").strip()
    ref_text = str(form.get("ref_text") or "").strip() or None
    if not name:
        raise HTTPException(400, "Hiányzó név.")
    if engine_id not in ENGINE_DIRS:
        raise HTTPException(400, f"Ismeretlen motor: {engine_id}")
    try:
        params = json.loads(str(form.get("params") or "{}"))
        assert isinstance(params, dict)
    except (json.JSONDecodeError, AssertionError) as e:
        raise HTTPException(400, "A paraméterek érvénytelen JSON objektumot alkotnak.") from e
    params = {**DEFAULT_ENGINE_PARAMS.get(engine_id, {}), **params}
    upload = form.get("ref_audio")
    has_file = upload is not None and hasattr(upload, "filename") and upload.filename
    builtin = engine_id == "xtts" and bool(params.get("speaker"))  # beépített XTTS hang, referencia nélkül
    if engine_id in REF_ENGINES and not has_file and not builtin:
        raise HTTPException(400, "Ehhez a motorhoz referencia hangminta (WAV) kell.")
    if engine_id in REF_ENGINES and not ref_text and not builtin:
        raise HTTPException(400, "Ehhez a motorhoz a referencia átirata is kell.")
    voice_id = str(form.get("id") or "").strip() or state.repo.unique_voice_id(name)
    ref_path = None
    if has_file:
        tmp = state.config.paths.tmp_dir / f"ref-{uuid.uuid4().hex}.wav"
        with tmp.open("wb") as f:
            shutil.copyfileobj(upload.file, f)
        try:
            info = sf.info(str(tmp))
        except Exception as e:
            tmp.unlink(missing_ok=True)
            raise HTTPException(400, f"A referencia nem olvasható hangfájl: {e}") from e
        if not REF_MIN_S <= info.duration <= REF_MAX_S:
            tmp.unlink(missing_ok=True)
            raise HTTPException(400, f"A referencia hossza {info.duration:.1f} s; 6 és 30 s között kell lennie "
                                     "(ajánlott 6-15 s).")
        dst = state.config.paths.voices_dir / f"{voice_id}.wav"
        shutil.move(str(tmp), dst)
        ref_path = str(dst)
    return state.repo.upsert_voice(voice_id, name, engine_id, ref_path, ref_text, params)


@router.delete("/api/voices/{voice_id}")
def delete_voice(voice_id: str, state: AppState = Depends(get_state)) -> dict:
    voice = state.repo.get_voice(voice_id)
    state.repo.delete_voice(voice_id)
    ref = (voice or {}).get("ref_audio_path")
    if ref and Path(ref).parent == state.config.paths.voices_dir:
        Path(ref).unlink(missing_ok=True)
    return {"ok": True}


@router.post("/api/voices/{voice_id}/test")
def test_voice(voice_id: str, body: dict | None = None, state: AppState = Depends(get_state)) -> Response:
    voice = state.repo.get_voice(voice_id)
    if voice is None:
        raise HTTPException(404, "A hangprofil nem található.")
    text = (body or {}).get("text") or TEST_SENTENCE
    norm, _ = Normalizer(state.repo.lexicon_entries()).normalize(text)
    max_chars = state.runner.max_chars(voice["engine_id"])
    try:
        wav = synthesize_texts(state, voice, voice["params"], pack(norm, max_chars, 350))
    except EngineError as e:
        raise HTTPException(503, f"A motor hibát jelzett: {e.message}") from e
    return Response(content=wav, media_type="audio/wav")
