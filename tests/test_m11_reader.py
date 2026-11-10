"""Olvasónézet: eredeti szöveg a forgatókönyvben, csoportosítás, időzítés és a lejátszás végpontjai."""

from fastapi.testclient import TestClient

from app.main import create_app
from app.reader.view import build_reader, render_markdown
from app.ttsmd.parser import parse
from app.ttsmd.validator import validate_text
from tests.conftest import needs_ffmpeg
from tests.test_m3_jobs_export import make_state, wait_for

SCRIPT = """---
format: ttsmd/1
title: Olvasó teszt
language: hu
---

<!-- eredeti
### 1. Térerősség
-->
# Első tétel. Térerősség

<!-- eredeti
| Jel | Mit jelent |
| --- | --- |
| E | térerősség |
| q | töltés |
-->
## Jelölések

Az E jel a térerősséget jelenti.

A q jel a töltést jelenti.

<!-- eredeti
**Térerősség.** A definíció:

```latex
\\vec E = \\frac{\\vec F}{q}
```
-->
## Térerősség

A definíció: E vektor egyenlő F vektor per q. [[pause 500]]

Saját eredeti nélküli bekezdés, {{Coulomb|kulomb}} nevével.

# Második tétel. Rövid

Csak felolvasott szöveg.
"""


def test_parser_attaches_originals_to_next_block():
    script, issues = parse(SCRIPT)
    assert issues == []
    by_text = {b.text[:12]: b for b in script.blocks}
    assert by_text["Első tétel. "].original == "### 1. Térerősség"
    assert by_text["Jelölések"].original.startswith("| Jel |")
    assert by_text["Az E jel a t"].original is None
    assert "```latex" in by_text["Térerősség"].original
    # a megjegyzés nem változtat a felolvasott szövegen és a validáláson
    _, report = validate_text(SCRIPT)
    assert report.errors == [] and report.warnings == []


def test_groups_and_rendering(tmp_path):
    script, _ = parse(SCRIPT)
    data = build_reader(script, tmp_path)
    ch1, ch2 = data["chapters"]
    assert ch1["title"] == "Első tétel. Térerősség" and not ch1["audio"]
    kinds = [len(g["blocks"]) for g in ch1["groups"]]
    # cím | táblázat + 2 mondat | definíció cím + bekezdés + eredeti nélküli bekezdés
    assert kinds == [1, 3, 3]
    assert "<table>" in ch1["groups"][1]["html"]
    assert 'class="math-display"' in ch1["groups"][2]["html"]
    assert ch2["groups"][0]["html"] == "<h2>Második tétel. Rövid</h2>"
    assert ch2["groups"][1]["html"] == "<p>Csak felolvasott szöveg.</p>"
    assert "<script>" not in render_markdown("<script>x</script>")


@needs_ffmpeg
def test_timing_after_job_and_reader_api(config):
    st = make_state(config)
    with TestClient(create_app(st)) as client:
        pid = client.post("/api/projects", json={"script_text": SCRIPT, "voice_id": "dummy-test"}).json()[
            "project"]["id"]
        job = client.post(f"/api/projects/{pid}/jobs", json={"chapters": "all", "formats": ["mp3"]}).json()
        wait_for(lambda: client.get(f"/api/jobs/{job['job_id']}").json()["status"] in ("done", "failed"))
        data = client.get(f"/api/projects/{pid}/reader").json()
        ch1 = data["chapters"][0]
        assert ch1["audio"] and ch1["synced"] and ch1["audio_url"]
        starts = [g["start"] for g in ch1["groups"]]
        assert starts[0] == 0 and starts == sorted(starts)
        assert all(g["end"] > g["start"] for g in ch1["groups"])
        assert abs(ch1["groups"][-1]["end"] - ch1["duration"]) < 0.01
        r = client.get(ch1["audio_url"], headers={"Range": "bytes=0-99"})
        assert r.status_code == 206 and len(r.content) == 100
        assert client.get(f"/projects/{pid}/reader").status_code == 200

        # a felolvasott szöveg változása után a fejezet már nincs szinkronban; megjegyzés hozzáadása nem számít
        text = st.repo.read_script(st.repo.get_project(pid))
        st.repo.save_script(pid, text.replace("Csak felolvasott", "<!-- eredeti\nÚj\n-->\nCsak felolvasott"))
        data = client.get(f"/api/projects/{pid}/reader").json()
        assert data["chapters"][1]["synced"]
        st.repo.save_script(pid, text.replace("Csak felolvasott szöveg.", "Más szöveg."))
        data = client.get(f"/api/projects/{pid}/reader").json()
        assert data["chapters"][0]["synced"] and not data["chapters"][1]["synced"]
