"""PDF importer PyMuPDF-fel (6.1, L1-05..L1-07).

Lépések: span kinyerés -> törzsméret -> élőfej/élőláb/oldalszám szűrés -> lábjegyzetek ->
felső indexes hivatkozások törlése -> olvasási sorrend (kéthasábos rendezés) -> címfelismerés
(vagy TOC) -> bekezdésekre tördelés elválasztás-javítással -> képletgyanú.
"""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from app.ingest.base import (
    BlockBuilder,
    Document,
    ImportError,
    clean_text,
    is_math_font,
    is_math_text,
    title_from_filename,
)

EDGE_ZONE = 0.08
FOOTNOTE_ZONE = 0.25
HEADER_REPEAT = 0.30
HEADING_RATIO = 1.15
FOOTNOTE_RATIO = 0.9
PAGE_NUM_RE = re.compile(r"^\s*(?:[-–—]\s*)?(?:\d{1,4}|[ivxlcdm]{1,7})(?:\s*[-–—])?\s*$", re.IGNORECASE)
CAPTION_RE = re.compile(r"^\s*(?:\d+[.)]?\s*)?(?:ábra|táblázat|fig\.|figure|table)\b", re.IGNORECASE)
REF_RE = re.compile(r"^[\d*†‡,\s]+$")
HYPHENS = "-­‐‑"  # kötőjel, lágy kötőjel (PDF-ben gyakori), Unicode kötőjelek


@dataclass
class Span:
    text: str
    size: float
    bold: bool
    font: str
    superscript: bool
    bbox: tuple[float, float, float, float]
    origin_y: float


@dataclass
class Line:
    spans: list[Span]
    bbox: tuple[float, float, float, float]
    page: int
    block_no: int
    text: str = ""
    size: float = 0.0
    bold: bool = False
    math_font: bool = False
    kind: str = "body"  # body | heading | footnote | figure
    level: int | None = None

    @property
    def x0(self) -> float:
        return self.bbox[0]

    @property
    def y0(self) -> float:
        return self.bbox[1]

    @property
    def y1(self) -> float:
        return self.bbox[3]

    @property
    def height(self) -> float:
        return max(1.0, self.bbox[3] - self.bbox[1])


@dataclass
class PageData:
    number: int
    width: float
    height: float
    lines: list[Line] = field(default_factory=list)
    figures: list[tuple[float, str]] = field(default_factory=list)  # (y, felirat)


def _norm_key(text: str) -> str:
    return re.sub(r"\d+", "#", clean_text(text).lower())


