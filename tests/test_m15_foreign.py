"""Idegen szavak és betűszavak magyar kiejtése (hunglish)."""

from app.normalize.foreign_hu import spell
from app.normalize.hu import LexiconEntry, normalize


def n(text: str) -> str:
    return normalize(text)[0]


def test_acronyms_spelled_with_hungarian_letter_names_and_suffix():
    assert n("A CPU-t a GPU-val vetjük össze.") == "A cépéút a gépéúval vetjük össze."
    assert n("Az USB és a HTML-ben") == "Az úesbé és a hátéemelben"
    assert spell("SZTK") == "esztéká"


def test_word_acronyms_and_lowercase_ones():
    assert n("A RAM-ot a BIOS ellenőrzi.") == "A ramot a bájosz ellenőrzi."
    assert n("a cpu és az url") == "a cépéú és az úerel"


def test_english_terms_with_hungarian_suffixes():
    assert n("Bootoláskor a cache-ben") == "Bútoláskor a kesben"
    assert n("commitolni kell a repository-ba") == "komitolni kell a repozitoriba"
    assert n("a Hewlett-Packard") == "a Hjúlet pekard"
    # rövid tő kötőjel nélkül csak ismert toldalékkal: a "catalog" nem "ket" + "alog"
    assert n("a catalog és a bugot") == "a catalog és a bagot"


def test_physics_names():
    assert n("A Coulomb-törvény és a Joule-hő") == "A Kulombtörvény és a Dzsúlhő"
    assert n("öt newton") == "öt nyúton"


def test_vowelless_command_names_spelled():
    assert n("az fsck és a pwd") == "az efescéká és a pévédé"


def test_digits_after_acronym_and_roman_numerals_untouched():
    assert n("MP3 és CO2") == "empé három és céó kettő"
    assert n("A XIV. fejezet") == "A tizennegyedik fejezet"


def test_shouting_heading_not_spelled():
    assert n("BEVEZETÉS A RENDSZEREKBE") == "BEVEZETÉS A RENDSZEREKBE"


def test_unknown_foreign_word_warns_and_lexicon_overrides():
    out, warnings = normalize("a framework és a throughput")
    assert "frémvörk" in out
    assert any("throughput" in w for w in warnings)
    out, _ = normalize("a CPU", [LexiconEntry("CPU", "processzor", case_sensitive=True)])
    assert out == "a processzor"
