"""Képletolvasó-jelentés: lefedettség és összevetés egy Claude-dal készült referencia-forgatókönyvvel.

    uv run python -m app.prepare.math_report jegyzet.md [referencia.tts.md]
"""

from __future__ import annotations

import difflib
import re
import sys
from pathlib import Path

from app.normalize.hu import Normalizer
from app.prepare.math_doc import prepare_markdown
from app.ttsmd.parser import parse
from app.ttsmd.validator import INLINE_PRON_RE, validate_text

FORMULA_HINT_RE = re.compile(r"```latex|[=≈∫∮∑√∂∇]")


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _groups(text: str) -> dict[str, str]:
    """`eredeti` forrás -> a hozzá tartozó felolvasott szöveg (címek nélkül, kiejtés feloldva)."""
    script, _ = parse(text)
    out: dict[str, str] = {}
    key = None
    for b in script.blocks:
        if b.original is not None:
            key = _norm(b.original)
            out.setdefault(key, "")
        if key is None or b.kind not in ("paragraph", "list_item"):
            continue
        spoken = INLINE_PRON_RE.sub(lambda m: m.group(2), b.text)
        spoken = re.sub(r"\[\[pause \d+\]\]", " ", spoken)
        out[key] = _norm(out[key] + " " + spoken)
    return out


def _words(text: str) -> list[str]:
    return re.findall(r"[a-záéíóöőúüű]+", text.lower())


def report(md: str, reference: str | None = None, source: str = "jegyzet.md") -> dict:
    text, _warnings, stats = prepare_markdown(md, Path(source).stem, "Ismeretlen", source)
    _, val = validate_text(text, Normalizer().normalize)
    result = {
        "formulas": stats.formulas,
        "spoken": stats.spoken,
        "llm": stats.llm,
        "suspects": stats.suspects,
        "coverage": stats.coverage,
        "errors": len(val.errors),
        "warnings": len(val.warnings),
        "other_warnings": [w.message for w in val.warnings if "MATH_SUSPECT" not in w.message],
        "script": text,
    }
    if reference:
        mine, ref = _groups(text), _groups(reference)
        ratios = []
        for key, spoken in mine.items():
            if key in ref and FORMULA_HINT_RE.search(key) and spoken and ref[key]:
                ratios.append(difflib.SequenceMatcher(None, _words(spoken), _words(ref[key])).ratio())
        result["compared_parts"] = len(ratios)
        result["similarity"] = sum(ratios) / len(ratios) if ratios else 0.0
    return result


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    md = Path(argv[0]).read_text(encoding="utf-8-sig")
    ref = Path(argv[1]).read_text(encoding="utf-8-sig") if len(argv) > 1 else None
    r = report(md, ref, Path(argv[0]).name)
    print(f"Képletek: {r['formulas']}, szabályalapú: {r['spoken']}, nyelvi modell: {r['llm']}, "
          f"MATH_SUSPECT: {len(r['suspects'])} -> lefedettség {r['coverage'] * 100:.1f}%")
    print(f"Validátor: {r['errors']} hiba, {r['warnings']} figyelmeztetés "
          f"({len(r['other_warnings'])} nem MATH_SUSPECT)")
    if "similarity" in r:
        print(f"Referenciával összevetett képletes részek: {r['compared_parts']}, "
              f"átlagos szóegyezés: {r['similarity'] * 100:.0f}%")
    for s in r["suspects"]:
        print(f"  Claude kell: {s[:160]}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
