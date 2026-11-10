import re
import time

from fastapi.testclient import TestClient

from app.main import create_app
from app.state import AppState
from tests.conftest import needs_ffmpeg
from tests.test_m3_jobs_export import SCRIPT3


def _client(config):
    st = AppState(config)
    st.repo.upsert_voice("dummy-test", "Dummy", "dummy", None, None, {})
    return TestClient(create_app(st)), st


def test_every_screen_renders_with_one_h1_and_skip_link(config):
    client, _st = _client(config)
    with client:
        pid = client.post("/api/projects", json={"script_text": SCRIPT3, "voice_id": "dummy-test"}).json()[
            "project"]["id"]
        for url in ("/", "/jobs", "/voices", "/lexicon", "/settings", "/outputs", f"/projects/{pid}",
                    f"/projects/{pid}/script", f"/projects/{pid}/reader"):
            r = client.get(url)
            assert r.status_code == 200, url
            assert r.text.count("<h1") == 1, url
            assert 'href="#main"' in r.text and 'lang="hu"' in r.text
            assert re.search(r'aria-current="page"', r.text), url
        assert client.get("/static/htmx.min.js").status_code == 200
        home = client.get("/").text
        assert "Eredeti jegyzet" in home and "Felolvasó forgatókönyv" in home and "psz // v" in home
        # a generálási sor és a kész fájlok a hangoskönyv oldalán vannak, nem külön menüpontban
        assert 'href="/jobs"><svg' not in home and 'href="/outputs"' not in home
        page = client.get(f"/projects/{pid}").text
        assert "Generálás indítása" in page and "Még nincs hang" in page and 'hx-trigger="every 1s"' not in page


def test_import_editor_save_and_issue_lines(config, tmp_path):
    client, st = _client(config)
    with client:
        r = client.post("/ui/projects", files={"file": ("jegyzet.tts.md", SCRIPT3.encode(), "text/markdown")},
                        data={"voice_id": "dummy-test"})
        pid = st.repo.list_projects()[0]["id"]
        assert r.headers.get("HX-Redirect") == f"/projects/{pid}"
        page = client.get(f"/projects/{pid}").text
        assert "Három fejezet" in page and "képletek vannak" not in page and "Generálás indítása" in page
        page = client.get(f"/projects/{pid}/script").text
        assert "Első fejezet" in page and 'data-goto-line="8"' in page
        bad = SCRIPT3.replace("# Második fejezet", "#### Második fejezet")
        r = client.post(f"/ui/projects/{pid}/script", data={"script_text": bad})
        assert "Mentve, de hibás" in r.text and 'data-goto-line="14"' in r.text and "Túl mély" in r.text
        assert 'hx-swap-oob="true"' in r.text
        # a hangoskönyv oldala kiírja a hibát, a szerkesztőre mutat, és nem kínál generálást
        page = client.get(f"/projects/{pid}").text
        assert "1 hiba van" in page and "Túl mély" in page and f'href="/projects/{pid}/script"' in page
        assert "Generálás indítása" not in page
        r = client.post(f"/ui/projects/{pid}/script", data={"script_text": SCRIPT3})
        assert "A forgatókönyv érvényes" in r.text
        r = client.post(f"/ui/projects/{pid}/settings", data={"voice_id": "dummy-test", "qa_enabled": "",
                                                              "fmt_mp3": "on", "export_speed": "1.2"})
        assert "mentve" in r.text
        assert st.repo.get_project(pid)["settings"]["export_formats"] == ["mp3"]


def test_import_with_start_now_queues_job_and_redirects(config):
    client, st = _client(config)
    # a sor indítása nélkül (nincs `with`) a feladat csak sorba kerül, nem fut le
    r = client.post("/ui/projects", files={"file": ("jegyzet.tts.md", SCRIPT3.encode(), "text/markdown")},
                    data={"voice_id": "dummy-test", "start_now": "on"})
    pid = st.repo.list_projects()[0]["id"]
    assert r.headers.get("HX-Redirect") == f"/projects/{pid}"
    jobs = st.repo.list_jobs()
    assert len(jobs) == 1 and jobs[0]["project_id"] == pid and jobs[0]["request"]["chapters"] == "all"
    # a hangoskönyv oldala maga mutatja a haladást, és másodpercenként frissül
    page = client.get(f"/projects/{pid}").text
    assert 'role="progressbar"' in page and page.count('hx-trigger="every 1s"') == 1
    assert f'hx-get="/ui/projects/{pid}/status"' in page


