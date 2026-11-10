import asyncio
import os
import sys
import time

import pytest
from fastapi.testclient import TestClient

import mcp_server.server as srv
from app.main import create_app
from app.state import AppState
from tests.conftest import needs_ffmpeg
from tests.test_m3_jobs_export import SCRIPT3


@pytest.fixture
def api(config, monkeypatch):
    st = AppState(config)
    st.repo.upsert_voice("dummy-test", "Dummy", "dummy", None, None, {})
    client = TestClient(create_app(st))
    with client:
        monkeypatch.setattr(srv, "make_client", lambda: _NoClose(client))
        yield st


class _NoClose:
    """A TestClient ne záródjon le az eszközhívás `with` blokkja után."""

    def __init__(self, c):
        self.c = c

    def __enter__(self):
        return self.c

    def __exit__(self, *a):
        return False


def test_format_voices_validate(api):
    assert "ttsmd/1" in srv.get_script_format() and "[[pause N]]" in srv.get_script_format()
    voices = srv.list_voices()
    assert {"id": "dummy-test", "name": "Dummy", "engine": "dummy"} in voices
    report = srv.validate_script(SCRIPT3.replace("ttsmd/1", "ttsmd/2"))
    assert report["errors"] and report["errors"][0]["line"] == 1


def test_submit_invalid_creates_no_project(api):
    res = srv.submit_script("# Nincs front matter\n", "Hibás")
    assert res["project_id"] is None and res["report"]["errors"]
    assert srv.list_projects() == []


@needs_ffmpeg
def test_submit_and_follow_job(api):
    res = srv.submit_script(SCRIPT3, "MCP projekt", voice_id="dummy-test", formats=["mp3", "m4b"])
    assert res["project_id"] and res["job_id"]
    end = time.time() + 60
    status = srv.get_job_status(res["job_id"])
    while status["status"] not in ("done", "failed") and time.time() < end:
        time.sleep(0.2)
        status = srv.get_job_status(res["job_id"])
    assert status["status"] == "done", status
    assert len(status["outputs"]) == 4 and any(o.endswith(".m4b") for o in status["outputs"])
    assert srv.list_projects()[0]["name"] == "MCP projekt"
    assert srv.add_lexicon_entry("AND", "end") == {"ok": True}


def test_service_not_running(monkeypatch):
    monkeypatch.setenv("FELOLVASO_URL", "http://127.0.0.1:9")
    with pytest.raises(Exception, match="nem fut"):
        srv.list_voices()


def test_stdio_protocol_lists_tools():
    """L9-01: valódi MCP kliens stdio-n indítja a szervert, és felsorolja az eszközöket."""
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    async def run():
        params = StdioServerParameters(command=sys.executable, args=["-m", "mcp_server.server"],
                                       cwd=os.getcwd(), env={**os.environ, "FELOLVASO_URL": "http://127.0.0.1:9"})
        async with stdio_client(params) as (r, w), ClientSession(r, w) as s:
            await s.initialize()
            tools = {t.name for t in (await s.list_tools()).tools}
            fmt = await s.call_tool("get_script_format", {})
            err = await s.call_tool("list_voices", {})
            return tools, fmt, err

    tools, fmt, err = asyncio.run(run())
    assert tools == {"get_script_format", "list_voices", "validate_script", "submit_script", "get_job_status",
                     "list_projects", "add_lexicon_entry"}
    assert "ttsmd/1" in fmt.content[0].text
    assert err.is_error and "nem fut" in err.content[0].text
