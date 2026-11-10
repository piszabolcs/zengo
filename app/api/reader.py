"""Olvasónézet végpontok: szöveg csoportokkal és időzítéssel, fejezetek hangja."""

from __future__ import annotations

import mimetypes
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from app.api.deps import get_project_or_404, get_state
from app.reader.timing import load_timing
from app.reader.view import build_reader
from app.state import AppState
from app.ttsmd.parser import parse

router = APIRouter()


@router.get("/api/projects/{project_id}/reader")
def reader_data(project_id: str, state: AppState = Depends(get_state)) -> dict:
    p = get_project_or_404(state, project_id)
    script, _ = parse(state.repo.read_script(p))
    data = build_reader(script, state.repo.project_dir(p["id"]))
    for ch in data["chapters"]:
        ch["audio_url"] = f"/api/projects/{p['id']}/audio/{ch['index']}" if ch["audio"] else None
    return {"project": {"id": p["id"], "name": p["name"]}, **data}


def original_file(project_dir: Path) -> Path | None:
    """A feltöltött eredeti jegyzet (`original.*`) a projekt mappájában, ha van."""
    return next((f for f in sorted(project_dir.glob("original.*")) if f.is_file()), None)


@router.get("/api/projects/{project_id}/original")
def original_document(project_id: str, state: AppState = Depends(get_state)) -> FileResponse:
    p = get_project_or_404(state, project_id)
    path = original_file(state.repo.project_dir(p["id"]))
    if path is None:
        raise HTTPException(404, "Ehhez a hangoskönyvhöz nincs feltöltött eredeti jegyzet.")
    media = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    # inline: a böngésző a PDF-et a saját nézőjében nyitja meg, nem tölti le
    return FileResponse(path, media_type=media, content_disposition_type="inline",
                        filename=f"{p['name']}{path.suffix}")


@router.get("/api/projects/{project_id}/audio/{chapter_index}")
def chapter_audio(project_id: str, chapter_index: int, state: AppState = Depends(get_state)) -> FileResponse:
    p = get_project_or_404(state, project_id)
    t = load_timing(state.repo.project_dir(p["id"]))["chapters"].get(str(chapter_index))
    if not t or not t.get("mp3"):
        raise HTTPException(404, "Ennek a fejezetnek még nincs hangja.")
    base = state.repo.project_dir(p["id"]) if t.get("local") else state.runner.output_dir(p)
    path = base / t["mp3"]
    if not path.is_file():
        raise HTTPException(404, "A fejezet MP3 fájlja nem található.")
    return FileResponse(path, media_type="audio/mpeg")
