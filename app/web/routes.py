"""Webes felület: szerver által renderelt HTML + htmx részletek (L8, 9. fejezet)."""

from __future__ import annotations

import re
from pathlib import Path

from fastapi import APIRouter, Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api import jobs as jobs_api
from app.api import outputs as outputs_api
from app.api import projects as projects_api
from app.api.deps import get_project_or_404, get_state
from app.api.health import ffmpeg_status
from app.config import ENGINE_DIRS, REPO_ROOT
from app.state import AppState
from app.ttsmd.parser import parse
from app.ttsmd.validator import written_form

WEB_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=str(WEB_DIR / "templates"))
router = APIRouter(include_in_schema=False)

ENGINE_NAMES = {"f5_hu": "F5-TTS (magyar)", "xtts": "XTTS-v2", "piper_hu": "Piper (gyors előnézet)",
                "dummy": "Tesztmotor"}
STATUS_NAMES = {"queued": "Várakozik", "running": "Fut", "paused": "Szüneteltetve", "done": "Kész",
                "failed": "Hiba", "cancelled": "Törölve"}
PHASE_NAMES = {"planning": "Tervezés", "generating": "Hanggenerálás", "exporting": "Export (MP3, M4B)"}


def fmt_duration(seconds) -> str:
    if seconds is None:
        return "–"
    s = int(seconds)
    return f"{s // 3600:d}:{s % 3600 // 60:02d}:{s % 60:02d}"


