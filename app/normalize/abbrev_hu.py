"""Magyar rövidítések feloldása (6.3, 12. lépés)."""

# írott alak -> kiejtés. A ponttal végződő rövidítések után álló mondatzáró pontot a normalizáló kezeli.
ABBREVIATIONS: dict[str, str] = {
    "pl.": "például",
    "stb.": "és a többi",
    "ill.": "illetve",
    "kb.": "körülbelül",
    "ún.": "úgynevezett",
    "ld.": "lásd",
    "vö.": "vesd össze",
    "db": "darab",
    "db.": "darab",
    "max.": "maximum",
    "min.": "minimum",
    "Dr.": "doktor",
    "dr.": "doktor",
    "ford.": "fordította",
    "ti.": "tudniillik",
    "ui.": "ugyanis",
    "uo.": "ugyanott",
    "sz.": "szám",
    "évf.": "évfolyam",
    "o.": "oldal",
    "ny.": "nyugalmazott",
    "id.": "idősebb",
    "ifj.": "ifjabb",
    "kr. e.": "Krisztus előtt",
    "Kr. e.": "Krisztus előtt",
    "Kr. u.": "Krisztus után",
    "i. e.": "időszámításunk előtt",
    "i. sz.": "időszámításunk szerint",
}

# Ezek után álló pont nem mondathatár (a chunker használja a normalizálatlan maradékokra is).
NON_TERMINAL = {a.rstrip(".").lower() for a in ABBREVIATIONS if a.endswith(".")} | {
    "mr", "mrs", "prof", "st", "u", "ü", "kft", "zrt", "bt", "nyrt", "vs", "ca", "cf", "etc", "jan", "febr",
    "márc", "ápr", "jún", "júl", "aug", "szept", "okt", "nov", "dec", "fej", "tsz", "hrsz", "ker",
}
