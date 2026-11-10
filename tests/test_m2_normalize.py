import pytest

from app.normalize.chunker import Chunker, ChunkSettings, chunk_hash, split_sentences
from app.normalize.hu import LexiconEntry, normalize
from app.ttsmd.parser import parse
from app.ttsmd.validator import validate_text


def n(text, **kw):
    return normalize(text, **kw)[0]


def test_acceptance_sentence():
    src = "A 3. tételben 12,5 V-os feszültséget mérünk 10 kΩ-on, pl. 2026. 11. 08-án."
    assert n(src) == ("A harmadik tételben tizenkettő egész öt tized voltos feszültséget mérünk "
                      "tíz kiloómon, például kétezer-huszonhat november nyolcadikán.")


# L3-02: számok, sorszámok, tizedes törtek, dátum, idő (40+ eset)
NUMBERS = [
    ("0", "nulla"), ("1", "egy"), ("2", "kettő"), ("7", "hét"), ("10", "tíz"), ("11", "tizenegy"),
    ("19", "tizenkilenc"), ("20", "húsz"), ("21", "huszonegy"), ("30", "harminc"), ("45", "negyvenöt"),
    ("99", "kilencvenkilenc"), ("100", "száz"), ("101", "százegy"), ("250", "kétszázötven"),
    ("1000", "ezer"), ("1848", "ezernyolcszáznegyvennyolc"), ("2000", "kétezer"),
    ("2001", "kétezer-egy"), ("2026", "kétezer-huszonhat"), ("12 500", "tizenkétezer-ötszáz"),
    ("12.500", "tizenkétezer-ötszáz"), ("1 000 000", "egymillió"), ("2500000", "kétmillió-ötszázezer"),
    ("3,14", "három egész tizennégy század"), ("12,5", "tizenkettő egész öt tized"),
    ("0,05", "nulla egész öt század"), ("2,125", "kettő egész százhuszonöt ezred"),
    ("3,14159", "három egész egy négy egy öt kilenc"), ("van -5 fok", "van mínusz öt fok"),
    ("a 3. tétel", "a harmadik tétel"), ("az 1. fejezet", "az első fejezet"),
    ("a 2. oldalon", "a második oldalon"), ("A 3. Fejezet", "A harmadik Fejezet"),
    ("a 10. évfolyam", "a tizedik évfolyam"), ("Kaptam 5. Utána", "Kaptam öt. Utána"),
    ("2026. 11. 08.", "kétezer-huszonhat november nyolcadika"),
    ("2026.11.08.", "kétezer-huszonhat november nyolcadika"),
    ("2026. 11. 08-án", "kétezer-huszonhat november nyolcadikán"),
    ("2026. 01. 01-jén", "kétezer-huszonhat január elsején"),
    ("1848. március 15-én", "ezernyolcszáznegyvennyolc március tizenötödikén"),
    ("március 15.", "március tizenötödike"), ("május 1-jén", "május elsején"),
    ("2026. novemberben", "kétezer-huszonhat novemberben"),
    ("14:30", "tizennégy óra harminc perc"), ("8:00", "nyolc óra"), ("14:30-kor", "tizennégy óra harminc perckor"),
    ("23:05", "huszonhárom óra öt perc"),
]


@pytest.mark.parametrize("src,expected", NUMBERS)
def test_numbers_dates_times(src, expected):
    assert n(src) == expected


@pytest.mark.parametrize("src,expected", [
    ("Az E térerősség egyenlő F per q.", "Az é térerősség egyenlő ef per kú."),
    ("A fluxus egyenlő B szorozva A.", "A fluxus egyenlő bé szorozva á."),
    ("A D-vonalak és a H tér.", "A dé-vonalak és a há tér."),
    ("S ekkor az r távolság.", "S ekkor az er távolság."),
    ("Az RL kör, a s e o szavak.", "Az erel kör, a s e o szavak."),
])
def test_single_letter_symbols(src, expected):
    assert normalize(src)[0] == expected


def test_title_roman_and_arabic():
    assert n("III. A váltakozó áram", is_title=True) == "Harmadik. A váltakozó áram"
    assert n("3. fejezet. A váltakozó áram", is_title=True) == "Harmadik fejezet. A váltakozó áram"
    assert n("IV. fejezet") == "negyedik fejezet"


