"""Forgatókönyv-validátor (6.3, L3-01)."""

from __future__ import annotations

import re
from collections.abc import Callable

from app.ttsmd.models import Issue, Script, ValidationReport
from app.ttsmd.parser import parse

DIRECTIVE_RE = re.compile(r"\[\[(.*?)\]\]")
PAUSE_RE = re.compile(r"^pause\s+(\d+)$")
LATEX_RE = re.compile(r"\\[A-Za-z]")
MATH_CHARS_RE = re.compile("[∀-⋿Α-Ωα-ω\U0001d400-\U0001d7ff²³¹⁰-₟]")
DIGIT_RE = re.compile(r"\d")
INLINE_PRON_RE = re.compile(r"\{\{([^{}|]*)\|([^{}]*)\}\}")


def written_form(text: str) -> str:
    """A `{{írott|kiejtés}}` jelölések helyén az írott alak (címek megjelenítéséhez, fájlnévhez)."""
    return INLINE_PRON_RE.sub(lambda m: m.group(1), text)

REQUIRED_FIELDS = ("format", "title", "language")


def _check_inline(text: str, line: int, errors: list[Issue]) -> None:
    for m in DIRECTIVE_RE.finditer(text):
        body = m.group(1).strip()
        pm = PAUSE_RE.match(body)
        if not pm:
            errors.append(Issue(line=line, message=f"Ismeretlen direktíva: [[{body}]]"))
        elif not 0 <= int(pm.group(1)) <= 10000:
            errors.append(Issue(line=line, message=f"A szünet hossza 0 és 10000 ms között lehet: {body}"))
    rest = DIRECTIVE_RE.sub("", text)
    if "[[" in rest or "]]" in rest:
        errors.append(Issue(line=line, message="Lezáratlan [[...]] direktíva."))
    pos = 0
    while True:
        start = text.find("{{", pos)
        if start < 0:
            break
        end = text.find("}}", start + 2)
        if end < 0:
            errors.append(Issue(line=line, message="Lezáratlan {{...}} kiejtési jelölés."))
            break
        inner = text[start + 2:end]
        if "|" not in inner or "{{" in inner:
            errors.append(Issue(line=line, message=f"Hibás kiejtési jelölés: {{{{{inner}}}}} (helyes: {{{{írott|kiejtés}}}})"))
        pos = end + 2
    if "}}" in re.sub(r"\{\{.*?\}\}", "", text):
        errors.append(Issue(line=line, message="Párosítatlan }} a szövegben."))


def validate_script(script: Script, parse_issues: list[Issue],
                    normalize: Callable[[str], tuple[str, list[str]]] | None = None) -> ValidationReport:
    errors: list[Issue] = list(parse_issues)
    warnings: list[Issue] = []
    fm = script.front_matter
    fm_missing = any(i.message.startswith("Hiányzó front matter") for i in parse_issues)
    if not fm_missing:
        for field in REQUIRED_FIELDS:
            if not str(fm.get(field, "")).strip():
                errors.append(Issue(line=1, message=f"Hiányzó kötelező front matter mező: {field}"))
        if fm.get("format") and fm.get("format") != "ttsmd/1":
            errors.append(Issue(line=1, message=f"Ismeretlen formátum: {fm.get('format')} (elvárt: ttsmd/1)"))
        if "symbols" in fm and not isinstance(fm["symbols"], dict):
            errors.append(Issue(line=1, message="A symbols mezőnek leképezésnek kell lennie."))

    if not script.chapters():
        errors.append(Issue(line=1, message="Nincs egyetlen # fejezet sem."))

    for ln in script.math_suspect_lines:
        warnings.append(Issue(line=ln, message="Képletgyanús blokk (MATH_SUSPECT): ellenőrizd a felolvasást."))

    for b in script.blocks:
        _check_inline(b.text, b.line, errors)
        if b.chapter_index < 0:
            warnings.append(Issue(line=b.line, message="Szöveg az első fejezetcím előtt: nem olvasódik fel."))
            continue
        spoken = INLINE_PRON_RE.sub(lambda m: m.group(2), b.text)
        if LATEX_RE.search(spoken):
            warnings.append(Issue(line=b.line, message="LaTeX parancs a szövegben."))
        if normalize is None:
            if MATH_CHARS_RE.search(spoken):
                warnings.append(Issue(line=b.line, message="Matematikai szimbólum a szövegben."))
            continue
        normalized, norm_warnings = normalize(b.text)
        # normalizálás után: a mértékegység (pl. kΩ) már szó, a görög betű viszont megmarad
        if MATH_CHARS_RE.search(normalized):
            warnings.append(Issue(line=b.line, message="Matematikai szimbólum maradt a szövegben."))
        for w in norm_warnings:
            warnings.append(Issue(line=b.line, message=w))
        if DIGIT_RE.search(DIRECTIVE_RE.sub("", normalized)):
            warnings.append(Issue(line=b.line, message="Normalizálás után számjegy maradt."))

    errors.sort(key=lambda i: i.line)
    warnings.sort(key=lambda i: i.line)
    return ValidationReport(errors=errors, warnings=warnings)


def validate_text(text: str, normalize: Callable[[str], tuple[str, list[str]]] | None = None
                  ) -> tuple[Script, ValidationReport]:
    script, issues = parse(text)
    return script, validate_script(script, issues, normalize)
