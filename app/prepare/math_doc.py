"""Képletes Markdown (és DOCX-ből készült Markdown) -> `.tts.md` forgatókönyv, Claude nélkül.

Minden forrásrész elé `<!-- eredeti ... -->` megjegyzés kerül (formátum 9. szabály), a képletek
kimondott mondatok lesznek `[[pause 500]]` szünettel, a jelöléstáblázat mondatokká, a félkövér
bevezető (`**Térerősség.**`) címmé alakul. Amit a képletolvasó nem ért, `<!-- MATH_SUSPECT -->`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from itertools import pairwise
from pathlib import Path

from markdown_it import MarkdownIt

from app.ingest.base import title_from_filename
from app.normalize.hu import ordinal, roman_to_int
from app.prepare.math_prose import (
    Fallback,
    find_spans,
    prose_letters,
    protect_inline_latex,
    restore_inline_latex,
    span_source,
    verbalize_prose,
    with_pauses,
)
from app.prepare.mathspeak_hu import (
    Ctx,
    MathSpeakError,
    both_cases,
    letters_in,
    sentence,
    speak,
    speak_one,
    speak_unit,
)

PAUSE = "[[pause 500]]"
MATH_FENCES = {"latex", "math", "tex", "katex"}
FRONT_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
FOOTNOTE_DEF_RE = re.compile(r"^\[\^([^\]]+)\]:\s*(.*)$")
FOOTNOTE_REF_RE = re.compile(r"\[\^[^\]]+\]")
SYMBOL_HEADERS = {"jel", "jelölés", "szimbólum", "betű", "jelek", "mennyiség"}
PAUSE_RE = re.compile(r"\s*\[\[pause \d+\]\]")


@dataclass
class Stats:
    formulas: int = 0
    spoken: int = 0
    llm: int = 0
    suspects: list[str] = field(default_factory=list)

    @property
    def coverage(self) -> float:
        return 1.0 if not self.formulas else (self.spoken + self.llm) / self.formulas


@dataclass
class Seg:
    kind: str  # heading, para, list, table, formula, figure
    raw: str
    level: int = 0
    text: str = ""
    lead: str | None = None  # félkövér bevezető
    items: list[str] = field(default_factory=list)
    rows: list[list[str]] = field(default_factory=list)
    header: list[str] = field(default_factory=list)


def _escape(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    text = text.replace("[[", "[ [").replace("]]", "] ]").replace("{{", "{ {").replace("}}", "} }")
    text = text.replace("<!--", "< !--").replace("-->", "-- >")
    return re.sub(r"^#+\s*", "", text)


def _inline(tok) -> tuple[str, str | None]:
    """Inline token -> (szöveg, félkövér bevezető vagy None)."""
    parts: list[str] = []
    lead = None
    children = [c for c in (tok.children or []) if not (c.type == "text" and not c.content)]
    k = 0
    if len(children) >= 3 and children[0].type == "strong_open":
        j = 1
        buf = []
        while j < len(children) and children[j].type != "strong_close":
            buf.append(children[j].content if children[j].type in ("text", "code_inline") else " ")
            j += 1
        head = "".join(buf).strip()
        rest = children[j + 1].content if j + 1 < len(children) and children[j + 1].type == "text" else ""
        if head and len(head) <= 90 and (head[-1] in ".:?!" or rest[:1] in ".:"):
            lead = head.rstrip(".:?! ")
            k = j + 1
            if rest[:1] in ".:":
                children = list(children)
                parts.append(rest[1:])
                k += 1
    for child in children[k:]:
        if child.type in ("text", "code_inline"):
            parts.append(child.content)
        elif child.type in ("softbreak", "hardbreak"):
            parts.append(" ")
    return "".join(parts).strip(), lead


def _images(tok) -> list[str]:
    return [c.content or c.attrs.get("alt", "") for c in (tok.children or []) if c.type == "image"]


def segment(md: str, read_figure_captions: bool = False) -> list[Seg]:
    tokens = MarkdownIt("commonmark").enable("table").parse(md)
    lines = md.split("\n")
    segs: list[Seg] = []

    def raw(tok) -> str:
        if not tok.map:
            return ""
        a, b = tok.map
        return "\n".join(lines[a:b]).strip("\n")

    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t.type == "heading_open":
            text, _ = _inline(tokens[i + 1])
            segs.append(Seg("heading", raw(t), level=int(t.tag[1]), text=text))
            i += 3
            continue
        if t.type == "paragraph_open":
            inline = tokens[i + 1]
            text, lead = _inline(inline)
            if read_figure_captions:
                for alt in _images(inline):
                    if alt.strip():
                        segs.append(Seg("figure", raw(t), text=alt))
            if re.fullmatch(r"\s*[-]\s*", text) and "$$" in raw(t):
                segs.append(Seg("formula", raw(t), text=text.strip()))
            elif text:
                segs.append(Seg("para", raw(t), text=text, lead=lead))
            i += 3
            continue
        if t.type in ("bullet_list_open", "ordered_list_open"):
            close = t.type.replace("_open", "_close")
            depth, j, items = 0, i, []
            while j < len(tokens):
                tj = tokens[j]
                if tj.type == t.type:
                    depth += 1
                elif tj.type == close:
                    depth -= 1
                    if depth == 0:
                        break
                elif tj.type == "inline":
                    text, lead = _inline(tj)
                    if lead:
                        text = f"{lead}: {text}"
                    if text:
                        items.append(text)
                j += 1
            segs.append(Seg("list", raw(t), items=items))
            i = j + 1
            continue
        if t.type == "table_open":
            j, rows, header, cur, in_head = i, [], [], [], False
            while j < len(tokens) and tokens[j].type != "table_close":
                tj = tokens[j]
                if tj.type == "thead_open":
                    in_head = True
                elif tj.type == "thead_close":
                    in_head = False
                elif tj.type == "tr_open":
                    cur = []
                elif tj.type == "tr_close":
                    (header if in_head else rows).append(cur) if not in_head else header.extend(cur)
                elif tj.type == "inline":
                    cur.append(_inline(tj)[0])
                j += 1
            segs.append(Seg("table", raw(t), header=header, rows=rows))
            i = j + 1
            continue
        if t.type == "fence":
            if t.info.strip().lower() in MATH_FENCES:
                segs.append(Seg("formula", raw(t), text=t.content))
            i += 1
            continue
        i += 1
    return segs


# --- címszintek ---

def _heading_plan(segs: list[Seg]) -> dict[int, int]:
    """Forrás címszint -> forgatókönyv-szint. Egyetlen nyitó H1 = dokumentumcím (saját fejezete
    a bevezető), a csak alcímeket tartalmazó "burkoló" szint (pl. `## 1. rész`) nem lesz fejezet."""
    heads = [(k, s) for k, s in enumerate(segs) if s.kind == "heading"]
    levels = sorted({s.level for _, s in heads})
    if not levels:
        return {}
    title_level = None
    if len(levels) > 1 and sum(1 for _, s in heads if s.level == levels[0]) == 1 and heads[0][1].level == levels[0]:
        title_level = levels[0]
    rest = [lv for lv in levels if lv != title_level]
    wrappers: set[int] = set()
    for lv in rest[:-1]:
        idx = [k for k, s in heads if s.level == lv]
        if all(k + 1 < len(segs) and segs[k + 1].kind == "heading" and segs[k + 1].level > lv for k in idx):
            wrappers.add(lv)
        else:
            break
    chapter_levels = [lv for lv in rest if lv not in wrappers]
    plan: dict[int, int] = {}
    if title_level is not None:
        plan[title_level] = 1
    for lv in wrappers:
        plan[lv] = 0  # beolvad a következő fejezetcímbe
    for n, lv in enumerate(chapter_levels):
        plan[lv] = min(1 + n, 3)
    return plan


NUM_HEAD_RE = re.compile(r"^(\d+)\.\s+(?=\S)")
ROMAN_RE = re.compile(r"\b([IVXLC]+)\.\s+(?=[a-záéíóöőúüű])")


def _heading_words(text: str) -> str:
    # "1. rész" -> "Első rész", "1. Elektromos ..." -> "Első. Elektromos ..."
    text = NUM_HEAD_RE.sub(lambda m: ordinal(int(m.group(1))).capitalize()
                           + (" " if text[m.end():m.end() + 1].islower() else ". "), text)
    text = ROMAN_RE.sub(lambda m: (ordinal(roman_to_int(m.group(1))) + " ") if roman_to_int(m.group(1)) else
                        m.group(0), text)
    return text


# --- jelöléstáblázat ---

ACC_CONS_T = ("j", "l", "ly", "n", "ny", "r", "s", "sz", "z", "zs")
CASE_SUFFIX_RE = re.compile(r"(tól|től|ból|ből|ról|ről|nak|nek|val|vel|hoz|hez|höz|ban|ben|ként|ért|ra|re|ig)$")


def accusative(word: str) -> str | None:
    """Egyszerű főnév tárgyesete: erő -> erőt, töltés -> töltést, térerősség -> térerősséget."""
    w = word
    if not re.fullmatch(r"[A-ZÁÉÍÓÖŐÚÜŰ]?[a-záéíóöőúüű-]+", w) or len(w) < 2:
        return None
    if w[-1] == "a":
        return w[:-1] + "át"
    if w[-1] == "e":
        return w[:-1] + "ét"
    if w[-1] in "áéiíoóöőuúüű":
        return w + "t"
    if w.endswith(ACC_CONS_T):
        return w + "t"
    last_vowel = next((c for c in reversed(w) if c in "aáeéiíoóöőuúüű"), "e")
    link = "o" if last_vowel in "aáoóuú" else ("ö" if last_vowel in "öőüű" else "e")
    return w + link + "t"


def _top_split(text: str, sep: str = ",") -> list[str]:
    parts, depth, cur = [], 0, []
    for k, c in enumerate(text):
        depth += c == "("
        depth -= c == ")"
        decimal = 0 < k < len(text) - 1 and text[k - 1].isdigit() and text[k + 1].isdigit()
        if c == sep and depth == 0 and not decimal:
            parts.append("".join(cur).strip())
            cur = []
        else:
            cur.append(c)
    parts.append("".join(cur).strip())
    return [p for p in parts if p]


def _art(word: str) -> str:
    return "Az" if word[:1].lower() in "aáeéiíoóöőuúüű" else "A"


class Builder:
    def __init__(self, store: list[str], fallback: Fallback | None):
        self.store = store
        self.fallback = fallback
        self.stats = Stats()
        self.ctx = Ctx()

    # képlet (blokk) -> mondatok
    def formula_sentences(self, src: str) -> list[tuple[str, bool]]:
        """[(mondat, gyanús-e)]"""
        try:
            parts = speak(src, self.ctx)
            self.stats.formulas += len(parts)
            self.stats.spoken += len(parts)
            return [(sentence(p) + " " + PAUSE, False) for p in parts]
        except MathSpeakError:
            pass
        # képletenként újra: a jók megmaradnak, a rossz egyedül kap jelölést (mátrixot nem bontunk sorokra)
        pieces = []
        for big in re.split(r"\\qquad", src):
            pieces += [big] if "\\begin" in big else re.split(r"\\quad(?![a-zA-Z])|\\\\", big)
        pieces = [p for p in pieces if p.strip(" ,;\n")]
        out = []
        for p in pieces:
            p = p.strip().rstrip(",;")
            self.stats.formulas += 1
            try:
                out.append((sentence(speak_one(p, self.ctx)) + " " + PAUSE, False))
                self.stats.spoken += 1
                continue
            except MathSpeakError:
                pass
            spoken = self.fallback(p) if self.fallback else None
            if spoken:
                self.stats.llm += 1
                out.append((sentence(spoken) + " " + PAUSE, False))
            else:
                self.stats.suspects.append(p.strip())
                out.append(("Itt egy képlet következik, lásd a jegyzetben.", True))
        return out

    def prose(self, text: str) -> tuple[str, bool]:
        r = verbalize_prose(_escape(text), self.ctx, self.store, self.fallback)
        self.stats.formulas += r.formulas
        self.stats.spoken += r.spoken
        self.stats.llm += r.llm
        self.stats.suspects += r.suspects
        return with_pauses(r.text, r.pause_after, PAUSE), bool(r.suspects)

    def symbol_words(self, cell: str) -> list[tuple[str, str | None]]:
        """Jel cella -> [(jel kimondva, definiáló képlet kimondva vagy None)]; `ε = ε₀εᵣ, k = 1/(4πε)`."""
        out = []
        for part in _top_split(cell.strip()):
            src = span_source(part, self.store)
            if re.search(r"[=≈]", part):
                lhs = re.split(r"[=≈]", src)[0].strip()
                out.append((speak_one(lhs, self.ctx), speak_one(src, self.ctx)))
            else:
                out.append((speak_one(src, self.ctx), None))
        if not out:
            raise MathSpeakError("Üres jel cella")
        return out

    def symbol_row(self, row: list[str], unit_col: int | None, mean_col: int) -> list[tuple[str, bool]]:
        sym_cell = row[0] if row else ""
        meaning = row[mean_col] if mean_col < len(row) else ""
        unit = row[unit_col] if unit_col is not None and unit_col < len(row) else ""
        self.stats.formulas += 1
        # magyarázó zárójel a jel cellában: "ℓ (vagy d)" -> a jelentés zárójelébe kerül
        note = re.search(r"\s*\(([^()]*[a-záéíóöőúüű]{3,}[^()]*)\)", sym_cell)
        if note:
            sym_cell = sym_cell[:note.start()] + sym_cell[note.end():]
            meaning = f"{meaning} ({note.group(1)})" if "(" not in meaning else f"{meaning}, {note.group(1)}"
        try:
            syms = self.symbol_words(sym_cell)
            self.stats.spoken += 1
        except MathSpeakError:
            self.stats.suspects.append(sym_cell)
            text, _ = self.prose(" ".join(c for c in row if c))
            return [(text, True)]
        meanings = _top_split(meaning)
        units = _top_split(unit) if unit.strip() else []
        paired = not any(re.match(r"(illetve|ill\.|és|vagy)\b", x) for x in meanings)
        if paired and len(syms) > 1 and len(meanings) == len(syms) and len(units) in (0, 1, len(syms)):
            out = []
            for k, (s, d) in enumerate(syms):
                u = units[k] if len(units) == len(syms) else (units[0] if units else "")
                out.append(self._symbol_sentence([s], d, [meanings[k]], u))
            return out
        defs = [d for _, d in syms if d]
        return [self._symbol_sentence([s for s, _ in syms], ", ".join(defs) or None, meanings, unit)]

    def _unit_words(self, unit: str) -> tuple[str, bool]:
        """Mértékegység cella -> ", mértékegysége ..." (több egység vesszővel)."""
        parts = _top_split(unit)
        spoken = [speak_unit(p) for p in parts]
        if parts and all(spoken):
            if len(spoken) == 1:
                u = spoken[0]
                if u == "nincs":
                    return ", mértékegysége nincs", False
                single = " " not in re.sub(r"\{\{[^|]*\|[^}]*\}\}", "x", u)  # type: ignore[arg-type]
                return f", mértékegysége {'a ' if single else ''}{u}", False
            return ", mértékegysége " + ", illetve ".join(spoken), False  # type: ignore[arg-type]
        text, sus = self.prose(unit.strip())
        return f", mértékegysége: {PAUSE_RE.sub('', text).rstrip('.')}", sus

    def _symbol_sentence(self, syms: list[str], definition: str | None, meanings: list[str],
                         unit: str) -> tuple[str, bool]:
        names = syms[0] if len(syms) == 1 else " és ".join(
            [syms[0]] + [f"{_art(s).lower()} {s}" for s in syms[1:]])
        subject = f"{_art(names)} {names} jel"
        head, extra = (meanings[0] if meanings else ""), meanings[1:]
        paren = ""
        m = re.match(r"^(.*?)\s*(\(.*\))\s*$", head)
        if m:
            head, paren = m.group(1), m.group(2)
        suspect = False
        values: list[str] = []
        others: list[str] = []
        for x in extra:
            if re.match(r"^[≈=~∼]", x.strip()):
                spoken, sus = self.prose(x.strip())
                values.append(PAUSE_RE.sub("", spoken))
                suspect |= sus
            else:
                others.append(x)
        acc = None
        words = head.split()
        if words and len(words) <= 5 and not CASE_SUFFIX_RE.search(words[-1]) and not others \
                and "és" not in words and "illetve" not in words \
                and all(re.fullmatch(r"[a-záéíóöőúüűA-ZÁÉÍÓÖŐÚÜŰ-]+", w) for w in words):
            last = accusative(words[-1]) if words[-1].islower() or "-" in words[-1] else None
            if last:
                phrase = " ".join(words[:-1] + [last])
                has_article = words[0].lower() in ("a", "az", "egy")
                acc = phrase if has_article else f"{_art(phrase).lower()} {phrase}"
        if acc:
            text = f"{subject} {acc} jelenti"
        elif head:
            text = f"{subject} jelentése: {', '.join([head] + others)}"
        else:
            text = subject
        if paren:
            text += " " + paren
        if definition:
            text += f": {definition}"
        for v in values:
            v = re.sub(r"^közelítőleg egyenlő", "közelítőleg", v)
            v = re.sub(r"^egyenlő ", "", v)
            text += f", értéke {v[0].lower() + v[1:]}"
        tail = ""
        if unit.strip():
            tail, sus_u = self._unit_words(unit)
            suspect |= sus_u
        spoken, sus = self.prose(text)
        has_formula = bool(definition or values) or PAUSE in spoken
        spoken = PAUSE_RE.sub("", spoken).rstrip(".") + tail + "."
        return (spoken + " " + PAUSE if has_formula else spoken), suspect or sus

    def generic_row(self, header: list[str], row: list[str]) -> tuple[str, bool]:
        cells = []
        for k, c in enumerate(row):
            if not c.strip():
                continue
            h = header[k] if k < len(header) else ""
            cells.append(c if k == 0 or not h else f"{h[:1].lower() + h[1:]}: {c}")
        if not cells:
            return "", False
        first, rest = cells[0], cells[1:]
        text = first + (": " + "; ".join(rest) if rest else "") + "."
        return self.prose(text)


def _section_letters(segs: list[Seg], store: list[str]) -> set[str]:
    out: set[str] = set()
    for s in segs:
        if s.kind == "formula":
            out |= letters_in(span_source(s.text, store))
        texts = [s.text] + s.items + [c for r in s.rows for c in r]
        for t in texts:
            if t:
                out |= prose_letters(t, store)
        if s.kind == "table":
            for r in s.rows:
                if r:
                    for x in _top_split(r[0]):
                        out |= letters_in(span_source(re.split(r"[=≈]", x)[0], store))
    return out


def _orig(raw: str, store: list[str]) -> list[str]:
    body = restore_inline_latex(raw, store).replace("-->", "-- >").strip("\n")
    return ["<!-- eredeti", body, "-->"]


def _fm(v: str) -> str:
    v = re.sub(r"\s+", " ", v).strip()
    if '"' in v and "'" in v:
        v = v.replace('"', "”")
    return f"'{v}'" if '"' in v else f'"{v}"'


def prepare_markdown(md: str, title: str, author: str, source: str, read_footnotes: bool = False,
                     read_figure_captions: bool = False, fallback: Fallback | None = None
                     ) -> tuple[str, list[str], Stats]:
    md = md.replace("\r\n", "\n")
    m = FRONT_RE.match(md)
    if m:
        md = md[m.end():]
    footnotes: list[str] = []
    body: list[str] = []
    for line in md.split("\n"):
        fm = FOOTNOTE_DEF_RE.match(line)
        if fm:
            footnotes.append(fm.group(2))
            continue
        body.append(line)
    md = FOOTNOTE_REF_RE.sub("", "\n".join(body))
    store: list[str] = []
    md = protect_inline_latex(md, store)
    segs = segment(md, read_figure_captions)
    b = Builder(store, fallback)
    plan = _heading_plan(segs)

    heads = [s for s in segs if s.kind == "heading"]
    if heads and plan.get(heads[0].level) == 1 and heads[0] is segs[0] and len(heads) > 1 \
            and sum(1 for h in heads if h.level == heads[0].level) == 1:
        title = title if title and title != title_from_filename(Path(source)) else heads[0].text

    lines = ["---", "format: ttsmd/1", f"title: {_fm(title)}", f"author: {_fm(author)}", "language: hu",
             f"source: {_fm(source)}", "---", ""]
    chapters = 0
    cur_level = 0
    pending_wrap: list[Seg] = []
    k = 0
    # szakaszonkénti kis/nagybetű-környezet (2. szintig)
    bounds = [i for i, s in enumerate(segs) if s.kind == "heading" and 0 < plan.get(s.level, 1) <= 2]
    ctx_at: dict[int, set[str]] = {}
    edges = [0] + bounds + [len(segs)]
    for a, z in pairwise(edges):
        letters = _section_letters(segs[a:z], store)
        for i in range(a, z):
            ctx_at[i] = both_cases(letters)

    out: list[str] = []

    def chapter(text_title: str, raw_lines: list[str]) -> None:
        nonlocal chapters, cur_level
        out.extend(raw_lines)
        out.extend([f"# {text_title}", ""])
        chapters += 1
        cur_level = 1

    def ensure_chapter() -> None:
        if chapters == 0:
            out.extend([f"# {_escape(title)}", ""])
            _bump()

    def _bump() -> None:
        nonlocal chapters, cur_level
        chapters += 1
        cur_level = 1

    while k < len(segs):
        s = segs[k]
        b.ctx = Ctx(ctx_at.get(k, set()))
        if s.kind == "heading":
            lvl = plan.get(s.level, 1)
            if lvl == 0:
                pending_wrap.append(s)
                k += 1
                continue
            raw = "\n\n".join(w.raw for w in pending_wrap + [s])
            words = [_heading_words(w.text) for w in pending_wrap + [s]]
            text, _ = b.prose(". ".join(x.rstrip(".") for x in words))
            text = PAUSE_RE.sub("", text)
            pending_wrap = []
            if lvl == 1:
                chapter(_escape(text), _orig(raw, store))
            else:
                ensure_chapter()
                out.extend(_orig(raw, store) + [f"{'#' * lvl} {_escape(text)}", ""])
                cur_level = lvl
            k += 1
            continue
        ensure_chapter()
        group = [s]
        if s.kind == "para" and s.text.rstrip().endswith(":") and k + 1 < len(segs) \
                and segs[k + 1].kind == "formula":
            group.append(segs[k + 1])
        out.extend(_orig("\n\n".join(g.raw for g in group), store))
        for g in group:
            out.extend(_render(b, g, cur_level))
        k += len(group)

    if read_footnotes and footnotes:
        ensure_chapter()
        out.extend(["## Lábjegyzetek", ""])
        for fn in footnotes:
            text, sus = b.prose(fn)
            out.extend((["<!-- MATH_SUSPECT -->"] if sus else []) + [text, ""])
    if chapters == 0:
        out.extend([f"# {_escape(title)}", "", "(A dokumentumban nem található felolvasható szöveg.)", ""])
    warnings = []
    st = b.stats
    if st.formulas:
        warnings.append(f"{st.formulas} képlet, ebből {st.spoken} szabályalapú felolvasással"
                        + (f", {st.llm} helyi nyelvi modellel" if st.llm else "") + " készült: hallgasd meg ellenőrzésképp.")
    if st.suspects:
        warnings.append(f"{len(st.suspects)} képletgyanús blokk. Képletes anyaghoz a Claude skill ajánlott.")
    text = "\n".join(lines + out)
    text = re.sub(r"\n{3,}", "\n\n", text).rstrip() + "\n"
    return text, warnings, st


def _render(b: Builder, s: Seg, cur_level: int) -> list[str]:
    out: list[str] = []
    if s.kind == "para":
        if s.lead:
            lead_text = PAUSE_RE.sub("", b.prose(_heading_words(s.lead))[0])
            if cur_level < 3:
                out.extend([f"{'#' * (cur_level + 1)} {_escape(lead_text)}", ""])
                text = s.text
            else:
                text = f"{s.lead}. {s.text}"
        else:
            text = s.text
        if text.strip():
            spoken, sus = b.prose(text)
            out.extend((["<!-- MATH_SUSPECT -->"] if sus else []) + [spoken, ""])
        return out
    if s.kind == "formula":
        for sent, sus in b.formula_sentences(span_source(s.text, b.store)):
            out.extend((["<!-- MATH_SUSPECT -->"] if sus else []) + [sent, ""])
        return out
    if s.kind == "list":
        items = []
        any_sus = False
        for it in s.items:
            spoken, sus = b.prose(it)
            any_sus |= sus
            items.append(f"- {spoken}")
        return (["<!-- MATH_SUSPECT -->"] if any_sus else []) + items + [""]
    if s.kind == "figure":
        text, _ = b.prose(f"Ábra: {s.text}")
        return [text, ""]
    if s.kind == "table":
        header = [h.strip() for h in s.header]
        low = [h.lower() for h in header]
        is_symbols = bool(header) and low[0] in SYMBOL_HEADERS and any("jelent" in h for h in low)
        if is_symbols:
            mean_col = next(i for i, h in enumerate(low) if "jelent" in h)
            unit_col = next((i for i, h in enumerate(low) if "egység" in h), None)
            if cur_level < 3:
                out.extend([f"{'#' * (cur_level + 1)} Jelölések", ""])
            for r in s.rows:
                for sent, sus in b.symbol_row(r, unit_col, mean_col):
                    out.extend((["<!-- MATH_SUSPECT -->"] if sus else []) + [sent, ""])
        else:
            for r in s.rows:
                sent, sus = b.generic_row(header, r)
                if sent:
                    out.extend((["<!-- MATH_SUSPECT -->"] if sus else []) + [sent, ""])
        return out
    return out


def find_math(md: str) -> bool:
    """Van-e képlet a Markdown forrásban (LaTeX blokk, `$...$` vagy Unicode képletrész)."""
    if re.search(r"```\s*(latex|math|tex|katex)\b|\$\$|(?<!\\)\$[^$\n]+\$|\\\(|\\\[", md):
        return True
    return any(sp.is_formula for line in md.split("\n") for sp in find_spans(line))

