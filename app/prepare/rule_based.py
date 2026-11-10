"""Szabályalapú előkészítés: `Document` -> `.tts.md` forgatókönyv, LLM nélkül (6.2, L2-01..L2-03)."""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

from app.ingest.base import Block, Document

LONG_CHAPTER_CHARS = 60_000


@dataclass
class _Chapter:
    title: str
    body: list[Block] = field(default_factory=list)
    footnotes: list[Block] = field(default_factory=list)


def _fm_value(v: str) -> str:
    v = re.sub(r"\s+", " ", v).strip()
    if '"' in v and "'" in v:
        v = v.replace('"', "”")
    return f"'{v}'" if '"' in v else f'"{v}"'


def _escape(text: str) -> str:
    """Olyan szöveg, ami nem értelmeződik direktívának, kiejtésnek, megjegyzésnek vagy címnek."""
    text = re.sub(r"\s+", " ", text).strip()
    text = text.replace("[[", "[ [").replace("]]", "] ]").replace("{{", "{ {").replace("}}", "} }")
    text = text.replace("<!--", "< !--").replace("-->", "-- >")
    return re.sub(r"^#+\s*", "", text)


def _author_title(doc: Document) -> tuple[str, str]:
    title = doc.title.strip()
    author = (doc.author or "").strip()
    if not author:
        stem = Path(doc.source_path).stem
        if " - " in stem and (title == stem or not title or stem.endswith(title)):
            a, _, t = stem.partition(" - ")
            author, title = a.strip(), t.strip() or title
    return title or "Névtelen", author or "Ismeretlen"


def _math_markdown(doc: Document) -> str | None:
    """Képletes Markdown/DOCX forrás Markdown-szövege a képletolvasónak; None, ha nincs benne képlet."""
    from app.prepare.docx_md import docx_has_math, docx_to_markdown
    from app.prepare.math_doc import find_math

    path = Path(doc.source_path)
    suffix = path.suffix.lower()
    try:
        if suffix in (".md", ".markdown") and path.exists():
            md = path.read_text(encoding="utf-8-sig")
            return md if find_math(md) else None
        if suffix == ".docx" and path.exists():
            md = docx_to_markdown(path)
            return md if docx_has_math(path) or find_math(md) else None
    except (OSError, UnicodeDecodeError, ValueError):
        return None
    return None


def prepare(doc: Document, read_footnotes: bool = False, read_figure_captions: bool = False,
            math_fallback: Callable[[str], str | None] | None = None) -> tuple[str, list[str]]:
    md = _math_markdown(doc)
    if md is not None:
        # képletes jegyzet: szabályalapú képletfelolvasás (app/prepare/math_doc.py)
        from app.prepare.math_doc import prepare_markdown

        title, author = _author_title(doc)
        text, warnings, _ = prepare_markdown(md, title, author, Path(doc.source_path).name, read_footnotes,
                                             read_figure_captions, math_fallback)
        return text, warnings
    warnings: list[str] = []
    title, author = _author_title(doc)
    headings = [b for b in doc.blocks if b.type == "heading" and b.level]
    levels = {b.level for b in headings}
    shift = 0
    if headings and 1 not in levels:
        shift = min(levels) - 1  # a legmagasabb meglévő szint lép elő fejezetté

    chapters: list[_Chapter] = []
    for b in doc.blocks:
        if b.type == "heading" and b.level:
            lvl = max(1, b.level - shift)
            if lvl == 1:
                chapters.append(_Chapter(title=_escape(b.text)))
                continue
            b = b.model_copy(update={"level": min(lvl, 3)})
        if not chapters:
            chapters.append(_Chapter(title=_escape(title)))
        if b.type == "footnote":
            chapters[-1].footnotes.append(b)
        else:
            chapters[-1].body.append(b)

    lines = ["---", "format: ttsmd/1", f"title: {_fm_value(title)}", f"author: {_fm_value(author)}",
             "language: hu", f"source: {_fm_value(Path(doc.source_path).name)}", "---", ""]
    math_count = 0
    written = 0
    for ch in chapters:
        out: list[str] = []
        has_text = False
        for b in ch.body:
            if b.type == "heading":
                out += [f"{'#' * b.level} {_escape(b.text)}", ""]
            elif b.type == "figure":
                if read_figure_captions and b.text.strip():
                    out += [f"Ábra: {_escape(b.text)}", ""]
                    has_text = True
            elif b.type == "paragraph":
                text = _escape(b.text)
                if not text:
                    continue
                if b.math_suspect:
                    out.append("<!-- MATH_SUSPECT -->")
                    math_count += 1
                out += [text, ""]
                has_text = True
        if read_footnotes and ch.footnotes:
            out += ["## Lábjegyzetek", ""]
            for fn in ch.footnotes:
                if fn.math_suspect:
                    out.append("<!-- MATH_SUSPECT -->")
                    math_count += 1
                out += [_escape(fn.text), ""]
            has_text = True
        if not has_text:
            warnings.append(f"Üres fejezet kihagyva: {ch.title}")
            continue
        chars = sum(len(x) for x in out)
        if chars > LONG_CHAPTER_CHARS:
            warnings.append(f"Nagyon hosszú fejezet ({chars} karakter): {ch.title}")
        lines += [f"# {ch.title}", ""] + out
        written += 1
    if written == 0:
        lines += [f"# {_escape(title)}", "", "(A dokumentumban nem található felolvasható szöveg.)", ""]
        warnings.append("A dokumentumban nem található felolvasható szöveg.")
    if math_count:
        warnings.append(f"{math_count} képletgyanús blokk. Képletes anyaghoz a Claude skill ajánlott.")
    return "\n".join(lines).rstrip() + "\n", warnings
