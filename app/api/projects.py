"""Projekt végpontok: import, forgatókönyv, beállítások, előhallgatás, generálás indítása (L7-03, L7-05)."""

from __future__ import annotations

import io
import json
import shutil
import uuid
from pathlib import Path
from typing import Any

import numpy as np
import soundfile as sf
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import Response
from pydantic import BaseModel

from app.api.deps import get_project_or_404, get_state
from app.engines.protocol import EngineError
from app.normalize.chunker import chunk_hash
from app.normalize.hu import Normalizer
from app.state import AppState
from app.storage.repo import sanitize_filename
from app.ttsmd.models import ValidationReport
from app.ttsmd.parser import parse
from app.ttsmd.validator import validate_text

router = APIRouter()

# kimenet: fejezetenként külön MP3, vagy egyetlen MP3 fejezetjelölőkkel
OUTPUT_MODES = ("chapters", "single")
SUPPORTED_EXT = (".tts.md", ".pdf", ".docx", ".epub", ".md", ".markdown")


def validate_for(state: AppState, text: str) -> ValidationReport:
    norm = Normalizer(state.repo.lexicon_entries())
    _, report = validate_text(text, norm.normalize)
    return report


def report_warnings(report: ValidationReport) -> list[str]:
    return [f"{w.line}. sor: {w.message}" for w in report.warnings]


def _upload(form, key: str):
    """A feltöltött fájl, ha a mező nem üres (a böngésző üres fájlmezőt is elküld)."""
    up = form.get(key)
    return up if up is not None and hasattr(up, "filename") and up.filename else None


def _save_upload(upload, folder: Path) -> Path:
    filename = sanitize_filename(Path(upload.filename or "dokumentum").name, max_len=120)
    if not filename.lower().endswith(SUPPORTED_EXT):
        raise HTTPException(400, "Nem támogatott formátum. Támogatott: PDF, DOCX, EPUB, Markdown, .tts.md.")
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / filename
    with path.open("wb") as f:
        shutil.copyfileobj(upload.file, f)
    return path


def merge_original(script_text: str, original: Path) -> tuple[str, str]:
    """Kész forgatókönyv + külön eredeti jegyzet: az eredeti blokkjai `<!-- eredeti -->` megjegyzésként.

    A feltöltött szöveges jegyzet (Markdown, DOCX) felülírja a forgatókönyvbe ágyazott eredetit. A PDF és az
    EPUB szövegkinyerése gyengébb (a képletek elvesznek), ezért ott a beágyazott eredeti marad a kiemeléses
    nézetben, a PDF-et pedig az olvasó közvetlenül mutatja.
    """
    from app.prepare.attach_original import (
        attach_originals,
        has_originals,
        original_markdown,
        strip_originals,
    )

    if has_originals(script_text):
        if original.suffix.lower() in (".pdf", ".epub"):
            return script_text, ("A forgatókönyv már tartalmaz eredeti részeket, a kiemeléses nézet ezeket "
                                 "használja; a feltöltött jegyzetet az olvasó külön mutatja.")
        script_text = strip_originals(script_text)
    text, n = attach_originals(script_text, original_markdown(original))
    return text, (f"Az eredeti jegyzet {n} blokkját illesztettem a forgatókönyvhöz (olvasónézet). "
                  "A szerkesztőben ellenőrizheted az `eredeti` megjegyzéseket.")


def import_source(state: AppState, path: Path, options: dict) -> tuple[str, str, list[str], bytes | None]:
    """Fájl -> (név, forgatókönyv, figyelmeztetések, borító). `.tts.md` közvetlenül, más az L1 + L2 úton."""
    name = path.name
    if name.lower().endswith(".tts.md"):
        text = path.read_text(encoding="utf-8-sig")
        script, _ = parse(text)
        return (script.title or name[: -len(".tts.md")]), text, [], None
    from app.ingest.registry import load_document
    from app.prepare.math_llm import fallback_for
    from app.prepare.rule_based import prepare

    doc = load_document(path)
    llm = fallback_for(state.config, state.gate)
    text, warnings = prepare(doc, read_footnotes=bool(options.get("read_footnotes")),
                             read_figure_captions=bool(options.get("read_figure_captions")), math_fallback=llm)
    if llm is not None and llm.skipped_gpu:
        warnings.append(f"{llm.skipped_gpu} képlethez nem futott a helyi nyelvi modell, mert GPU-s felolvasás "
                        "fut. Importáld újra, ha a feladat végzett.")
    return doc.title, text, list(doc.warnings) + warnings, doc.cover_image


def project_summary(state: AppState, p: dict) -> dict:
    try:
        script, _ = parse(state.repo.read_script(p))
        chapters = [{"index": b.chapter_index, "title": b.text, "line": b.line} for b in script.chapters()]
    except OSError:
        chapters = []
    jobs = state.repo.list_jobs(p["id"])
    last = jobs[0] if jobs else None
    return {**p, "chapters": chapters, "chapter_count": len(chapters),
            "last_job": {"id": last["id"], "status": last["status"]} if last else None}


