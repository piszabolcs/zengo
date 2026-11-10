"""Szóhiba-arány (WER) és hossz-arány ellenőrzés (6.5, L5-01)."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

WER_THRESHOLD = 0.25
CER_THRESHOLD = 0.12
RATIO_MIN, RATIO_MAX = 0.04, 0.12  # másodperc / karakter

# Betűszintű összevetéshez: a felismerő írásmódja eltérhet (epsilon / epszilon, pi / pí,
# kulombállandó / kulomb-állandó), ezek nem kiejtési hibák.
FOLD = str.maketrans({"í": "i", "ó": "o", "ú": "u", "ő": "ö", "ű": "ü"})
FOLD_SEQ = (("sz", "s"), ("cs", "c"), ("zs", "z"), ("ty", "t"), ("gy", "g"), ("ny", "n"), ("ly", "j"))


def words(text: str) -> list[str]:
    t = text.lower()
    t = re.sub(r"[^\w\s]|_", " ", t)
    return t.split()


def wer(reference: str, hypothesis: str) -> float:
    """Szószintű Levenshtein távolság / a referencia szószáma."""
    ref, hyp = words(reference), words(hypothesis)
    if not ref:
        return 0.0 if not hyp else 1.0
    prev = list(range(len(hyp) + 1))
    for i, r in enumerate(ref, start=1):
        cur = [i] + [0] * len(hyp)
        for j, h in enumerate(hyp, start=1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (r != h))
        prev = cur
    return prev[-1] / len(ref)


def folded(text: str) -> str:
    t = "".join(words(text)).translate(FOLD)
    for a, b in FOLD_SEQ:
        t = t.replace(a, b)
    return re.sub(r"(.)\1+", r"\1", t)  # kettőzött betűk egyszerűsítése


def cer(reference: str, hypothesis: str) -> float:
    """Betűszintű Levenshtein távolság szóközök nélkül, egységesített írásmóddal."""
    ref, hyp = folded(reference), folded(hypothesis)
    if not ref:
        return 0.0 if not hyp else 1.0
    prev = list(range(len(hyp) + 1))
    for i, r in enumerate(ref, start=1):
        cur = [i] + [0] * len(hyp)
        for j, h in enumerate(hyp, start=1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (r != h))
        prev = cur
    return prev[-1] / len(ref)


def length_ratio(duration_s: float, text: str) -> float:
    return duration_s / max(1, len(text))


@dataclass
class QaResult:
    ok: bool
    wer: float
    ratio: float
    recognized: str = ""
    # a felismerő szavai időbélyeggel (szó, kezdet, vég); a szünetbeszúráshoz
    words: list[tuple[str, float, float]] = field(default_factory=list)


def evaluate(expected: str, recognized: str, duration_s: float) -> QaResult:
    w = wer(expected, recognized)
    ratio = length_ratio(duration_s, expected)
    close = w <= WER_THRESHOLD or cer(expected, recognized) <= CER_THRESHOLD
    ok = close and RATIO_MIN <= ratio <= RATIO_MAX
    return QaResult(ok=ok, wer=w, ratio=ratio, recognized=recognized)