# L3-03: toldalékos számok (30 eset)
SUFFIXED = [
    ("5-ös", "ötös"), ("3-at", "hármat"), ("10-ben", "tízben"), ("1-jén", "elsején"), ("3-mal", "hárommal"),
    ("8-cal", "nyolccal"), ("5-tel", "öttel"), ("6-os", "hatos"), ("7-es", "hetes"), ("1000-es", "ezres"),
    ("2-es", "kettes"), ("2-t", "kettőt"), ("0-ban", "nullában"), ("20-szal", "hússzal"),
    ("2026-ban", "kétezer-huszonhatban"), ("5-ösben", "ötösben"), ("3-asban", "hármasban"),
    ("5-en", "öten"), ("3-an", "hárman"), ("3-on", "háromon"), ("5-ön", "ötön"), ("10-zel", "tízzel"),
    ("100-szor", "százszor"), ("5-ször", "ötször"), ("3-ig", "háromig"), ("2-ből", "kettőből"),
    ("1-gyel", "eggyel"), ("40-nel", "negyvennel"), ("4-et", "négyet"), ("5-höz", "öthöz"),
    ("3-hoz", "háromhoz"), ("7-től", "héttől"), ("9-re", "kilencre"), ("15-én", "tizenötödikén"),
    ("6-ban", "hatban"),
]


@pytest.mark.parametrize("src,expected", SUFFIXED)
def test_suffixed_numbers(src, expected):
    assert n(src) == expected


# L3-03: mértékegységek (20+ eset)
UNITS = [
    ("12 V", "tizenkettő volt"), ("12V", "tizenkettő volt"), ("2 A", "kettő amper"), ("50 Ω", "ötven óm"),
    ("60 W", "hatvan vatt"), ("50 Hz", "ötven herc"), ("5 kHz", "öt kilohertz"), ("100 MHz", "száz megahertz"),
    ("20 mA", "húsz milliamper"), ("5 mV", "öt millivolt"), ("10 kΩ", "tíz kiloóm"), ("1 F", "egy farad"),
    ("47 µF", "negyvenhét mikrofarad"), ("10 nF", "tíz nanofarad"), ("2 H", "kettő henri"),
    ("5 mH", "öt millihenri"), ("3 s", "három másodperc"), ("20 ms", "húsz milliszekundum"),
    ("100 m", "száz méter"), ("5 cm", "öt centiméter"), ("2 mm", "kettő milliméter"),
    ("42 km", "negyvenkettő kilométer"), ("3 kg", "három kilogramm"), ("200 g", "kétszáz gramm"),
    ("25 °C", "huszonöt celsius-fok"), ("300 K", "háromszáz kelvin"), ("15%", "tizenöt százalék"),
    ("500 Ft", "ötszáz forint"), ("10 €", "tíz euró"), ("5 $", "öt dollár"),
    ("12,5 V-os", "tizenkettő egész öt tized voltos"), ("10 kΩ-on", "tíz kiloómon"),
    ("25%-kal", "huszonöt százalékkal"),
]


@pytest.mark.parametrize("src,expected", UNITS)
def test_units(src, expected):
    assert n(src) == expected


# L3-04: rövidítések, szimbólumok, kiejtési szótár, inline kiejtés
@pytest.mark.parametrize("src,expected", [
    ("pl. alma", "például alma"), ("Pl. alma", "Például alma"), ("kb. tíz", "körülbelül tíz"),
    ("ún. hatás", "úgynevezett hatás"), ("vö. fent", "vesd össze fent"), ("5 db alma", "öt darab alma"),
    ("Dr. Kiss", "doktor Kiss"), ("alma, körte stb.", "alma, körte és a többi."),
    ("alma stb. Utána", "alma és a többi. Utána"), ("max. érték", "maximum érték"),
    ("A & B", "A és bé"), ("a + b = c", "a plusz bé egyenlő cé"), ("km/óra", "kilométer per óra"),
    ("A → B", "A nyíl bé"), ("Ez... az", "Ez… az"), ("„idézet”", '"idézet"'),
    ("sok   szóköz", "sok szóköz"), ("www.pelda.hu", "link"), ("nev@pelda.hu", "e-mail cím"),
])
def test_abbrev_symbols(src, expected):
    assert n(src) == expected


def test_unreadable_char_warning():
    text, warnings = normalize("a # b")
    assert text == "a bé"
    assert warnings and "#" in warnings[0]


def test_inline_pronunciation_and_lexicon():
    assert n("{{Kirchhoff|kirhhoff}} törvénye") == "kirhhoff törvénye"
    lex = [LexiconEntry("Kirchhoff", "kirhhof"), LexiconEntry("pl.", "plusz-mínusz")]
    assert n("Kirchhoff és kirchhoff", lexicon=lex) == "kirhhof és kirhhof"
    # a szótár bejegyzése felülírja az alapértelmezett rövidítést
    assert n("pl. ez", lexicon=lex) == "plusz-mínusz ez"
    cs = [LexiconEntry("AND", "end kapu", case_sensitive=True)]
    assert n("AND és and", lexicon=cs) == "end kapu és and"
    # inline kiejtés előnyt élvez a szótárral szemben, és a számlépés nem bántja
    assert n("{{R2|er kettő}} Kirchhoff", lexicon=lex) == "er kettő kirhhof"


