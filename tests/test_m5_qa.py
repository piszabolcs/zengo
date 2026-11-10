import time

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.qa.wer import QaResult, cer, evaluate, length_ratio, wer
from app.state import AppState
from tests.conftest import needs_ffmpeg
from tests.test_m4_engines import REAL

SCRIPT = """---
format: ttsmd/1
title: QA teszt
language: hu
---

# Fejezet

Egyetlen rövid mondat.
"""


# L5-01
@pytest.mark.parametrize("ref,hyp,expected", [
    ("az r ellenállás", "az r ellenállás", 0.0),
    ("Az R ellenállás.", "az r, ellenállás", 0.0),
    ("egy kettő három négy", "egy kettő négy", 0.25),
    ("egy kettő három négy", "egy kettő öt három négy", 0.25),
    ("egy kettő", "három négy", 1.0),
    ("egy kettő három négy", "", 1.0),
    ("", "", 0.0),
])
def test_wer(ref, hyp, expected):
    assert wer(ref, hyp) == pytest.approx(expected)


def test_length_ratio_and_threshold():
    text = "x" * 100
    assert length_ratio(6.0, text) == pytest.approx(0.06)
    assert evaluate(text, text, 6.0).ok
    assert not evaluate(text, text, 2.0).ok      # csonka: 0.02 s/karakter
    assert not evaluate(text, text, 15.0).ok     # túl hosszú: 0.15 s/karakter
    assert not evaluate("egy kettő három négy", "egy kettő", 1.0).ok  # WER 0.5


def test_spelling_variants_pass_by_cer():
    ref = "A ká kulomb-állandó egyenlő négy pí szorozva epszilon nulla, mértékegysége volt méter per amper szekundum."
    hyp = "A ká kulombállandó egyenlő négy pi szorozva epsilon nulla, mértékegysége voltméter per amperszekundum."
    assert wer(ref, hyp) > 0.25
    assert cer(ref, hyp) < 0.05
    assert evaluate(ref, hyp, len(ref) * 0.06).ok
    assert not evaluate("A feszültség nagy, az áram kicsi.", "A feszültség kicsi, az áram nagy.", 2.0).ok


class FakeQa:
    """Az első N próbát elutasítja."""

    def __init__(self, fail_first: int):
        self.fail_first = fail_first
        self.calls = 0

    def check(self, wav, expected, duration):
        self.calls += 1
        ok = self.calls > self.fail_first
        return QaResult(ok=ok, wer=0.0 if ok else 0.9 - self.calls * 0.1, ratio=0.06)


def _run(config, qa, voice_params=None):
    st = AppState(config, qa=qa)
    st.repo.upsert_voice("dummy-test", "Dummy", "dummy", None, None, voice_params or {})
    with TestClient(create_app(st)) as client:
        pid = client.post("/api/projects", json={"script_text": SCRIPT, "voice_id": "dummy-test"}).json()[
            "project"]["id"]
        client.put(f"/api/projects/{pid}/settings", json={"qa_enabled": True})
        jid = client.post(f"/api/projects/{pid}/jobs", json={"formats": ["mp3"]}).json()["job_id"]
        end = time.time() + 300
        while time.time() < end:
            job = client.get(f"/api/jobs/{jid}").json()
            if job["status"] in ("done", "failed"):
                break
            time.sleep(0.2)
        return job, st.repo.job_chunks(jid)


@needs_ffmpeg
def test_regeneration_cycle_success_on_second_try(config):
    job, chunks = _run(config, FakeQa(fail_first=1))
    assert job["status"] == "done"
    body = next(c for c in chunks if c["seq"] == 0)  # az első generált chunk (a fejezetcím)
    assert body["attempts"] == 2 and body["qa_warning"] == 0
    assert job["qa_warnings"] == []


@needs_ffmpeg
def test_regeneration_gives_up_after_two_retries(config):
    qa = FakeQa(fail_first=99)
    job, chunks = _run(config, qa)
    assert job["status"] == "done"
    assert all(c["attempts"] == 3 and c["qa_warning"] == 1 for c in chunks)
    # a legkisebb WER-ű változat marad
    assert [c["wer"] for c in chunks] == [pytest.approx(0.6), pytest.approx(0.3)]
    assert {w["text"] for w in job["qa_warnings"]} == {"Fejezet.", "Egyetlen rövid mondat."}


@pytest.mark.engines
@needs_ffmpeg
@pytest.mark.skipif(not (REAL.paths.models_dir / "whisper-large-v3-turbo" / "model.bin").exists(),
                    reason="whisper modell nincs letöltve")
def test_real_whisper_flags_wrong_audio(config):
    """L5-02: a dummy motor szinuszhangja nem a várt szöveg -> 2 újragenerálás, utána qa_warning."""
    from app.qa.whisper_check import WhisperChecker

    config.data["qa"]["device"] = "cpu"
    qa = WhisperChecker(config, models_dir=REAL.paths.models_dir)
    job, chunks = _run(config, qa)
    assert job["status"] == "done"
    assert all(c["attempts"] == 3 and c["qa_warning"] == 1 for c in chunks)
    assert len(job["qa_warnings"]) == len(chunks)
