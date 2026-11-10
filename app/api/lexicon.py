"""Kiejtési szótár végpontok (L7-06)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.api.deps import get_state
from app.state import AppState

router = APIRouter()


class Entry(BaseModel):
    written: str
    spoken: str
    case_sensitive: bool = False


@router.get("/api/lexicon")
def get_lexicon(state: AppState = Depends(get_state)) -> list[dict]:
    return state.repo.lexicon()


@router.put("/api/lexicon")
def put_lexicon(entries: list[Entry], state: AppState = Depends(get_state)) -> list[dict]:
    state.repo.set_lexicon([e.model_dump() for e in entries])
    return state.repo.lexicon()


@router.post("/api/lexicon")
def add_entry(entry: Entry, state: AppState = Depends(get_state)) -> dict:
    if not entry.written.strip() or not entry.spoken.strip():
        raise HTTPException(400, "Az írott alak és a kiejtés sem lehet üres.")
    state.repo.add_lexicon_entry(entry.written.strip(), entry.spoken.strip(), entry.case_sensitive)
    return {"ok": True}


@router.delete("/api/lexicon/{written}")
def delete_entry(written: str, state: AppState = Depends(get_state)) -> dict:
    state.repo.delete_lexicon_entry(written)
    return {"ok": True}
