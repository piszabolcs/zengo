"""Olvasónézet időzítése: melyik blokk hol szól a fejezet hangjában.

Exportkor fejezetenként a chunkok tényleges hossza (csendvágás után, szünettel) kerül a
`<projekt mappa>/timing.json`-ba. A tempó (atempo) arányosan rövidíti az időket.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from app.ttsmd.models import ChapterPlan

TIMING_FILE = "timing.json"


def load_timing(project_dir: Path) -> dict:
    path = project_dir / TIMING_FILE
    if not path.exists():
        return {"chapters": {}}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"chapters": {}}


def save_chapter_timing(project_dir: Path, chapter: ChapterPlan, durations: list[float], speed: float,
                        mp3_name: str | None, sig: str, local: bool = False) -> None:
    """Egy fejezet időzítése: [block_id, kezdet, vég] chunkonként, másodpercben.

    `local`: az MP3 a projekt mappájában van (egyfájlos kimenetnél az olvasó fejezethangjai), nem a kimeneti mappában.
    """
    segments = []
    t = 0.0
    for chunk, dur in zip(chapter.chunks, durations):
        start, t = t, t + dur
        segments.append([chunk.block_id, round(start / speed, 3), round(t / speed, 3)])
    data = load_timing(project_dir)
    data["chapters"][str(chapter.index)] = {
        "title": chapter.title, "mp3": mp3_name, "local": local, "duration": round(t / speed, 3), "sig": sig,
        "chunk_ids": [c.chunk_id for c in chapter.chunks], "segments": segments,
    }
    tmp = project_dir / (TIMING_FILE + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, project_dir / TIMING_FILE)
