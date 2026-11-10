"""Magyar szöveg-normalizáló (6.3): a szöveget kiolvasható szavakra és írásjelekre alakítja.

A lépések sorrendje a specifikáció szerinti. A már kimondható alakra hozott részeket
(inline kiejtés, kiejtési szótár, direktívák) helyőrzők védik a későbbi lépésektől.
"""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Iterable
from dataclasses import dataclass

from num2words import num2words

from app.normalize import foreign_hu as foreign
from app.normalize.abbrev_hu import ABBREVIATIONS
from app.normalize.foreign_hu import foreign_warnings
from app.normalize.suffix_hu import apply_suffix, day_with_suffix, is_day_suffix
from app.normalize.units_hu import UNIT_KEYS, UNITS


@dataclass
class LexiconEntry:
    written: str
    spoken: str
    case_sensitive: bool = False


MONTHS = ["január", "február", "március", "április", "május", "június", "július", "augusztus",
          "szeptember", "október", "november", "december"]
MONTH_RE = "|".join(MONTHS)

COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
INLINE_PRON_RE = re.compile(r"\{\{([^{}|]*)\|([^{}]*)\}\}")
DIRECTIVE_RE = re.compile(r"\[\[\s*pause\s+\d+\s*\]\]")
URL_RE = re.compile(r"\b(?:https?://|www\.)[^\s<>\"]+[^\s<>\".,;:!?)]", re.IGNORECASE)
EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b")
SUFFIX = r"(?:-(?P<suf>[a-záéíóöőúüű]+))?"
HU_LOWER = "a-záéíóöőúüű"
ORDINAL_WORDS = r"(?:fejezet|oldal|tétel|évfolyam|rész|kötet|lecke|szakasz|osztály|század|alkalom)"

# Helyőrző: egyetlen magánhasználatú karakter (U+F0000-tól), így a számlépések nem érintik.
PH_BASE = 0xF0000
PH_RE = re.compile("[󰀀-󿿽]")


def _is_ph(ch: str) -> bool:
    return PH_BASE <= ord(ch) <= 0xFFFFD


def _fix_compounds(words: str) -> str:
    """num2words javítás: összetételben 'két' ('tizenkétezer', 'kétmillió'), és a milliomodik."""
    words = re.sub(r"kettő(?=(ezer|millió|milliárd|száz))", "két", words)
    words = words.replace("mmilliomodik", "milliomodik")
    return words


def cardinal(n: int) -> str:
    if n < 0:
        return "mínusz " + cardinal(-n)
    return _fix_compounds(num2words(n, lang="hu"))


def ordinal(n: int) -> str:
    return _fix_compounds(num2words(n, lang="hu", to="ordinal"))


PLACE_NAMES = {1: "tized", 2: "század", 3: "ezred"}


def decimal_words(int_part: str, frac: str) -> str:
    whole = cardinal(int(int_part))
    if len(frac) <= 3:
        return f"{whole} egész {cardinal(int(frac))} {PLACE_NAMES[len(frac)]}"
    return f"{whole} egész " + " ".join(cardinal(int(d)) for d in frac)


ROMAN_VALUES = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def roman_to_int(s: str) -> int | None:
    if not s or not re.fullmatch(r"M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})", s):
        return None
    total, prev = 0, 0
    for ch in reversed(s):
        v = ROMAN_VALUES[ch]
        total = total - v if v < prev else total + v
        prev = max(prev, v)
    return total


def _cap_like(src: str, out: str) -> str:
    return out[:1].upper() + out[1:] if src[:1].isupper() else out