def create_from_text(state: AppState, name: str, text: str, source_path: str | None, warnings: list[str],
                     settings: dict, cover: bytes | None = None) -> tuple[dict, ValidationReport]:
    report = validate_for(state, text)
    project = state.repo.create_project(name, text, source_path, warnings + report_warnings(report), settings)
    if cover:
        ext = "png" if cover[:8] == b"\x89PNG\r\n\x1a\n" else "jpg"
        (state.repo.project_dir(project["id"]) / f"cover.{ext}").write_bytes(cover)
    return project, report


@router.get("/api/projects")
def list_projects(state: AppState = Depends(get_state)) -> list[dict]:
    return [project_summary(state, p) for p in state.repo.list_projects()]


@router.post("/api/projects")
async def create_project(request: Request, state: AppState = Depends(get_state)) -> dict:
    ctype = request.headers.get("content-type", "")
    settings: dict[str, Any] = {}
    if ctype.startswith("multipart/form-data"):
        form = await request.form()
        upload, original = _upload(form, "file"), _upload(form, "original")
        if upload is None and original is None:
            raise HTTPException(400, "Adj meg egy eredeti jegyzetet vagy egy kész forgatókönyvet (vagy mindkettőt).")
        for key in ("read_footnotes", "read_figure_captions"):
            settings[key] = str(form.get(key, "")).lower() in ("1", "true", "on", "yes")
        if form.get("voice_id"):
            settings["voice_id"] = str(form.get("voice_id"))
        if form.get("output_mode") in OUTPUT_MODES:
            settings["output_mode"] = str(form.get("output_mode"))
        tmp_dir = state.config.paths.tmp_dir / f"upload-{uuid.uuid4().hex}"
        tmp_dir.mkdir(parents=True)
        try:
            src = _save_upload(upload, tmp_dir / "script") if upload is not None else None
            orig = _save_upload(original, tmp_dir / "original") if original is not None else None
            if src is not None and orig is not None and not src.name.lower().endswith(".tts.md"):
                raise HTTPException(400, "Ha az eredeti jegyzetet is megadod, a másik mezőbe kész .tts.md "
                                         "forgatókönyv kell.")
            try:
                name, text, warnings, cover = import_source(state, src or orig, settings)
                if src is not None and orig is not None:
                    text, note = merge_original(text, orig)
                    warnings.append(note)
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(422, f"A fájl nem nyitható meg: {e}") from e
            if form.get("name"):
                name = str(form.get("name"))
            main = src or orig
            project, report = create_from_text(state, name, text, main.name, warnings, settings, cover)
            pdir = state.repo.project_dir(project["id"])
            shutil.copyfile(main, pdir / ("source" + "".join(main.suffixes[-2:])))
            if orig is not None:
                shutil.copyfile(orig, pdir / ("original" + orig.suffix.lower()))
        finally:
            shutil.rmtree(tmp_dir, ignore_errors=True)
    else:
        body = await request.json()
        text = body.get("script_text")
        if not text:
            raise HTTPException(400, "Hiányzó script_text.")
        script, _ = parse(text)
        name = body.get("name") or body.get("project_name") or script.title or "Névtelen projekt"
        if body.get("voice_id"):
            settings["voice_id"] = body["voice_id"]
        elif script.front_matter.get("voice") and state.repo.get_voice(str(script.front_matter["voice"])):
            settings["voice_id"] = str(script.front_matter["voice"])
        project, report = create_from_text(state, name, text, None, [], settings)
    return {"project": project_summary(state, state.repo.get_project(project["id"])),
            "report": report.model_dump()}


@router.get("/api/projects/{project_id}")
def get_project(project_id: str, state: AppState = Depends(get_state)) -> dict:
    p = get_project_or_404(state, project_id)
    return {**project_summary(state, p), "jobs": state.repo.list_jobs(project_id)}


@router.get("/api/projects/{project_id}/script")
def get_script(project_id: str, state: AppState = Depends(get_state)) -> dict:
    p = get_project_or_404(state, project_id)
    text = state.repo.read_script(p)
    return {"script_text": text, "report": validate_for(state, text).model_dump()}


class ScriptBody(BaseModel):
    script_text: str


@router.put("/api/projects/{project_id}/script")
def put_script(project_id: str, body: ScriptBody, state: AppState = Depends(get_state)) -> dict:
    get_project_or_404(state, project_id)
    report = validate_for(state, body.script_text)
    state.repo.save_script(project_id, body.script_text, report_warnings(report))
    return {"report": report.model_dump()}


SETTINGS_KEYS = {"voice_id", "read_footnotes", "read_figure_captions", "pauses", "announce_chapters",
                 "qa_enabled", "export_formats", "export_speed", "seed", "output_mode"}


