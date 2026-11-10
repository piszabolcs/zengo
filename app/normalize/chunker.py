"""Mondatbontás, chunkolás és szünetek (6.3, L3-05, L3-06)."""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Iterable
from dataclasses import dataclass, field

from app.config import DEFAULT_PAUSES
from app.normalize.abbrev_hu import NON_TERMINAL
from app.normalize.hu import LexiconEntry, Normalizer
from app.ttsmd.models import ChapterPlan, Chunk, ChunkPlan, Script, ScriptBlock
from app.ttsmd.validator import written_form

PAUSE_SPLIT_RE = re.compile(r"\[\[\s*pause\s+(\d+)\s*\]\]")
SENT_END_RE = re.compile(r"[.!?…]+[\"'”»)]*(?=\s+)")
CLAUSE_RE = re.compile(r"[,;:](?=\s)")
INTRA_SENTENCE_PAUSE_MS = 150


# A worker hangot érintő változásakor nő: a régi gyorsítótárazott chunkok így újragenerálódnak.
ENGINE_REVISION = {"f5_hu": 8}  # 2: kisbetűs szöveg; 3: mondatonkénti generálás, szünetek; 4: 70 Hz-es felüláteresztő; 5: új Férfi referencia; 6: lágy szóvégek; 7: mondatcsoportok legfeljebb 160 karakterig; 8: eldobható zárószó a vég lecsengéséhez


