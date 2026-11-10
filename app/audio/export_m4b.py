"""M4B export fejezetjelölőkkel és borítóval (L6-04)."""

from __future__ import annotations

import os
from pathlib import Path

from app.audio.assemble import concat_wavs
from app.audio.ffmpeg import Ffmpeg
from app.storage.repo import sanitize_filename


def _esc(value: str) -> str:
    """FFMETADATA1 escape: `=`, `;`, `#`, `\\` és sortörés."""
    out = value.replace("\\", "\\\\")
    for ch in "=;#":
        out = out.replace(ch, "\\" + ch)
    return out.replace("\n", "\\\n")


def metadata_text(title: str, artist: str, chapters: list[tuple[str, float]]) -> str:
    lines = [";FFMETADATA1", f"title={_esc(title)}", f"album={_esc(title)}", f"artist={_esc(artist)}",
             "genre=Audiobook", ""]
    start = 0
    for ch_title, dur in chapters:
        end = start + round(dur * 1000)
        lines += ["[CHAPTER]", "TIMEBASE=1/1000", f"START={start}", f"END={end}", f"title={_esc(ch_title)}", ""]
        start = end
    return "\n".join(lines)


def m4b_name(title: str) -> str:
    return f"{sanitize_filename(title)}.m4b"


def export_m4b(ff: Ffmpeg, chapter_wavs: list[tuple[str, Path]], out: Path, *, title: str, artist: str,
               work_dir: Path, cover: Path | None = None) -> Path:
    work_dir.mkdir(parents=True, exist_ok=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    chapters = [(t, ff.duration(p)) for t, p in chapter_wavs]
    meta = work_dir / "chapters.ffmeta"
    meta.write_text(metadata_text(title, artist, chapters), encoding="utf-8")
    joined = work_dir / "all_chapters.wav"
    concat_wavs(ff, [p for _, p in chapter_wavs], joined, work_dir)
    tmp = out.with_name(out.stem + ".tmp.m4b")
    args = ["-i", str(joined), "-i", str(meta)]
    has_cover = cover is not None and cover.exists()
    if has_cover:
        args += ["-i", str(cover)]
    args += ["-map", "0:a", "-map_metadata", "1", "-map_chapters", "1"]
    if has_cover:
        args += ["-map", "2:v", "-c:v", "mjpeg", "-disposition:v:0", "attached_pic"]
    args += ["-c:a", "aac", "-profile:a", "aac_low", "-b:a", "96k", "-ac", "1", "-movflags", "+faststart",
             "-f", "mp4", str(tmp)]
    ff.run(args)
    os.replace(tmp, out)
    joined.unlink(missing_ok=True)
    return out
