"""MCP szerver (stdio): a Felolvasó REST API-ját eszközökként adja Claude-nak (6.9, L9).

Saját logikát nem tartalmaz; minden eszköz egy REST hívás. Indítás:
    uv run --project <repo> felolvaso-mcp
A szolgáltatás címe a FELOLVASO_URL környezeti változóval módosítható (alapértelmezés: http://127.0.0.1:8765).
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import httpx
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

REPO = Path(__file__).resolve().parent.parent
FORMAT_DOC = REPO / "docs" / "ttsmd-format.md"
NOT_RUNNING = "A Felolvasó szolgáltatás nem fut. Indítsd el a start.bat-tal."

mcp = MCPServer(
    name="felolvaso",
    instructions=(
        "Helyi magyar hangoskönyv-készítő. A felolvasási forgatókönyv formátumát a get_script_format adja; "
        "beküldés előtt validate_script-tel ellenőrizd, majd submit_script-tel indítsd a generálást, és "
        "get_job_status-szal kövesd."
    ),
)


def base_url() -> str:
    return os.environ.get("FELOLVASO_URL", "http://127.0.0.1:8765").rstrip("/")


def make_client() -> httpx.Client:
    return httpx.Client(base_url=base_url(), timeout=httpx.Timeout(60.0, connect=5.0))


def _request(method: str, path: str, **kwargs: Any) -> Any:
    try:
        with make_client() as client:
            resp = client.request(method, path, **kwargs)
    except httpx.TransportError as e:
        raise ToolError(NOT_RUNNING) from e
    if resp.status_code >= 400:
        try:
            detail = resp.json().get("detail", resp.text)
        except ValueError:
            detail = resp.text
        raise ToolError(f"A Felolvasó hibát jelzett ({resp.status_code}): {detail}")
    return resp.json()


@mcp.tool()
def get_script_format() -> str:
    """A felolvasási forgatókönyv (.tts.md, ttsmd/1) formátumának leírása."""
    return FORMAT_DOC.read_text(encoding="utf-8")


@mcp.tool()
def list_voices() -> list[dict]:
    """A hangprofilok listája (id, név, motor)."""
    return [{"id": v["id"], "name": v["name"], "engine": v["engine_id"]} for v in _request("GET", "/api/voices")]


@mcp.tool()
def validate_script(script_text: str) -> dict:
    """Forgatókönyv validálása projekt létrehozása nélkül. Visszaadja a hibákat és figyelmeztetéseket sorszámmal."""
    return _request("POST", "/api/validate", json={"script_text": script_text})


@mcp.tool()
def submit_script(script_text: str, project_name: str, voice_id: str | None = None,
                  formats: list[str] | None = None, start: bool = True) -> dict:
    """Forgatókönyv beküldése: projektet hoz létre, és (start=true esetén) elindítja a generálást.

    Validációs hiba esetén nem jön létre projekt; a hibák visszajönnek, hogy javítani lehessen.
    """
    report = validate_script(script_text)
    if report["errors"]:
        return {"project_id": None, "job_id": None, "report": report,
                "message": "A forgatókönyv hibás, nem jött létre projekt. Javítsd a hibákat, és küldd be újra."}
    body: dict[str, Any] = {"script_text": script_text, "name": project_name}
    if voice_id:
        body["voice_id"] = voice_id
    created = _request("POST", "/api/projects", json=body)
    project_id = created["project"]["id"]
    result: dict[str, Any] = {"project_id": project_id, "job_id": None, "report": created["report"]}
    if start:
        job = _request("POST", f"/api/projects/{project_id}/jobs",
                       json={"chapters": "all", "formats": formats or ["mp3", "m4b"]})
        result["job_id"] = job["job_id"]
    return result


@mcp.tool()
def get_job_status(job_id: str) -> dict:
    """Feladat állapota: státusz, haladás, hátralévő idő, és kész állapotban a kimeneti fájlok útvonala."""
    job = _request("GET", f"/api/jobs/{job_id}")
    out = {k: job.get(k) for k in ("status", "phase", "done_chunks", "total_chunks", "percent", "eta_s", "error")}
    out["qa_warnings"] = len(job.get("qa_warnings") or [])
    if job["status"] == "done":
        out["outputs"] = job.get("outputs") or [f["path"] for f in
                                                 _request("GET", f"/api/outputs/{job['project_id']}")["files"]]
    return out


@mcp.tool()
def list_projects() -> list[dict]:
    """A projektek listája (id, név, fejezetszám, utolsó feladat állapota)."""
    return [{"id": p["id"], "name": p["name"], "chapters": p["chapter_count"],
             "last_job": p["last_job"]} for p in _request("GET", "/api/projects")]


@mcp.tool()
def add_lexicon_entry(written: str, spoken: str) -> dict:
    """Bejegyzés a globális kiejtési szótárba (írott alak -> kiejtés)."""
    return _request("POST", "/api/lexicon", json={"written": written, "spoken": spoken})


def main() -> None:
    mcp.run("stdio")


if __name__ == "__main__":
    main()
