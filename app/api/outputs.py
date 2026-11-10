"""Kimeneti fájlok (6.6, L8-07)."""

from __future__ import annotations

import os
import sys

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_project_or_404, get_state
from app.state import AppState

router = APIRouter()


@router.get("/api/outputs/{project_id}")
def list_outputs(project_id: str, state: AppState = Depends(get_state)) -> dict:
    p = get_project_or_404(state, project_id)
    out_dir = state.runner.output_dir(p)
    files = []
    if out_dir.exists():
        for f in sorted(out_dir.iterdir()):
            if f.is_file() and f.suffix.lower() in (".mp3", ".m4b") and ".tmp" not in f.name:
                files.append({"name": f.name, "path": str(f), "bytes": f.stat().st_size})
    return {"dir": str(out_dir), "exists": out_dir.exists(), "files": files}


@router.post("/api/outputs/{project_id}/open")
def open_folder(project_id: str, state: AppState = Depends(get_state)) -> dict:
    p = get_project_or_404(state, project_id)
    out_dir = state.runner.output_dir(p)
    if not out_dir.exists():
        raise HTTPException(404, "A kimeneti mappa még nem létezik.")
    if sys.platform == "win32":
        os.startfile(out_dir)  # type: ignore[attr-defined]
    return {"ok": True, "dir": str(out_dir)}
