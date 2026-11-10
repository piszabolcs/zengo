---
name: felolvaso-elokeszito
description: Magyar nyelvű egyetemi jegyzetből, tételből vagy könyvfejezetből felolvasási forgatókönyvet (.tts.md, ttsmd/1) készít a Felolvasó hangoskönyv-készítőhöz, úgy, hogy minden képlet, szimbólum, szám és mértékegység teljes magyar mondatként hangozzon el. Használd, ha a felhasználó jegyzetet, PDF-et vagy képletes anyagot szeretne felolvastatni, hangoskönyvvé alakítani, „tts.md”-t vagy forgatókönyvet kér, vagy a Felolvasó MCP eszközeit (submit_script) említi.
---

# Felolvasó előkészítő

A feladat: a felhasználó anyagából (jellemzően PDF, amit közvetlenül látsz) egyetlen érvényes
`.tts.md` forgatókönyvet készíteni, amiből a Felolvasó helyi TTS motorja hangoskönyvet generál.
A TTS motor csak kiolvasható magyar szöveget kap: képletet, szimbólumot, számjegyet nem tud felolvasni.

Olvasd el, mielőtt dolgozol:
- `references/ttsmd-format.md` – a formátum pontos szabályai
- `references/math-reading-hu.md` – a magyar képletfelolvasás szabályai és táblázata
- `references/examples.md` – öt kidolgozott példa (forrás → forgatókönyv)

## Munkafolyamat

1. **Áttekintés.** Nézd át a forrást: fejezetek/tételek szerkezete, jelöléslisták, képletek, ábrák.
   Hosszú anyagnál (több tétel, több tíz oldal) tételenként vagy fejezetenként dolgozz, és
   fejezetenként fűzd a fájlhoz, hogy ne fuss ki a kontextusból.
2. **Front matter.** `format: ttsmd/1`, `title`, `author` (ha ismert), `language: hu`, `source`
   (a forrásfájl neve). Ha az anyag jelöléslistát tartalmaz, vedd fel a `symbols` mezőbe.
3. **Szerkezet.** Fejezet vagy tétel = `#`, szakasz = `##` / `###`. A fejezetcím maradjon a forrásé,
   csak a számot írd ki betűvel („Harmadik tétel. A váltakozó áram”).
4. **Szöveg.** A forrás minden mondata megmarad. Összefoglalás, átfogalmazás, kihagyás tilos,
   kivéve: oldalszám, élőfej, lábjegyzet-hivatkozás, tartalomjegyzék, ábra. Ábra helyett egy
   mondatos „Ábra: …” leírás, ha az aláírás informatív.
5. **Képletek.** Minden képlet teljes magyar mondat, számjegy és szimbólum nélkül, a
   `math-reading-hu.md` szerint. Képlet után `[[pause 500]]`.
6. **Jelölésszótár.** Ha a tétel elején jelöléslista áll (pl. „R: ellenállás”), a szimbólum első
   előfordulásánál a teljes alakot olvastasd („az R ellenállás”), utána a betűnevet („er”), kivéve
   ha a mondat érthetősége a teljes alakot kívánja.
7. **Számok és mértékegységek** szóval: „tíz kiloóm”, „huszonöt celsius-fok”, „kétezer-huszonhat”.
8. **Eredeti szöveg.** A forrás minden eleme (cím, bekezdés, teljes táblázat, teljes lista,
   képletblokk) elé, az első belőle készült felolvasott blokk fölé tedd be az eredetit változatlanul:
   `<!-- eredeti` sor, a forrás Markdownja (képletek LaTeX-ben ```` ```latex ```` blokkban), `-->` sor.
   A Felolvasó olvasónézete ezt mutatja hallgatás közben, kiemelve, éppen hol tart a felolvasás.
   Ha a forrás PDF, a képleteket írd vissza LaTeX-ben, a szöveget a forrás szerint.
9. **Önellenőrzés** a végén (lásd lent), majd kimenet.

## Kimeneti szabályok

- Egyetlen `.tts.md` fájl; a fájl elején a front matter.
- Bekezdések között üres sor. Egy bekezdés lehet több sor is (szóközként olvasódik).
- Csak `[[pause N]]` direktíva létezik (N = 0–10000 ms). Nehéz kiejtésű szóhoz `{{írott|kiejtés}}`
  (pl. `{{Kirchhoff|kirhhoff}}`, `{{Ohm|óm}}`).
- Zárójeles, egymásba ágyazott kifejezéseknél tagolj szünetekkel és a „zárójelben” szóval, ha a
  hallgató különben elveszítené a szerkezetet.
- Megjegyzés (`<!-- ... -->`) nem olvasódik fel; használd, ha a forrás egy részét szándékosan
  kihagyod (pl. `<!-- ábra kihagyva: kapcsolási rajz -->`).

## Önellenőrzés (kötelező, a kimenet előtt)

Menj végig a teljes fájlon, és javíts, amíg mind igaz:
1. A front matterben `format: ttsmd/1`, `title`, `language: hu` szerepel.
2. Van legalább egy `#` fejezet; nincs `####` vagy mélyebb cím.
3. A törzsszövegben **nincs számjegy** (0–9), a `[[pause N]]` direktívák számait kivéve.
4. **Nincs LaTeX** (`\frac`, `\alpha`, `$...$`, `^`, `_`).
5. **Nincs matematikai szimbólum**: `= + − · × / < > ≤ ≥ ≈ ≠ √ ∫ ∑ ∂ ∇ ∞ →` és görög betű
   (α, β, ρ, Ω, …) sem maradhat; mindegyik szóval szerepel.
6. Minden képlet után áll `[[pause 500]]`.
7. A forrás egyetlen tartalmi mondata sem maradt ki.
8. Minden forráselemhez van `<!-- eredeti ... -->` megjegyzés, és egyikben sincs `-->` a tartalomban.

## Kimenet átadása

- **claude.ai-on**: add ki a teljes forgatókönyvet egy letölthető `.tts.md` fájlként
  (pl. `elektro-3-tetel.tts.md`). A felhasználó a Felolvasó felületén importálja.
- **Claude Desktopban / Claude Code-ban, ha elérhetők a Felolvasó MCP eszközei**:
  1. `validate_script` a kész szövegre; ha hibát vagy figyelmeztetést ad, javítsd és ellenőrizd újra.
  2. `submit_script` (`script_text`, `project_name`, opcionálisan `voice_id` – a `list_voices` adja).
  3. `get_job_status` a visszakapott `job_id`-val; a végén közöld a kimeneti fájlok útvonalát.
  Ha a szolgáltatás nem fut, kérd meg a felhasználót, hogy indítsa el a `start.bat`-tal.