class Normalizer:
    def __init__(self, lexicon: Iterable[LexiconEntry] | None = None):
        self.lexicon = list(lexicon or [])
        self._lex_patterns = []
        for e in sorted(self.lexicon, key=lambda e: len(e.written), reverse=True):
            if not e.written:
                continue
            flags = 0 if e.case_sensitive else re.IGNORECASE
            pat = re.compile(r"(?<![\w])" + re.escape(e.written) + r"(?![\w])", flags)
            self._lex_patterns.append((pat, e.spoken))
        self._abbr_map = dict(ABBREVIATIONS)
        for a, v in ABBREVIATIONS.items():
            self._abbr_map.setdefault(a[:1].upper() + a[1:], v)
        abbr_sorted = sorted(self._abbr_map, key=len, reverse=True)
        self._abbr_re = re.compile(
            r"(?<![\w.])(" + "|".join(re.escape(a) for a in abbr_sorted) + r")(?![\w])"
        )
        unit_alt = "|".join(re.escape(u) for u in UNIT_KEYS)
        self._unit_re = re.compile(
            r"(?P<num>\d(?:[\d\s.,]*\d)?)(?P<sp>\s?)(?P<unit>" + unit_alt + r")"
            r"(?![\w°%€$Ω])" + SUFFIX
        )

    # --- segédek ---
    def _protect(self, store: list[str], text: str) -> str:
        store.append(text)
        return chr(PH_BASE + len(store) - 1)

    def normalize(self, text: str, is_title: bool = False, respell: bool = True) -> tuple[str, list[str]]:
        """`respell=False`: az idegen szavak írott alakban maradnak (megjelenített fejezetcímhez)."""
        warnings: list[str] = []
        store: list[str] = []
        t = text

        # 1. HTML megjegyzések
        t = COMMENT_RE.sub(" ", t)
        # direktívák védelme (a tagoló dolgozza fel)
        t = DIRECTIVE_RE.sub(lambda m: self._protect(store, m.group(0)), t)
        # 2. inline kiejtés
        t = INLINE_PRON_RE.sub(lambda m: self._protect(store, m.group(2)), t)
        # 3. kiejtési szótár
        for pat, spoken in self._lex_patterns:
            t = pat.sub(lambda m, s=spoken: self._protect(store, s), t)
        # 4. URL és e-mail
        t = URL_RE.sub(lambda m: self._protect(store, "link"), t)
        t = EMAIL_RE.sub(lambda m: self._protect(store, "e-mail cím"), t)
        # betűszó + szám (MP3, CO2): külön szó, hogy a betűszó betűzhető maradjon ("empé három")
        t = re.sub(r"(?<![\w-])([A-Z]{2,6})(\d{1,3})(?![\w])", r"\1 \2", t)
        # 5. dátum
        t = self._dates(t)
        # 6. idő
        t = re.sub(r"(?<![\d:])([01]?\d|2[0-3]):([0-5]\d)(?![\d:])" + SUFFIX, self._time, t)
        # 7. sorszám
        t = self._ordinals(t, is_title)
        # 8. toldalékos szám (a mértékegységes alak a 9. lépésben)
        t = re.sub(r"(?<![\w,.])(\d+(?:[ .]\d{3})*)-(?P<suf>[a-záéíóöőúüű]+)\b", self._suffixed_number, t)
        # 9. mértékegység szám után
        t = self._unit_re.sub(self._unit, t)
        # negatív szám
        t = re.sub(r"(?:(?<=\s)|^)[-−–](?=\d)", "mínusz ", t)
        # 10. tizedes tört
        t = re.sub(r"(?<![\d,])(\d+),(\d+)(?![\d,])", lambda m: decimal_words(m.group(1), m.group(2)), t)
        # 11. egész szám (ezres tagolással)
        t = re.sub(r"(?<![\d])\d{1,3}(?:(?:\.|\s| | )\d{3})+(?![\d])",
                   lambda m: cardinal(int(re.sub(r"\D", "", m.group(0)))), t)
        t = re.sub(r"\d+", lambda m: cardinal(int(m.group(0))), t)
        # 12. rövidítések
        t = self._abbrev(t)
        # 12/a. idegen szavak és betűszavak magyar kiejtéssel (CPU -> cépéú, cache -> kes)
        if respell:
            t = foreign.apply(t, lambda spoken: self._protect(store, spoken), units=UNITS)
        unknown = foreign_warnings(t) if respell else []  # a már lecseréltek helyőrzők mögött vannak
        if unknown:
            warnings.append("Idegen szó, ellenőrizd a kiejtését (kiejtési szótár): " + ", ".join(unknown[:12]))
        # 12/b. önálló betűjelek (képletek szimbólumai) betűnévvel
        t = self._letters(t)
        # 13. szimbólumok
        t = self._symbols(t, warnings)
        # 14. szóközök és írásjelek
        t = self._tidy(t)
        if is_title and t:
            t = t[0].upper() + t[1:]
        # helyőrzők visszaállítása (egymásba ágyazva is)
        for _ in range(3):
            if not PH_RE.search(t):
                break
            t = PH_RE.sub(lambda m: store[ord(m.group(0)) - PH_BASE], t)
        return t, warnings

    # --- lépések ---
    def _dates(self, t: str) -> str:
        def ymd(m: re.Match) -> str:
            y, mo, d = int(m.group("y")), int(m.group("m")), int(m.group("d"))
            if not (1 <= mo <= 12 and 1 <= d <= 31):
                return m.group(0)
            suf = m.group("suf")
            day = day_with_suffix(ordinal(d), suf) if suf and is_day_suffix(suf) else (
                apply_suffix(ordinal(d), suf) if suf else day_with_suffix(ordinal(d), "a"))
            return f"{cardinal(y)} {MONTHS[mo - 1]} {day}"

        # 2026. 11. 08.  |  2026.11.08.  |  2026. 11. 08-án
        t = re.sub(r"(?<!\d)(?P<y>\d{4})\.\s?(?P<m>\d{1,2})\.\s?(?P<d>\d{1,2})(?:\.|-(?P<suf>[a-záéíóöőúüű]+))",
                   ymd, t)

        def named(m: re.Match) -> str:
            year = f"{cardinal(int(m.group('y')))} " if m.group("y") else ""
            month = m.group("mon")
            d = int(m.group("d"))
            suf = m.group("suf")
            if suf and is_day_suffix(suf):
                day = day_with_suffix(ordinal(d), suf)
            elif suf:
                day = apply_suffix(cardinal(d), suf)
            else:
                day = day_with_suffix(ordinal(d), "a")
            return f"{year}{month} {day}"

        # (2026.) november 8.  |  november 8-án
        t = re.sub(r"(?:(?P<y>\d{4})\.\s+)?(?P<mon>" + MONTH_RE + r")\s+(?P<d>\d{1,2})"
                   r"(?:\.(?!\d)|-(?P<suf>[a-záéíóöőúüű]+))", named, t, flags=re.IGNORECASE)
        # 2026. novemberben -> évszám tőszámnévként
        t = re.sub(r"(?<!\d)(\d{4})\.(?=\s+(?:" + MONTH_RE + r"))",
                   lambda m: cardinal(int(m.group(1))), t, flags=re.IGNORECASE)
        return t

    def _time(self, m: re.Match) -> str:
        h, mi = int(m.group(1)), int(m.group(2))
        out = f"{cardinal(h)} óra" + (f" {cardinal(mi)} perc" if mi else "")
        suf = m.group("suf")
        if suf:
            last = out.split(" ")[-1]
            out = out[: len(out) - len(last)] + (last + suf.lower())
        return out

    def _ordinals(self, t: str, is_title: bool) -> str:
        def arabic(m: re.Match) -> str:
            return ordinal(int(m.group(1)))

        t = re.sub(r"(?<![\w,.])(\d+)\.(?=\s+(?:[" + HU_LOWER + r"]|(?i:" + ORDINAL_WORDS + r")))", arabic, t)

        def roman(m: re.Match) -> str:
            v = roman_to_int(m.group(1))
            return ordinal(v) if v else m.group(0)

        def roman_title(m: re.Match) -> str:
            v = roman_to_int(m.group(1))
            return ordinal(v) + "." if v else m.group(0)

        if is_title:
            t = re.sub(r"^\s*([IVXLCDM]+)\.(?=\s|$)", roman_title, t)
        t = re.sub(r"(?<![\w.])([IVXLCDM]+)\.(?=\s+(?i:" + ORDINAL_WORDS + r"))", roman, t)
        return t

    def _suffixed_number(self, m: re.Match) -> str:
        n = int(re.sub(r"\D", "", m.group(1)))
        suf = m.group("suf")
        if is_day_suffix(suf) and 1 <= n <= 31:
            return day_with_suffix(ordinal(n), suf)
        return apply_suffix(cardinal(n), suf)

    def _unit(self, m: re.Match) -> str:
        num = m.group("num")
        unit = UNITS[m.group("unit")]
        suf = m.group("suf")
        return f"{num} {unit}{suf or ''}"

    def _abbrev(self, t: str) -> str:
        def repl(m: re.Match) -> str:
            src = m.group(1)
            if src.lower() in NAME_PREFIXES:
                return self._abbr_map[src]
            out = _cap_like(src, self._abbr_map[src])
            # mondatzáró pont megtartása: a rövidítés pontja egyben a mondat vége
            if src.endswith("."):
                rest = t[m.end():]
                if not rest.strip() or re.match(r"\s+[A-ZÁÉÍÓÖŐÚÜŰ\"„]", rest):
                    out += "."
            return out

        return self._abbr_re.sub(repl, t)

    def _letters(self, t: str) -> str:
        shouting = foreign._shouting(t)  # csupa nagybetűs címben az "A" névelő, nem betűjel

        def repl(m: re.Match) -> str:
            ch = m.group(0)
            if shouting and ch.isupper():
                return ch
            if ch in SENTENCE_WORD_LETTERS:
                # mondat elején névelő vagy kötőszó ("A", "S"), mondat közben jel ("per A")
                before = t[: m.start()].rstrip()
                if not before or before[-1] in ".!?:…\"„(" or _is_ph(before[-1]):
                    return ch
            return LETTER_NAMES[ch.upper()]

        return SINGLE_LETTER_RE.sub(repl, t)

    def _symbols(self, t: str, warnings: list[str]) -> str:
        t = t.replace("&", " és ").replace("+", " plusz ").replace("=", " egyenlő ").replace("→", " nyíl ")
        t = re.sub(r"(?<=[\w\U000F0000-\U000FFFFD])\s*/\s*(?=[\w\U000F0000-\U000FFFFD])", " per ", t)  # helyőrző mellett is
        removed: list[str] = []
        out = []
        for ch in t:
            if _is_ph(ch) or ch.isalnum() or ch.isspace() or ch in ALLOWED_PUNCT:
                out.append(ch)
            else:
                cat = unicodedata.category(ch)
                if cat.startswith("M"):  # kombináló jelek (pl. ékezet) maradnak
                    out.append(ch)
                    continue
                removed.append(ch)
                out.append(" ")
        if removed:
            uniq = "".join(dict.fromkeys(removed))
            warnings.append(f"Nem kiolvasható karakter törölve: {uniq}")
        return "".join(out)

    def _tidy(self, t: str) -> str:
        t = re.sub(r"[„“”«»″]", '"', t)
        t = re.sub(r"[‘’‚′]", "'", t)
        t = t.replace("...", "…")
        t = re.sub(r"\s+", " ", t)
        t = re.sub(r"\s+([,.;:!?…)])", r"\1", t)
        t = re.sub(r"([(])\s+", r"\1", t)
        t = re.sub(r"([,;:])(?=[^\s\d\"')])", r"\1 ", t)
        return t.strip()


