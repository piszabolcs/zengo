"""Képletek a folyó szövegben: Unicode képletrészek (`F = qE`, `ε₀εᵣ`) és `$...$` LaTeX felismerése,
kiolvasása a `mathspeak_hu` szabályaival.

Egy képletrész ott kezdődik, ahol matematikai jel (görög betű, index, műveleti vagy relációjel) van,
és addig tart, amíg képletelemek (rövid betűjelek, számok, jelek, zárójelek) követik egymást. Magyar
szó, vessző, pontosvessző, kettőspont, mondatvég vagy a mondat zárójele lezárja.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass, field

from app.normalize.hu import LETTER_NAMES
from app.normalize.suffix_hu import apply_suffix
from app.prepare.mathspeak_hu import (
    ADD_WORDS,
    GREEK,
    PRIMES,
    REL_WORDS,
    SUBSCRIPTS,
    SUPERSCRIPTS,
    UNICODE_FUNCS,
    VEC_MARK,
    VULGAR,
    Ctx,
    MathSpeakError,
    letters_in,
    speak_one,
)

# `$...$` helyőrzők: magánhasználatú karakterek (a normalizáló helyőrzőitől eltérő tartomány)
PH_BASE = 0xE000
PH_MAX = 0xE8FF
PH_CLASS = f"[{chr(PH_BASE)}-{chr(PH_MAX)}]"
PH_RE = re.compile(PH_CLASS)

SCRIPT_SIGNS = "⁺⁻⁼⁽⁾₊₋₌₍₎"
STRONG_CHARS = ((set(GREEK) | set(SUPERSCRIPTS) | set(SUBSCRIPTS) | set(PRIMES) | set(VULGAR)
                 | {VEC_MARK, "ℓ", "ħ"}) - {"'"})
OP_CHARS = set("=≈≠<>≤≥≡∝∼~→⇒⇔∥⊥↔+±∓−·⋅×∙/^_*∫∬∭∮∯∑∏√∛∂∇∞…|‖°%")
SEED_OPS = OP_CHARS - {"/", "%", "°", "|"}
HU_SHORT_WORDS = {
    "a", "az", "e", "o", "s", "és", "is", "ha", "ez", "le", "be", "ki", "el", "fel", "de", "mi", "ma", "ne",
    "se", "na", "ő", "ön", "én", "te", "mű", "ott", "itt", "van", "nem", "sem", "még", "már", "csak", "egy",
    "két", "pl", "ill", "vagy", "fok", "tér", "rá", "jó", "kis", "sok", "pár", "mag", "ami", "aki", "hol",
}
TOKEN_RE = re.compile(
    rf"(?P<ph>{PH_CLASS})"
    rf"|(?P<word>(?:[^\W_]|[′″{VEC_MARK}{SCRIPT_SIGNS}])+)"
    r"|(?P<space>\s+)"
    r"|(?P<paren>[()\[\]])"
    r"|(?P<op>[" + re.escape("".join(sorted(OP_CHARS))) + r"\-–])"
    r"|(?P<punct>.)",
    re.DOTALL,
)
LETTER_WORDS = set(LETTER_NAMES.values()) | set(GREEK.values())
TRAIL_RE = re.compile(r"[\s=≈≠<>≤≥≡∝∼~→⇒⇔∥⊥↔+±∓−·⋅×∙/^_*\-–]+$")
LEAD_RE = re.compile(r"^[\s,;:]+")


@dataclass
class Span:
    start: int
    end: int
    src: str
    is_formula: bool  # reláció vagy művelet van benne (utána szünet jár)


@dataclass
class ProseResult:
    text: str
    formulas: int = 0
    spoken: int = 0
    suspects: list[str] = field(default_factory=list)
    llm: int = 0
    pause_after: list[int] = field(default_factory=list)


def protect_inline_latex(text: str, store: list[str]) -> str:
    """`$$...$$`, `$...$`, `\\(...\\)`, `\\[...\\]` -> helyőrző karakter; a LaTeX forrás a `store`-ba."""
    def repl(m: re.Match) -> str:
        body = next(g for g in m.groups() if g is not None)
        if len(store) > PH_MAX - PH_BASE:
            return m.group(0)
        store.append(body)
        return chr(PH_BASE + len(store) - 1)

    return re.sub(r"\$\$(.+?)\$\$|(?<![\\$])\$(?!\s)([^$\n]+?)(?<!\s)\$|\\\((.+?)\\\)|\\\[(.+?)\\\]",
                  repl, text, flags=re.DOTALL)


def restore_inline_latex(text: str, store: list[str]) -> str:
    def repl(m: re.Match) -> str:
        body = store[ord(m.group(0)) - PH_BASE]
        return f"$${body}$$" if "\n" in body else f"${body}$"

    return PH_RE.sub(repl, text)


def span_source(src: str, store: list[str]) -> str:
    """A helyőrzőket visszacseréli LaTeX-re (a lexer a vegyes Unicode + LaTeX szöveget is érti)."""
    return PH_RE.sub(lambda m: "{" + store[ord(m.group(0)) - PH_BASE] + "}", src)


def _word_kind(w: str) -> str:
    """strong / weak / func / num / prose"""
    if any(c in STRONG_CHARS or c in SCRIPT_SIGNS for c in w):
        return "strong"
    if w.isascii() and w.isdigit():
        return "num"
    if any(c.isdigit() for c in w):
        return "strong" if re.fullmatch(r"\d+[A-Za-z]{1,3}", w) else "prose"
    if not w.isascii():
        return "prose"
    if w in UNICODE_FUNCS or w == "lim":
        return "func"
    if w.lower() in HU_SHORT_WORDS and (w.islower() or w[1:].islower()):
        return "prose"
    if len(w) == 1:
        return "weak"
    if len(w) <= 3 and (any(c.isupper() for c in w[1:]) or (w[0].isupper() and len(w) == 2)
                        or not re.search("[aeiouAEIOU]", w)):
        return "weak"
    return "prose"


def _kinds(toks: list[tuple[str, str, int, int]]) -> list[str]:
    n = len(toks)
    kinds: list[str] = []
    for i, (g, v, _s, _e) in enumerate(toks):
        if g == "word":
            kind = _word_kind(v)
            # műveleti jelhez tapadó rövid szó képletelem: e^(−t/τ), H_in, m/s
            if kind == "prose" and len(v) <= 6 and (
                    (i > 0 and toks[i - 1][0] == "op" and toks[i - 1][1] in "_^/·*")
                    or (len(v) == 1 and i + 1 < n and toks[i + 1][0] == "op" and toks[i + 1][1] in "^_/−+·×=")):
                kind = "weak"
            kinds.append(kind)
        elif g == "op" and v in "-–":
            # kötőjel szóösszetételben ("D-vonal", "ε-szeres"): nem mínusz
            prev_tight = i > 0 and toks[i - 1][0] in ("word", "paren")
            nxt = toks[i + 1] if i + 1 < n else None
            # toldalék: "ℓ-t", "0-ra", "R-rel" (rövid kisbetűs szó, utána nem folytatódik a szó)
            suffix = (nxt is not None and nxt[0] == "word" and re.fullmatch(r"[a-záéíóöőúüű]{1,5}", nxt[1])
                      and (i + 2 >= n or toks[i + 2][0] != "word"))
            next_word = nxt is not None and nxt[0] == "word" and (_word_kind(nxt[1]) == "prose" or bool(suffix))
            dash_loose = v == "–" and not (i > 0 and toks[i - 1][0] == "space")
            kinds.append("hyphen" if (prev_tight and next_word) or dash_loose else "op")
        elif (g == "punct" and v == "," and 0 < i < n - 1 and toks[i - 1][1].isdigit()
              and toks[i + 1][1].isdigit()):
            kinds.append("num")  # tizedesvessző
        else:
            kinds.append(g or "punct")
    return kinds


MEMBER = {"strong", "weak", "func", "num", "op", "paren", "ph"}


def find_spans(text: str) -> list[Span]:
    toks = [(m.lastgroup or "punct", m.group(0), m.start(), m.end()) for m in TOKEN_RE.finditer(text)]
    kinds = _kinds(toks)
    n = len(toks)
    spans: list[Span] = []
    i = 0
    while i < n:
        if kinds[i] not in MEMBER:
            i += 1
            continue
        j = i
        while j < n and (kinds[j] in MEMBER or (kinds[j] == "space" and j + 1 < n and kinds[j + 1] in MEMBER)):
            j += 1
        s, e = toks[i][2], toks[j - 1][3]
        i = j
        for a, b in _paren_split(text, s, e):
            sp = _make_span(text, a, b)
            if sp is not None:
                spans.append(sp)
    return spans


def _paren_split(text: str, s: int, e: int) -> list[tuple[int, int]]:
    """A párosítatlan zárójeleknél kettévágja a részt (a mondat zárójele nem a képlet része)."""
    stack: list[int] = []
    cuts: list[int] = []
    for k in range(s, e):
        c = text[k]
        if c in "([":
            stack.append(k)
        elif c in ")]":
            if stack:
                stack.pop()
            else:
                cuts.append(k)
    cuts += stack
    out, a = [], s
    for c in sorted(cuts):
        out.append((a, c))
        a = c + 1
    out.append((a, e))
    return [(x, y) for x, y in out if y > x]


def _wraps(src: str) -> bool:
    """`(...)` egésze egy zárójelpár-e."""
    if not (src.startswith("(") and src.endswith(")")):
        return False
    depth = 0
    for k, c in enumerate(src):
        depth += c == "("
        depth -= c == ")"
        if depth == 0 and k < len(src) - 1:
            return False
    return True


def _make_span(text: str, s: int, e: int) -> Span | None:
    src = text[s:e]
    m = LEAD_RE.match(src)
    if m:
        s, src = s + m.end(), src[m.end():]
    m = TRAIL_RE.search(src)
    if m and m.start() > 0:
        e, src = e - (len(src) - m.start()), src[:m.start()]
    stripped = src.strip()
    s += len(src) - len(src.lstrip())
    src = stripped
    # a teljes egészében zárójeles rész a mondat zárójele: "(F = qE)"
    while _wraps(src):
        src, s = src[1:-1].strip(), s + 1
    e = s + len(src)
    if not src:
        return None
    seeded = any(c in STRONG_CHARS or c in SEED_OPS or c in SCRIPT_SIGNS or PH_RE.match(c) for c in src)
    # a "/" csak két oldalán képletelemmel számít képletnek (az "és/vagy" nem az)
    if not seeded and not re.fullmatch(r"\S+\s*/\s*\S+.*", src):
        return None
    if not seeded and not any(_word_kind(w) in ("strong", "weak", "num")
                              for w in re.findall(r"[^\W_]+", src.split("/")[0])):
        return None
    has_op = any(c in OP_CHARS - {"°", "%"} for c in src) or bool(PH_RE.search(src))
    return Span(s, e, src, has_op)


def _lone_op_words(src: str) -> str | None:
    s = src.strip()
    if len(s) > 1:
        s = s.rstrip("-–")  # "−-tól": a kötőjel a toldaléké
    if s in ("-", "−", "–"):
        return "mínusz"
    if s in ADD_WORDS:
        return ADD_WORDS[s]
    if s in REL_WORDS:
        return REL_WORDS[s]
    return {"/": "per", "·": "szorozva", "×": "szorozva", "∞": "végtelen"}.get(s)


def prose_letters(text: str, store: list[str]) -> set[str]:
    out: set[str] = set()
    for sp in find_spans(text):
        out |= letters_in(span_source(sp.src, store))
    return out


Fallback = Callable[[str], "str | None"]


def verbalize_prose(text: str, ctx: Ctx, store: list[str], fallback: Fallback | None = None) -> ProseResult:
    """A szövegben talált képletrészek helyére a kimondott alak; a nem érthetőké `suspects`-be."""
    res = ProseResult(text="")
    out: list[str] = []
    pos = 0
    for sp in find_spans(text):
        if sp.start < pos:
            continue
        out.append(text[pos:sp.start])
        pos = sp.end
        lone = _lone_op_words(sp.src)
        if lone is not None:
            out.append(lone)
            continue
        src = span_source(sp.src, store)
        res.formulas += 1
        try:
            spoken = speak_one(src, ctx)
            res.spoken += 1
        except MathSpeakError:
            spoken = fallback(src) if fallback else None
            if spoken:
                res.llm += 1
            else:
                res.suspects.append(sp.src)
                spoken = "képlet, lásd a jegyzetben"
        # toldalék a képlet után ("0-ra", "εᵣ-szeres"): számnévhez illesztve, a "tart ...-hoz" után elhagyva
        m = re.match(r"-([a-záéíóöőúüű]+)\b", text[pos:])
        if m:
            last = spoken.split(" ")[-1]
            if re.search(r"(hoz|hez|höz)$", last) and " tart " in f" {spoken} ":
                pos += m.end()
            elif last in NUMBER_WORDS or re.fullmatch(r"[a-záéíóöőúüű]+", last) and last not in LETTER_WORDS:
                spoken = spoken[: len(spoken) - len(last)] + apply_suffix(last, m.group(1))
                pos += m.end()
        before = "".join(out)
        # névelő a kimondott alakhoz: "Az M" -> "A nagy em"
        am = re.search(r"(?:^|(?<=\s))([Aa])z? $", before)
        if am:
            art = "az" if spoken[:1].lower() in "aáeéiíoóöőuúüű" else "a"
            if am.group(1) == "A":
                art = art.capitalize()
            before = before[: am.start(1)] + art + " "
            out = [before]
        if not before.strip() or re.search(r"[.!?]\s+$", before) and not ABBREV_END_RE.search(before):
            spoken = spoken[0].upper() + spoken[1:]
        if before[-1:].isalnum():
            spoken = " " + spoken
        if text[pos:pos + 1].isalnum():
            spoken += " "
        out.append(spoken)
        if sp.is_formula:
            res.pause_after.append(len("".join(out)))
    out.append(text[pos:])
    res.text = LEFTOVER_RE.sub(lambda m: f" {LEFTOVER[m.group(0)]} ", "".join(out))
    res.text = re.sub(r"[ \t]{2,}", " ", res.text)
    return res


LEFTOVER = {"·": "szorozva", "×": "szorozva", "−": "mínusz", "→": "nyíl", "↔": "megfelel", "∥": "párhuzamos",
            "⊥": "merőleges", "≈": "körülbelül", "∞": "végtelen"}
LEFTOVER["/"] = "per"
LEFTOVER_RE = re.compile("|".join(re.escape(k) for k in LEFTOVER if k != "/") + r"|/(?=\()")
ABBREV_END_RE = re.compile(r"\b(pl|stb|ill|ún|kb|vö|ld|lásd|max|min|dr|ca|kül|ford)\.\s*$", re.IGNORECASE)
NUMBER_WORDS = {"nulla", "egy", "kettő", "három", "négy", "öt", "hat", "hét", "nyolc", "kilenc", "tíz", "száz",
                "ezer", "végtelen"}


SENT_END_RE = re.compile(r"[.!?…](?=\s|$|[)\"”])")


def with_pauses(text: str, marks: list[int], pause: str = "[[pause 500]]") -> str:
    """Szünet minden olyan mondat végére, amelyben képlet volt."""
    if not marks:
        return text
    ends: set[int] = set()
    for m in marks:
        found = SENT_END_RE.search(text, m)
        while found and ABBREV_END_RE.search(text[: found.end()]):
            found = SENT_END_RE.search(text, found.end())
        e = found.end() if found else len(text)
        while e < len(text) and text[e] in ")\"”":
            e += 1
        ends.add(e)
    out = []
    last = 0
    for e in sorted(ends):
        out.append(text[last:e].rstrip())
        out.append(" " + pause)
        last = e
    out.append(text[last:])
    return "".join(out).strip()