class PdfImporter:
    def can_handle(self, path: Path) -> bool:
        return path.suffix.lower() == ".pdf"

    # --- kinyerés ---
    def _extract(self, doc) -> tuple[list[PageData], list[str]]:
        import pymupdf

        warnings: list[str] = []
        pages: list[PageData] = []
        for pno, page in enumerate(doc, start=1):
            pd = PageData(pno, page.rect.width, page.rect.height)
            table_boxes = []
            try:
                for t in page.find_tables().tables:
                    table_boxes.append(pymupdf.Rect(t.bbox))
                    pd.figures.append((t.bbox[1], ""))
            except Exception:  # noqa: BLE001, S110 - a táblázatfelismerés hiánya nem végzetes
                pass
            d = page.get_text("dict", flags=pymupdf.TEXT_PRESERVE_WHITESPACE | pymupdf.TEXT_MEDIABOX_CLIP)
            has_text = False
            for bno, block in enumerate(d["blocks"]):
                if block.get("type") == 1:
                    pd.figures.append((block["bbox"][1], ""))
                    continue
                for ln in block.get("lines", []):
                    spans = []
                    for s in ln.get("spans", []):
                        if not s["text"].strip():
                            if spans and s["text"]:
                                spans[-1].text += " "
                            continue
                        spans.append(Span(text=s["text"], size=round(s["size"], 1),
                                          bold=bool(s["flags"] & 16) or "bold" in s["font"].lower(),
                                          font=s["font"], superscript=bool(s["flags"] & 1),
                                          bbox=tuple(s["bbox"]), origin_y=s["origin"][1]))
                    if not spans:
                        continue
                    bbox = tuple(ln["bbox"])
                    if any(pymupdf.Rect(bbox).intersects(tb) for tb in table_boxes):
                        continue
                    has_text = True
                    pd.lines.append(Line(spans=spans, bbox=bbox, page=pno, block_no=bno))
            if not has_text:
                warnings.append(f"Az {pno}. oldalon nincs szöveg, kihagyva.")
            pages.append(pd)
        return pages, warnings

    @staticmethod
    def _body_size(pages: list[PageData]) -> float:
        counter: Counter = Counter()
        for p in pages:
            for ln in p.lines:
                for s in ln.spans:
                    counter[s.size] += len(s.text.strip())
        return counter.most_common(1)[0][0] if counter else 10.0

    # --- szűrés ---
    def _strip_superscripts(self, ln: Line, body: float) -> None:
        """Felső indexes lábjegyzet-hivatkozások törlése (flag vagy kisebb méret + magasabb alapvonal)."""
        base = max((s.origin_y for s in ln.spans if s.size >= body * 0.9), default=None)
        kept = []
        for s in ln.spans:
            raised = base is not None and s.size < body * 0.85 and s.origin_y < base - s.size * 0.2
            if (s.superscript or raised) and REF_RE.match(s.text.strip()):
                continue
            kept.append(s)
        ln.spans = kept or ln.spans[:0]

    def _finalize_line(self, ln: Line) -> None:
        ln.text = "".join(s.text for s in ln.spans)
        chars = sum(len(s.text.strip()) for s in ln.spans) or 1
        ln.size = round(sum(s.size * len(s.text.strip()) for s in ln.spans) / chars, 1) if ln.spans else 0
        ln.bold = bool(ln.spans) and all(s.bold for s in ln.spans if s.text.strip())
        ln.math_font = any(is_math_font(s.font) for s in ln.spans)

    def _filter_edges(self, pages: list[PageData]) -> None:
        """Élőfej, élőláb és oldalszám eldobása."""
        counts: Counter = Counter()
        for p in pages:
            keys = set()
            for ln in p.lines:
                if self._in_edge(ln, p):
                    keys.add(_norm_key(ln.text))
            counts.update(keys)
        min_pages = max(2, int(len(pages) * HEADER_REPEAT + 0.999))
        repeated = {k for k, c in counts.items() if c >= min_pages and k}
        for p in pages:
            p.lines = [ln for ln in p.lines if not (
                self._in_edge(ln, p) and (_norm_key(ln.text) in repeated or PAGE_NUM_RE.match(clean_text(ln.text))))]

    @staticmethod
    def _in_edge(ln: Line, p: PageData) -> bool:
        return ln.y1 <= p.height * EDGE_ZONE or ln.y0 >= p.height * (1 - EDGE_ZONE)

    def _mark_footnotes(self, p: PageData, body: float) -> None:
        """Az oldal alsó 25%-ában lévő, kisebb betűs, számmal vagy *-gal kezdődő blokk lábjegyzet."""
        by_block: dict[int, list[Line]] = defaultdict(list)
        for ln in p.lines:
            by_block[ln.block_no].append(ln)
        fn_started = False
        for bno in sorted(by_block, key=lambda b: by_block[b][0].y0):
            lines = by_block[bno]
            if lines[0].y0 < p.height * (1 - FOOTNOTE_ZONE):
                continue
            avg = sum(ln.size for ln in lines) / len(lines)
            if avg > body * FOOTNOTE_RATIO:
                continue
            first = lines[0].text.lstrip()
            starts_marker = bool(re.match(r"^[\d*†]", first)) or (lines[0].spans and lines[0].spans[0].superscript)
            if starts_marker or fn_started:
                fn_started = True
                for ln in lines:
                    ln.kind = "footnote"

    # --- olvasási sorrend ---
    def _order(self, p: PageData) -> list[Line]:
        """Kéthasábos oldal: blokkok hasábonként (2 klaszter a bal szél szerint), azon belül y szerint."""
        blocks: dict[int, list[Line]] = defaultdict(list)
        for ln in p.lines:
            blocks[ln.block_no].append(ln)
        info = []
        for bno, lines in blocks.items():
            x0 = min(ln.x0 for ln in lines)
            x1 = max(ln.bbox[2] for ln in lines)
            y0 = min(ln.y0 for ln in lines)
            info.append((bno, x0, x1, y0))
        narrow = [b for b in info if (b[2] - b[1]) < p.width * 0.6]
        two_col = False
        split = 0.0
        if len(narrow) >= 4:
            xs = sorted(b[1] for b in narrow)
            c1, c2 = xs[0], xs[-1]
            for _ in range(10):
                g1 = [x for x in xs if abs(x - c1) <= abs(x - c2)]
                g2 = [x for x in xs if abs(x - c1) > abs(x - c2)]
                if not g1 or not g2:
                    break
                c1, c2 = sum(g1) / len(g1), sum(g2) / len(g2)
            if g1 and g2 and min(len(g1), len(g2)) >= 0.2 * len(xs) and (c2 - c1) > p.width * 0.25:
                two_col = True
                split = (c1 + c2) / 2
        if two_col:
            def key(b):
                col = 1 if b[1] >= split else 0
                return (col, b[3])
        else:
            def key(b):
                return (b[3], b[1])
        ordered: list[Line] = []
        for b in sorted(info, key=key):
            ordered.extend(sorted(blocks[b[0]], key=lambda ln: (ln.y0, ln.x0)))
        return ordered

    # --- címek ---
    def _heading_levels(self, lines: list[Line], body: float) -> None:
        by_block: dict[tuple[int, int], list[Line]] = defaultdict(list)
        for ln in lines:
            by_block[(ln.page, ln.block_no)].append(ln)
        candidates: list[Line] = []
        for ln in lines:
            if ln.kind != "body":
                continue
            text = ln.text.strip()
            if not text or len(text) > 200:
                continue
            block_lines = [x for x in by_block[(ln.page, ln.block_no)] if x.kind == "body"]
            standalone = len(block_lines) <= 3
            big = ln.size >= body * HEADING_RATIO
            bold_short = ln.bold and len(text) < 120 and not text.endswith(".") and standalone
            if (big and standalone) or bold_short:
                candidates.append(ln)
        sizes = sorted({round(c.size * 2) / 2 for c in candidates}, reverse=True)
        level_of = {s: min(i + 1, 3) for i, s in enumerate(sizes)}
        for c in candidates:
            c.kind = "heading"
            c.level = level_of[round(c.size * 2) / 2]

    def _apply_toc(self, lines: list[Line], toc: list) -> None:
        """A PDF könyvjelzői felülírják a heurisztikát."""
        for ln in lines:
            if ln.kind == "heading":
                ln.kind, ln.level = "body", None
        for level, title, page in toc:
            want = clean_text(title).lower()
            if not want:
                continue
            for ln in lines:
                if ln.page != page or ln.kind != "body":
                    continue
                got = clean_text(ln.text).lower()
                if got and (got == want or (len(got) > 3 and (want.startswith(got) or got.startswith(want)))):
                    ln.kind, ln.level = "heading", min(int(level), 3)
                    break

    # --- összeállítás ---
    def load(self, path: Path) -> Document:
        import pymupdf

        try:
            doc = pymupdf.open(str(path))
        except Exception as e:
            raise ImportError(f"A fájl nem nyitható meg: {e}") from e
        if doc.needs_pass:
            raise ImportError("A fájl nem nyitható meg: jelszóval védett.")
        try:
            pages, warnings = self._extract(doc)
            toc = doc.get_toc(simple=True)
            meta = doc.metadata or {}
        finally:
            doc.close()

        body = self._body_size(pages)
        for p in pages:
            for ln in p.lines:
                self._strip_superscripts(ln, body)
                self._finalize_line(ln)
            p.lines = [ln for ln in p.lines if ln.text.strip()]
        self._filter_edges(pages)
        ordered: list[Line] = []
        figures: list[tuple[int, float, str]] = []
        for p in pages:
            self._mark_footnotes(p, body)
            ordered.extend(self._order(p))
            figures.extend((p.number, y, cap) for y, cap in p.figures)
        if toc:
            self._apply_toc(ordered, toc)
        else:
            self._heading_levels(ordered, body)

        bb = BlockBuilder()
        para: list[Line] = []
        fig_iter = sorted(figures)
        fig_idx = 0

        def emit_figures_until(page: int, y: float) -> None:
            nonlocal fig_idx
            while fig_idx < len(fig_iter) and (fig_iter[fig_idx][0], fig_iter[fig_idx][1]) <= (page, y):
                bb.add("figure", fig_iter[fig_idx][2], page=fig_iter[fig_idx][0])
                fig_idx += 1

        def flush() -> None:
            if not para:
                return
            text = join_lines([ln.text for ln in para])
            math = any(ln.math_font for ln in para) or is_math_text(text)
            if CAPTION_RE.match(text) and len(text) < 300:
                bb.add("figure", text, page=para[0].page)
            else:
                bb.add("paragraph", text, page=para[0].page, math_suspect=math)
            para.clear()

        fn_buf: list[Line] = []

        def flush_fn() -> None:
            if fn_buf:
                text = join_lines([ln.text for ln in fn_buf])
                bb.add("footnote", text, page=fn_buf[0].page, math_suspect=any(ln.math_font for ln in fn_buf))
                fn_buf.clear()

        prev: Line | None = None
        for ln in ordered:
            if ln.kind == "footnote":
                if fn_buf and re.match(r"^\s*[\d*†]", ln.text) and ln.block_no != fn_buf[-1].block_no:
                    flush_fn()
                fn_buf.append(ln)
                continue
            flush_fn()
            emit_figures_until(ln.page, ln.y0)
            if ln.kind == "heading":
                flush()
                if prev is not None and prev.kind == "heading" and prev.level == ln.level and \
                        prev.page == ln.page and ln.y0 - prev.y1 < ln.height * 0.8 and bb.blocks:
                    bb.blocks[-1].text = clean_text(bb.blocks[-1].text + " " + ln.text)
                else:
                    bb.add("heading", ln.text, level=ln.level, page=ln.page, math_suspect=ln.math_font)
                prev = ln
                continue
            if para and prev is not None and self._new_paragraph(prev, ln, para):
                flush()
            para.append(ln)
            prev = ln
        flush()
        flush_fn()
        while fig_idx < len(fig_iter):
            bb.add("figure", fig_iter[fig_idx][2], page=fig_iter[fig_idx][0])
            fig_idx += 1
        _attach_captions(bb)
        return Document(title=(meta.get("title") or "").strip() or title_from_filename(path),
                        author=(meta.get("author") or "").strip() or None, source_path=str(path),
                        blocks=bb.blocks, warnings=warnings)

    @staticmethod
    def _new_paragraph(prev: Line, ln: Line, para: list[Line]) -> bool:
        if prev.kind == "heading":
            return True
        if ln.page != prev.page:
            # oldaltörésen átnyúló bekezdés: folytatódik, ha az előző sor nem mondatvég
            return bool(re.search(r"[.!?:\"”]\s*$", prev.text))
        line_h = max(prev.height, ln.height)
        gap = ln.y0 - prev.y1
        if gap > line_h * 1.5 - line_h or gap < -line_h * 2:
            # függőleges térköz > sormagasság × 1.5 (a sor tetejétől mérve), vagy hasábváltás
            return True
        left = min(x.x0 for x in para)
        return ln.x0 - left > ln.size * 1.0 and ln.x0 > prev.x0 + ln.size * 0.8


def join_lines(lines: list[str]) -> str:
    """Sorok összevonása: sorvégi kötőjel + kisbetűs folytatás -> egybeírás, egyébként szóköz."""
    out = ""
    for raw in lines:
        t = raw.replace(" ", " ").strip()
        if not t:
            continue
        if out and out[-1] in HYPHENS and t[:1].islower() and len(out) > 1 and out[-2].isalpha():
            out = out[:-1] + t
        else:
            out = f"{out} {t}" if out else t
    return clean_text(out)


def _attach_captions(bb: BlockBuilder) -> None:
    """Üres ábrablokk + közvetlenül utána álló képaláírás -> egy ábrablokk felirattal."""
    merged = []
    for b in bb.blocks:
        if merged and merged[-1].type == "figure" and not merged[-1].text and b.type == "figure" and b.text:
            merged[-1].text = b.text
            continue
        merged.append(b)
    bb.blocks[:] = merged
