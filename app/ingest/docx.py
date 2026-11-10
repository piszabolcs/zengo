"""DOCX importer: címsorok, lábjegyzetek (`footnotes.xml`), OMML képletek (L1-03)."""

from __future__ import annotations

import re
from pathlib import Path

from lxml import etree

from app.ingest.base import BlockBuilder, Document, ImportError, title_from_filename

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
M = "http://schemas.openxmlformats.org/officeDocument/2006/math"
NS = {"w": W, "m": M}
HEADING_RE = re.compile(r"^(?:heading|címsor|cmsor)\s*(\d)$", re.IGNORECASE)
CAPTION_STYLES = {"caption", "képaláírás", "kpalrs"}


def _q(ns: str, tag: str) -> str:
    return f"{{{ns}}}{tag}"


def paragraph_text(p) -> tuple[str, bool]:
    """Bekezdés szövege dokumentumsorrendben; az OMML képlet `[képlet: ...]` jelöléssel."""
    parts: list[str] = []
    has_math = False

    def walk(el) -> None:
        nonlocal has_math
        tag = el.tag
        if tag in (_q(M, "oMath"), _q(M, "oMathPara")):
            texts = "".join(t.text or "" for t in el.iter(_q(M, "t")))
            if texts.strip():
                parts.append(f" [képlet: {texts.strip()}] ")
                has_math = True
            return
        if tag == _q(W, "t"):
            parts.append(el.text or "")
        elif tag == _q(W, "tab") or tag in (_q(W, "br"), _q(W, "cr")):
            parts.append(" ")
        elif tag in (_q(W, "footnoteReference"), _q(W, "endnoteReference"), _q(W, "delText")):
            return
        for child in el:
            walk(child)

    walk(p)
    return "".join(parts), has_math


def _style_name(p, styles: dict[str, str]) -> str:
    pstyle = p.find(f"{_q(W, 'pPr')}/{_q(W, 'pStyle')}")
    if pstyle is None:
        return ""
    sid = pstyle.get(_q(W, "val"), "")
    return styles.get(sid, sid)


def _heading_level(style: str) -> int | None:
    m = HEADING_RE.match(style.strip())
    if m:
        return min(max(int(m.group(1)), 1), 3)
    if style.strip().lower() in ("title", "cím"):
        return 1
    return None


class DocxImporter:
    def can_handle(self, path: Path) -> bool:
        return path.suffix.lower() == ".docx"

    def load(self, path: Path) -> Document:
        import docx

        try:
            d = docx.Document(str(path))
        except Exception as e:
            raise ImportError(f"A fájl nem nyitható meg: {e}") from e
        styles = {s.style_id: s.name for s in d.styles if s.style_id}
        bb = BlockBuilder()
        notes = self._footnotes(d)
        emitted: set[str] = set()
        body = d.element.body
        for el in body.iterchildren():
            refs = [r.get(_q(W, "id")) for r in el.iter(_q(W, "footnoteReference"))]
            if el.tag == _q(W, "p"):
                style = _style_name(el, styles)
                text, has_math = paragraph_text(el)
                level = _heading_level(style)
                if level:
                    bb.add("heading", text, level=level, math_suspect=has_math)
                elif style.strip().lower() in CAPTION_STYLES:
                    bb.add("figure", text)
                elif el.find(f".//{_q(W, 'drawing')}") is not None and not text.strip():
                    bb.add("figure", "")
                else:
                    bb.add("paragraph", text, math_suspect=has_math)
            elif el.tag == _q(W, "tbl"):
                bb.add("figure", "")
            for rid in refs:
                if rid in notes and rid not in emitted:
                    emitted.add(rid)
                    bb.add("footnote", notes[rid])
        for rid, fn in notes.items():
            if rid not in emitted:
                bb.add("footnote", fn)
        props = d.core_properties
        return Document(title=(props.title or "").strip() or title_from_filename(path),
                        author=(props.author or "").strip() or None, source_path=str(path), blocks=bb.blocks)

    def _footnotes(self, d) -> dict[str, str]:
        part = None
        for rel in d.part.rels.values():
            if rel.reltype.endswith("/footnotes") and not rel.is_external:
                part = rel.target_part
                break
        if part is None:
            return {}
        root = etree.fromstring(part.blob)
        out: dict[str, str] = {}
        for fn in root.findall("w:footnote", NS):
            ftype = fn.get(_q(W, "type"))
            if ftype in ("separator", "continuationSeparator", "continuationNotice"):
                continue
            texts = [paragraph_text(p)[0] for p in fn.findall("w:p", NS)]
            text = " ".join(t.strip() for t in texts if t.strip())
            if text:
                out[fn.get(_q(W, "id"))] = text
        return out