def fmt_bytes(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024
    return str(n)


templates.env.filters["duration"] = fmt_duration
templates.env.filters["bytes"] = fmt_bytes
def _app_version() -> str:
    """A verzió egyetlen forrása a pyproject.toml."""
    import tomllib

    with (REPO_ROOT / "pyproject.toml").open("rb") as f:
        return tomllib.load(f)["project"]["version"]


APP_NAME = "Zengő"  # a felületen megjelenő név, egy helyen
APP_VERSION = _app_version()
templates.env.globals.update(APP_NAME=APP_NAME, APP_VERSION=APP_VERSION, ENGINE_NAMES=ENGINE_NAMES, STATUS_NAMES=STATUS_NAMES,
                             PHASE_NAMES=PHASE_NAMES)


def render(request: Request, name: str, state: AppState, **ctx) -> HTMLResponse:
    ctx.setdefault("nav", "")
    ctx["ffmpeg"] = ffmpeg_status(state) if not name.startswith("partials/") else None
    return templates.TemplateResponse(request, name, ctx)


# --- projektek ---
@router.get("/", response_class=HTMLResponse)
def projects_page(request: Request, state: AppState = Depends(get_state)):
    projects = [projects_api.project_summary(state, p) for p in state.repo.list_projects()]
    return render(request, "projects.html", state, nav="projects", projects=projects, voices=state.repo.list_voices(),
                  default_voice=state.config["default_voice"])


@router.post("/ui/projects", response_class=HTMLResponse)
async def import_project(request: Request, state: AppState = Depends(get_state)):
    try:
        result = await projects_api.create_project(request, state)
    except HTTPException as e:
        return render(request, "partials/import_result.html", state, error=str(e.detail))
    project = result["project"]
    # minden a hangoskönyv saját oldalán folytatódik: ott látszik a haladás, a hiba és a kész hang is
    form = await request.form()
    if form.get("start_now") == "on" and not result["report"]["errors"]:
        projects_api.start_job(project["id"], projects_api.JobBody(), state)
    resp = HTMLResponse("")
    resp.headers["HX-Redirect"] = f"/projects/{project['id']}"
    return resp


# --- szerkesztő ---
def _issues_ctx(report: dict) -> dict:
    return {"errors": report["errors"], "warnings": report["warnings"]}


@router.get("/projects/{project_id}/reader", response_class=HTMLResponse)
def reader_page(project_id: str, request: Request, state: AppState = Depends(get_state)):
    from app.api.reader import original_file

    p = get_project_or_404(state, project_id)
    orig = original_file(state.repo.project_dir(p["id"]))
    # a PDF-et a böngésző saját nézője mutatja, ugyanúgy, ahogy feltöltötted; a többi formátum a szöveges nézetben
    pdf = orig is not None and orig.suffix.lower() == ".pdf"
    return render(request, "reader.html", state, nav="projects", project=p, original_pdf=pdf)


def _chapters(text: str) -> list[dict]:
    script, _ = parse(text)
    return [{"index": b.chapter_index, "title": written_form(b.text), "line": b.line} for b in script.chapters()]


def _project_ctx(state: AppState, p: dict) -> dict:
    """A hangoskönyv oldalának állapota: hol tart (szöveg, generálás, kész hang), és mi a következő lépés."""
    text = state.repo.read_script(p)
    report = projects_api.validate_for(state, text).model_dump()
    jobs = state.repo.list_jobs(p["id"])
    job = jobs_api.job_view(state, jobs[0], detail=True) if jobs else None
    outputs = outputs_api.list_outputs(p["id"], state)
    has_audio = bool(outputs["files"]) and any(j["status"] == "done" for j in jobs)
    if job and job["status"] in ("queued", "running", "paused", "failed"):
        stage = "run"
    elif has_audio:
        stage = "done"
    else:
        stage = "start"
    return {"project": p, "chapters": _chapters(text), "job": job, "outputs": outputs, "has_audio": has_audio,
            "stage": stage, "live": bool(job) and job["status"] in ("queued", "running"),
            "math": any("képletgyanús blokk" in w for w in p["warnings"]), **_issues_ctx(report)}


@router.get("/projects/{project_id}", response_class=HTMLResponse)
def project_page(project_id: str, request: Request, state: AppState = Depends(get_state)):
    p = get_project_or_404(state, project_id)
    return render(request, "project.html", state, nav="projects", voices=state.repo.list_voices(),
                  **_project_ctx(state, p))


@router.get("/ui/projects/{project_id}/status", response_class=HTMLResponse)
def project_status(project_id: str, request: Request, state: AppState = Depends(get_state)):
    p = get_project_or_404(state, project_id)
    return render(request, "partials/project_status.html", state, **_project_ctx(state, p))


@router.get("/projects/{project_id}/script", response_class=HTMLResponse)
def editor_page(project_id: str, request: Request, state: AppState = Depends(get_state)):
    p = get_project_or_404(state, project_id)
    text = state.repo.read_script(p)
    report = projects_api.validate_for(state, text).model_dump()
    return render(request, "editor.html", state, nav="projects", project=p, script_text=text,
                  chapters=_chapters(text), **_issues_ctx(report))


@router.post("/ui/projects/{project_id}/script", response_class=HTMLResponse)
def save_script(project_id: str, request: Request, script_text: str = Form(...),
                state: AppState = Depends(get_state)):
    get_project_or_404(state, project_id)
    text = script_text.replace("\r\n", "\n")
    report = projects_api.put_script(project_id, projects_api.ScriptBody(script_text=text), state)["report"]
    return render(request, "partials/issues.html", state, saved=True, chapters=_chapters(text), oob_chapters=True,
                  **_issues_ctx(report))


@router.post("/ui/projects/{project_id}/settings", response_class=HTMLResponse)
async def save_project_settings(project_id: str, request: Request, state: AppState = Depends(get_state)):
    get_project_or_404(state, project_id)
    form = await request.form()
    changes = {
        "voice_id": str(form.get("voice_id")),
        "read_footnotes": form.get("read_footnotes") == "on",
        "read_figure_captions": form.get("read_figure_captions") == "on",
        "announce_chapters": form.get("announce_chapters") == "on",
        "qa_enabled": form.get("qa_enabled") == "on",
        # az MP3 mindig készül (fejezetenként vagy egy fájlban), az M4B választható
        "export_formats": ["mp3"] + (["m4b"] if form.get("fmt_m4b") == "on" else []),
        "output_mode": "single" if form.get("output_mode") == "single" else "chapters",
        "export_speed": float(form.get("export_speed") or 1.0),
    }
    try:
        projects_api.put_settings(project_id, changes, state)
    except HTTPException as e:
        return HTMLResponse(f'<p class="banner banner-error" role="alert">{e.detail}</p>')
    return HTMLResponse('<p class="banner banner-ok" role="status">A projekt beállításai mentve.</p>')


@router.post("/ui/projects/{project_id}/jobs")
async def start_job(project_id: str, request: Request, state: AppState = Depends(get_state)):
    p = get_project_or_404(state, project_id)
    form = await request.form()
    chapters = [int(c) for c in form.getlist("chapter")]
    script, _ = parse(state.repo.read_script(p))
    all_idx = [b.chapter_index for b in script.chapters()]
    body = projects_api.JobBody(chapters="all" if not chapters or sorted(chapters) == all_idx else chapters,
                                formats=p["settings"].get("export_formats"))
    try:
        projects_api.start_job(project_id, body, state)
    except HTTPException as e:
        detail = e.detail["message"] if isinstance(e.detail, dict) else e.detail
        return HTMLResponse(f'<p class="banner banner-error" role="alert">{detail}</p>')
    resp = HTMLResponse("")
    resp.headers["HX-Redirect"] = f"/projects/{project_id}"
    return resp


@router.post("/ui/projects/{project_id}/delete", response_class=HTMLResponse)
def delete_project(project_id: str, state: AppState = Depends(get_state)):
    """Leveszi a hangoskönyvet a listáról. A már elkészült hangfájlok a kimeneti mappában maradnak."""
    get_project_or_404(state, project_id)
    if any(j["status"] in ("queued", "running") for j in state.repo.list_jobs(project_id)):
        return HTMLResponse('<p class="banner banner-error" role="alert">Éppen készül a hangja: előbb állítsd le '
                            'a generálást.</p>')
    state.repo.delete_project(project_id)
    resp = HTMLResponse("")
    resp.headers["HX-Redirect"] = "/"
    return resp


@router.post("/ui/projects/{project_id}/open-folder", response_class=HTMLResponse)
def open_folder(project_id: str, state: AppState = Depends(get_state)):
    try:
        outputs_api.open_folder(project_id, state)
    except HTTPException as e:
        return HTMLResponse(f'<span class="issue-error" role="alert">{e.detail}</span>')
    return HTMLResponse('<span role="status">Megnyitva az Intézőben.</span>')


# --- feladatok ---
@router.get("/jobs", response_class=HTMLResponse)
def jobs_page(request: Request, state: AppState = Depends(get_state)):
    jobs = [jobs_api.job_view(state, j, detail=True) for j in state.repo.list_jobs()]
    return render(request, "jobs.html", state, nav="projects", jobs=jobs)


@router.get("/ui/jobs/{job_id}", response_class=HTMLResponse)
def job_card(job_id: str, request: Request, state: AppState = Depends(get_state)):
    job = state.repo.get_job(job_id)
    if job is None:
        return HTMLResponse("")
    # a hangoskönyv oldaláról jövő gombok az egész állapotblokkot frissítik, nem csak a kártyát
    if request.headers.get("HX-Target") == "project-status" and job.get("project_id"):
        return project_status(job["project_id"], request, state)
    return render(request, "partials/job_card.html", state, job=jobs_api.job_view(state, job, detail=True))


@router.post("/ui/jobs/{job_id}/{action}", response_class=HTMLResponse)
def job_action(job_id: str, action: str, request: Request, state: AppState = Depends(get_state)):
    handlers = {"pause": state.queue.pause, "resume": state.queue.resume, "cancel": state.queue.cancel}
    if action not in handlers:
        raise HTTPException(404)
    handlers[action](job_id)
    return job_card(job_id, request, state)


@router.post("/ui/jobs/{job_id}/regenerate/{chunk_id}", response_class=HTMLResponse)
def regenerate_chunk(job_id: str, chunk_id: str, request: Request, state: AppState = Depends(get_state)):
    try:
        jobs_api.regenerate(job_id, {"chunk_id": chunk_id}, state)
    except HTTPException as e:
        return HTMLResponse(f'<p class="banner banner-error" role="alert">{e.detail}</p>')
    return job_card(job_id, request, state)


@router.get("/ui/chunks/{chunk_id}.wav")
def chunk_audio(chunk_id: str, state: AppState = Depends(get_state)):
    if not re.fullmatch(r"[0-9a-f]{64}", chunk_id):
        raise HTTPException(404)
    path = state.cache.path_for(chunk_id)
    if not path.exists():
        raise HTTPException(404, "A chunk hangja nincs a gyorsítótárban.")
    return FileResponse(path, media_type="audio/wav")


# --- hangok ---
@router.get("/voices", response_class=HTMLResponse)
def voices_page(request: Request, state: AppState = Depends(get_state), error: str | None = None,
                created: str | None = None):
    engines = {e: state.config.engine_python(e).exists() for e in ENGINE_DIRS if e != "dummy"}
    return render(request, "voices.html", state, nav="voices", voices=state.repo.list_voices(), engines=engines,
                  error=error, created=created)


@router.post("/ui/voices")
async def create_voice(request: Request, state: AppState = Depends(get_state)):
    from app.api.voices import create_voice as api_create

    try:
        v = await api_create(request, state)
    except HTTPException as e:
        return voices_page(request, state, error=str(e.detail))
    return RedirectResponse(f"/voices?created={v['id']}", status_code=303)


@router.post("/ui/voices/{voice_id}/delete")
def delete_voice(voice_id: str, state: AppState = Depends(get_state)):
    state.repo.delete_voice(voice_id)
    return RedirectResponse("/voices", status_code=303)


# --- kiejtési szótár ---
@router.get("/lexicon", response_class=HTMLResponse)
def lexicon_page(request: Request, state: AppState = Depends(get_state)):
    return render(request, "lexicon.html", state, nav="lexicon", entries=state.repo.lexicon(),
                  voices=state.repo.list_voices(), default_voice=state.config["default_voice"])


@router.post("/ui/lexicon", response_class=HTMLResponse)
def add_lexicon(request: Request, written: str = Form(...), spoken: str = Form(...),
                case_sensitive: str | None = Form(None), state: AppState = Depends(get_state)):
    error = None
    if written.strip() and spoken.strip():
        state.repo.add_lexicon_entry(written.strip(), spoken.strip(), case_sensitive == "on")
    else:
        error = "Az írott alak és a kiejtés sem lehet üres."
    return render(request, "partials/lexicon_rows.html", state, entries=state.repo.lexicon(), error=error)


@router.post("/ui/lexicon/delete", response_class=HTMLResponse)
def delete_lexicon(request: Request, written: str = Form(...), state: AppState = Depends(get_state)):
    state.repo.delete_lexicon_entry(written)
    return render(request, "partials/lexicon_rows.html", state, entries=state.repo.lexicon())


# --- beállítások ---
@router.get("/settings", response_class=HTMLResponse)
def settings_page(request: Request, state: AppState = Depends(get_state), saved: int = 0):
    return render(request, "settings.html", state, nav="settings", cfg=state.config.data, saved=bool(saved),
                  voices=state.repo.list_voices(), cache_bytes=state.cache.total_bytes())


@router.post("/ui/settings")
async def save_settings(request: Request, state: AppState = Depends(get_state)):
    form = await request.form()
    pauses = {}
    for key in state.config["pauses"]:
        val = form.get(f"pause_{key}")
        if val not in (None, ""):
            pauses[key] = max(0, min(10000, int(float(val))))
    speed = min(1.5, max(0.8, float(form.get("export_speed") or 1.0)))
    changes = {
        "output_root": str(form.get("output_root") or state.config["output_root"]).strip(),
        "ffmpeg_path": str(form.get("ffmpeg_path") or "").strip(),
        "default_voice": str(form.get("default_voice") or state.config["default_voice"]),
        "announce_chapters": form.get("announce_chapters") == "on",
        "pauses": pauses,
        "qa": {"enabled": form.get("qa_enabled") == "on", "device": str(form.get("qa_device") or "cpu")},
        "export": {"formats": [f for f in ("mp3", "m4b") if form.get(f"fmt_{f}") == "on"] or ["mp3"],
                   "speed": speed},
        "cache": {"max_gb": max(1.0, float(form.get("cache_max_gb") or 20))},
    }
    state.config.update(changes)
    return RedirectResponse("/settings?saved=1", status_code=303)


# --- kimenetek ---
@router.get("/outputs", response_class=HTMLResponse)
def outputs_page(request: Request, state: AppState = Depends(get_state)):
    rows = []
    for p in state.repo.list_projects():
        rows.append({"project": p, "outputs": outputs_api.list_outputs(p["id"], state)})
    return render(request, "outputs.html", state, nav="projects", rows=rows)


class RevalidatedStatic(StaticFiles):
    """Frissítés után ne a böngésző régi példánya fusson: mindig újraellenőrzés (ETag, 304)."""

    def file_response(self, *args, **kwargs):
        response = super().file_response(*args, **kwargs)
        response.headers["Cache-Control"] = "no-cache"
        return response


def mount_web(app: FastAPI) -> None:
    app.mount("/static", RevalidatedStatic(directory=str(WEB_DIR / "static")), name="static")
    app.include_router(router)


__all__ = ["mount_web"]
