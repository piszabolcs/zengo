"""Feltöltés eredeti jegyzettel + forgatókönyvvel, és az egyfájlos MP3 kimenet."""

from fastapi.testclient import TestClient

from app.main import create_app
from app.prepare.attach_original import attach_originals, original_blocks
from app.ttsmd.parser import parse
from tests.conftest import needs_ffmpeg
from tests.test_m3_jobs_export import make_state, wait_for

SCRIPT = """---
format: ttsmd/1
title: Illesztés
language: hu
---

# Első tétel. Térerősség

A térerősség megmutatja, mekkora erő hat az egységnyi pozitív töltésre.

E egyenlő F per q.

A Coulomb-törvény szerint két pontszerű töltés között ható erő a távolság négyzetével fordítottan arányos.

# Második tétel. Potenciál

A potenciál az egységnyi töltésen végzett munka a végtelenből idáig.
"""

ORIGINAL = """# 1. Térerősség

A **térerősség** megmutatja, mekkora erő hat az egységnyi pozitív töltésre:

$$E = F/q$$

A Coulomb-törvény szerint két pontszerű töltés között ható erő a távolság négyzetével fordítottan arányos.

# 2. Potenciál

A potenciál az egységnyi töltésen végzett munka a végtelenből idáig.
"""


def test_attach_originals_follows_order():
    text, n = attach_originals(SCRIPT, ORIGINAL)
    assert n == len(original_blocks(ORIGINAL)) == 6
    script, _report = parse(text)
    by_text = {b.text.split(".")[0]: b.original for b in script.blocks}
    assert "**térerősség**" in by_text["A térerősség megmutatja, mekkora erő hat az egységnyi pozitív töltésre"]
    assert by_text["A potenciál az egységnyi töltésen végzett munka a végtelenből idáig"].startswith("A potenciál")
    # a képlet a felolvasott alakjához kerül (vagy a megelőző bekezdéshez), de semmi nem vész el
    joined = "\n".join(b.original or "" for b in script.blocks)
    assert "$$E = F/q$$" in joined and "# 2. Potenciál" in joined


def test_upload_script_and_original(config):
    st = make_state(config)
    with TestClient(create_app(st)) as client:
        r = client.post("/api/projects", data={"voice_id": "dummy-test", "output_mode": "single"}, files={
            "file": ("jegyzet.tts.md", SCRIPT.encode("utf-8"), "text/markdown"),
            "original": ("jegyzet.md", ORIGINAL.encode("utf-8"), "text/markdown"),
        })
        assert r.status_code == 200, r.text
        project = r.json()["project"]
        assert project["settings"]["output_mode"] == "single"
        assert any("illesztettem" in w for w in project["warnings"])
        assert "<!-- eredeti" in st.repo.read_script(st.repo.get_project(project["id"]))
        assert (st.repo.project_dir(project["id"]) / "original.md").exists()
        # az olvasó a feltöltött jegyzetet adja vissza; a Markdown a szöveges nézetben jelenik meg, nem PDF-ként
        r = client.get(f"/api/projects/{project['id']}/original")
        assert r.status_code == 200 and "**térerősség**" in r.text and "inline" in r.headers["content-disposition"]
        assert 'id="reader-pdf"' not in client.get(f"/projects/{project['id']}/reader").text

        # a feltöltött szöveges jegyzet felülírja a forgatókönyvbe ágyazott régi eredetit
        old = SCRIPT.replace("# Második tétel", "<!-- eredeti\nRÉGI BEÁGYAZOTT\n-->\n# Második tétel")
        r = client.post("/api/projects", files={"file": ("x.tts.md", old.encode("utf-8"), "text/markdown"),
                                                "original": ("jegyzet.md", ORIGINAL.encode("utf-8"), "text/markdown")})
        text = st.repo.read_script(st.repo.get_project(r.json()["project"]["id"]))
        assert "RÉGI BEÁGYAZOTT" not in text and "**térerősség**" in text

        # PDF eredeti: az olvasó a PDF-et mutatja, a beágyazott eredeti marad a kiemeléses nézetnek
        pdf = b"%PDF-1.4\n1 0 obj<<>>endobj\ntrailer<<>>\n%%EOF\n"
        r = client.post("/api/projects", files={"file": ("x.tts.md", old.encode("utf-8"), "text/markdown"),
                                                "original": ("jegyzet.pdf", pdf, "application/pdf")})
        assert r.status_code == 200, r.text
        pid = r.json()["project"]["id"]
        assert "RÉGI BEÁGYAZOTT" in st.repo.read_script(st.repo.get_project(pid))
        page = client.get(f"/projects/{pid}/reader").text
        assert 'id="reader-pdf"' in page and 'data-view="pdf"' in page
        r = client.get(f"/api/projects/{pid}/original")
        assert r.status_code == 200 and r.headers["content-type"] == "application/pdf"
        assert client.get(f"/api/projects/{project['id']}x/original").status_code == 404

        # csak eredeti jegyzet: az app maga készíti el a forgatókönyvet
        r = client.post("/api/projects", files={"original": ("jegyzet.md", ORIGINAL.encode("utf-8"), "text/markdown")})
        assert r.status_code == 200, r.text
        # egyik sem: hiba; mindkettő, de a forgatókönyv nem .tts.md: hiba
        assert client.post("/api/projects", files={"file": ("", b"", "text/markdown")}).status_code == 400
        r = client.post("/api/projects", files={"file": ("a.md", b"# A", "text/markdown"),
                                                "original": ("b.md", b"# B", "text/markdown")})
        assert r.status_code == 400


@needs_ffmpeg
def test_single_file_output_keeps_reader_audio(config):
    st = make_state(config)
    with TestClient(create_app(st)) as client:
        pid = client.post("/api/projects", json={"script_text": SCRIPT, "voice_id": "dummy-test"}).json()[
            "project"]["id"]
        assert client.put(f"/api/projects/{pid}/settings", json={"output_mode": "single"}).status_code == 200
        assert client.put(f"/api/projects/{pid}/settings", json={"output_mode": "x"}).status_code == 400
        job = client.post(f"/api/projects/{pid}/jobs", json={"chapters": "all", "formats": ["mp3"]}).json()
        wait_for(lambda: client.get(f"/api/jobs/{job['job_id']}").json()["status"] in ("done", "failed"))
        j = client.get(f"/api/jobs/{job['job_id']}").json()
        assert j["status"] == "done", j
        outs = j["outputs"]
        assert len(outs) == 1 and outs[0].endswith("Illesztés.mp3")
        data = client.get(f"/api/projects/{pid}/reader").json()
        for ch in data["chapters"]:
            r = client.get(ch["audio_url"], headers={"Range": "bytes=0-99"})
            assert r.status_code == 206