@router.put("/api/projects/{project_id}/settings")
def put_settings(project_id: str, body: dict, state: AppState = Depends(get_state)) -> dict:
    get_project_or_404(state, project_id)
    unknown = set(body) - SETTINGS_KEYS
    if unknown:
        raise HTTPException(400, f"Ismeretlen beállítás: {', '.join(sorted(unknown))}")
    if "voice_id" in body and not state.repo.get_voice(body["voice_id"]):
        raise HTTPException(400, "Ismeretlen hangprofil.")
    if "output_mode" in body and body["output_mode"] not in OUTPUT_MODES:
        raise HTTPException(400, "A kimenet módja: chapters (fejezetenként) vagy single (egy fájl).")
    if "export_speed" in body and not 0.8 <= float(body["export_speed"]) <= 1.5:
        raise HTTPException(400, "A tempó 0.8 és 1.5 között lehet.")
    return {"settings": state.repo.update_settings(project_id, body)}


def synthesize_texts(state: AppState, voice: dict, params: dict, items: list[tuple[str, int]]) -> bytes:
    """Chunkok generálása gyorsítótárral, összefűzve egy WAV-ba (előhallgatás, hangteszt)."""
    arrays: list[np.ndarray] = []
    sr = 24000
    work = state.config.paths.tmp_dir / f"preview-{uuid.uuid4().hex}"
    work.mkdir(parents=True)
    try:
        with state.gate.priority():
            for i, (text, pause_ms) in enumerate(items):
                cid = chunk_hash(voice["engine_id"], voice["id"], params, text)
                if not state.cache.has(cid):
                    out = work / f"{i}.wav"
                    state.manager.synthesize(voice["engine_id"], voice, cid, text, params, out)
                    state.cache.put(cid, out)
                data, sr = sf.read(str(state.cache.path_for(cid)), dtype="float32")
                arrays.append(data)
                arrays.append(np.zeros(int(sr * min(pause_ms, 1500) / 1000), dtype=np.float32))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    buf = io.BytesIO()
    sf.write(buf, np.concatenate(arrays) if arrays else np.zeros(1, dtype=np.float32), sr,
             format="WAV", subtype="PCM_16")
    return buf.getvalue()


@router.post("/api/projects/{project_id}/preview")
def preview(project_id: str, body: dict, state: AppState = Depends(get_state)) -> Response:
    p = get_project_or_404(state, project_id)
    runner = state.runner
    voice = runner.resolve_voice(p)
    chunker = runner.make_chunker(p, voice)
    if body.get("block_id"):
        script, _ = parse(state.repo.read_script(p))
        block = next((b for b in script.blocks if b.id == body["block_id"]), None)
        if block is None:
            raise HTTPException(404, "A blokk nem található.")
    elif body.get("line"):
        script, _ = parse(state.repo.read_script(p))
        line = int(body["line"])
        block = next((b for b in script.blocks if b.line <= line <= b.end_line), None)
        if block is None:
            raise HTTPException(404, "Ezen a soron nincs felolvasható blokk.")
    elif body.get("text"):
        from app.ttsmd.models import ScriptBlock

        block = ScriptBlock(id="preview", kind="paragraph", text=str(body["text"]), line=0, end_line=0,
                            chapter_index=0)
    else:
        raise HTTPException(400, "Adj meg block_id-t, line-t vagy text-et.")
    items = chunker.block_chunks(block)
    if not items:
        raise HTTPException(400, "A blokkban nincs felolvasható szöveg.")
    try:
        wav = synthesize_texts(state, voice, runner.engine_params(voice, p), items)
    except EngineError as e:
        raise HTTPException(503, f"A motor hibát jelzett: {e.message}") from e
    return Response(content=wav, media_type="audio/wav",
                    headers={"X-Chunk-Texts": json.dumps([t for t, _ in items], ensure_ascii=True)})


class JobBody(BaseModel):
    chapters: list[int] | str = "all"
    formats: list[str] | None = None


@router.post("/api/projects/{project_id}/jobs")
def start_job(project_id: str, body: JobBody, state: AppState = Depends(get_state)) -> dict:
    p = get_project_or_404(state, project_id)
    report = validate_for(state, state.repo.read_script(p))
    if report.errors:
        raise HTTPException(422, {"message": "A forgatókönyv hibás, a generálás nem indul.",
                                  "report": report.model_dump()})
    formats = body.formats or p["settings"].get("export_formats") or ["mp3", "m4b"]
    bad = set(formats) - {"mp3", "m4b"}
    if bad:
        raise HTTPException(400, f"Ismeretlen formátum: {', '.join(bad)}")
    if isinstance(body.chapters, str) and body.chapters != "all":
        raise HTTPException(400, "A chapters értéke 'all' vagy fejezetindexek listája.")
    job = state.repo.create_job(project_id, {"chapters": body.chapters, "formats": formats})
    state.queue.notify()
    return {"job_id": job["id"], "status": job["status"]}


@router.post("/api/validate")
def validate(body: ScriptBody, state: AppState = Depends(get_state)) -> dict:
    """Validálás projekt létrehozása nélkül (az MCP `validate_script` eszköze használja)."""
    return validate_for(state, body.script_text).model_dump()
