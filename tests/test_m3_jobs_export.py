import re
import time
from pathlib import Path

import numpy as np
import pytest
import soundfile as sf
from fastapi.testclient import TestClient

from app.audio.assemble import ChunkAudio, build_chapter, loudnorm
from app.audio.export_m4b import export_m4b
from app.audio.export_mp3 import export_mp3
from app.audio.ffmpeg import Ffmpeg
from app.config import Config
from app.main import create_app
from app.state import AppState
from tests.conftest import needs_ffmpeg

pytestmark = needs_ffmpeg

SCRIPT3 = """---
format: ttsmd/1
title: Három fejezet
author: Teszt Elek
language: hu
---

# Első fejezet

Ez az első fejezet első bekezdése. Van benne két mondat.

Második bekezdés 3 V-tal.

# Második fejezet

## Alcím

Itt a második fejezet szövege, kicsit hosszabban, hogy több chunk legyen belőle.

# Harmadik fejezet

Utolsó fejezet. Vége.
"""


def tone(path: Path, seconds: float, sr: int = 24000, lead_silence: float = 0.0) -> Path:
    t = np.arange(int(seconds * sr)) / sr
    data = 0.3 * np.sin(2 * np.pi * 330 * t)
    data = np.concatenate([np.zeros(int(lead_silence * sr)), data, np.zeros(int(lead_silence * sr))])
    sf.write(str(path), data.astype(np.float32), sr, subtype="PCM_16")
    return path


@pytest.fixture
def ff(config) -> Ffmpeg:
    return Ffmpeg(config["ffmpeg_path"])


def test_ffmpeg_version(ff):
    v = ff.version()
    assert re.match(r"\d+\.\d+", v)


def test_chapter_length_matches_chunks_and_pauses(ff, tmp_path):
    chunks = [ChunkAudio(tone(tmp_path / "a.wav", 1.0, lead_silence=0.3), 500),
              ChunkAudio(tone(tmp_path / "b.wav", 2.0, sr=22050), 700),
              ChunkAudio(tone(tmp_path / "c.wav", 1.5, lead_silence=0.2), 2000)]
    out = tmp_path / "ch.wav"
    build_chapter(ff, chunks, out, tmp_path / "work")
    expected = 1.0 + 2.0 + 1.5 + 0.5 + 0.7 + 2.0
    info = sf.info(str(out))
    assert info.samplerate == 24000 and info.channels == 1
    assert abs(info.duration - expected) / expected < 0.05


def test_loudnorm_mp3_tags_and_m4b_chapters(ff, tmp_path):
    norm_files = []
    for i in range(3):
        raw = tone(tmp_path / f"raw{i}.wav", 6.0)
        norm = tmp_path / f"n{i}.wav"
        loudnorm(ff, raw, norm)
        norm_files.append(norm)
    stats = ff.run(["-i", str(norm_files[0]), "-af", "ebur128", "-f", "null", "-"])
    lufs = float(re.findall(r"I:\s+(-?\d+\.\d) LUFS", stats)[-1])
    assert abs(lufs - (-18.0)) <= 1.0

    cover = tmp_path / "cover.jpg"
    ff.run(["-f", "lavfi", "-i", "color=c=blue:s=300x300", "-frames:v", "1", str(cover)])
    mp3 = export_mp3(ff, norm_files[0], tmp_path / "out" / "01 - Első.mp3", title="Első", album="Könyv",
                     artist="Szerző", track=1, total_tracks=3, cover=cover)
    tags = ff.probe(["-show_format", str(mp3)])["format"]["tags"]
    assert tags["title"] == "Első" and tags["album"] == "Könyv" and tags["artist"] == "Szerző"
    assert tags["track"].startswith("1")

    m4b = export_m4b(ff, [("Első", norm_files[0]), ("Második", norm_files[1]), ("Harmadik", norm_files[2])],
                     tmp_path / "out" / "Könyv.m4b", title="Könyv", artist="Szerző", work_dir=tmp_path / "w",
                     cover=cover)
    chapters = ff.probe(["-show_chapters", str(m4b)])["chapters"]
    assert [c["tags"]["title"] for c in chapters] == ["Első", "Második", "Harmadik"]
    streams = ff.probe(["-show_streams", str(m4b)])["streams"]
    assert any(s.get("disposition", {}).get("attached_pic") == 1 for s in streams)
    assert any(s.get("codec_name") == "aac" for s in streams)


