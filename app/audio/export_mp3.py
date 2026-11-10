"""MP3 export ID3v2 címkékkel és borítóval: fejezetenként, vagy egy fájlban fejezetjelölőkkel (L6-03)."""

from __future__ import annotations

import os
from pathlib import Path

from app.audio.assemble import concat_wavs
from app.audio.ffmpeg import Ffmpeg
from app.storage.repo import sanitize_filename


def mp3_name(index: int, title: str) -> str:
    return f"{index:02d} - {sanitize_filename(title)}.mp3"


def export_mp3(ff: Ffmpeg, src_wav: Path, out: Path, *, title: str, album: str, artist: str, track: int,
               total_tracks: int, cover: Path | None = None) -> Path:
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_name(out.stem + ".tmp.mp3")
    args = ["-i", str(src_wav)]
    if cover is not None and cover.exists():
        args += ["-i", str(cover), "-map", "0:a", "-map", "1:v", "-c:v", "mjpeg",
                 "-metadata:s:v", "title=Album cover", "-metadata:s:v", "comment=Cover (front)",
                 "-disposition:v", "attached_pic"]
    args += ["-c:a", "libmp3lame", "-b:a", "128k", "-ac", "1", "-id3v2_version", "3",
             "-metadata", f"title={title}", "-metadata", f"album={album}", "-metadata", f"artist={artist}",
             "-metadata", f"track={track}/{total_tracks}", "-metadata", "genre=Audiobook", "-f", "mp3", str(tmp)]
    ff.run(args)
    os.replace(tmp, out)
    return out


def book_mp3_name(title: str) -> str:
    return f"{sanitize_filename(title)}.mp3"


def export_mp3_book(ff: Ffmpeg, chapter_wavs: list[tuple[str, Path]], out: Path, *, title: str, artist: str,
                    work_dir: Path, cover: Path | None = None) -> Path:
    """Egyetlen MP3 az összes fejezettel, ID3v2 fejezetjelölőkkel (CHAP), ahogy az M4B-ben."""
    from app.audio.export_m4b import metadata_text

    work_dir.mkdir(parents=True, exist_ok=True)
    out.parent.mkdir(parents=True, exist_ok=True)
    meta = work_dir / "book.ffmeta"
    meta.write_text(metadata_text(title, artist, [(t, ff.duration(p)) for t, p in chapter_wavs]), encoding="utf-8")
    joined = work_dir / "book.wav"
    concat_wavs(ff, [p for _, p in chapter_wavs], joined, work_dir)
    tmp = out.with_name(out.stem + ".tmp.mp3")
    args = ["-i", str(joined), "-i", str(meta)]
    has_cover = cover is not None and cover.exists()
    if has_cover:
        args += ["-i", str(cover)]
    args += ["-map", "0:a", "-map_metadata", "1", "-map_chapters", "1"]
    if has_cover:
        args += ["-map", "2:v", "-c:v", "mjpeg", "-metadata:s:v", "title=Album cover",
                 "-metadata:s:v", "comment=Cover (front)", "-disposition:v", "attached_pic"]
    args += ["-c:a", "libmp3lame", "-b:a", "128k", "-ac", "1", "-id3v2_version", "3", "-f", "mp3", str(tmp)]
    ff.run(args)
    os.replace(tmp, out)
    joined.unlink(missing_ok=True)
    return out
