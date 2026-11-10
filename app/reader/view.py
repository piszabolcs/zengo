"""Olvasónézet adatai: a forgatókönyv blokkjai csoportokba fogva, eredeti szöveggel és időzítéssel.

Csoport: egy `eredeti` megjegyzéssel kezdődő blokk és az utána következő, saját eredeti nélküli
blokkok (pl. egy táblázatból több felolvasott mondat lett). Eredeti nélküli címek és bekezdések
saját csoportot alkotnak, az írott alakjukkal.
"""

from __future__ import annotations

import hashlib
import html
import re

from markdown_it import MarkdownIt

from app.reader.timing import load_timing
from app.ttsmd.models import Script, ScriptBlock
from app.ttsmd.validator import written_form

PAUSE_RE = re.compile(r"\s*\[\[\s*pause\s+\d+\s*\]\]")
MATH_FENCES = {"latex", "tex", "math", "katex"}

_md = MarkdownIt("commonmark", {"html": False}).enable("table")


def _fence(self, tokens, idx, options, env) -> str:
    tok = tokens[idx]
    if tok.info.strip().lower() in MATH_FENCES:
        tex = tok.content.strip()
        return f'<div class="math-display" data-tex="{html.escape(tex)}">{html.escape(tex)}</div>\n'
    return f"<pre><code>{html.escape(tok.content)}</code></pre>\n"


_md.add_render_rule("fence", _fence)


def render_markdown(text: str) -> str:
    return _md.render(text)


def chapter_block_sig(script: Script, chapter_index: int) -> str:
    """A fejezet felolvasott blokkjainak ujjlenyomata: ha változik, az időzítés elavult."""
    h = hashlib.sha1()
    for b in script.blocks:
        if b.chapter_index == chapter_index:
            h.update(f"{b.id}\x1f{b.kind}\x1f{b.text}\x1e".encode())
    return h.hexdigest()


def _written_html(b: ScriptBlock) -> str:
    text = html.escape(PAUSE_RE.sub("", written_form(b.text)).strip())
    if b.kind == "chapter":
        return f"<h2>{text}</h2>"
    if b.kind in ("h2", "h3"):
        return f"<h3>{text}</h3>"
    if b.kind == "list_item":
        return f'<p class="li">{text}</p>'
    return f"<p>{text}</p>"


def build_reader(script: Script, project_dir) -> dict:
    timing = load_timing(project_dir)["chapters"]
    chapters: dict[int, dict] = {}
    for b in script.blocks:
        if b.chapter_index < 0:
            continue
        ch = chapters.get(b.chapter_index)
        if ch is None:
            t = timing.get(str(b.chapter_index))
            fresh = bool(t) and t.get("sig") == chapter_block_sig(script, b.chapter_index)
            ch = chapters[b.chapter_index] = {
                "index": b.chapter_index, "title": PAUSE_RE.sub("", written_form(b.text)).strip(),
                "audio": bool(t and t.get("mp3")), "synced": fresh, "duration": t["duration"] if t else None,
                "groups": [], "_times": _block_times(t) if fresh else {},
            }
        groups = ch["groups"]
        joins = (b.original is None and b.kind != "chapter" and groups and groups[-1]["has_original"])
        if joins:
            groups[-1]["blocks"].append(b.id)
        else:
            groups.append({
                "id": b.id, "blocks": [b.id], "has_original": b.original is not None,
                "html": render_markdown(b.original) if b.original is not None else _written_html(b),
            })
    out = []
    for idx in sorted(chapters):
        ch = chapters[idx]
        times = ch.pop("_times")
        for g in ch["groups"]:
            spans = [times[bid] for bid in g["blocks"] if bid in times]
            g["start"] = min(s for s, _ in spans) if spans else None
            g["end"] = max(e for _, e in spans) if spans else None
        out.append(ch)
    return {"title": script.title, "chapters": out}


def _block_times(t: dict) -> dict[str, tuple[float, float]]:
    times: dict[str, tuple[float, float]] = {}
    for bid, start, end in t.get("segments", []):
        s, e = times.get(bid, (start, end))
        times[bid] = (min(s, start), max(e, end))
    return times
