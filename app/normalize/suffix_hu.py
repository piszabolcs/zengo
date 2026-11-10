"""Toldalékos számok: a szám szóalakja + toldalék magánhangzó-illeszkedéssel (6.3, 8. lépés).

A szám utolsó tagjának hangrendje (mély / magas / magas ajakkerekítéses) határozza meg a toldalék
alakját, a tőváltozatok (`három` -> `hárm-`, `hét` -> `het-`, `ezer` -> `ezr-`) táblázatból jönnek.
"""

from __future__ import annotations

import re

BACK, FRONT, ROUND = 0, 1, 2

# utolsó számtag -> (hangrend, magánhangzós tő, kötőhangzó a -t / -s előtt)
NUMERAL_TAILS: dict[str, tuple[int, str, str]] = {
    "nulla": (BACK, "nullá", ""),
    "egy": (FRONT, "egy", "e"),
    "kettő": (ROUND, "kettő", ""),
    "három": (BACK, "hárm", "a"),
    "négy": (FRONT, "négy", "e"),
    "öt": (ROUND, "öt", "ö"),
    "hat": (BACK, "hat", "o"),
    "hét": (FRONT, "het", "e"),
    "nyolc": (BACK, "nyolc", "a"),
    "kilenc": (FRONT, "kilenc", "e"),
    "tíz": (FRONT, "tíz", "e"),
    "húsz": (BACK, "húsz", "a"),
    "harminc": (BACK, "harminc", "a"),
    "negyven": (FRONT, "negyven", "e"),
    "ötven": (FRONT, "ötven", "e"),
    "hatvan": (BACK, "hatvan", "a"),
    "hetven": (FRONT, "hetven", "e"),
    "nyolcvan": (BACK, "nyolcvan", "a"),
    "kilencven": (FRONT, "kilencven", "e"),
    "száz": (BACK, "száz", "a"),
    "ezer": (FRONT, "ezr", "e"),
    "millió": (BACK, "millió", ""),
    "milliárd": (BACK, "milliárd", "o"),
}
_TAIL_KEYS = sorted(NUMERAL_TAILS, key=len, reverse=True)

# A 30 leggyakoribb toldalék: (mély, magas, magas-kerek) alakok.
# A sorrend számít: a gyűjtőszámnév (`-an/-en`, hárman, öten) megelőzi a `-on/-en/-ön` ragot.
SUFFIX_CLASSES: list[tuple[str, str, str]] = [
    ("ban", "ben", "ben"), ("ba", "be", "be"), ("ból", "ből", "ből"), ("nak", "nek", "nek"),
    ("tól", "től", "től"), ("ra", "re", "re"), ("ról", "ről", "ről"), ("nál", "nél", "nél"),
    ("hoz", "hez", "höz"), ("ig", "ig", "ig"), ("ért", "ért", "ért"), ("ként", "ként", "ként"),
    ("kor", "kor", "kor"), ("szor", "szer", "ször"), ("val", "vel", "vel"), ("an", "en", "en"),
    ("on", "en", "ön"), ("s", "s", "s"), ("t", "t", "t"), ("ul", "ül", "ül"),
    ("nként", "nként", "nként"), ("stul", "stül", "stül"), ("szoros", "szeres", "szörös"),
    ("nyi", "nyi", "nyi"), ("i", "i", "i"), ("ba", "be", "be"), ("hoz", "hez", "höz"),
    ("ig", "ig", "ig"), ("ul", "ül", "ül"), ("kor", "kor", "kor"),
]
_COLLECTIVE = 15
_SUPERESSIVE = 16
_ADJ_S = 17
_ACC_T = 18

_VOWELS = "aáeéiíoóöőuúüű"
_LINK_VOWELS = "aoeö"
_DIGRAPHS = ("dzs", "cs", "dz", "gy", "ly", "ny", "sz", "ty", "zs")


def _class_of(written: str) -> int | None:
    for i, cls in enumerate(SUFFIX_CLASSES):
        if written in cls:
            return i
    return None