def test_math_banner_for_rule_based_import(config, tmp_path):
    client, _st = _client(config)
    # a szabályalapú képletolvasó által nem értett képlet (mátrix) MATH_SUSPECT lesz, erre jön a sáv
    md = "# Fejezet\n\nA képlet: $A = \\begin{pmatrix}1 & 2\\end{pmatrix}$.\n"
    with client:
        r = client.post("/ui/projects", files={"file": ("jegyzet.md", md.encode(), "text/markdown")})
        assert "Ebben az anyagban képletek vannak" in client.get(r.headers["HX-Redirect"]).text
        ok = "# Fejezet\n\nA képlet: $R = \\rho l / A$.\n"
        r = client.post("/ui/projects", files={"file": ("ok.md", ok.encode(), "text/markdown")})
        assert "Ebben az anyagban képletek vannak" not in client.get(r.headers["HX-Redirect"]).text
        r = client.post("/ui/projects", files={"file": ("x.odt", b"x", "application/octet-stream")})
        assert "banner-error" in r.text and "Nem támogatott" in r.text


@needs_ffmpeg
def test_job_flow_from_ui(config):
    client, st = _client(config)
    with client:
        pid = client.post("/api/projects", json={"script_text": SCRIPT3, "voice_id": "dummy-test"}).json()[
            "project"]["id"]
        r = client.post(f"/ui/projects/{pid}/jobs", data={"chapter": ["0", "2"]})
        assert r.headers.get("hx-redirect") == f"/projects/{pid}"
        job = st.repo.list_jobs()[0]
        assert job["request"]["chapters"] == [0, 2]
        card = client.get(f"/ui/jobs/{job['id']}").text
        assert 'role="progressbar"' in card
        end = time.time() + 60
        while time.time() < end and st.repo.get_job(job["id"])["status"] != "done":
            time.sleep(0.2)
        card = client.get(f"/ui/jobs/{job['id']}").text
        assert "Kész" in card and 'hx-trigger="every 1s"' not in card
        page = client.get(f"/projects/{pid}").text
        assert "Kész a hangoskönyv" in page and "Meghallgatás és olvasás" in page
        assert "01 - Első fejezet.mp3" in page and 'hx-trigger="every 1s"' not in page
        # a szünet gomb a hangoskönyv oldaláról az egész állapotblokkot adja vissza
        r = client.post(f"/ui/jobs/{job['id']}/pause", headers={"HX-Target": "project-status"})
        assert 'id="project-status"' in r.text
        out = client.get("/outputs").text
        assert "01 - Első fejezet.mp3" in out and "03 - Harmadik fejezet.mp3" in out
        r = client.post(f"/ui/projects/{pid}/delete")
        assert r.headers.get("HX-Redirect") == "/" and st.repo.get_project(pid) is None
        assert client.get(f"/projects/{pid}").status_code == 404


def test_lexicon_and_settings_persist(config):
    client, _st = _client(config)
    with client:
        r = client.post("/ui/lexicon", data={"written": "AND", "spoken": "end kapu", "case_sensitive": "on"})
        assert "end kapu" in r.text
        r = client.post("/ui/lexicon/delete", data={"written": "AND"})
        assert "A szótár üres" in r.text
        r = client.post("/ui/settings", data={"output_root": "D:/Hangos", "default_voice": "dummy-test",
                                              "pause_sentence": "400", "qa_device": "cpu", "fmt_m4b": "on",
                                              "export_speed": "1.1", "cache_max_gb": "10"}, follow_redirects=False)
        assert r.status_code == 303
    from app.config import Config

    cfg = Config.load(config.paths)
    assert cfg["output_root"] == "D:/Hangos" and cfg["pauses"]["sentence"] == 400
    assert cfg["export"]["formats"] == ["m4b"] and cfg["qa"]["enabled"] is False
