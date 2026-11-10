from __future__ import annotations

from fastapi import HTTPException, Request

from app.state import AppState


def get_state(request: Request) -> AppState:
    return request.app.state.app


def get_project_or_404(state: AppState, project_id: str) -> dict:
    p = state.repo.get_project(project_id)
    if p is None:
        raise HTTPException(404, "A projekt nem található.")
    return p