def numeral_tail(word: str) -> tuple[int, str, str]:
    """(hangrend, magánhangzós tő, kötőhangzó) a számnév utolsó tagja alapján."""
    last = word.split("-")[-1]
    for key in _TAIL_KEYS:
        if last.endswith(key):
            harmony, vstem, link = NUMERAL_TAILS[key]
            return harmony, word[: len(word) - len(key)] + vstem, link
    h = word_harmony(word)
    return h, word, "o" if h == BACK else ("ö" if h == ROUND else "e")


def word_harmony(word: str) -> int:
    for ch in reversed(word.lower()):
        if ch in "aáoóuú":
            return BACK
        if ch in "öőüű":
            return ROUND
        if ch in "eé":
            return FRONT
        if ch in "ií":
            # az i/í semleges: a korábbi magánhangzó dönt
            continue
    return FRONT


def _double_last_consonant(word: str) -> str:
    for dg in _DIGRAPHS:
        if word.endswith(dg):
            return word[: -len(dg)] + dg[0] + dg
    return word + word[-1]


def _render(word: str, idx: int) -> str:
    harmony, vstem, link = numeral_tail(word)
    form = SUFFIX_CLASSES[idx][harmony]
    vowel_final = word[-1] in _VOWELS
    if idx in (_ADJ_S, _ACC_T):
        if idx == _ADJ_S and word.endswith("kettő"):
            return word[:-1] + "es"
        return vstem + form if vowel_final or not link else vstem + link + form
    if idx == _COLLECTIVE:
        if word.endswith("kettő"):
            return word[:-2] + "tten"
        return vstem + ("a" if harmony == BACK else "e") + "n" if not vowel_final else vstem + "n"
    if idx == _SUPERESSIVE:
        return vstem + "n" if vowel_final else word + form
    if form in ("val", "vel"):
        return vstem + form if vowel_final else _double_last_consonant(word) + form[1:]
    return vstem + form if vowel_final else word + form


def apply_suffix(word: str, suffix: str) -> str:
    """Számnév + írott toldalék. Ismert toldalékot újraillesztve, ismeretlent változatlanul fűz."""
    suffix = suffix.lower()
    idx = _class_of(suffix)
    # hasonult -val/-vel: 'hússzal', 'öttel', 'egygyel' -> a 'val' osztály
    m = re.fullmatch(r"([^aáeéiíoóöőuúüű]{1,3})([ae]l)", suffix)
    if idx is None and m:
        idx = _class_of("v" + m.group(2))
    if idx is None and len(suffix) == 2 and suffix[0] in _LINK_VOWELS and suffix[1] in "ts":
        idx = _ACC_T if suffix[1] == "t" else _ADJ_S
    if idx is not None:
        return _render(word, idx)
    _, vstem, _ = numeral_tail(word)
    if suffix and suffix[0] in _VOWELS:
        return vstem + suffix
    return word + suffix


_DAY_SUFFIX_RE = re.compile(r"^(?:j?[áé](?P<tail>n|ig|tól|től|i)|j?[ae])$")


def is_day_suffix(suffix: str) -> bool:
    return bool(_DAY_SUFFIX_RE.match(suffix.lower()))


def day_possessive(ordinal: str) -> str:
    """'nyolcadik' -> 'nyolcadika', 'első' -> 'elseje', 'negyedik' -> 'negyedike'."""
    if ordinal.endswith("első"):
        return ordinal[:-4] + "elseje"
    if ordinal.endswith("második"):
        return ordinal + "a"
    return ordinal + ("a" if word_harmony(ordinal) == BACK else "e")


def day_with_suffix(ordinal: str, suffix: str) -> str:
    """Hónap napja toldalékkal: 'nyolcadikán', 'elsején', 'tizenötödikéig'."""
    base = day_possessive(ordinal)
    m = _DAY_SUFFIX_RE.match(suffix.lower())
    tail = (m.group("tail") if m else "") or ""
    if not tail:
        return base
    long_base = base[:-1] + {"a": "á", "e": "é"}[base[-1]]
    if tail in ("tól", "től"):
        tail = "tól" if base[-1] == "a" else "től"
    return long_base + tail