def make_state(config: Config, delay: float = 0.0) -> AppState:
    st = AppState(config)
    st.repo.upsert_voice("dummy-test", "Dummy", "dummy", None, None, {"delay_s": delay} if delay else {})
    return st


def wait_for(fn, timeout=60.0, interval=0.1):
    end = time.time() + timeout
    while time.time() < end:
        v = fn()
        if v:
            return v
        time.sleep(interval)
    raise TimeoutError


def test_full_job_via_api(config):
    st = make_state(config)
    with TestClient(create_app(st)) as client:
        r = client.post("/api/projects", json={"script_text": SCRIPT3, "voice_id": "dummy-test"})
        assert r.status_code == 200, r.text
        pid = r.json()["project"]["id"]
        assert r.json()["report"]["errors"] == []
        assert r.json()["project"]["chapter_count"] == 3
        job_id = client.post(f"/api/projects/{pid}/jobs", json={"chapters": "all",
                                                                 "formats": ["mp3", "m4b"]}).json()["job_id"]
        job = wait_for(lambda: (j := client.get(f"/api/jobs/{job_id}").json())["status"] in
                       ("done", "failed") and j)
        assert job["status"] == "done", job
        assert job["done_chunks"] == job["total_chunks"] > 0
        outs = client.get(f"/api/outputs/{pid}").json()
        names = sorted(f["name"] for f in outs["files"])
        assert names == ["01 - Első fejezet.mp3", "02 - Második fejezet.mp3", "03 - Harmadik fejezet.mp3",
                         "Három fejezet.m4b"]
        ff = Ffmpeg(config["ffmpeg_path"])
        m4b = Path(outs["dir"]) / "Három fejezet.m4b"
        chapters = ff.probe(["-show_chapters", str(m4b)])["chapters"]
        assert [c["tags"]["title"] for c in chapters] == ["Első fejezet", "Második fejezet", "Harmadik fejezet"]

        # forgatókönyv módosítása után csak a megváltozott chunk generálódik újra
        new = SCRIPT3.replace("Utolsó fejezet. Vége.", "Utolsó fejezet. Ez már más.")
        assert client.put(f"/api/projects/{pid}/script", json={"script_text": new}).json()["report"]["errors"] == []
        calls = []
        orig = st.manager.synthesize
        st.manager.synthesize = lambda *a, **k: (calls.append(a[3]), orig(*a, **k))[1]
        job2 = client.post(f"/api/projects/{pid}/jobs", json={"chapters": [2], "formats": ["mp3"]}).json()["job_id"]
        wait_for(lambda: client.get(f"/api/jobs/{job2}").json()["status"] == "done")
        assert calls == ["Utolsó fejezet. Ez már más."]


def test_invalid_script_does_not_start(config):
    st = make_state(config)
    with TestClient(create_app(st)) as client:
        bad = SCRIPT3.replace("format: ttsmd/1", "format: ttsmd/9")
        r = client.post("/api/projects", json={"script_text": bad, "voice_id": "dummy-test"})
        pid = r.json()["project"]["id"]
        assert r.json()["report"]["errors"]
        r = client.post(f"/api/projects/{pid}/jobs", json={})
        assert r.status_code == 422


