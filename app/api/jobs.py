"""Feladat végpontok: lista, állapot, szüneteltetés, folytatás, törlés (L7-04)."""

from __future__ import annotations

import time

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_state
from app.state import AppState

router = APIRouter()


def chunk_texts(state: AppState, job: dict) -> dict[tuple[int, int], str]:
    """(fejezet, sorszám) -> szöveg, a forgatókönyv aktuális tervéből."""
    project = state.repo.get_project(job["project_id"])
    if project is None:
        return {}
    try:
        _, plan, _, _ = state.runner.plan_for(project, job["request"].get("chapters", "all"))
    except Exception:  # noqa: BLE001
        return {}
    return {(c.chapter_index, c.seq): c.text for c in plan.all_chunks()}


def job_view(state: AppState, job: dict, detail: bool = False) -> dict:
    prog = state.runner.progress.get(job["id"])
    total = job["total_chunks"] or 0
    done = job["done_chunks"] or 0
    project = state.repo.get_project(job["project_id"])
    view = {
        "id": job["id"], "project_id": job["project_id"],
        "project_name": project["name"] if project else None,
        "status": job["status"], "total_chunks": total, "done_chunks": done,
        "percent": round(100.0 * done / total, 1) if total else 0.0,
        "error": job["error"], "created_at": job["created_at"], "started_at": job["started_at"],
        "finished_at": job["finished_at"], "request": {k: v for k, v in job["request"].items() if k != "outputs"},
        "phase": prog.phase if prog and job["status"] == "running" else job["status"],
        "eta_s": round(prog.eta_s) if prog and prog.eta_s is not None and job["status"] == "running" else None,
        "elapsed_s": round(time.time() - prog.started) if prog and job["status"] == "running" else None,
        "outputs": job["request"].get("outputs", []) if job["status"] == "done" else [],
    }
    if detail:
        rows = state.db.query(
            "SELECT chunk_id, chapter_index, seq, wer, attempts FROM chunks WHERE job_id = ? AND qa_warning = 1 "
            "ORDER BY chapter_index, seq", (job["id"],))
        failed = state.db.query(
            "SELECT chunk_id, chapter_index, seq FROM chunks WHERE job_id = ? AND status = 'failed'", (job["id"],))
        texts = chunk_texts(state, job) if rows or failed else {}
        view["qa_warnings"] = [{**dict(r), "text": texts.get((r["chapter_index"], r["seq"]), "")} for r in rows]
        view["failed_chunks"] = [{**dict(r), "text": texts.get((r["chapter_index"], r["seq"]), "")}
                                 for r in failed]
    return view


def _job_or_404(state: AppState, job_id: str) -> dict:
    job = state.repo.get_job(job_id)
    if job is None:
        raise HTTPException(404, "A feladat nem található.")
    return job


@router.get("/api/jobs")
def list_jobs(state: AppState = Depends(get_state)) -> list[dict]:
    return [job_view(state, j) for j in state.repo.list_jobs()]


@router.get("/api/jobs/{job_id}")
def get_job(job_id: str, state: AppState = Depends(get_state)) -> dict:
    return job_view(state, _job_or_404(state, job_id), detail=True)


@router.post("/api/jobs/{job_id}/pause")
def pause(job_id: str, state: AppState = Depends(get_state)) -> dict:
    _job_or_404(state, job_id)
    return {"ok": state.queue.pause(job_id)}


@router.post("/api/jobs/{job_id}/resume")
def resume(job_id: str, state: AppState = Depends(get_state)) -> dict:
    _job_or_404(state, job_id)
    return {"ok": state.queue.resume(job_id)}


@router.post("/api/jobs/{job_id}/cancel")
def cancel(job_id: str, state: AppState = Depends(get_state)) -> dict:
    _job_or_404(state, job_id)
    return {"ok": state.queue.cancel(job_id)}


@router.post("/api/jobs/{job_id}/regenerate")
def regenerate(job_id: str, body: dict, state: AppState = Depends(get_state)) -> dict:
    """Egy ellenőrizendő chunk újragenerálása: törlés a gyorsítótárból, majd a feladat újra sorba áll."""
    job = _job_or_404(state, job_id)
    if job["status"] in ("running", "queued"):
        raise HTTPException(409, "A feladat még fut.")
    chunk_id = str(body.get("chunk_id", ""))
    row = state.db.one("SELECT 1 FROM chunks WHERE job_id = ? AND chunk_id = ?", (job_id, chunk_id))
    if row is None:
        raise HTTPException(404, "A chunk nem tartozik a feladathoz.")
    state.cache.path_for(chunk_id).unlink(missing_ok=True)
    state.db.execute("DELETE FROM cache_entries WHERE chunk_id = ?", (chunk_id,))
    state.db.execute("UPDATE chunks SET status = 'pending', qa_warning = 0 WHERE job_id = ? AND chunk_id = ?",
                     (job_id, chunk_id))
    state.db.execute("UPDATE jobs SET status = 'queued', error = NULL, finished_at = NULL WHERE id = ?", (job_id,))
    state.queue.notify()
    return {"ok": True}
