"""Rövid szünetek utólagos beszúrása vesszőnél, zárójelnél, gondolatjelnél és tört előtt.

A diffúziós modell a vesszőn sokszor átszalad. A minőségellenőrző felismerő szóidőbélyegei megadják,
hol ér véget a vessző előtti szó; ott a hangban a legcsendesebb pontot keressük, és csendet szúrunk be
(a már meglévő szünetet beszámítva). Ha a szóhatár nem tiszta (nincs csendes pont), nem vágunk.
"""

from __future__ import annotations

import bisect
import re
from difflib import SequenceMatcher
from pathlib import Path

import numpy as np
import soundfile as sf

SOFT_PAUSES = {"comma": 0.18, "paren": 0.20, "dash": 0.20, "fraction": 0.12}
# a "csend" küszöbe a beszéd medián energiájához képest; a tört előtt ("tér | egy per") a modell egybeolvaszt,
# ott a legcsendesebb ponton akkor is vágunk, ha nem csend: a rövid megszakítás hangsúlyt ad az "egy"-nek
QUIET = {"comma": 0.12, "paren": 0.12, "dash": 0.12, "fraction": 0.8}

_SOFT = re.compile(
    r"(?P<comma>,)(?=\s)"
    r"|(?P<paren>\s*[()]\s*)"
    r"|(?P<dash>\s+[–—-]\s+)"
    r"|(?P<fraction>(?<=\w)\s+(?=egy per\b))",
    re.IGNORECASE,
)
_WORD = re.compile(r"\w+(?:[-']\w+)*")
_FOLD = str.maketrans({"í": "i", "ó": "o", "ú": "u", "ő": "ö", "ű": "ü", "á": "a", "é": "e"})

FRAME_S = 0.01
SEARCH_PAD_S = 0.06
FADE_S = 0.005


def _fold(word: str) -> str:
    return re.sub(r"[^\w]", "", word.lower()).translate(_FOLD)


def pause_points(text: str) -> tuple[list[str], list[tuple[int, float, str]]]:
    """A szöveg szavai és a (szóindex, szünet mp, fajta) hármasok: a szünet az adott szó UTÁN jön."""
    matches = list(_WORD.finditer(text))
    ends = [m.end() for m in matches]
    points: dict[int, tuple[float, str]] = {}
    for m in _SOFT.finditer(text):
        before = bisect.bisect_right(ends, m.start())  # ennyi szó ér véget a határ előtt
        if before == 0 or before >= len(matches):
            continue  # a chunk elején / végén a szünetet a chunkok közti szünet adja
        i = before - 1
        kind = m.lastgroup
        if SOFT_PAUSES[kind] > points.get(i, (0.0, ""))[0]:
            points[i] = (SOFT_PAUSES[kind], kind)
    return [m.group(0) for m in matches], [(i, p, k) for i, (p, k) in sorted(points.items())]


def _envelope(data: np.ndarray, sr: int) -> np.ndarray:
    win = max(1, int(sr * FRAME_S))
    n = len(data) // win
    return np.sqrt(np.mean(data[: n * win].reshape(n, win) ** 2, axis=1)) if n else np.zeros(0)


def _find_gap(env: np.ndarray, t0: float, t1: float, quiet: float) -> tuple[int, float] | None:
    """A [t0, t1] környékén a legcsendesebb keret indexe és a körülötte már meglévő csend hossza."""
    lo = max(0, int((min(t0, t1) - SEARCH_PAD_S) / FRAME_S))
    hi = min(len(env), int((max(t0, t1) + SEARCH_PAD_S) / FRAME_S) + 1)
    if hi - lo < 1:
        return None
    k = lo + int(np.argmin(env[lo:hi]))
    if env[k] > quiet:
        return None
    a = k
    while a > 0 and env[a - 1] <= quiet:
        a -= 1
    b = k
    while b + 1 < len(env) and env[b + 1] <= quiet:
        b += 1
    return k, (b - a + 1) * FRAME_S


def insert_pauses(wav: Path, text: str, asr_words: list[tuple[str, float, float]]) -> int:
    """Szünetek beszúrása a WAV-ba helyben. Visszaadja a beszúrt szünetek számát."""
    words, points = pause_points(text)
    if not points or not asr_words:
        return 0
    sm = SequenceMatcher(None, [_fold(w) for w in words], [_fold(w) for w, _, _ in asr_words], autojunk=False)
    mapping: dict[int, int] = {}
    for a, b, size in sm.get_matching_blocks():
        for k in range(size):
            mapping[a + k] = b + k
    data, sr = sf.read(str(wav), dtype="float32")
    if data.ndim > 1:
        data = data.mean(axis=1)
    env = _envelope(data, sr)
    voiced = env[env > env.max() * 0.1] if env.size else env
    if voiced.size == 0:
        return 0
    level = float(np.median(voiced))
    cuts: list[tuple[int, float]] = []
    for i, pause, kind in points:
        j = mapping.get(i)
        if j is None or mapping.get(i + 1) != j + 1:
            continue  # a felismerés itt eltér a szövegtől: nem kockáztatunk vágást
        gap = _find_gap(env, asr_words[j][2], asr_words[j + 1][1], level * QUIET[kind])
        if gap is None:
            continue
        frame, existing = gap
        add = pause - existing
        if add >= 0.03:
            cuts.append((int((frame + 0.5) * FRAME_S * sr), add))
    if not cuts:
        return 0
    fade = int(sr * FADE_S)
    parts, prev = [], 0
    for pos, add in cuts:
        seg = data[prev:pos].copy()
        if fade and len(seg) > 2 * fade:
            seg[-fade:] *= np.linspace(1.0, 0.0, fade, dtype=np.float32)
            if prev:
                seg[:fade] *= np.linspace(0.0, 1.0, fade, dtype=np.float32)
        parts += [seg, np.zeros(int(sr * add), dtype=np.float32)]
        prev = pos
    tail = data[prev:].copy()
    if fade and len(tail) > fade:
        tail[:fade] *= np.linspace(0.0, 1.0, fade, dtype=np.float32)
    parts.append(tail)
    sf.write(str(wav), np.concatenate(parts), sr, subtype="PCM_16")
    return len(cuts)