def chunk_hash(engine_id: str, voice_id: str, engine_params: dict, normalized_text: str) -> str:
    params_json = json.dumps(engine_params, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    rev = f"#r{ENGINE_REVISION[engine_id]}" if engine_id in ENGINE_REVISION else ""
    return hashlib.sha256((engine_id + rev + voice_id + params_json + normalized_text).encode("utf-8")).hexdigest()


def split_sentences(text: str) -> list[str]:
    """Mondathatár: `.`, `!`, `?`, `…` után, ha a folytatás nem szóköz + kisbetű.

    Rövidítés és sorszám után álló pont nem mondathatár.
    """
    out: list[str] = []
    start = 0
    for m in SENT_END_RE.finditer(text):
        end = m.end()
        rest = text[end:].lstrip()
        if not rest:
            continue
        if rest[0].islower():
            continue
        if m.group(0).startswith(".") and len(m.group(0).rstrip("\"'”»)")) == 1:
            prev = re.search(r"(\w+)$", text[start:m.start()])
            if prev and (prev.group(1).lower() in NON_TERMINAL or prev.group(1).isdigit()):
                continue
        out.append(text[start:end].strip())
        start = end
    tail = text[start:].strip()
    if tail:
        out.append(tail)
    return out


def _split_long(sentence: str, max_chars: int) -> list[str]:
    """Túl hosszú mondat bontása vessző/pontosvessző/kettőspont, végső esetben szóhatár mentén."""
    if len(sentence) <= max_chars:
        return [sentence]
    parts: list[str] = []
    start = 0
    for m in CLAUSE_RE.finditer(sentence):
        parts.append(sentence[start:m.end()].strip())
        start = m.end()
    parts.append(sentence[start:].strip())
    pieces: list[str] = []
    cur = ""
    for p in parts:
        if not p:
            continue
        cand = f"{cur} {p}".strip()
        if len(cand) <= max_chars:
            cur = cand
            continue
        if cur:
            pieces.append(cur)
        if len(p) <= max_chars:
            cur = p
        else:
            words = p.split()
            cur = ""
            for w in words:
                cand = f"{cur} {w}".strip()
                if len(cand) <= max_chars:
                    cur = cand
                else:
                    if cur:
                        pieces.append(cur)
                    cur = w[:max_chars]
    if cur:
        pieces.append(cur)
    return pieces


def pack(text: str, max_chars: int, sentence_pause: int) -> list[tuple[str, int]]:
    """Egy szakasz (bekezdés vagy két szünetdirektíva közti rész) chunkjai a köztük lévő szünettel."""
    result: list[tuple[str, int]] = []
    cur = ""
    for sentence in split_sentences(text):
        if len(sentence) > max_chars:
            if cur:
                result.append((cur, sentence_pause))
                cur = ""
            pieces = _split_long(sentence, max_chars)
            for i, p in enumerate(pieces):
                result.append((p, sentence_pause if i == len(pieces) - 1 else INTRA_SENTENCE_PAUSE_MS))
            continue
        cand = f"{cur} {sentence}".strip()
        if len(cand) <= max_chars:
            cur = cand
        else:
            result.append((cur, sentence_pause))
            cur = sentence
    if cur:
        result.append((cur, sentence_pause))
    return result


@dataclass
class ChunkSettings:
    engine_id: str
    voice_id: str
    engine_params: dict
    max_chars: int
    pauses: dict = field(default_factory=lambda: dict(DEFAULT_PAUSES))
    announce_chapters: bool = True


def _ensure_terminal(text: str) -> str:
    return text if re.search(r"[.!?…]$", text) else text + "."


class Chunker:
    def __init__(self, settings: ChunkSettings, lexicon: Iterable[LexiconEntry] | None = None):
        self.s = settings
        self.p = {**DEFAULT_PAUSES, **(settings.pauses or {})}
        self.normalizer = Normalizer(lexicon)

    def block_chunks(self, block: ScriptBlock) -> list[tuple[str, int]]:
        """Egy blokk normalizált chunkjai (szöveg, utána következő szünet), a blokk végi szünet nélkül."""
        if block.kind in ("chapter", "h2", "h3"):
            text, _ = self.normalizer.normalize(block.text, is_title=True)
            return pack(_ensure_terminal(text), self.s.max_chars, self.p["sentence"]) if text else []
        out: list[tuple[str, int]] = []
        segments = PAUSE_SPLIT_RE.split(block.text)
        # segments: [szöveg, ms, szöveg, ms, ...]
        for i in range(0, len(segments), 2):
            raw = segments[i]
            explicit = int(segments[i + 1]) if i + 1 < len(segments) else None
            norm, _ = self.normalizer.normalize(raw)
            chunks = pack(norm, self.s.max_chars, self.p["sentence"]) if norm else []
            if explicit is not None:
                if chunks:
                    chunks[-1] = (chunks[-1][0], explicit)
                elif out:
                    out[-1] = (out[-1][0], explicit)
            out.extend(chunks)
        return out

    def plan(self, script: Script, chapters: Iterable[int] | None = None) -> ChunkPlan:
        wanted = set(chapters) if chapters is not None else None
        plan = ChunkPlan()
        blocks = [b for b in script.blocks if b.chapter_index >= 0]
        by_chapter: dict[int, list[ScriptBlock]] = {}
        for b in blocks:
            by_chapter.setdefault(b.chapter_index, []).append(b)
        for idx in sorted(by_chapter):
            if wanted is not None and idx not in wanted:
                continue
            chapter_blocks = by_chapter[idx]
            title_block = chapter_blocks[0]
            # a fájlnévbe és a címkékbe az írott alak kerül, nem a kiejtés
            title_norm, _ = self.normalizer.normalize(written_form(title_block.text), is_title=True, respell=False)
            cp = ChapterPlan(index=idx, title=title_norm.rstrip(".") or title_block.text)
            items: list[tuple[str, int, str]] = []  # (szöveg, szünet, block_id)

            def add_pause_before(items: list[tuple[str, int, str]], ms: int) -> None:
                if items:
                    t, p, bid = items[-1]
                    items[-1] = (t, max(p, ms), bid)

            for bi, b in enumerate(chapter_blocks):
                nxt = chapter_blocks[bi + 1] if bi + 1 < len(chapter_blocks) else None
                if b.kind == "chapter":
                    if self.s.announce_chapters:
                        title_chunks = self.block_chunks(b)
                        for i, (t, p) in enumerate(title_chunks):
                            last = i == len(title_chunks) - 1
                            items.append((t, self.p["chapter_title_after"] if last else p, b.id))
                    continue
                if b.kind in ("h2", "h3"):
                    before, after = (self.p["h2_before"], self.p["h2_after"]) if b.kind == "h2" else (
                        self.p["h3_before"], self.p["h3_after"])
                    add_pause_before(items, before)
                    title_chunks = self.block_chunks(b)
                    for i, (t, p) in enumerate(title_chunks):
                        items.append((t, after if i == len(title_chunks) - 1 else p, b.id))
                    continue
                chunks = self.block_chunks(b)
                if not chunks:
                    continue
                explicit_end = bool(re.search(r"\[\[\s*pause\s+\d+\s*\]\]\s*$", b.text))
                if not explicit_end:
                    if b.kind == "list_item" and nxt is not None and nxt.kind == "list_item":
                        end_pause = self.p["list_item"]
                    else:
                        end_pause = self.p["paragraph"]
                    chunks[-1] = (chunks[-1][0], end_pause)
                for t, p in chunks:
                    items.append((t, p, b.id))
            if items:
                t, _, bid = items[-1]
                items[-1] = (t, self.p["chapter_end"], bid)
            for seq, (t, p, bid) in enumerate(items):
                cp.chunks.append(Chunk(
                    chunk_id=chunk_hash(self.s.engine_id, self.s.voice_id, self.s.engine_params, t),
                    chapter_index=idx, block_id=bid, seq=seq, text=t, pause_after_ms=p,
                ))
            plan.chapters.append(cp)
        return plan