# L3-05 mondatbontás és chunkolás
def test_sentence_split():
    s = split_sentences("Ez az első. Ez a második! Harmadik? Negyedik… Ötödik. ez nem új")
    assert s == ["Ez az első.", "Ez a második!", "Harmadik?", "Negyedik…", "Ötödik. ez nem új"]
    assert split_sentences("Lásd pl. Kiss munkáját. Igen.") == ["Lásd pl. Kiss munkáját.", "Igen."]


SCRIPT = """---
format: ttsmd/1
title: Teszt
language: hu
---

# 3. fejezet. A váltakozó áram

Első mondat ez itt. Második mondat, ami kicsit hosszabb, és vesszőket is tartalmaz, hogy bontható legyen. Harmadik.

## Alfejezet

Szöveg [[pause 500]] folytatás 12 V-tal.

- egy elem
- másik elem

# Második fejezet

Rövid.
"""


def _plan(max_chars=60, **kw):
    script, report = validate_text(SCRIPT)
    assert report.errors == []
    s = ChunkSettings(engine_id="dummy", voice_id="v", engine_params={"seed": 1}, max_chars=max_chars, **kw)
    return Chunker(s).plan(script)


def test_chunks_respect_max_chars_and_paragraphs():
    for max_chars in (25, 40, 60, 300):
        plan = _plan(max_chars)
        for c in plan.all_chunks():
            assert len(c.text) <= max_chars, (max_chars, c.text)
    script, _ = parse(SCRIPT)
    plan = _plan(40)
    # egy chunk egyetlen blokkhoz tartozik (bekezdéshatárt nem lép át)
    block_texts = {b.id for b in script.blocks}
    assert all(c.block_id in block_texts for c in plan.all_chunks())


def test_pauses_and_announcement():
    plan = _plan(300)
    ch0 = plan.chapters[0]
    assert ch0.chunks[0].text == "Harmadik fejezet. A váltakozó áram."
    assert ch0.chunks[0].pause_after_ms == 1500
    texts = [c.text for c in ch0.chunks]
    pauses = [c.pause_after_ms for c in ch0.chunks]
    i_alf = texts.index("Alfejezet.")
    assert pauses[i_alf - 1] == 1200 and pauses[i_alf] == 800
    i_szoveg = texts.index("Szöveg")
    assert pauses[i_szoveg] == 500
    assert texts[i_szoveg + 1] == "folytatás tizenkettő volttal."
    assert pauses[i_szoveg + 1] == 700
    assert texts[-2:] == ["egy elem", "másik elem"]
    assert pauses[-2] == 350 and pauses[-1] == 2000
    assert ch0.title == "Harmadik fejezet. A váltakozó áram"
    plan2 = _plan(300, announce_chapters=False)
    assert plan2.chapters[0].chunks[0].text.startswith("Első mondat")


def test_chapter_title_keeps_written_form():
    script, _ = validate_text("---\nformat: ttsmd/1\ntitle: T\nlanguage: hu\n---\n"
                              "# A {{Biot|bió}}-{{Savart|szavár}}-törvény\n\nSzöveg.\n")
    plan = Chunker(ChunkSettings(engine_id="dummy", voice_id="v", engine_params={}, max_chars=300)).plan(script)
    assert plan.chapters[0].title == "A Biot-Savart-törvény"
    assert plan.chapters[0].chunks[0].text == "A bió-szavár-törvény."


def test_chunk_hash():
    a = chunk_hash("f5_hu", "v1", {"seed": 1, "speed": 1.0}, "Szöveg.")
    assert a == chunk_hash("f5_hu", "v1", {"speed": 1.0, "seed": 1}, "Szöveg.")
    assert a != chunk_hash("xtts", "v1", {"seed": 1, "speed": 1.0}, "Szöveg.")
    assert a != chunk_hash("f5_hu", "v2", {"seed": 1, "speed": 1.0}, "Szöveg.")
    assert a != chunk_hash("f5_hu", "v1", {"seed": 2, "speed": 1.0}, "Szöveg.")
    assert a != chunk_hash("f5_hu", "v1", {"seed": 1, "speed": 1.0}, "Szöveg!")


def test_validator_with_normalizer_flags_leftover_digits():
    from app.normalize.hu import normalize as norm
    text = "---\nformat: ttsmd/1\ntitle: X\nlanguage: hu\n---\n# A\n\nTiszta szöveg [[pause 300]] itt.\n"
    _, report = validate_text(text, norm)
    assert report.warnings == []
