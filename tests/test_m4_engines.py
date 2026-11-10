"""Valódi motorok (M4). Csak telepített workerrel és súlyokkal futnak: `uv run pytest -m engines`."""

import io
import time
from pathlib import Path

import numpy as np
import pytest
import soundfile as sf
from fastapi.testclient import TestClient

from app.config import Config
from app.main import create_app
from app.state import AppState
from tests.conftest import FFMPEG

REAL = Config.load()
REF_TEXT = ("Jó reggelt kívánok mindenkinek. Ma egy rövid szöveget olvasok fel, lassan és érthetően, "
            "hogy a hangom jól hallható legyen.")
REF_WAV = REAL.paths.voices_dir / "teszt-referencia.wav"


def installed(engine_id: str, *files: str) -> bool:
    w = REAL.engine_weights(engine_id)
    return REAL.engine_python(engine_id).exists() and all((w / f).exists() for f in files)


HAS_PIPER = installed("piper_hu", "hu_HU-anna-medium.onnx")
HAS_F5 = installed("f5_hu", "vocab.txt") and REF_WAV.exists()
HAS_XTTS = installed("xtts", "model.pth") and REF_WAV.exists()

pytestmark = [pytest.mark.engines, pytest.mark.skipif(FFMPEG is None, reason="ffmpeg kell")]

SCRIPT = """---
format: ttsmd/1
title: Motorteszt
language: hu
---

# 1. fejezet. Az ellenállás

Az R ellenállás egyenlő ró szorozva l per A. [[pause 500]]
A 3. tételben 12,5 V-os feszültséget mérünk.

# Második fejezet

Ez a második fejezet rövid szövege.
"""


def _client(config: Config, voices: list[tuple]) -> tuple[TestClient, AppState]:
    """Ideiglenes adatkönyvtár, de a valódi modellek és worker venv-ek."""
    for e in ("piper_hu", "f5_hu", "xtts"):
        config.data["engines"][e]["weights_path"] = str(REAL.engine_weights(e))
    st = AppState(config)
    st.manager._command_orig = st.manager._command

    def command(engine_id):
        cmd, cwd = st.manager._command_orig(engine_id)
        i = cmd.index("--models-dir")
        cmd[i + 1] = str(REAL.paths.models_dir)
        return cmd, cwd

    st.manager._command = command
    for vid, engine, ref, params in voices:
        st.repo.upsert_voice(vid, vid, engine, str(ref) if ref else None, REF_TEXT if ref else None, params)
    return TestClient(create_app(st)), st


def run_job(client: TestClient, voice_id: str, timeout: float = 600) -> dict:
    pid = client.post("/api/projects", json={"script_text": SCRIPT, "voice_id": voice_id,
                                              "name": f"teszt-{voice_id}"}).json()["project"]["id"]
    jid = client.post(f"/api/projects/{pid}/jobs", json={"formats": ["mp3", "m4b"]}).json()["job_id"]
    end = time.time() + timeout
    while time.time() < end:
        job = client.get(f"/api/jobs/{jid}").json()
        if job["status"] in ("done", "failed", "paused"):
            break
        time.sleep(0.5)
    job["outputs_list"] = client.get(f"/api/outputs/{pid}").json()["files"]
    job["project_id"] = pid
    return job


@pytest.mark.parametrize("voice_id,engine,ref,params,needed", [
    ("piper-anna", "piper_hu", None, {"model": "hu_HU-anna-medium"}, HAS_PIPER),
    ("f5-teszt", "f5_hu", REF_WAV, {}, HAS_F5),
    ("xtts-teszt", "xtts", REF_WAV, {}, HAS_XTTS),
])
def test_same_script_runs_on_every_engine(config, voice_id, engine, ref, params, needed):
    if not needed:
        pytest.skip(f"{engine} nincs telepítve")
    client, _st = _client(config, [(voice_id, engine, ref, params)])
    with client:
        job = run_job(client, voice_id)
        assert job["status"] == "done", job
        names = sorted(f["name"] for f in job["outputs_list"])
        assert names == ["01 - Első fejezet. Az ellenállás.mp3", "02 - Második fejezet.mp3", "Motorteszt.m4b"]


@pytest.mark.skipif(not HAS_F5, reason="F5 nincs telepítve")
def test_f5_preview_under_30s_and_voice_upload(config):
    client, st = _client(config, [("f5-teszt", "f5_hu", REF_WAV, {})])
    with client:
        pid = client.post("/api/projects", json={"script_text": SCRIPT, "voice_id": "f5-teszt"}).json()[
            "project"]["id"]
        st.manager.get("f5_hu")  # a modellbetöltés nem része az előhallgatás idejének
        t0 = time.time()
        r = client.post(f"/api/projects/{pid}/preview", json={"line": 9})
        assert r.status_code == 200, r.text
        assert time.time() - t0 < 30
        assert sf.info(io.BytesIO(r.content)).duration > 1.0

        # hangprofil feltöltés: túl rövid referencia elutasítva, érvényes elfogadva, tesztmondat szól
        short = io.BytesIO()
        sf.write(short, np.zeros(24000 * 3, dtype=np.float32), 24000, format="WAV")
        r = client.post("/api/voices", data={"name": "Rövid", "engine_id": "f5_hu", "ref_text": "x"},
                        files={"ref_audio": ("r.wav", short.getvalue(), "audio/wav")})
        assert r.status_code == 400 and "6 és 30" in r.json()["detail"]
        r = client.post("/api/voices", data={"name": "Saját F5", "engine_id": "f5_hu", "ref_text": REF_TEXT},
                        files={"ref_audio": ("ref.wav", Path(REF_WAV).read_bytes(), "audio/wav")})
        assert r.status_code == 200, r.text
        vid = r.json()["id"]
        assert vid == "sajat-f5"
        r = client.post(f"/api/voices/{vid}/test")
        assert r.status_code == 200 and sf.info(io.BytesIO(r.content)).duration > 3.0


@pytest.mark.skipif(not HAS_XTTS, reason="XTTS súlyok kellenek")
def test_xtts_builtin_speaker_without_reference(config):
    client, _st = _client(config, [])
    with client:
        r = client.post("/api/voices", data={"name": "XTTS beépített", "engine_id": "xtts"})
        assert r.status_code == 400
        r = client.post("/api/voices", data={"name": "XTTS Baldur", "engine_id": "xtts",
                                             "params": '{"speaker": "Baldur Sanjin"}'})
        assert r.status_code == 200, r.text
        r = client.post(f"/api/voices/{r.json()['id']}/test")
        assert r.status_code == 200 and sf.info(io.BytesIO(r.content)).duration > 2.0