# Név előtt álló rövidítések: utánuk nagybetű jön, de nem mondatvég.
NAME_PREFIXES = {"dr.", "id.", "ifj.", "ny.", "ford."}

# Betűnevek (6.3 / skill math-reading-hu.md). A kis "a", "e", "o", "s" magyar szó is lehet, ezért marad.
LETTER_NAMES = {
    "A": "á", "B": "bé", "C": "cé", "D": "dé", "E": "é", "F": "ef", "G": "gé", "H": "há", "I": "í", "J": "jé",
    "K": "ká", "L": "el", "M": "em", "N": "en", "O": "ó", "P": "pé", "Q": "kú", "R": "er", "S": "es", "T": "té",
    "U": "ú", "V": "vé", "W": "dupla vé", "X": "iksz", "Y": "ipszilon", "Z": "zé",
}
SENTENCE_WORD_LETTERS = {"A", "S"}
SINGLE_LETTER_RE = re.compile(r"(?<![\w'’.-])(?:[A-Z]|[bcdfghijklmnpqrtuvwxyz])(?![\w'’]|\.\w)")

ALLOWED_PUNCT = set(".,;:!?…-–—()\"'„“”«»‘’")


_default = Normalizer()


def normalize(text: str, lexicon: Iterable[LexiconEntry] | None = None, is_title: bool = False
              ) -> tuple[str, list[str]]:
    n = Normalizer(lexicon) if lexicon else _default
    return n.normalize(text, is_title=is_title)
