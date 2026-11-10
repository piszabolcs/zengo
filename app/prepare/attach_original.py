"""Külön megadott eredeti jegyzet illesztése egy kész forgatókönyvhöz (`<!-- eredeti -->` megjegyzések).

Az eredeti Markdownt blokkokra bontjuk (cím, bekezdés, listaelem, táblázat, képlet), majd a
forgatókönyv blokkjaihoz sorrendtartó illesztéssel rendeljük: a felolvasott szöveg szavai nagyrészt
egyeznek az eredetiével (a képletek kimondott alakja nem, de a környező próza igen). Egy eredeti blokk
az első hozzá rendelt forgatókönyv-blokk elé kerül; a többi blokk folytatásként ugyanahhoz tartozik.
"""

from __future__ import annotations

import math
import re
from pathlib import Path

from markdown_it import MarkdownIt

from app.ttsmd.parser import parse

_WORD = re.compile(r"[^\W\d_]{3,}")
_FOLD = str.maketrans({"á": "a", "é": "e", "í": "i", "ó": "o", "ö": "o", "ő": "o", "ú": "u", "ü": "u",
                       "ű": "u"})
# a kimondott formában gyakori, az eredetiben ritka töltelékszavak nem számítanak egyezésnek
_STOP = {"egyenlő", "szorozva", "osztva", "plusz", "mínusz", "négyzet", "alsó", "index", "per"}


def _words(text: str) -> set[str]:
    return {w.lower().translate(_FOLD) for w in _WORD.findall(text) if w.lower() not in _STOP}


def original_blocks(md: str) -> list[str]:
    """Felső szintű Markdown blokkok forrásszövege; a listák elemenként."""
    lines = md.replace("\r\n", "\n").split("\n")
    tokens = MarkdownIt("commonmark").enable("table").parse(md)
    blocks: list[str] = []
    depth = 0
    for i, tok in enumerate(tokens):
        # felső szintű blokk, vagy egy felső szintű lista közvetlen eleme (a beágyazott lista a szülőben marad)
        top_item = (depth == 1 and tok.type == "list_item_open"
                    and tokens[i - 1].type in ("bullet_list_open", "ordered_list_open", "list_item_close"))
        if tok.nesting == 1 and tok.map and (depth == 0 or top_item):
            if tok.type not in ("bullet_list_open", "ordered_list_open"):
                a, b = tok.map
                blocks.append("\n".join(lines[a:b]).strip())
        elif tok.nesting == 0 and depth == 0 and tok.map and tok.type in ("fence", "code_block", "html_block",
                                                                           "hr", "math_block"):
            a, b = tok.map
            blocks.append("\n".join(lines[a:b]).strip())
        depth += tok.nesting
    return [b for b in blocks if b and not re.fullmatch(r"[-*_]{3,}", b)]


def _sim(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / math.sqrt(len(a) * len(b))


def align(script_words: list[set[str]], orig_words: list[set[str]]) -> list[int]:
    """Sorrendtartó hozzárendelés: minden forgatókönyv-blokkhoz egy eredeti blokk indexe (nem csökkenő)."""
    m, n = len(script_words), len(orig_words)
    if not m or not n:
        return [0] * m
    prev = [_sim(script_words[0], orig_words[k]) for k in range(n)]
    back: list[list[int]] = []
    for j in range(1, m):
        # prefix-maximum: a j-1. blokk legjobb pontszáma bármely k' <= k indexszel
        best_k, best_v, pm, arg = 0, -1.0, [0.0] * n, [0] * n
        for k in range(n):
            if prev[k] > best_v:
                best_v, best_k = prev[k], k
            pm[k], arg[k] = best_v, best_k
        sw = script_words[j]
        prev = [pm[k] + _sim(sw, orig_words[k]) for k in range(n)]
        back.append(arg)
    k = max(range(n), key=lambda i: prev[i])
    path = [k]
    for arg in reversed(back):
        k = arg[k]
        path.append(k)
    return path[::-1]


def has_originals(script_text: str) -> bool:
    script, _ = parse(script_text)
    return any(b.original is not None for b in script.blocks)


def strip_originals(script_text: str) -> str:
    """A forgatókönyvbe ágyazott `<!-- eredeti -->` megjegyzések eltávolítása."""
    return re.sub(r"^[ \t]*<!--[ \t]*eredeti\b.*?-->[ \t]*\n?", "", script_text, flags=re.DOTALL | re.MULTILINE)


def attach_originals(script_text: str, original_md: str) -> tuple[str, int]:
    """A forgatókönyv `<!-- eredeti -->` megjegyzésekkel; visszaadja az illesztett eredeti blokkok számát."""
    script, _ = parse(script_text)
    blocks = [b for b in script.blocks if b.text.strip()]
    origs = original_blocks(original_md)
    if not blocks or not origs:
        return script_text, 0
    path = align([_words(b.text) for b in blocks], [_words(o) for o in origs])
    # eredeti blokk -> az első forgatókönyv-blokk, amelyhez rendeltük; a kimaradók a következőhöz tapadnak
    first_for: dict[int, int] = {}
    for j, k in enumerate(path):
        first_for.setdefault(k, j)
    groups: dict[int, list[str]] = {}
    pending: list[str] = []
    last_j = None
    for k, src in enumerate(origs):
        pending.append(src)
        if k in first_for:
            groups.setdefault(first_for[k], []).extend(pending)
            pending = []
            last_j = first_for[k]
    if pending and last_j is not None:
        groups[last_j].extend(pending)
    lines = script_text.replace("\r\n", "\n").split("\n")
    for j in sorted(groups, reverse=True):
        body = "\n\n".join(groups[j]).replace("-->", "-- >")
        at = blocks[j].line - 1
        lines[at:at] = ["<!-- eredeti", body, "-->"]
    return "\n".join(lines), len(origs)


def original_markdown(path: Path) -> str:
    """Eredeti jegyzet -> Markdown (az olvasónézetben ez jelenik meg)."""
    suffix = path.suffix.lower()
    if suffix in (".md", ".markdown", ".txt"):
        return path.read_text(encoding="utf-8-sig")
    if suffix == ".docx":
        from app.prepare.docx_md import docx_to_markdown

        return docx_to_markdown(path)
    from app.ingest.registry import load_document

    doc = load_document(path)
    out = []
    for b in doc.blocks:
        if b.type == "heading":
            out.append("#" * min(6, max(1, b.level or 1)) + " " + b.text)
        else:
            out.append(b.text)
    return "\n\n".join(out)
