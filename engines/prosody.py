"""Chunk szövegének prozódiai szegmensekre bontása írásjelek mentén (csak standard könyvtár).

A diffúziós modellek (F5) az írásjeleknél alig tartanak szünetet, és a hosszú szövegben elfolyik a
mondatvégi lejtés. Az erős határoknál (mondatvég, kettőspont, pontosvessző) a szegmenseket külön
generáljuk, és valódi csenddel fűzzük össze; a vessző / zárójel szünetét a fő folyamat utólag szúrja be.
"""

from __future__ import annotations

import re

# szünet másodpercben a szegmens után, a lezáró jel szerint
PAUSES = {
    "sentence": 0.42,
    "question": 0.48,
    "colon": 0.34,
    "semicolon": 0.30,
    "paren": 0.22,
    "dash": 0.22,
    "comma": 0.17,
    "fraction": 0.10,
}
# ennél rövidebb (karakterben) vesszős szegmenst a következővel vonunk össze: a felsorolás ne daraboljon
MIN_COMMA_CHARS = 14
# ennél rövidebb szegmens semmilyen jelnél nem marad önálló (az F5 a nagyon rövid szöveget elnyújtja)
MIN_CHARS = 6
# a tört ("egy per er") előtti szünetnél elég rövid az előzmény is: az "egy" ne névelőként olvadjon bele
MIN_FRACTION_CHARS = 4

_BOUNDARY = re.compile(
    r"(?P<sentence>[.!…]+[\"”»]?)(?=\s|$)"
    r"|(?P<question>\?+[\"”»]?)(?=\s|$)"
    r"|(?P<colon>:)(?=\s)"
    r"|(?P<semicolon>;)(?=\s)"
    r"|(?P<comma>,)(?=\s)"
    r"|(?P<open>\s*\(\s*)"
    r"|(?P<close>\s*\))"
    r"|(?P<dash>\s+[–—-]\s+)"
    r"|(?P<fraction>(?<=\w)\s+(?=egy per\b))"
)


# erős határok: itt külön szegmensben generálunk (a mondatvégi lejtés így minden mondatnál a helyén van)
STRONG = frozenset({"sentence", "question", "colon", "semicolon"})


def split_segments(text: str, kinds: frozenset[str] | None = None) -> list[tuple[str, float]]:
    """(szegmens szövege, utána tartandó szünet mp) párok; az utolsó szünete 0.

    `kinds`: mely határfajtáknál vágunk (alapból mindnél); a többi a szövegben marad.
    """
    raw: list[tuple[str, str]] = []  # (szöveg, jel fajtája)
    pos = 0
    buf = ""
    for m in _BOUNDARY.finditer(text):
        kind = m.lastgroup
        piece = text[pos:m.start()]
        if kinds is not None and kind not in kinds and not (kind in ("open", "close") and "paren" in kinds):
            continue
        pos = m.end()
        if kind in ("open", "close", "dash", "fraction"):
            buf += piece
            # a zárójel egy írásjel előtt (", ." stb.) nem nyit külön szünetet: az írásjel adja
            if kind == "close" and re.match(r"\s*[,.;:!?]", text[pos:]):
                continue
            raw.append((buf, "paren" if kind in ("open", "close") else kind))
        else:
            buf += piece + m.group(0)
            raw.append((buf, kind))
        buf = ""
    buf += text[pos:]
    if buf.strip():
        raw.append((buf, "end"))

    segs: list[list] = []
    carry = ""
    for seg_text, kind in raw:
        seg_text = (carry + " " + seg_text if carry else seg_text).strip()
        carry = ""
        if not seg_text:
            continue
        limit = {"comma": MIN_COMMA_CHARS, "fraction": MIN_FRACTION_CHARS}.get(kind, MIN_CHARS)
        short = len(seg_text) < limit
        if short and kind != "end":
            carry = seg_text
            continue
        segs.append([seg_text, PAUSES.get(kind, 0.0)])
    if carry:
        if segs:
            segs[-1][0] = f"{segs[-1][0]} {carry}"
        else:
            segs.append([carry, 0.0])
    # a rövid záró darab az előzőhöz tapad
    if len(segs) >= 2 and len(segs[-1][0]) < MIN_CHARS:
        tail = segs.pop()
        segs[-1][0] = f"{segs[-1][0]} {tail[0]}"
    if segs:
        segs[-1][1] = 0.0
    return [(re.sub(r"\s+", " ", t), p) for t, p in segs]
