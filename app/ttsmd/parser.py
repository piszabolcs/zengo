"""`.tts.md` (ttsmd/1) parser (8.1, L3-01)."""

from __future__ import annotations

import re

from app.ttsmd.models import Issue, Script, ScriptBlock

COMMENT_RE = re.compile(r"<!--(.*?)-->", re.DOTALL)
ORIGINAL_RE = re.compile(r"^\s*eredeti\b[ \t]*:?[ \t]*\n?(.*)$", re.DOTALL)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
BULLET_RE = re.compile(r"^\s*[-*•]\s+(.*)$")
NUMBERED_RE = re.compile(r"^\s*\d{1,3}[.)]\s+(.*)$")


class ParseError(Exception):
    def __init__(self, issues: list[Issue]):
        super().__init__("; ".join(f"{i.line}. sor: {i.message}" for i in issues))
        self.issues = issues


def _strip_quotes(v: str) -> str:
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    return v


def _strip_inline_comment(v: str) -> str:
    # YAML: a `#` csak szóköz után kezd megjegyzést, idézőjelen kívül
    in_q = None
    for i, ch in enumerate(v):
        if ch in "\"'":
            in_q = None if in_q == ch else (in_q or ch)
        elif ch == "#" and in_q is None and (i == 0 or v[i - 1] in " \t"):
            return v[:i].rstrip()
    return v.rstrip()


def parse_front_matter(lines: list[str]) -> tuple[dict, list[Issue]]:
    """Egyszerű YAML részhalmaz: `kulcs: érték` és egy szint mélységű beágyazott leképezés."""
    data: dict = {}
    issues: list[Issue] = []
    current_map: str | None = None
    for idx, raw in enumerate(lines, start=2):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indented = raw[:1] in (" ", "\t")
        line = _strip_inline_comment(raw)
        if not line.strip():
            continue
        if ":" not in line:
            issues.append(Issue(line=idx, message=f"Érvénytelen front matter sor: {raw.strip()!r}"))
            continue
        key, _, value = line.strip().partition(":")
        key, value = key.strip(), value.strip()
        if indented and current_map is not None:
            data[current_map][_strip_quotes(key)] = _strip_quotes(value)
            continue
        if indented:
            issues.append(Issue(line=idx, message=f"Váratlan behúzás a front matterben: {raw.strip()!r}"))
            continue
        if value == "":
            data[key] = {}
            current_map = key
        else:
            data[key] = _strip_quotes(value)
            current_map = None
    return data, issues


def _blank_comments(text: str) -> tuple[str, list[int], list[tuple[int, str]]]:
    """A HTML megjegyzéseket a sorszámok megtartásával törli.

    Visszaadja a MATH_SUSPECT sorokat és az `eredeti` megjegyzéseket (záró sor, tartalom).
    """
    math_lines: list[int] = []
    originals: list[tuple[int, str]] = []

    def repl(m: re.Match) -> str:
        if m.group(1).strip() == "MATH_SUSPECT":
            math_lines.append(text.count("\n", 0, m.start()) + 1)
        orig = ORIGINAL_RE.match(m.group(1))
        if orig and orig.group(1).strip():
            originals.append((text.count("\n", 0, m.end()) + 1, orig.group(1).strip("\n").rstrip()))
        return "\n" * m.group(0).count("\n")

    return COMMENT_RE.sub(repl, text), math_lines, originals


def split_front_matter(text: str) -> tuple[list[str] | None, int, list[str]]:
    """(front matter sorai vagy None, a törzs első sorának sorszáma, törzs sorai)."""
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    if lines and lines[0].startswith("﻿"):
        lines[0] = lines[0][1:]
    if not lines or lines[0].strip() != "---":
        return None, 1, lines
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i], i + 2, lines[i + 1:]
    return None, 1, lines


def parse(text: str) -> tuple[Script, list[Issue]]:
    """A forgatókönyvet blokkokra bontja. A szerkezeti hibákat issue-ként adja vissza."""
    issues: list[Issue] = []
    fm_lines, body_start, body_lines = split_front_matter(text)
    front: dict = {}
    if fm_lines is None:
        issues.append(Issue(line=1, message="Hiányzó front matter (a fájlnak '---' sorral kell kezdődnie)."))
    else:
        front, fm_issues = parse_front_matter(fm_lines)
        issues.extend(fm_issues)

    body, math_lines, originals = _blank_comments("\n".join(body_lines))
    math_lines = [ln + body_start - 1 for ln in math_lines]
    lines = body.split("\n")

    blocks: list[ScriptBlock] = []
    chapter_index = -1
    para: list[tuple[int, str]] = []

    def add(kind: str, text: str, line: int, end_line: int) -> None:
        blocks.append(ScriptBlock(id=f"b{len(blocks) + 1}", kind=kind, text=text, line=line,
                                  end_line=end_line, chapter_index=chapter_index))

    def flush() -> None:
        if not para:
            return
        bullet = [BULLET_RE.match(t) for _, t in para]
        numbered = [NUMBERED_RE.match(t) for _, t in para]
        is_list = all(bullet) or (len(para) >= 2 and all(numbered))
        if is_list:
            matches = bullet if all(bullet) else numbered
            for (ln, _), m in zip(para, matches):
                add("list_item", m.group(1).strip(), ln, ln)
        else:
            text = " ".join(t.strip() for _, t in para)
            add("paragraph", text, para[0][0], para[-1][0])
        para.clear()

    for offset, raw in enumerate(lines):
        ln = body_start + offset
        if not raw.strip():
            flush()
            continue
        m = HEADING_RE.match(raw.strip())
        if m:
            flush()
            level = len(m.group(1))
            title = m.group(2).strip()
            if level > 3:
                issues.append(Issue(line=ln, message=f"Túl mély címszint ({'#' * level}); legfeljebb ###."))
                add("paragraph", title, ln, ln)
            elif level == 1:
                chapter_index += 1
                add("chapter", title, ln, ln)
            else:
                add("h2" if level == 2 else "h3", title, ln, ln)
            continue
        para.append((ln, raw))
    flush()
    # az `eredeti` megjegyzés az utána következő első blokkhoz tartozik
    bi = 0
    for end_line, original in originals:
        end_line += body_start - 1
        while bi < len(blocks) and blocks[bi].line <= end_line:
            bi += 1
        if bi < len(blocks) and blocks[bi].original is None:
            blocks[bi].original = original
    return Script(front_matter=front, blocks=blocks, math_suspect_lines=math_lines), issues


def chapter_text_ranges(script: Script) -> list[tuple[int, str, int]]:
    """(fejezet index, cím, sorszám) a felület fejezetlistájához."""
    return [(b.chapter_index, b.text, b.line) for b in script.blocks if b.kind == "chapter"]
