# Felolvasási forgatókönyv: `.tts.md` (ttsmd/1)

A Felolvasó a hanganyagot kizárólag ebből a formátumból készíti. Minden előkészítési út
(szabályalapú import, Claude skill) ilyen fájlt állít elő.

## Példa

```text
---
format: ttsmd/1
title: Villamosságtan jegyzet
author: Ismeretlen
language: hu
source: elektro_jegyzet.pdf
voice: f5-alap            # opcionális, hangprofil id
symbols:                   # opcionális, csak dokumentáció és Claude számára
  R: er, ellenállás
  rho: ró, fajlagos ellenállás
---

# Első tétel. Az ellenállás

## A fajlagos ellenállás

Az R ellenállás egyenlő ró szorozva l per A. [[pause 500]]
Ahol l a vezeték hossza, A pedig a keresztmetszete.

{{Kirchhoff|kirhhoff}} első törvénye szerint ...

<!-- megjegyzés, nem olvasódik fel -->
```

## Szabályok

1. UTF-8 kódolás, LF vagy CRLF sorvég.
2. Front matter YAML a fájl elején, `---` sorok között. Kötelező mezők: `format` (értéke `ttsmd/1`),
   `title`, `language`. Opcionális: `author`, `source`, `voice`, `symbols`, `cover`
   (képfájl útvonala a forgatókönyvhöz képest).
3. `# ` fejezet, `## ` és `### ` szakaszcím. Mélyebb szint nem megengedett. Legalább egy `#` fejezet kell.
   Fejezetenként egy MP3 fájl és egy M4B fejezetjelölő készül.
4. Bekezdés: üres sorral elválasztott szövegsorok; a bekezdésen belüli sortörés szóközként értelmeződik.
5. Direktívák: `[[pause N]]` (N ezredmásodperc, 0–10000). Más direktíva nincs.
6. Inline kiejtés: `{{írott|kiejtés}}` – a felolvasó a kiejtést mondja ki.
7. HTML megjegyzés: `<!-- ... -->`, nem olvasódik fel. A `<!-- MATH_SUSPECT -->` speciális megjegyzés:
   a validátor figyelmeztet rá.
8. Listák (`- `, `1. `) bekezdésként olvasódnak, a felsorolásjel nélkül, elemenként 350 ms szünettel.
9. Eredeti szöveg az olvasónézethez: `<!-- eredeti` sor, utána a forrás szövege változatlanul
   (Markdown, képletekkel, táblázattal, ```` ```latex ```` blokkal), majd `-->` külön sorban. Nem olvasódik
   fel; a közvetlenül utána következő blokkhoz tartozik, és az olvasónézet ezt mutatja a felolvasott
   szöveg helyett. Az utána jövő, saját `eredeti` nélküli blokkok ugyanahhoz a részhez tartoznak
   (pl. egy táblázatból több felolvasott mondat lett). A tartalom nem tartalmazhat `-->` jelet.

   ```text
   <!-- eredeti
   **Térerősség.** Ponttöltésre a Coulomb-törvényből:

   ```latex
   E = krac{Q}{r^2}
   ```
   -->
   ## Térerősség

   Ponttöltésre a {{Coulomb|kulomb}}-törvényből: é egyenlő ká szorozva nagy kú per er négyzet. [[pause 500]]
   ```

## Amit a normalizáló elvégez

Számok, sorszámok, tizedes törtek, dátumok, időpontok, toldalékos számok (`5-ös`), mértékegységek
(`12 V`, `10 kΩ`), gyakori rövidítések (`pl.`, `stb.`) és a `& + = / →` jelek kiolvasható alakra
kerülnek. Képleteket, LaTeX-et és matematikai szimbólumokat **nem** ért: ezeket a forgatókönyvben
teljes magyar mondatként kell leírni (pl. „az R ellenállás egyenlő ró szorozva l per A”).

## Validálás

- Hiba (a generálás nem indul): hiányzó vagy érvénytelen front matter, `format` nem `ttsmd/1`,
  nincs `#` fejezet, ismeretlen `[[...]]` direktíva, lezáratlan `{{...}}`, `####` vagy mélyebb cím.
- Figyelmeztetés: normalizálás után megmaradt számjegy, LaTeX parancs, matematikai Unicode karakter,
  `MATH_SUSPECT` megjegyzés, nem kiolvasható karakter.
