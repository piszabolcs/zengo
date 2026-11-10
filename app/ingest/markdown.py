"""Markdown importer: címek, bekezdések, `[^1]` lábjegyzetek, LaTeX képletgyanú (L1-02)."""

from __future__ import annotations

import re
from pathlib import Path

from markdown_it import MarkdownIt

from app.ingest.base import BlockBuilder, Document, ImportError, title_from_filename

FOOTNOTE_DEF_RE = re.compile(r"^\[\^([^\]]+)\]:\s*(.*)$")
FOOTNOTE_REF_RE = re.compile(r"\[\^[^\]]+\]")
LATEX_RE = re.compile(r"\$\$.+?\$\$|\$[^$\n]+\$", re.DOTALL)
FRONT_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
REF_OPEN, REF_CLOSE = "\u2063", "\u2064"
REF_PH_RE = re.compile(REF_OPEN + "(.*?)" + REF_CLOSE)


def _inline_text(token) -> tuple[str, list[str]]:
    """Inline token szövege; a képek alt szövegét külön adja vissza."""
    parts: list[str] = []
    images: list[str] = []
    for child in token.children or []:
        if child.type in ("text", "code_inline"):
            parts.append(child.content)
        elif child.type in ("softbreak", "hardbreak"):
            parts.append(" ")
        elif child.type == "image":
            images.append(child.content or child.attrs.get("alt", "") or "")
        elif child.type == "html_inline":
            continue
    return "".join(parts), images


class MarkdownImporter:
    def can_handle(self, path: Path) -> bool:
        name = path.name.lower()
        return (name.endswith((".md", ".markdown"))) and not name.endswith(".tts.md")

    def load(self, path: Path) -> Document:
        try:
            raw = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeDecodeError) as e:
            raise ImportError(f"A fájl nem nyitható meg: {e}") from e
        raw = raw.replace("\r\n", "\n")
        title = title_from_filename(path)
        author = None
        m = FRONT_RE.match(raw)
        if m:
            for line in m.group(1).splitlines():
                k, _, v = line.partition(":")
                if k.strip() == "title" and v.strip():
                    title = v.strip().strip("\"'")
                elif k.strip() == "author" and v.strip():
                    author = v.strip().strip("\"'")
            raw = raw[m.end():]

        # lábjegyzet-definíciók kigyűjtése (a folytatósorokkal együtt), hivatkozások törlése
        footnotes: dict[str, str] = {}
        body_lines: list[str] = []
        current: str | None = None
        for line in raw.split("\n"):
            fm = FOOTNOTE_DEF_RE.match(line)
            if fm:
                current = fm.group(1)
                footnotes[current] = fm.group(2)
                continue
            if current is not None and line.startswith(("    ", "\t")) and line.strip():
                footnotes[current] += " " + line.strip()
                continue
            current = None
            body_lines.append(line)
        # a hivatkozás helyőrzőt kap, hogy a lábjegyzet a hivatkozó bekezdés után kerüljön be
        body = FOOTNOTE_REF_RE.sub(lambda m: f"{REF_OPEN}{m.group(0)[2:-1]}{REF_CLOSE}", "\n".join(body_lines))
        emitted: set[str] = set()
        pending: list[str] = []

        def emit_refs(text: str) -> str:
            for label in REF_PH_RE.findall(text):
                if label in footnotes and label not in emitted:
                    emitted.add(label)
                    pending.append(footnotes[label])
            return REF_PH_RE.sub("", text)

        bb = BlockBuilder()
        tokens = MarkdownIt("commonmark").enable("table").parse(body)
        i = 0
        in_table = False
        while i < len(tokens):
            t = tokens[i]
            if t.type == "heading_open":
                level = min(int(t.tag[1]), 3)
                text, _ = _inline_text(tokens[i + 1])
                text = emit_refs(text)
                bb.add("heading", text, level=level, math_suspect=bool(LATEX_RE.search(text)))
                i += 3
                continue
            if t.type == "table_open":
                in_table = True
                bb.add("figure", "")
            elif t.type == "table_close":
                in_table = False
            elif t.type == "inline" and not in_table:
                text, images = _inline_text(t)
                text = emit_refs(text)
                for alt in images:
                    bb.add("figure", alt)
                if text.strip():
                    bb.add("paragraph", text, math_suspect=bool(LATEX_RE.search(text)))
                for fn in pending:
                    bb.add("footnote", fn, math_suspect=bool(LATEX_RE.search(fn)))
                pending.clear()
            elif t.type in ("fence", "code_block"):
                pass  # forráskód nem olvasható fel
            elif t.type == "math_block":
                bb.add("paragraph", t.content, math_suspect=True)
            i += 1
        for label, fn in footnotes.items():
            if label not in emitted:
                bb.add("footnote", fn, math_suspect=bool(LATEX_RE.search(fn)))
        # $$...$$ blokkok a commonmark szerint bekezdésként jönnek: jelölés
        for b in bb.blocks:
            if "$$" in b.text:
                b.math_suspect = True
        return Document(title=title, author=author, source_path=str(path), blocks=bb.blocks)