def test_resume_after_restart(config):
    st1 = make_state(config, delay=0.25)
    with TestClient(create_app(st1)) as client:
        pid = client.post("/api/projects", json={"script_text": SCRIPT3, "voice_id": "dummy-test"}).json()[
            "project"]["id"]
        job_id = client.post(f"/api/projects/{pid}/jobs", json={"formats": ["mp3"]}).json()["job_id"]
        wait_for(lambda: client.get(f"/api/jobs/{job_id}").json()["done_chunks"] >= 2, timeout=30, interval=0.05)
    # a TestClient lezárása leállítja a szolgáltatást (a futó feladat megszakad)
    job = st1.repo.get_job(job_id)
    assert job["status"] == "paused"
    done_before = job["done_chunks"]
    assert 2 <= done_before < job["total_chunks"]

    st2 = make_state(config, delay=0.25)
    calls = []
    orig = st2.manager.synthesize
    st2.manager.synthesize = lambda *a, **k: (calls.append(a[2]), orig(*a, **k))[1]
    with TestClient(create_app(st2)) as client:
        assert client.post(f"/api/jobs/{job_id}/resume").json()["ok"]
        final = wait_for(lambda: (j := client.get(f"/api/jobs/{job_id}").json())["status"] in
                         ("done", "failed") and j)
        assert final["status"] == "done", final
        assert len(calls) == final["total_chunks"] - done_before


def test_pause_resume_cancel_and_failures(config):
    st = make_state(config, delay=0.2)
    with TestClient(create_app(st)) as client:
        pid = client.post("/api/projects", json={"script_text": SCRIPT3, "voice_id": "dummy-test"}).json()[
            "project"]["id"]
        job_id = client.post(f"/api/projects/{pid}/jobs", json={"formats": ["mp3"]}).json()["job_id"]
        wait_for(lambda: client.get(f"/api/jobs/{job_id}").json()["status"] == "running")
        client.post(f"/api/jobs/{job_id}/pause")
        wait_for(lambda: client.get(f"/api/jobs/{job_id}").json()["status"] == "paused")
        client.post(f"/api/jobs/{job_id}/cancel")
        assert client.get(f"/api/jobs/{job_id}").json()["status"] == "cancelled"

        # OOM: a chunk kettévágva elkészül; időtúllépés: egyszer újrapróbálva, utána failed
        st.manager.timeout_s = 2
        text = SCRIPT3.replace("Utolsó fejezet. Vége.", "Első fele FAILONCETESZT. Második fele itt.").replace(
            "Ez az első fejezet első bekezdése.", "Lógó HANGTESZT mondat.")
        pid2 = client.post("/api/projects", json={"script_text": text, "voice_id": "dummy-test"}).json()[
            "project"]["id"]
        job2 = client.post(f"/api/projects/{pid2}/jobs", json={"formats": ["mp3"]}).json()["job_id"]
        final = wait_for(lambda: (j := client.get(f"/api/jobs/{job2}").json())["status"] in
                         ("done", "failed", "paused") and j, timeout=90)
        assert final["status"] == "failed"
        assert len(final["failed_chunks"]) == 1 and "HANGTESZT" in final["failed_chunks"][0]["text"]
        outs = {f["name"] for f in client.get(f"/api/outputs/{pid2}").json()["files"]}
        assert "03 - Harmadik fejezet.mp3" in outs and "01 - Első fejezet.mp3" not in outs


def test_preview_and_voice_test(config):
    st = make_state(config)
    with TestClient(create_app(st)) as client:
        pid = client.post("/api/projects", json={"script_text": SCRIPT3, "voice_id": "dummy-test"}).json()[
            "project"]["id"]
        r = client.post(f"/api/projects/{pid}/preview", json={"line": 10})
        assert r.status_code == 200 and r.headers["content-type"] == "audio/wav"
        assert "Ez az els" in r.headers["x-chunk-texts"].encode().decode("unicode_escape")
        r = client.post(f"/api/projects/{pid}/preview", json={"text": "12 V"})
        assert r.status_code == 200 and len(r.content) > 1000
        r = client.post("/api/voices/dummy-test/test")
        assert r.status_code == 200
        voices = {v["id"] for v in client.get("/api/voices").json()}
        assert {"piper-anna", "dummy-test"} <= voices
        client.put("/api/lexicon", json=[{"written": "AND", "spoken": "end", "case_sensitive": True}])
        assert client.get("/api/lexicon").json()[0]["spoken"] == "end"
        h = client.get("/api/health").json()
        assert h["ffmpeg"]["available"]
