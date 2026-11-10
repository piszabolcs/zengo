---
format: ttsmd/1
title: Elektrodinamika tételek – Tanuláshoz
language: hu
source: Elektrodinamika tételek kidolgozva (Tanuláshoz lap)
---

<!-- eredeti
# Tételek tanuláshoz
-->
# Bevezetés

<!-- eredeti
Minden tétel így épül fel: egy táblázat a benne szereplő jelekről (mit jelent, mi a mértékegysége), egy rövid, hétköznapi magyarázat arról, miről szól, majd a jegyzet tartalma képletekkel és levezetéssel, számpéldák nélkül. A végén egy sor arról, mit kell a vizsgán mindenképp leírni.
-->
Minden tétel így épül fel: egy táblázat a benne szereplő jelekről (mit jelent, mi a mértékegysége), egy rövid, hétköznapi magyarázat arról, miről szól, majd a jegyzet tartalma képletekkel és levezetéssel, számpéldák nélkül. A végén egy sor arról, mit kell a vizsgán mindenképp leírni.

<!-- eredeti
## 1. rész

### 1. Elektromos alapmennyiségek: térerősség, polarizáció, indukcióvektor, szuszceptibilitás
-->
# Első rész, első tétel. Elektromos alapmennyiségek: térerősség, polarizáció, indukcióvektor, szuszceptibilitás

<!-- eredeti
| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| F | erő | N |
| q, Q | töltés (q a kicsi próbatöltés) | C |
| E | elektromos térerősség | V/m = N/C |
| r | távolság a töltéstől | m |
| k = 1/(4πε₀) | Coulomb-állandó, ≈ 9·10⁹ | Vm/(As) |
| p | egy dipólus momentuma (p = Qℓ) | C·m |
| ΔV | kis térfogat | m³ |
| P | polarizációvektor (mennyire polarizált az anyag) | C/m² |
| κ | elektromos szuszceptibilitás (mennyire polarizálható) | nincs |
| ε₀ | vákuum permittivitása, ≈ 8,85·10⁻¹² | As/(Vm) |
| εᵣ | relatív permittivitás (hányszor nagyobb a vákuuménál) | nincs |
| ε = ε₀εᵣ | abszolút permittivitás | As/(Vm) |
| D | elektromos indukció (eltolás) | C/m² |
| Ψ | indukciófluxus (hány D-vonal megy át egy felületen) | C |
| A, dA | felület, felületelem (vektor: merőleges a felületre) | m² |
| ρ, ρ′ | szabad, illetve polarizációs töltéssűrűség | C/m³ |
-->
## Jelölések

Az F jel az erőt jelenti, mértékegysége a {{newton|nyúton}}.

A kis q és a nagy Q jel a töltést jelenti, a kis kú a kicsi próbatöltés, mértékegysége a {{coulomb|kulomb}}.

Az E jel az elektromos térerősséget jelenti, mértékegysége a volt per méter, ami egyenlő {{newton|nyúton}} per {{coulomb|kulomb}}. [[pause 500]]

Az r jel a töltéstől mért távolságot jelenti, mértékegysége a méter.

A k jel a {{Coulomb|kulomb}}-állandót jelenti: ká egyenlő egy per, zárójelben négy pí szorozva epszilon nulla. [[pause 500]] Értéke közelítőleg kilencszer tíz a kilencediken, mértékegysége volt méter per amper szekundum. [[pause 500]]

A kis p jel egy dipólus momentumát jelenti, ahol pé egyenlő nagy kú szorozva el, mértékegysége {{coulomb|kulomb}} szorozva méter. [[pause 500]]

A delta nagy V jel kis térfogatot jelent, mértékegysége a köbméter.

A nagy P jel a polarizációvektort jelenti (mennyire polarizált az anyag), mértékegysége {{coulomb|kulomb}} per négyzetméter.

A kappa jel az elektromos szuszceptibilitást jelenti (mennyire polarizálható), mértékegysége nincs.

Az epszilon nulla jel a vákuum permittivitását jelenti, értéke közelítőleg nyolc egész nyolcvanöt század szorozva tíz a mínusz tizenkettediken, mértékegysége amper szekundum per volt méter. [[pause 500]]

Az epszilon er jel a relatív permittivitást jelenti (hányszor nagyobb a vákuuménál), mértékegysége nincs.

Az epszilon jel az abszolút permittivitást jelenti: epszilon egyenlő epszilon nulla szorozva epszilon er, mértékegysége amper szekundum per volt méter. [[pause 500]]

A D jel az elektromos indukciót (eltolást) jelenti, mértékegysége {{coulomb|kulomb}} per négyzetméter.

A nagy pszí jel az indukciófluxust jelenti (hány dé-vonal megy át egy felületen), mértékegysége a {{coulomb|kulomb}}.

Az A és a dé A jel a felületet és a felületelemet jelenti (vektor: merőleges a felületre), mértékegysége a négyzetméter.

A ró és a ró vessző jel a szabad, illetve a polarizációs töltéssűrűséget jelenti, mértékegysége {{coulomb|kulomb}} per köbméter.

<!-- eredeti
**Miről szól?** A térerősség megmondja, mekkora és milyen irányú erő hatna egy pontba tett pici pozitív töltésre. Ha szigetelőt teszünk a térbe, a molekulái kicsit „megnyúlnak” vagy befordulnak: az anyag polarizálódik. Ezt méri P, és κ azt, mennyire könnyen történik meg. A D vektort azért találták ki, mert vele a Gauss-törvényben csak az általunk odavitt (szabad) töltések szerepelnek, a polarizációs töltésekkel nem kell külön foglalkozni.
-->
## Miről szól

A térerősség megmondja, mekkora és milyen irányú erő hatna egy pontba tett pici pozitív töltésre. Ha szigetelőt teszünk a térbe, a molekulái kicsit „megnyúlnak” vagy befordulnak: az anyag polarizálódik. Ezt méri a nagy pé polarizációvektor, és a kappa szuszceptibilitás azt, mennyire könnyen történik meg. A dé vektort azért találták ki, mert vele a {{Gauss|gausz}}-törvényben csak az általunk odavitt (szabad) töltések szerepelnek, a polarizációs töltésekkel nem kell külön foglalkozni.

<!-- eredeti
**Térerősség.** A próbatöltésre ható erő arányos a töltéssel (F = qE), a hányadosuk már csak a teret jellemzi. Ponttöltésre a Coulomb-törvényből:

```latex
\vec E = \frac{\vec F}{q} \qquad E = k\frac{Q}{r^2}
```
-->
## Térerősség

A próbatöltésre ható erő arányos a töltéssel, vagyis ef egyenlő kú szorozva é. [[pause 500]]
A hányadosuk már csak a teret jellemzi. Ponttöltésre a {{Coulomb|kulomb}}-törvényből:

A térerősség: é vektor egyenlő ef vektor per kú. [[pause 500]]
Ponttöltésre a térerősség nagysága: é egyenlő ká szorozva nagy kú per er négyzet. [[pause 500]]

<!-- eredeti
**Polarizáció jelensége.** Két fajtája van:

- *Indukált:* a tér széthúzza a molekula pozitív és negatív töltésközéppontját, így az is dipólus lesz, amelyik eddig nem volt az. Minden anyagban megtörténik.
- *Rendeződési (orientációs):* a már eleve dipólus molekulákat a tér beforítja a saját irányába. Minél hidegebb az anyag, annál jobban sikerül (a hőmozgás zavarja), tehát erősen hőmérsékletfüggő.
-->
## Polarizáció jelensége

Két fajtája van:

- Indukált: a tér széthúzza a molekula pozitív és negatív töltésközéppontját, így az is dipólus lesz, amelyik eddig nem volt az. Minden anyagban megtörténik.
- Rendeződési (orientációs): a már eleve dipólus molekulákat a tér befordítja a saját irányába. Minél hidegebb az anyag, annál jobban sikerül (a hőmozgás zavarja), tehát erősen hőmérsékletfüggő.

<!-- eredeti
Polarizálódás után inhomogén térben erő is hat a testre: ezért vonzza a dörzsölt üvegrúd a papírfecnit.
-->
Polarizálódás után inhomogén térben erő is hat a testre: ezért vonzza a dörzsölt üvegrúd a papírfecnit.

<!-- eredeti
**Polarizációvektor és szuszceptibilitás.** Egy kis térfogatban összeadjuk a molekulák dipólmomentumait, és elosztjuk a térfogattal. A legtöbb anyagban ez arányos a térerősséggel (lineáris anyagegyenlet):

```latex
\vec P = \lim_{\Delta V\to 0}\frac{\sum\vec p}{\Delta V} \qquad \vec P = \kappa\,\varepsilon_0\,\vec E
```
-->
## Polarizációvektor és szuszceptibilitás

Egy kis térfogatban összeadjuk a molekulák dipólmomentumait, és elosztjuk a térfogattal. A legtöbb anyagban ez arányos a térerősséggel (lineáris anyagegyenlet):

A polarizációvektor: nagy pé vektor egyenlő limesz delta nagy vé tart nullához, egy tört, a számláló szumma kis pé vektor, a nevező delta nagy vé. [[pause 500]]
A lineáris anyagegyenlet: nagy pé vektor egyenlő kappa szorozva epszilon nulla szorozva é vektor. [[pause 500]]

<!-- eredeti
Vákuumban κ = 0, anyagban általában κ > 0. Nem mindig igaz: nagy térben átütés lehet, anizotróp kristályban P és E nem párhuzamos (κ tenzor).
-->
Vákuumban kappa egyenlő nulla, anyagban általában kappa nagyobb, mint nulla. [[pause 500]]
Nem mindig igaz: nagy térben átütés lehet, anizotróp kristályban nagy pé és é nem párhuzamos (kappa tenzor).

<!-- eredeti
**Indukcióvektor.** Definíció szerint, majd a lineáris közelítést beírva:

```latex
\vec D = \varepsilon_0\vec E + \vec P = \varepsilon_0\vec E + \kappa\varepsilon_0\vec E = \varepsilon_0(1+\kappa)\vec E = \varepsilon_0\varepsilon_r\vec E = \varepsilon\vec E, \qquad \varepsilon_r = 1+\kappa
```
-->
## Indukcióvektor

Definíció szerint, majd a lineáris közelítést beírva:

Dé vektor egyenlő epszilon nulla szorozva é vektor plusz nagy pé vektor. [[pause 500]]
Ez egyenlő epszilon nulla szorozva é vektor plusz kappa szorozva epszilon nulla szorozva é vektor. [[pause 500]]
Ez egyenlő epszilon nulla szorozva, zárójelben egy plusz kappa, szorozva é vektor. [[pause 500]]
Ez egyenlő epszilon nulla szorozva epszilon er szorozva é vektor, ami egyenlő epszilon szorozva é vektor. [[pause 500]]
Ahol epszilon er egyenlő egy plusz kappa. [[pause 500]]

<!-- eredeti
**Fluxus és Gauss-törvény (II. alaptörvény).** A fluxus azt számolja, hány D-vonal megy át egy felületen (α a D és a felület normálisa közti szög): Ψ = ∫D dA, kicsiben ΔΨ = DΔA cos α. Ha egy Q ponttöltés köré r sugarú gömböt teszünk, D = Q/(4πr²) mindenhol merőleges a gömbre, így a fluxus D·4πr² = Q, a sugártól függetlenül: ahol kétszer akkora a sugár, négyszer akkora a felület, és negyed akkora a D. Ez bármilyen zárt felületre igaz, ami a töltést körbezárja (ami nincs bent, annak vonalai be is mennek, ki is jönnek, összesen 0):

```latex
\oint_f\vec D\,d\vec A = Q \qquad \operatorname{div}\vec D = \rho
```
-->
## Fluxus és {{Gauss|gausz}}-törvény, második alaptörvény

A fluxus azt számolja, hány dé-vonal megy át egy felületen (alfa a dé és a felület normálisa közti szög): nagy pszí egyenlő integrál dé vektor dé á, kicsiben delta nagy pszí egyenlő dé szorozva delta á szorozva koszinusz alfa. [[pause 500]]
Ha egy nagy kú ponttöltés köré er sugarú gömböt teszünk, akkor dé egyenlő nagy kú per, zárójelben négy pí szorozva er négyzet, és ez mindenhol merőleges a gömbre. [[pause 500]]
Így a fluxus dé szorozva négy pí szorozva er négyzet, ami egyenlő nagy kú, a sugártól függetlenül: ahol kétszer akkora a sugár, négyszer akkora a felület, és negyed akkora a dé. [[pause 500]]
Ez bármilyen zárt felületre igaz, ami a töltést körbezárja (ami nincs bent, annak vonalai be is mennek, ki is jönnek, összesen nulla):

Integrális alakban: zárt felületi integrál az ef zárt felületre, dé vektor skalárszorzat dé á vektor, egyenlő nagy kú. [[pause 500]]
Differenciális alakban: divergencia dé vektor egyenlő ró. [[pause 500]]

<!-- eredeti
**Ki minek a forrása?**

| Vektor | Forrása | Egyenlet |
| --- | --- | --- |
| D | csak a szabad töltések | div D = ρ |
| P | a polarizációs töltések (ellentétes előjellel) | div(−P) = ρ′ |
| E | mindkettő | div E = (ρ + ρ′)/ε₀ |
-->
## Ki minek a forrása

A dé vektor forrása csak a szabad töltések, egyenlete: divergencia dé egyenlő ró. [[pause 500]]

A nagy pé vektor forrása a polarizációs töltések (ellentétes előjellel), egyenlete: divergencia mínusz nagy pé egyenlő ró vessző. [[pause 500]]

Az é vektor forrása mindkettő, egyenlete: divergencia é egyenlő egy tört, a számláló ró plusz ró vessző, a nevező epszilon nulla. [[pause 500]]

<!-- eredeti
(Az E sort a felső kettő összeadásából kapjuk, mert E = (D − P)/ε₀.)
-->
Az é sort a felső kettő összeadásából kapjuk, mert é egyenlő egy tört, a számláló dé mínusz nagy pé, a nevező epszilon nulla. [[pause 500]]

<!-- eredeti
**Vizsgán:** E = F/q; a kétféle polarizáció; P definíciója; P = κε₀E; D = ε₀E + P → D = ε₀εᵣE, εᵣ = 1 + κ; a források táblázata.
-->
## Amit a vizsgán le kell írni

- é egyenlő ef per kú. [[pause 500]]
- a kétféle polarizáció.
- nagy pé definíciója.
- nagy pé egyenlő kappa szorozva epszilon nulla szorozva é. [[pause 500]]
- dé egyenlő epszilon nulla szorozva é plusz nagy pé, amiből dé egyenlő epszilon nulla szorozva epszilon er szorozva é, és epszilon er egyenlő egy plusz kappa. [[pause 500]]
- a források táblázata.

<!-- eredeti
### 2. A Maxwell-egyenletek teljes rendszere
-->
# Első rész, második tétel. A {{Maxwell|mekszvel}}-egyenletek teljes rendszere

<!-- eredeti
| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| E, D | elektromos térerősség, elektromos indukció | V/m, C/m² |
| H, B | mágneses térerősség, mágneses indukció | A/m, T = Vs/m² |
| I | áramerősség | A |
| j | áramsűrűség | A/m² |
| Q, ρ | töltés, térfogati töltéssűrűség | C, C/m³ |
| g, ds | zárt görbe, ívelem (vektor: a görbe irányába) | m |
| F, dA | görbe által határolt felület, felületelem | m² |
| f | zárt felület | m² |
| ε₀, εᵣ | permittivitás (vákuum, relatív) | As/(Vm), nincs |
| μ₀, μᵣ | permeabilitás (vákuum, relatív) | Vs/(Am), nincs |
| σ | fajlagos vezetőképesség | S/m |
| rot, div | örvényesség, forrásosság egy pontban |  |
-->
## Jelölések

Az E és a D jel az elektromos térerősséget és az elektromos indukciót jelenti, mértékegységük volt per méter, illetve {{coulomb|kulomb}} per négyzetméter.

A H és a B jel a mágneses térerősséget és a mágneses indukciót jelenti, mértékegységük amper per méter, illetve tesla, ami egyenlő volt szekundum per négyzetméter. [[pause 500]]

Az I jel az áramerősséget jelenti, mértékegysége az amper.

A j jel az áramsűrűséget jelenti, mértékegysége amper per négyzetméter.

A Q és a ró jel a töltést és a térfogati töltéssűrűséget jelenti, mértékegységük {{coulomb|kulomb}}, illetve {{coulomb|kulomb}} per köbméter.

A g és a dé s jel a zárt görbét és az ívelemet jelenti (vektor: a görbe irányába), mértékegysége a méter.

A nagy F és a dé A jel a görbe által határolt felületet és a felületelemet jelenti, mértékegysége a négyzetméter.

A kis f jel a zárt felületet jelenti, mértékegysége a négyzetméter.

Az epszilon nulla és az epszilon er jel a permittivitást jelenti (vákuum, relatív), mértékegysége amper szekundum per volt méter, illetve nincs.

A mű nulla és a mű er jel a permeabilitást jelenti (vákuum, relatív), mértékegysége volt szekundum per amper méter, illetve nincs.

A szigma jel a fajlagos vezetőképességet jelenti, mértékegysége {{siemens|szímensz}} per méter.

A rotáció és a divergencia jel az örvényességet és a forrásosságot jelenti egy pontban, ehhez a sorhoz nincs megadva mértékegység.

<!-- eredeti
**Miről szól?** Négy törvény arról, hogy mi hozza létre az elektromos és a mágneses teret. Az elméletben ezeket alaptételnek (axiómának) vesszük, és belőlük vezetünk le mindent. A leghíresebb következményük az elektromágneses hullámok létezése. Mindegyik kétféleképpen írható: integrálisan (egy egész görbére vagy felületre) és differenciálisan (egy pontra).
-->
## Miről szól

Négy törvény arról, hogy mi hozza létre az elektromos és a mágneses teret. Az elméletben ezeket alaptételnek (axiómának) vesszük, és belőlük vezetünk le mindent. A leghíresebb következményük az elektromágneses hullámok létezése. Mindegyik kétféleképpen írható: integrálisan (egy egész görbére vagy felületre) és differenciálisan (egy pontra).

<!-- eredeti
**1. Ampère-Maxwell-féle gerjesztési törvény:** áram és időben változó elektromos tér köré örvényes mágneses tér alakul ki. (A ∂D/∂t tag az eltolási áram.)

```latex
\oint_g\vec H\,d\vec s = \sum_k I_k + \frac{d}{dt}\int_F\vec D\,d\vec A \qquad \operatorname{rot}\vec H = \vec j + \frac{\partial\vec D}{\partial t}
```
-->
## Első, {{Ampère|amper}}-{{Maxwell|mekszvel}}-féle gerjesztési törvény

Áram és időben változó elektromos tér köré örvényes mágneses tér alakul ki. A dé vektor parciális té szerint tag az eltolási áram. [[pause 500]]

Integrális alakban: zárt görbe menti integrál a gé görbére, há vektor skalárszorzat dé es vektor, egyenlő szumma ká szerint í ká, plusz dé per dé té, integrál az ef felületre, dé vektor skalárszorzat dé á vektor. [[pause 500]]
Differenciális alakban: rotáció há vektor egyenlő jé vektor plusz dé vektor parciális té szerint. [[pause 500]]

<!-- eredeti
**2. Faraday-féle indukciótörvény:** időben változó mágneses tér köré örvényes elektromos tér alakul ki.

```latex
\oint_g\vec E\,d\vec s = -\frac{d}{dt}\int_F\vec B\,d\vec A \qquad \operatorname{rot}\vec E = -\frac{\partial\vec B}{\partial t}
```
-->
## Második, {{Faraday|faradéj}}-féle indukciótörvény

Időben változó mágneses tér köré örvényes elektromos tér alakul ki.

Integrális alakban: zárt görbe menti integrál a gé görbére, é vektor skalárszorzat dé es vektor, egyenlő mínusz dé per dé té, integrál az ef felületre, bé vektor skalárszorzat dé á vektor. [[pause 500]]
Differenciális alakban: rotáció é vektor egyenlő mínusz bé vektor parciális té szerint. [[pause 500]]

<!-- eredeti
**3. Elektromos Gauss-törvény:** az elektromos tér forrásai a töltések.

```latex
\oint_f\vec D\,d\vec A = Q \qquad \operatorname{div}\vec D = \rho
```
-->
## Harmadik, elektromos {{Gauss|gausz}}-törvény

Az elektromos tér forrásai a töltések.

Integrális alakban: zárt felületi integrál a kis ef zárt felületre, dé vektor skalárszorzat dé á vektor, egyenlő nagy kú. [[pause 500]]
Differenciális alakban: divergencia dé vektor egyenlő ró. [[pause 500]]

<!-- eredeti
**4. Mágneses Gauss-törvény:** nincs mágneses töltés, a B vonalak mindig zártak.

```latex
\oint_f\vec B\,d\vec A = 0 \qquad \operatorname{div}\vec B = 0
```
-->
## Negyedik, mágneses {{Gauss|gausz}}-törvény

Nincs mágneses töltés, a bé vonalak mindig zártak.

Integrális alakban: zárt felületi integrál a kis ef zárt felületre, bé vektor skalárszorzat dé á vektor, egyenlő nulla. [[pause 500]]
Differenciális alakban: divergencia bé vektor egyenlő nulla. [[pause 500]]

<!-- eredeti
**Anyagegyenletek.** A megoldáshoz kell még, hogy az anyagban hogyan függ össze D és E, B és H, j és E:

```latex
\vec D = \varepsilon_0\varepsilon_r\vec E \qquad \vec B = \mu_0\mu_r\vec H \qquad \vec j = \sigma\vec E
```
-->
## Anyagegyenletek

A megoldáshoz kell még, hogy az anyagban hogyan függ össze dé és é, bé és há, jé és é:

Dé vektor egyenlő epszilon nulla szorozva epszilon er szorozva é vektor. [[pause 500]]
Bé vektor egyenlő mű nulla szorozva mű er szorozva há vektor. [[pause 500]]
Jé vektor egyenlő szigma szorozva é vektor. [[pause 500]]

<!-- eredeti
A Maxwell-egyenletek egzakt természettörvények, az anyagegyenletek csak közelítések, bizonyos anyagokra jók (pl. a ferromágnesességet és az állandó mágneseket nem írják le).
-->
A {{Maxwell|mekszvel}}-egyenletek egzakt természettörvények, az anyagegyenletek csak közelítések, bizonyos anyagokra jók (például a ferromágnesességet és az állandó mágneseket nem írják le).

<!-- eredeti
**Vizsgán:** mind a négy egyenlet mindkét alakban, a nevükkel; mindegyikhez egy mondat jelentés; az anyagegyenletek, és hogy ezek közelítések.
-->
## Amit a vizsgán le kell írni

- mind a négy egyenlet mindkét alakban, a nevükkel.
- mindegyikhez egy mondat jelentés.
- az anyagegyenletek, és hogy ezek közelítések.

<!-- eredeti
### 3. Gauss-Osztrogradszkij és Stokes tétel. Az integrális és differenciális alak ekvivalenciája
-->
# Első rész, harmadik tétel. {{Gauss|gausz}}-{{Osztrogradszkij|osztrogradszkij}} és {{Stokes|sztoksz}} tétel. Az integrális és differenciális alak ekvivalenciája

<!-- eredeti
| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| v | tetszőleges vektormező (pl. E, D, H) | a mezőé |
| V, dV | térfogat, térfogatelem | m³ |
| F | zárt felület (a V határa) vagy görbével határolt felület | m² |
| dA | felületelem-vektor (merőleges a felületre, zárt felületnél kifelé) | m² |
| g, ds | zárt görbe, ívelem-vektor | m |
| div v | forráserősség egy pontban (+: forrás, −: nyelő) | (mező)/m |
| rot v | örvényerősség egy pontban | (mező)/m |
| ∇ | nabla-operátor (∂/∂x, ∂/∂y, ∂/∂z) | 1/m |
-->
## Jelölések

A kis v jel tetszőleges vektormezőt jelent (például é, dé, há), mértékegysége a mezőé.

A nagy V és a dé nagy V jel a térfogatot és a térfogatelemet jelenti, mértékegysége a köbméter.

Az F jel zárt felületet (a nagy vé határát) vagy görbével határolt felületet jelent, mértékegysége a négyzetméter.

A dé A jel a felületelem-vektort jelenti (merőleges a felületre, zárt felületnél kifelé), mértékegysége a négyzetméter.

A g és a dé s jel a zárt görbét és az ívelem-vektort jelenti, mértékegysége a méter.

A divergencia kis vé jel a forráserősséget jelenti egy pontban (plusz: forrás, mínusz: nyelő), mértékegysége a mező mértékegysége per méter.

A rotáció kis vé jel az örvényerősséget jelenti egy pontban, mértékegysége a mező mértékegysége per méter.

A nabla jel a nabla-operátort jelenti, amelynek komponensei: parciális iksz szerint, parciális ipszilon szerint, parciális zé szerint, mértékegysége egy per méter. [[pause 500]]

<!-- eredeti
**Miről szól?** A két tétel híd a „nagyban” és a „kicsiben” leírás között. *Gauss-Osztrogradszkij:* ami egy zárt felületen összesen kifá (fluxus), az pont a bent lévő források összege, mint amikor egy szobából kifolyó víz megegyezik a bent lévő locsolók hozamával. *Stokes:* egy zárt út mentén összegzett „sodrás” (cirkuláció) pont a körbezárt felületen lévő kis örvények összege. Ezekkel lehet a Maxwell-egyenleteket integrálisból differenciális alakra átírni és vissza.
-->
## Miről szól

A két tétel híd a „nagyban” és a „kicsiben” leírás között. {{Gauss|gausz}}-{{Osztrogradszkij|osztrogradszkij}}: ami egy zárt felületen összesen kifolyik (fluxus), az pont a bent lévő források összege, mint amikor egy szobából kifolyó víz megegyezik a bent lévő locsolók hozamával. {{Stokes|sztoksz}}: egy zárt út mentén összegzett „sodrás” (cirkuláció) pont a körbezárt felületen lévő kis örvények összege. Ezekkel lehet a {{Maxwell|mekszvel}}-egyenleteket integrálisból differenciális alakra átírni és vissza.

<!-- eredeti
**A differenciáloperátorok** (Függelék): a gradiens egy skálar leggyorsabb növekedésének irányába mutat; a divergencia a forrásosságot, a rotáció az örvényességet méri.

```latex
\operatorname{div}\vec v = \partial_x v_x + \partial_y v_y + \partial_z v_z \qquad \operatorname{rot}\vec v = \begin{pmatrix}\partial_y v_z - \partial_z v_y\\ \partial_z v_x - \partial_x v_z\\ \partial_x v_y - \partial_y v_x\end{pmatrix}
```
-->
## A differenciáloperátorok

A függelékből: a gradiens egy skalár leggyorsabb növekedésének irányába mutat; a divergencia a forrásosságot, a rotáció az örvényességet méri.

A divergencia: divergencia kis vé vektor egyenlő vé iksz parciális iksz szerint, plusz vé ipszilon parciális ipszilon szerint, plusz vé zé parciális zé szerint. [[pause 500]]
A rotáció kis vé vektor egy háromkomponensű oszlopvektor. [[pause 500]]
Első komponense: vé zé parciális ipszilon szerint, mínusz vé ipszilon parciális zé szerint. [[pause 500]]
Második komponense: vé iksz parciális zé szerint, mínusz vé zé parciális iksz szerint. [[pause 500]]
Harmadik komponense: vé ipszilon parciális iksz szerint, mínusz vé iksz parciális ipszilon szerint. [[pause 500]]

<!-- eredeti
Fontos azonosságok: rot grad φ ≡ 0 (gradiensnek nincs örvénye) és div rot v ≡ 0 (örvénynek nincs forrása).
-->
Fontos azonosságok: rotáció gradiens fí azonosan nulla (gradiensnek nincs örvénye) és divergencia rotáció kis vé azonosan nulla (örvénynek nincs forrása). [[pause 500]]

<!-- eredeti
**Gauss-Osztrogradszkij tétel** (F a V térfogat zárt határa, a normális kifelé mutat):

```latex
\oint_F\vec v\,d\vec A = \int_V\operatorname{div}\vec v\,dV
```
-->
## {{Gauss|gausz}}-{{Osztrogradszkij|osztrogradszkij}} tétel

Az ef a nagy vé térfogat zárt határa, a normális kifelé mutat.

Zárt felületi integrál az ef felületre, kis vé vektor skalárszorzat dé á vektor, egyenlő integrál a nagy vé térfogatra, divergencia kis vé vektor dé nagy vé. [[pause 500]]

<!-- eredeti
**Stokes-tétel** (a g zárt görbe az F felület pereme; a körüljárás és a normális jobbkéz-szabály szerint):

```latex
\oint_g\vec v\,d\vec s = \int_F\operatorname{rot}\vec v\,d\vec A
```
-->
## {{Stokes|sztoksz}}-tétel

A gé zárt görbe az ef felület pereme; a körüljárás és a normális jobbkéz-szabály szerint.

Zárt görbe menti integrál a gé görbére, kis vé vektor skalárszorzat dé es vektor, egyenlő integrál az ef felületre, rotáció kis vé vektor skalárszorzat dé á vektor. [[pause 500]]

<!-- eredeti
**Ekvivalencia, az 1. Maxwell-egyenleten bemutatva:**
-->
## Ekvivalencia, az első {{Maxwell|mekszvel}}-egyenleten bemutatva

<!-- eredeti
1. Integrális alak, az áramot áramsűrűséggel írva (I = ∫j dA):
-->
Első lépés: integrális alak, az áramot áramsűrűséggel írva, ahol í egyenlő integrál jé dé á. [[pause 500]]

<!-- eredeti
```latex
\oint_g\vec H\,d\vec s = \int_F\vec j\,d\vec A + \frac{d}{dt}\int_F\vec D\,d\vec A
```
-->
Zárt görbe menti integrál a gé görbére, há vektor skalárszorzat dé es vektor, egyenlő integrál az ef felületre, jé vektor skalárszorzat dé á vektor, plusz dé per dé té, integrál az ef felületre, dé vektor skalárszorzat dé á vektor. [[pause 500]]

<!-- eredeti
2. A bal oldalra Stokes-tétel: ∮H ds = ∫rot H dA.
3. Ha a felület nem mozog, a d/dt bevihető az integrál alá, ott ∂/∂t lesz:
-->
Második lépés: a bal oldalra {{Stokes|sztoksz}}-tétel: zárt görbe menti integrál, há dé es, egyenlő integrál, rotáció há dé á. [[pause 500]]

Harmadik lépés: ha a felület nem mozog, a dé per dé té bevihető az integrál alá, ott parciális per parciális té lesz: [[pause 500]]

<!-- eredeti
```latex
\int_F\operatorname{rot}\vec H\,d\vec A = \int_F\left(\vec j + \frac{\partial\vec D}{\partial t}\right)d\vec A
```
-->
Integrál az ef felületre, rotáció há vektor skalárszorzat dé á vektor, egyenlő integrál az ef felületre, zárójelben jé vektor plusz dé vektor parciális té szerint, skalárszorzat dé á vektor. [[pause 500]]

<!-- eredeti
4. Ez **bármilyen** felületre igaz, ezért a két oldalon az integrandusok is egyenlők: rot H = j + ∂D/∂t.
-->
Negyedik lépés: ez bármilyen felületre igaz, ezért a két oldalon az integrandusok is egyenlők: rotáció há egyenlő jé plusz dé parciális té szerint. [[pause 500]]

<!-- eredeti
A 2. egyenletnél ugyanígy. A Gauss-törvényeknél a Stokes helyett a Gauss-Osztrogradszkij tétel kell:

```latex
\oint_f\vec D\,d\vec A = \int_V\operatorname{div}\vec D\,dV = Q = \int_V\rho\,dV \;\Rightarrow\; \operatorname{div}\vec D = \rho
```
-->
A második egyenletnél ugyanígy. A {{Gauss|gausz}}-törvényeknél a {{Stokes|sztoksz}} helyett a {{Gauss|gausz}}-{{Osztrogradszkij|osztrogradszkij}} tétel kell:

Zárt felületi integrál a kis ef felületre, dé vektor skalárszorzat dé á vektor, egyenlő integrál a nagy vé térfogatra, divergencia dé vektor dé nagy vé. [[pause 500]]
Ez egyenlő nagy kú, ami egyenlő integrál a nagy vé térfogatra, ró dé nagy vé. [[pause 500]]
Ebből következik, hogy divergencia dé vektor egyenlő ró. [[pause 500]]

<!-- eredeti
Visszafelé ugyanezek a lépések fordítva.
-->
Visszafelé ugyanezek a lépések fordítva.

<!-- eredeti
**Vizsgán:** a két tétel képlettel és hogy mi a görbe, felület, térfogat; div és rot jelentése; az 1. ME átalakítása a négy lépéssel; Gauss-törvényeknél a divergencia-tétel.
-->
## Amit a vizsgán le kell írni

- a két tétel képlettel és hogy mi a görbe, felület, térfogat.
- divergencia és rotáció jelentése.
- az első {{Maxwell|mekszvel}}-egyenlet átalakítása a négy lépéssel.
- {{Gauss|gausz}}-törvényeknél a divergencia-tétel.

<!-- eredeti
### 4. Skálarpotenciál. Kirchhoff huroktörvénye
-->
# Első rész, negyedik tétel. Skalárpotenciál. {{Kirchhoff|kirhhoff}} huroktörvénye

<!-- eredeti
| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| E | térerősség | V/m |
| W\_AB | a mező munkája, miközben q-t A-ból B-be viszi | J |
| q, Q | próbatöltés, a teret keltő töltés | C |
| U\_AB | feszültség A és B között | V |
| U(P) | a P pont potenciálja | V |
| Eₚ | potenciális (helyzeti) energia | J |
| dr, ds | elmozdulás-, ívelem-vektor | m |
| d | távolság homogén térben | m |
| r | távolság a ponttöltéstől | m |
| k | Coulomb-állandó, 9·10⁹ | Vm/(As) |
-->
## Jelölések

Az E jel a térerősséget jelenti, mértékegysége a volt per méter.

A dupla vé á bé jel a mező munkáját jelenti, miközben a kú töltést az á pontból a bé pontba viszi, mértékegysége a {{joule|dzsúl}}.

A kis q és a nagy Q jel a próbatöltést, illetve a teret keltő töltést jelenti, mértékegysége a {{coulomb|kulomb}}.

Az ú á bé jel az á és bé közötti feszültséget jelenti, mértékegysége a volt.

Az ú zárójelben pé jel a pé pont potenciálját jelenti, mértékegysége a volt.

Az é pé jel a potenciális (helyzeti) energiát jelenti, mértékegysége a {{joule|dzsúl}}.

A dé r és a dé s jel az elmozdulás-, illetve ívelem-vektort jelenti, mértékegysége a méter.

A d jel a távolságot jelenti homogén térben, mértékegysége a méter.

Az r jel a ponttöltéstől mért távolságot jelenti, mértékegysége a méter.

A k jel a {{Coulomb|kulomb}}-állandót jelenti, értéke kilencszer tíz a kilencediken, mértékegysége volt méter per amper szekundum. [[pause 500]]

<!-- eredeti
**Miről szól?** Ha semmi nem változik időben (elektrosztatika), az elektromos tér olyan, mint a gravitáció: két pont között mindegy, merre viszünk egy töltést, a munka ugyanannyi. Ezért minden ponthoz rendelhetünk egy számot, a potenciált (mint a tengerszint feletti magasság), és a térerősség a „lejtő lefelé” irány. Ha körbemész és visszajössz, ugyanott vagy: ez a huroktörvény.
-->
## Miről szól

Ha semmi nem változik időben (elektrosztatika), az elektromos tér olyan, mint a gravitáció: két pont között mindegy, merre viszünk egy töltést, a munka ugyanannyi. Ezért minden ponthoz rendelhetünk egy számot, a potenciált (mint a tengerszint feletti magasság), és a térerősség a „lejtő lefelé” irány. Ha körbemész és visszajössz, ugyanott vagy: ez a huroktörvény.

<!-- eredeti
**I. alaptörvény.** A 2. Maxwell-egyenletben sztatikában ∂B/∂t = 0, ezért a mező konzervatív (örvénymentes):

```latex
\oint_g\vec E\,d\vec s = 0 \quad\Longleftrightarrow\quad \operatorname{rot}\vec E = 0
```
-->
## Első alaptörvény

A második {{Maxwell|mekszvel}}-egyenletben sztatikában bé vektor parciális té szerint egyenlő nulla, ezért a mező konzervatív (örvénymentes): [[pause 500]]

Zárt görbe menti integrál a gé görbére, é vektor skalárszorzat dé es vektor, egyenlő nulla, ami egyenértékű azzal, hogy rotáció é vektor egyenlő nulla. [[pause 500]]

<!-- eredeti
(Az egyenáram mágneses tere is állandó, tehát rá is igaz.) A potenciálos mezők tétele szerint ez három egyenértékű állítás: rot v = 0; bármely zárt görbére ∮v ds = 0 (az integrál független az úttól); létezik U, hogy v = ±grad U.
-->
(Az egyenáram mágneses tere is állandó, tehát rá is igaz.) A potenciálos mezők tétele szerint ez három egyenértékű állítás: rotáció vé egyenlő nulla; bármely zárt görbére a zárt görbe menti integrál, vé dé es, egyenlő nulla (az integrál független az úttól); létezik ú, hogy vé egyenlő plusz-mínusz gradiens ú. [[pause 500]]

<!-- eredeti
**Munka, feszültség, potenciál.** A feszültség az egységnyi töltésen végzett munka; homogén térben egyszerűen U = Ed.

```latex
W_{AB} = \int_A^B q\vec E\,d\vec r \qquad U_{AB} = \frac{W_{AB}}{q} = \int_A^B\vec E\,d\vec r = U(A) - U(B)
```
-->
## Munka, feszültség, potenciál

A feszültség az egységnyi töltésen végzett munka; homogén térben egyszerűen ú egyenlő é szorozva dé. [[pause 500]]

A munka: dupla vé á bé egyenlő integrál á-tól bé-ig, kú szorozva é vektor skalárszorzat dé er vektor. [[pause 500]]
A feszültség: ú á bé egyenlő dupla vé á bé per kú, ami egyenlő integrál á-tól bé-ig, é vektor skalárszorzat dé er vektor, és ez egyenlő ú á-ban mínusz ú bé-ben. [[pause 500]]

<!-- eredeti
A potenciál az egységnyi töltésre jutó helyzeti energia (U = Eₚ/q), csak egy állandó erejéig meghatározott. Szokásos választás, hogy a végtelenben 0, ekkor a pont potenciálja az a munka, amit a mező végez, amíg egységnyi pozitív töltést onnan a végtelenbe visz:

```latex
U(P) = \int_P^\infty\vec E\,d\vec r \qquad \vec E = -\operatorname{grad}U
```
-->
A potenciál az egységnyi töltésre jutó helyzeti energia: ú egyenlő é pé per kú. [[pause 500]]
A potenciál csak egy állandó erejéig meghatározott. Szokásos választás, hogy a végtelenben nulla, ekkor a pont potenciálja az a munka, amit a mező végez, amíg egységnyi pozitív töltést onnan a végtelenbe visz:

Ú pé-ben egyenlő integrál pé-től végtelenig, é vektor skalárszorzat dé er vektor. [[pause 500]]
A térerősség: é vektor egyenlő mínusz gradiens ú. [[pause 500]]

<!-- eredeti
Ponttöltésre:
-->
Ponttöltésre:

<!-- eredeti
```latex
U(r) = \int_r^\infty\frac{kQ}{r^2}\,dr = kQ\left[-\frac1r\right]_r^\infty = \frac{kQ}{r}
```
-->
Ú er-ben egyenlő integrál er-től végtelenig, ká szorozva nagy kú per er négyzet, dé er. [[pause 500]]
Ez egyenlő ká szorozva nagy kú, szorozva a mínusz egy per er kifejezés er-től végtelenig vett helyettesítési értékével. [[pause 500]]
Az eredmény: ú er-ben egyenlő ká szorozva nagy kú per er. [[pause 500]]

<!-- eredeti
Pozitív töltésre az alacsonyabb potenciál felé hat erő. Az azonos potenciálú pontok ekvipotenciális felületet alkotnak (ponttöltésnél gömbök); ezen mozogva nincs munka, és E merőleges rájuk.
-->
Pozitív töltésre az alacsonyabb potenciál felé hat erő. Az azonos potenciálú pontok ekvipotenciális felületet alkotnak (ponttöltésnél gömbök); ezen mozogva nincs munka, és é merőleges rájuk.

<!-- eredeti
**Kirchhoff huroktörvénye.** A konzervativitásból bármely zárt hurokra:

```latex
\sum U = 0
```
-->
## {{Kirchhoff|kirhhoff}} huroktörvénye

A konzervativitásból bármely zárt hurokra: szumma ú egyenlő nulla. [[pause 500]]

<!-- eredeti
Csak akkor igaz, ha rot E = 0. Ha B időben változik, ez a feszültség-fogalom nem működik (ezt a 2. részben az általános huroktörvény kezeli).
-->
Csak akkor igaz, ha rotáció é egyenlő nulla. [[pause 500]]
Ha bé időben változik, ez a feszültség-fogalom nem működik (ezt a második részben az általános huroktörvény kezeli).

<!-- eredeti
**Vizsgán:** I. alaptörvény és honnan jön; munka, feszültség, potenciál definíciója; U(∞) = 0; ponttöltés potenciálja levezetve; E = −grad U; ΣU = 0 és mikor nem igaz.
-->
## Amit a vizsgán le kell írni

- első alaptörvény és honnan jön.
- munka, feszültség, potenciál definíciója.
- ú a végtelenben egyenlő nulla. [[pause 500]]
- ponttöltés potenciálja levezetve.
- é egyenlő mínusz gradiens ú. [[pause 500]]
- szumma ú egyenlő nulla és mikor nem igaz. [[pause 500]]


<!-- eredeti
### 5. Vezetők az elektrosztatikus mezőben. Csúcshatás
-->
# Első rész, ötödik tétel. Vezetők az elektrosztatikus mezőben. Csúcshatás

<!-- eredeti
| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| E, D | térerősség, indukció | V/m, C/m² |
| ρ | térfogati töltéssűrűség | C/m³ |
| η | felületi töltéssűrűség (töltés/felület) | C/m² |
| Dₙ | D felületre merőleges (normális) komponense | C/m² |
| Eₜ | E felülettel párhuzamos (tangenciális) komponense | V/m |
| r, R | a kisebb és a nagyobb gömb sugara | m |
| Q₁, Q₂ | a két gömb töltése | C |
| A₁, A₂ | a két gömb felülete (4πr²) | m² |
| η₁, η₂ | a két gömb felületi töltéssűrűsége | C/m² |
-->
## Jelölések

Az E jel a térerősséget, a D jel az indukciót jelenti; mértékegységük volt per méter, illetve {{coulomb|kulomb}} per négyzetméter.

A ró jel a térfogati töltéssűrűséget jelenti, mértékegysége a {{coulomb|kulomb}} per köbméter.

Az éta jel a felületi töltéssűrűséget jelenti (töltés per felület), mértékegysége a {{coulomb|kulomb}} per négyzetméter.

A D en jel a D felületre merőleges (normális) komponensét jelenti, mértékegysége a {{coulomb|kulomb}} per négyzetméter.

Az E té jel az E felülettel párhuzamos (tangenciális) komponensét jelenti, mértékegysége a volt per méter.

A kis r és a nagy R jel a kisebb és a nagyobb gömb sugarát jelenti, mértékegysége a méter.

A Q egy és a Q kettő jel a két gömb töltését jelenti, mértékegysége a {{coulomb|kulomb}}.

Az A egy és az A kettő jel a két gömb felületét jelenti (négy pí er négyzet), mértékegysége a négyzetméter.

Az éta egy és az éta kettő jel a két gömb felületi töltéssűrűségét jelenti, mértékegysége a {{coulomb|kulomb}} per négyzetméter.

<!-- eredeti
**Miről szól?** A fémben szabadon mozgó elektronok vannak. Ha bent tér lenne, mozognának, áram folyna. Addig rendeződnek át, amíg a saját terük kioltja a teret, ezért nyugalomban a fém belsejében nincs tér. A töltés a felületre megy, de nem egyenletesen: a hegyes részeken sűrűbb, ott erősebb a tér (csúcshatás).
-->
## Miről szól

A fémben szabadon mozgó elektronok vannak. Ha bent tér lenne, mozognának, áram folyna. Addig rendeződnek át, amíg a saját terük kioltja a teret, ezért nyugalomban a fém belsejében nincs tér. A töltés a felületre megy, de nem egyenletesen: a hegyes részeken sűrűbb, ott erősebb a tér (csúcshatás).

<!-- eredeti
**Vezető sztatikus állapotban.**
-->
## Vezető sztatikus állapotban

<!-- eredeti
- Bent E = 0, különben a szabad töltések mozognának.
- Ezért bármely két pont közt a feszültség 0: a vezető **ekvipotenciális**. Üreges vezetőre is igaz, ha az üregben nincs töltés: zárt fémburokba (Faraday-kalitka) nem hatol be a tér. Erre épül az elektrosztatikai árnyékolás.
- Eₜ a határon folytonos, bent 0, tehát kívül sincs tangenciális tér: a tér a vezető körül **merőleges a felületre**.
- Bent E = 0 → D = 0 → (div D = ρ miatt) ρ = 0: a vezetőre vitt töltés a **külső felületre** húzódik.
- A határfeltételből (Dₙ₂ − Dₙ₁ = η, bent Dₙ₁ = 0) a felület mellett a szigetelőben Dₙ = η.
-->
- Bent az E térerősség egyenlő nulla, különben a szabad töltések mozognának. [[pause 500]]
- Ezért bármely két pont közt a feszültség nulla: a vezető ekvipotenciális. Üreges vezetőre is igaz, ha az üregben nincs töltés: zárt fémburokba ({{Faraday|faradéj}}-kalitka) nem hatol be a tér. Erre épül az elektrosztatikai árnyékolás.
- E té a határon folytonos, bent nulla, tehát kívül sincs tangenciális tér: a tér a vezető körül merőleges a felületre.
- Bent E egyenlő nulla, ebből következik, hogy D egyenlő nulla, és ebből, a divergencia D egyenlő ró összefüggés miatt, ró egyenlő nulla: a vezetőre vitt töltés a külső felületre húzódik. [[pause 500]]
- A határfeltételből, vagyis abból, hogy D en kettő mínusz D en egy egyenlő éta, és bent D en egy egyenlő nulla, a felület mellett a szigetelőben D en egyenlő éta. [[pause 500]]

<!-- eredeti
**Csúcshatás.** Két különböző méretű fémgömböt vezetékkel összekötünk, így egy vezetőként azonos potenciálra kerülnek. Gömb potenciálja kQ/(sugár), a töltés pedig η · felület:
-->
## Csúcshatás

Két különböző méretű fémgömböt vezetékkel összekötünk, így egy vezetőként azonos potenciálra kerülnek. Gömb potenciálja ká szorozva Q per sugár, a töltés pedig éta szorozva felület. [[pause 500]]

<!-- eredeti
```latex
k\frac{Q_1}{r} = k\frac{Q_2}{R} \;\Rightarrow\; \frac{\eta_1\,4\pi r^2}{r} = \frac{\eta_2\,4\pi R^2}{R} \;\Rightarrow\; \frac{\eta_1}{\eta_2} = \frac{R}{r}
```
-->
Ká szorozva Q egy per kis r egyenlő ká szorozva Q kettő per nagy R. [[pause 500]]
Ebből következik, hogy éta egy szorozva négy pí kis r négyzet, osztva kis r-rel, egyenlő éta kettő szorozva négy pí nagy R négyzet, osztva nagy R-rel. [[pause 500]]
Ebből pedig éta egy per éta kettő egyenlő nagy R per kis r. [[pause 500]]

<!-- eredeti
A kisebb gömbön sűrűbb a töltés, fordított arányban a sugárral. Általánosan: a csúcsokon (kis görbületi sugár) nagyobb a töltéssűrűség és így a tér. Pontos képlet a görbületre nincs. Ezért hegyes a villámhárító, és ezért lekerekítettek a nagyfeszültségű elektródák.
-->
A kisebb gömbön sűrűbb a töltés, fordított arányban a sugárral. Általánosan: a csúcsokon (kis görbületi sugár) nagyobb a töltéssűrűség és így a tér. Pontos képlet a görbületre nincs. Ezért hegyes a villámhárító, és ezért lekerekítettek a nagyfeszültségű elektródák.

<!-- eredeti
**Vizsgán:** miért E = 0 bent; ekvipotenciális, Faraday-kalitka; tér merőleges a felületre; ρ = 0, töltés a felületen, Dₙ = η; csúcshatás két gömbbel, η₁/η₂ = R/r.
-->
## Amit a vizsgán le kell írni

Miért E egyenlő nulla bent; ekvipotenciális, {{Faraday|faradéj}}-kalitka; tér merőleges a felületre; ró egyenlő nulla, töltés a felületen, D en egyenlő éta; csúcshatás két gömbbel, éta egy per éta kettő egyenlő nagy R per kis r. [[pause 500]]

<!-- eredeti
### 6-8. Gömb, henger és sík tere és potenciálja (a testen kívül)
-->
# Első rész, hatodik–nyolcadik tétel. Gömb, henger és sík tere és potenciálja (a testen kívül)

<!-- eredeti
| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| Q | a test teljes töltése | C |
| λ | vonalmenti töltéssűrűség: 1 m hosszú szakaszra jutó töltés (λ = Q/l) | C/m |
| η | felületi töltéssűrűség: 1 m²-re jutó töltés (η = Q/A) | C/m² |
| r | távolság a középponttól (gömb) vagy a tengelytől (henger) | m |
| z | távolság a síktól | m |
| h | a képzeletbeli henger magassága | m |
| A | a képzeletbeli henger alaplapjának területe | m² |
| R₀ | a távolság, ahol a henger potenciálját nullának választjuk | m |
| E, D | térerősség, indukció | V/m, C/m² |
| U | potenciál | V |
| ε = ε₀εᵣ, k = 1/(4πε) | permittivitás, Coulomb-állandó | As/(Vm), Vm/(As) |
-->
## Jelölések

A Q jel a test teljes töltését jelenti, mértékegysége a {{coulomb|kulomb}}.

A lambda jel a vonalmenti töltéssűrűséget jelenti: egy méter hosszú szakaszra jutó töltés, vagyis lambda egyenlő Q per l; mértékegysége a {{coulomb|kulomb}} per méter. [[pause 500]]

Az éta jel a felületi töltéssűrűséget jelenti: egy négyzetméterre jutó töltés, vagyis éta egyenlő Q per A; mértékegysége a {{coulomb|kulomb}} per négyzetméter. [[pause 500]]

Az r jel a távolságot jelenti a középponttól (gömb) vagy a tengelytől (henger), mértékegysége a méter.

A z jel a távolságot jelenti a síktól, mértékegysége a méter.

A h jel a képzeletbeli henger magasságát jelenti, mértékegysége a méter.

Az A jel a képzeletbeli henger alaplapjának területét jelenti, mértékegysége a négyzetméter.

Az R nulla jel azt a távolságot jelenti, ahol a henger potenciálját nullának választjuk, mértékegysége a méter.

Az E jel a térerősséget, a D jel az indukciót jelenti; mértékegységük volt per méter, illetve {{coulomb|kulomb}} per négyzetméter.

Az U jel a potenciált jelenti, mértékegysége a volt.

Az epszilon jel a permittivitást jelenti, epszilon egyenlő epszilon nulla szorozva epszilon er, mértékegysége az amper szekundum per volt méter. [[pause 500]]
A ká jel a {{Coulomb|kulomb}}-állandót jelenti, ká egyenlő egy per, zárójelben négy pí epszilon, mértékegysége a volt méter per amper szekundum. [[pause 500]]

<!-- eredeti
**Miről szól mindhárom?** Ugyanaz a trükk háromszor. A Gauss-törvény (∮D dA = Q) bármilyen zárt felületre igaz, de általában nehéz kiintegrálni. Ha viszont a szimmetriát kihasználva olyan képzeletbeli felületet (Gauss-felületet) választunk, amelyen D **mindenhol ugyanakkora** és **merőleges a felületre**, akkor az integrál egyszerű szorzás lesz: D · (felület) = bezárt töltés. Ebből kifejezzük D-t, elosztjuk ε-nal és megvan E. A potenciálhoz E-t kell integrálni.
-->
## Miről szól mindhárom

Ugyanaz a trükk háromszor. A {{Gauss|gausz}}-törvény, vagyis hogy D dé A zárt felületi integrálja egyenlő Q, bármilyen zárt felületre igaz, de általában nehéz kiintegrálni. [[pause 500]]
Ha viszont a szimmetriát kihasználva olyan képzeletbeli felületet ({{Gauss|gausz}}-felületet) választunk, amelyen D mindenhol ugyanakkora és merőleges a felületre, akkor az integrál egyszerű szorzás lesz: D szorozva a felülettel egyenlő a bezárt töltés. [[pause 500]]
Ebből kifejezzük D-t, elosztjuk epszilonnal és megvan E. A potenciálhoz E-t kell integrálni.

<!-- eredeti
**6. Gömbszimmetrikus töltéseloszlás** (ponttöltés, töltött gömb vagy gömbhéj)
-->
## Hatodik: gömbszimmetrikus töltéseloszlás (ponttöltés, töltött gömb vagy gömbhéj)

<!-- eredeti
- *Szimmetria:* D sugárirányú, nagysága csak r-től függ.
- *Gauss-felület:* a testtel koncentrikus, r sugarú gömb. Ezen D mindenhol ugyanakkora és merőleges rá. Felülete 4πr².
-->
- Szimmetria: D sugárirányú, nagysága csak er-től függ.
- {{Gauss|gausz}}-felület: a testtel koncentrikus, er sugarú gömb. Ezen D mindenhol ugyanakkora és merőleges rá. Felülete négy pí er négyzet. [[pause 500]]

<!-- eredeti
```latex
\oint\vec D\,d\vec A = D\cdot 4\pi r^2 = Q \;\Rightarrow\; E = \frac{D}{\varepsilon} = \frac{1}{4\pi\varepsilon}\frac{Q}{r^2}
```
-->
D vektor skalárszorzat dé A vektor zárt felületi integrálja egyenlő D szorozva négy pí er négyzet, és ez egyenlő Q. [[pause 500]]
Ebből E egyenlő D per epszilon, ami egyenlő egy per, zárójelben négy pí epszilon, szorozva Q per er négyzet. [[pause 500]]

<!-- eredeti
Ez a Coulomb-törvény, a 3. Maxwell-egyenletből levezetve. Nem használtuk ki, hogy a töltés pontszerű, csak a gömbszimmetriát: **kívülről bármilyen gömbszimmetrikus test úgy látszik, mintha minden töltése a középpontban lenne.** A tér 1/r² szerint csökken (kétszer messzebb negyed akkora), mert a vonalak egyre nagyobb gömbfelületen oszlanak el. Potenciál (nulla a végtelenben):
-->
Ez a {{Coulomb|kulomb}}-törvény, a harmadik {{Maxwell|mekszvel}}-egyenletből levezetve. Nem használtuk ki, hogy a töltés pontszerű, csak a gömbszimmetriát: kívülről bármilyen gömbszimmetrikus test úgy látszik, mintha minden töltése a középpontban lenne. A tér egy per er négyzet szerint csökken (kétszer messzebb negyed akkora), mert a vonalak egyre nagyobb gömbfelületen oszlanak el. [[pause 500]]
Potenciál (nulla a végtelenben):

<!-- eredeti
```latex
U(r) = \int_r^\infty E\,dr = \frac{Q}{4\pi\varepsilon}\int_r^\infty\frac{dr}{r^2} = \frac{1}{4\pi\varepsilon}\frac{Q}{r}
```
-->
U er-ben egyenlő integrál er-től végtelenig E dé er, ez egyenlő Q per, zárójelben négy pí epszilon, szorozva integrál er-től végtelenig dé er per er négyzet. [[pause 500]]
Ez pedig egyenlő egy per, zárójelben négy pí epszilon, szorozva Q per er. [[pause 500]]

<!-- eredeti
Ebből: egy R sugarú, Q töltésű fémgömb potenciálja U = kQ/R.
-->
Ebből: egy nagy R sugarú, Q töltésű fémgömb potenciálja U egyenlő ká Q per nagy R. [[pause 500]]

<!-- eredeti
**7. Hengerszimmetrikus töltéseloszlás** (hosszú egyenes töltött szál vagy henger)
-->
## Hetedik: hengerszimmetrikus töltéseloszlás (hosszú egyenes töltött szál vagy henger)

<!-- eredeti
- *Szimmetria:* a szál a z tengely, a térnek nincs z irányú része, sugárirányban mutat kifelé.
- *Gauss-felület:* a szállal koaxiális, r sugarú, h magas henger. Az alap- és fedőlapon a tér a lappal párhuzamos, ott nincs fluxus. Csak a palást számít, annak területe 2πrh. A bezárt töltés a h hosszú szálszakaszé: λh.
-->
- Szimmetria: a szál a zé tengely, a térnek nincs zé irányú része, sugárirányban mutat kifelé.
- {{Gauss|gausz}}-felület: a szállal koaxiális, er sugarú, há magas henger. Az alap- és fedőlapon a tér a lappal párhuzamos, ott nincs fluxus. Csak a palást számít, annak területe kettő pí er há. A bezárt töltés a há hosszú szálszakaszé: lambda há. [[pause 500]]

<!-- eredeti
```latex
D\cdot 2\pi r h = \lambda h \;\Rightarrow\; E = \frac{\lambda}{2\pi\varepsilon r} = \frac{2k\lambda}{r}
```
-->
D szorozva kettő pí er há egyenlő lambda há. [[pause 500]]
Ebből E egyenlő lambda per, zárójelben kettő pí epszilon er, ami egyenlő kettő ká lambda per er. [[pause 500]]

<!-- eredeti
A tér 1/r szerint csökken (kétszer messzebb fele akkora), mert a vonalak csak „oldalra”, egyre nagyobb palástra oszlanak el. **Potenciál:** itt nem lehet a végtelenben a nulla, mert az 1/r integrálja (ln) végtelen lenne; vékony szálnál magán a szálon sem, mert ott a tér végtelen. Ezért egy tetszőleges R₀ távolságban választjuk a nullát:
-->
A tér egy per er szerint csökken (kétszer messzebb fele akkora), mert a vonalak csak oldalra, egyre nagyobb palástra oszlanak el. [[pause 500]]
Potenciál: itt nem lehet a végtelenben a nulla, mert az egy per er integrálja (természetes alapú logaritmus) végtelen lenne; vékony szálnál magán a szálon sem, mert ott a tér végtelen. Ezért egy tetszőleges er nulla távolságban választjuk a nullát:

<!-- eredeti
```latex
U(r) = \int_r^{R_0}\frac{2k\lambda}{r}\,dr = 2k\lambda\ln\frac{R_0}{r}
```
-->
U er-ben egyenlő integrál er-től er nulláig kettő ká lambda per er dé er, ami egyenlő kettő ká lambda szorozva természetes alapú logaritmus er nulla per er. [[pause 500]]

<!-- eredeti
**8. Végtelen töltött sík**
-->
## Nyolcadik: végtelen töltött sík

<!-- eredeti
- *Szimmetria:* a tér merőleges a síkra, mindkét oldalon kifelé mutat.
- *Gauss-felület:* a síkot átszúró kis henger, A területű alap- és fedőlappal a sík két oldalán, egyforma távol. A paláston nincs fluxus (a tér párhuzamos vele), a **két** lapon egyaránt kilép, ezért van 2-es szorzó. A bezárt töltés ηA.
-->
- Szimmetria: a tér merőleges a síkra, mindkét oldalon kifelé mutat.
- {{Gauss|gausz}}-felület: a síkot átszúró kis henger, á területű alap- és fedőlappal a sík két oldalán, egyforma távol. A paláston nincs fluxus (a tér párhuzamos vele), a két lapon egyaránt kilép, ezért van kettes szorzó. A bezárt töltés éta á. [[pause 500]]

<!-- eredeti
```latex
2\varepsilon EA = \eta A \;\Rightarrow\; E = \frac{\eta}{2\varepsilon}
```
-->
Kettő epszilon E á egyenlő éta á. [[pause 500]]
Ebből E egyenlő éta per, zárójelben kettő epszilon. [[pause 500]]

<!-- eredeti
A tér **nem függ a távolságtól**, mert a vonalak párhuzamosak, nem tudnak szétszóródni. Ez addig igaz, amíg sokkal közelebb vagyunk a laphoz, mint annak mérete. **Potenciál:** a nullszint a síkon; a pozitív lap taszítja a pozitív töltést, tehát tőle távolodva mindkét irányban lineárisan csökken:
-->
A tér nem függ a távolságtól, mert a vonalak párhuzamosak, nem tudnak szétszóródni. Ez addig igaz, amíg sokkal közelebb vagyunk a laphoz, mint annak mérete. Potenciál: a nullszint a síkon; a pozitív lap taszítja a pozitív töltést, tehát tőle távolodva mindkét irányban lineárisan csökken:

<!-- eredeti
```latex
U(z) = -\frac{\eta}{2\varepsilon}\,\lvert z\rvert
```
-->
U zé-ben egyenlő mínusz éta per, zárójelben kettő epszilon, szorozva zé abszolút értéke. [[pause 500]]

<!-- eredeti
**Összehasonlítás:**
-->
## Összehasonlítás

<!-- eredeti
|  | Gauss-felület | Mekkora felületen van fluxus | E távolságfüggése |
| --- | --- | --- | --- |
| gömb | koncentrikus gömb | 4πr² (az egész gömb) | 1/r² |
| henger | koaxiális henger | 2πrh (csak a palást) | 1/r |
| sík | átszúró kis henger | 2A (csak a két lap) | nem függ |
-->
- Gömbnél a {{Gauss|gausz}}-felület koncentrikus gömb, a fluxus négy pí er négyzet nagyságú felületen van (az egész gömb), E távolságfüggése pedig egy per er négyzet. [[pause 500]]
- Hengernél a {{Gauss|gausz}}-felület koaxiális henger, a fluxus kettő pí er há nagyságú felületen van (csak a palást), E távolságfüggése pedig egy per er. [[pause 500]]
- Síknál a {{Gauss|gausz}}-felület átszúró kis henger, a fluxus kettő á nagyságú felületen van (csak a két lap), E pedig nem függ a távolságtól. [[pause 500]]

<!-- eredeti
**Vizsgán** (mindháromnál): szimmetria-érv, a Gauss-felület rajza és hogy hol nincs fluxus; a Gauss-törvény beírva; E kifejezve; potenciál integrálással és a nullszint választása.
-->
## Amit a vizsgán le kell írni

Mindháromnál: szimmetria-érv, a {{Gauss|gausz}}-felület rajza és hogy hol nincs fluxus; a {{Gauss|gausz}}-törvény beírva; E kifejezve; potenciál integrálással és a nullszint választása.

<!-- eredeti
### 9. Kapacitás. Síkkondenzátor kapacitása. Dielektrikummal töltött kondenzátor
-->
# Első rész, kilencedik tétel. Kapacitás. Síkkondenzátor kapacitása. Dielektrikummal töltött kondenzátor

<!-- eredeti
| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| C | kapacitás (mennyi töltés jut 1 V-ra) | F = C/V |
| Q | a pozitív fegyverzet töltése | C |
| U | feszültség a két fegyverzet között | V |
| A | egy lemez (fegyverzet) területe | m² |
| d | a lemezek távolsága | m |
| η | felületi töltéssűrűség a lemezen (Q/A) | C/m² |
| D, E | indukció és térerősség a lemezek között | C/m², V/m |
| ε₀, εᵣ | vákuum permittivitása, a szigetelő relatív permittivitása | As/(Vm), nincs |
| C₀ | ugyanannak a kondenzátornak a kapacitása vákuummal | F |
| R | gömb sugara | m |
-->
## Jelölések

A C jel a kapacitást jelenti (mennyi töltés jut egy voltra), mértékegysége a farad, ami {{coulomb|kulomb}} per volt.

A Q jel a pozitív fegyverzet töltését jelenti, mértékegysége a {{coulomb|kulomb}}.

Az U jel a két fegyverzet közötti feszültséget jelenti, mértékegysége a volt.

Az A jel egy lemez (fegyverzet) területét jelenti, mértékegysége a négyzetméter.

A d jel a lemezek távolságát jelenti, mértékegysége a méter.

Az éta jel a lemezen lévő felületi töltéssűrűséget jelenti (Q per A), mértékegysége a {{coulomb|kulomb}} per négyzetméter.

A D jel az indukciót, az E jel a térerősséget jelenti a lemezek között; mértékegységük {{coulomb|kulomb}} per négyzetméter, illetve volt per méter.

Az epszilon nulla jel a vákuum permittivitását jelenti, mértékegysége az amper szekundum per volt méter; az epszilon er jel a szigetelő relatív permittivitását jelenti, ez mértékegység nélküli.

A C nulla jel ugyanannak a kondenzátornak a kapacitását jelenti vákuummal, mértékegysége a farad.

Az R jel a gömb sugarát jelenti, mértékegysége a méter.

<!-- eredeti
**Miről szól?** Ha egy vezetőre kétszer annyi töltést viszünk, minden kétszeres lesz, a potenciálja is. A töltés és a feszültség aránya tehát állandó, ez a kapacitás: megmutatja, mennyi töltés „fér el” 1 V feszültségnél. A kondenzátor két közeli lemez: a közelség miatt kis feszültséghez is sok töltés tartozik. Ha szigetelőt teszünk közé, az polarizálódik és gyengíti a teret, így ugyanannyi töltéshez még kisebb feszültség kell: nő a kapacitás.
-->
## Miről szól

Ha egy vezetőre kétszer annyi töltést viszünk, minden kétszeres lesz, a potenciálja is. A töltés és a feszültség aránya tehát állandó, ez a kapacitás: megmutatja, mennyi töltés fér el egy volt feszültségnél. A kondenzátor két közeli lemez: a közelség miatt kis feszültséghez is sok töltés tartozik. Ha szigetelőt teszünk közé, az polarizálódik és gyengíti a teret, így ugyanannyi töltéshez még kisebb feszültség kell: nő a kapacitás.

<!-- eredeti
**Definíció.** Lineáris közegben a potenciál egyenesen arányos a töltéssel, a hányados állandó (csak a geometriától és az anyagtól függ):

```latex
C = \frac{Q}{U}
```
-->
## Definíció

Lineáris közegben a potenciál egyenesen arányos a töltéssel, a hányados állandó (csak a geometriától és az anyagtól függ): a C kapacitás egyenlő Q per U. [[pause 500]]

<!-- eredeti
Magányos R sugarú gömbre U = kQ/R, így C = 4πε₀R; ez hétköznapi testeknél nagyon kicsi. Növelni úgy lehet, hogy közel teszünk egy másik (pl. földelt) vezetőt: a tér rövidebb útra integrálódik, kisebb a feszültség. A kondenzátor két, szigetelővel elválasztott vezető (fegyverzet), a töltésük ellentetten egyenlő.
-->
Magányos er sugarú gömbre U egyenlő ká Q per er, így C egyenlő négy pí epszilon nulla er; ez hétköznapi testeknél nagyon kicsi. [[pause 500]]
Növelni úgy lehet, hogy közel teszünk egy másik (például földelt) vezetőt: a tér rövidebb útra integrálódik, kisebb a feszültség. A kondenzátor két, szigetelővel elválasztott vezető (fegyverzet), a töltésük ellentetten egyenlő.

<!-- eredeti
**Síkkondenzátor** (feltétel: d sokkal kisebb a lemezek méreténél):
-->
## Síkkondenzátor

Feltétel: dé sokkal kisebb a lemezek méreténél.

<!-- eredeti
1. A két ellentétes töltésű lemez tere (8. tétel) a lemezek között összeadódik, kívül kioltja egymást. A lemezek között: D = η.
2. Ebből a térerősség E = η/(ε₀εᵣ), homogén.
3. A feszültség U = Ed = ηd/(ε₀εᵣ).
4. A kapacitás (Q = ηA):
-->
- Első lépés: a két ellentétes töltésű lemez tere (nyolcadik tétel) a lemezek között összeadódik, kívül kioltja egymást. A lemezek között D egyenlő éta. [[pause 500]]
- Második lépés: ebből a térerősség E egyenlő éta per, zárójelben epszilon nulla epszilon er, homogén. [[pause 500]]
- Harmadik lépés: a feszültség U egyenlő E dé, ami egyenlő éta dé per, zárójelben epszilon nulla epszilon er. [[pause 500]]
- Negyedik lépés: a kapacitás, ahol Q egyenlő éta á:

<!-- eredeti
```latex
C = \frac{Q}{U} = \frac{\eta A}{\dfrac{\eta d}{\varepsilon_0\varepsilon_r}} = \varepsilon_0\varepsilon_r\frac{A}{d}
```
-->
C egyenlő Q per U, ez egyenlő egy tört, a számláló éta á, a nevező éta dé per, zárójelben epszilon nulla epszilon er. [[pause 500]]
Ez pedig egyenlő epszilon nulla szorozva epszilon er szorozva á per dé. [[pause 500]]

<!-- eredeti
Ha d nem elég kicsi, a vonalak a széleken kiszóródnak, és a képlet pontatlan.
-->
Ha dé nem elég kicsi, a vonalak a széleken kiszóródnak, és a képlet pontatlan.

<!-- eredeti
**Dielektrikummal töltött kondenzátor.** A képletből látszik, hogy a kapacitás εᵣ-szeresre nő a vákuumhoz képest:

```latex
C = \varepsilon_r C_0
```
-->
## Dielektrikummal töltött kondenzátor

A képletből látszik, hogy a kapacitás epszilon er-szeresre nő a vákuumhoz képest: C egyenlő epszilon er szorozva C nulla. [[pause 500]]

<!-- eredeti
Oka: ugyanaz a szabad töltés ugyanakkora D-t hoz létre (D = η), de a polarizációs töltések miatt E = D/(ε₀εᵣ) kisebb, így U is kisebb.
-->
Oka: ugyanaz a szabad töltés ugyanakkora D-t hoz létre (D egyenlő éta), de a polarizációs töltések miatt E, ami egyenlő D per, zárójelben epszilon nulla epszilon er, kisebb, így U is kisebb. [[pause 500]]

<!-- eredeti
(Kiegészítés: gömbkondenzátor C = 4πε r₁r₂/(r₂ − r₁), hengerkondenzátor C = 2πεh/ln(r₂/r₁).)
-->
Kiegészítés: gömbkondenzátor esetén C egyenlő négy pí epszilon szorozva er egy er kettő, osztva, zárójelben er kettő mínusz er egy. [[pause 500]]
Hengerkondenzátor esetén C egyenlő kettő pí epszilon há per természetes alapú logaritmus er kettő per er egy. [[pause 500]]

<!-- eredeti
**Vizsgán:** C = Q/U és miért állandó; kondenzátor fogalma; síkkondenzátor levezetése (D = η → E → U → C); C = εᵣC₀ és miért.
-->
## Amit a vizsgán le kell írni

C egyenlő Q per U és miért állandó; kondenzátor fogalma; síkkondenzátor levezetése (D egyenlő éta, ebből E, ebből U, ebből C); C egyenlő epszilon er szorozva C nulla és miért. [[pause 500]]

<!-- eredeti
### 10. Síkkondenzátor feltöltésének munkája. Az elektromos tér energiája és energiasűrűsége
-->
# Első rész, tizedik tétel. Síkkondenzátor feltöltésének munkája. Az elektromos tér energiája és energiasűrűsége

<!-- eredeti
| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| W | munka, illetve a tárolt energia | J |
| q, u | töltés és feszültség a feltöltés egy közbülső pillanatában | C, V |
| Δq, dq | egy kicsi átvitt töltésadag | C |
| Q, U | végső töltés és feszültség | C, V |
| C | kapacitás | F |
| V | a lemezek közti térfogat (V = Ad) | m³ |
| w | energiasűrűség (energia 1 m³-ben) | J/m³ |
| D, E, η, A, d | mint a 9. tételben |  |
| F | a lemezek közti vonzóerő | N |
-->
## Jelölések

A W jel a munkát, illetve a tárolt energiát jelenti, mértékegysége a {{joule|dzsúl}}.

A kis q és a kis u jel a töltést és a feszültséget jelenti a feltöltés egy közbülső pillanatában; mértékegységük {{coulomb|kulomb}}, illetve volt.

A delta q és a dé q jel egy kicsi átvitt töltésadagot jelent, mértékegysége a {{coulomb|kulomb}}.

A nagy Q és a nagy U jel a végső töltést és feszültséget jelenti; mértékegységük {{coulomb|kulomb}}, illetve volt.

A C jel a kapacitást jelenti, mértékegysége a farad.

A nagy V jel a lemezek közti térfogatot jelenti, nagy V egyenlő á dé, mértékegysége a köbméter. [[pause 500]]

A kis w jel az energiasűrűséget jelenti (energia egy köbméterben), mértékegysége a {{joule|dzsúl}} per köbméter.

A D, E, éta, A és d jel ugyanazt jelenti, mint a kilencedik tételben.

Az F jel a lemezek közti vonzóerőt jelenti, mértékegysége a {{newton|nyúton}}.

<!-- eredeti
**Miről szól?** A kondenzátort apránként töltjük: az első adagot szinte ingyen viszük át, de minél több töltés van már rajta, annál nagyobb feszültség ellenében kell vinni a következőt. Átlagosan a végső feszültség felén dolgozunk, innen az ½. A befektetett munka a lemezek közötti **térben** tárolódik; a tér minden köbméterének van energiája.
-->
## Miről szól

A kondenzátort apránként töltjük: az első adagot szinte ingyen viszük át, de minél több töltés van már rajta, annál nagyobb feszültség ellenében kell vinni a következőt. Átlagosan a végső feszültség felén dolgozunk, innen az egy ketted szorzó. A befektetett munka a lemezek közötti térben tárolódik; a tér minden köbméterének van energiája.

<!-- eredeti
**A feltöltés munkája.** Közbülső állapotban a töltés q, a feszültség u = q/C. Egy kis Δq átvitelének munkája ΔW = uΔq (a feszültség az egységnyi töltésen végzett munka). 0-tól Q-ig összegezve:
-->
## A feltöltés munkája

Közbülső állapotban a töltés kis q, a feszültség kis u egyenlő q per C. [[pause 500]]
Egy kis delta q átvitelének munkája delta W egyenlő u szorozva delta q (a feszültség az egységnyi töltésen végzett munka). [[pause 500]]
Nullától nagy Q-ig összegezve:

<!-- eredeti
```latex
\Delta W = \frac{q}{C}\Delta q \;\Rightarrow\; W = \frac1C\int_0^Q q\,dq = \frac{Q^2}{2C} = \frac12 QU = \frac12 CU^2
```
-->
Delta W egyenlő q per C szorozva delta q. [[pause 500]]
Ebből W egyenlő egy per C szorozva integrál nullától nagy Q-ig q dé q, ami egyenlő nagy Q négyzet per, zárójelben kettő C. [[pause 500]]
Ez egyenlő egy ketted Q U, és egyenlő egy ketted C U négyzet. [[pause 500]]

<!-- eredeti
**Energiasűrűség.** Síkkondenzátorban a tér homogén. Beírjuk, hogy Q = ηA, U = Ed, D = η és V = Ad:
-->
## Energiasűrűség

Síkkondenzátorban a tér homogén. Beírjuk, hogy Q egyenlő éta á, U egyenlő E dé, D egyenlő éta és V egyenlő á dé. [[pause 500]]

<!-- eredeti
```latex
W = \frac12 QU = \frac12\eta A\cdot Ed = \frac12 DE\cdot Ad = \frac12 DE\cdot V
```
-->
W egyenlő egy ketted Q U, ami egyenlő egy ketted éta á szorozva E dé. [[pause 500]]
Ez egyenlő egy ketted D E szorozva á dé, végül egyenlő egy ketted D E szorozva V. [[pause 500]]

<!-- eredeti
Az energiasűrűség az 1 m³-re jutó energia, w = W/V:
-->
Az energiasűrűség az egy köbméterre jutó energia, kis w egyenlő nagy W per nagy V. [[pause 500]]

<!-- eredeti
```latex
w = \frac12\vec D\vec E \;\left(= \frac12\varepsilon E^2\right)
```
-->
Kis w egyenlő egy ketted D vektor skalárszorzat E vektor, zárójelben: ez egyenlő egy ketted epszilon E négyzet. [[pause 500]]

<!-- eredeti
Ez általánosan is igaz (nem csak kondenzátorban, nem csak sztatikusan). Ha a tér nem homogén, pontonként számolunk és összegzünk:
-->
Ez általánosan is igaz (nem csak kondenzátorban, nem csak sztatikusan). Ha a tér nem homogén, pontonként számolunk és összegzünk:

<!-- eredeti
```latex
W = \int_V w\,dV = \frac12\int_V\vec D\vec E\,dV
```
-->
W egyenlő a V térfogatra vett integrál w dé V, ami egyenlő egy ketted szorozva a V térfogatra vett integrál D vektor skalárszorzat E vektor dé V. [[pause 500]]

<!-- eredeti
**Másik út: a lemezek közti erőből.** Ha F = QE-t írnánk E = η/ε₀-lal, kétszer többet kapnánk a valóságosnál: a tér felét a lemez maga kelti, az önmagára nem hat. Helyesen F = QE/2 = Q²/(2ε₀A), ami nem függ d-től. Állandó töltésnél 0-ról d távolságra széthúzva a lemezeket: W = Fd = Q²d/(2ε₀A) = Q²/(2C), ugyanaz.
-->
## Másik út a lemezek közti erőből

Ha F egyenlő Q E-t írnánk E egyenlő éta per epszilon nullával, kétszer többet kapnánk a valóságosnál: a tér felét a lemez maga kelti, az önmagára nem hat. [[pause 500]]
Helyesen F egyenlő Q E per kettő, ami egyenlő Q négyzet per, zárójelben kettő epszilon nulla á, ami nem függ dé-től. [[pause 500]]
Állandó töltésnél nulláról dé távolságra széthúzva a lemezeket: W egyenlő F dé, ami egyenlő Q négyzet dé per, zárójelben kettő epszilon nulla á, ami egyenlő Q négyzet per, zárójelben kettő C, ugyanaz. [[pause 500]]

<!-- eredeti
**Vizsgán:** feltöltés kis adagokban, ΔW = (q/C)Δq, integrálás; W = Q²/2C = ½QU = ½CU²; síkkondenzátorral W = ½DE·V → w = ½D·E; W = ½∫D·E dV.
-->
## Amit a vizsgán le kell írni

Feltöltés kis adagokban, delta W egyenlő, zárójelben q per C, szorozva delta q, integrálás. [[pause 500]]
W egyenlő Q négyzet per kettő C, egyenlő egy ketted Q U, egyenlő egy ketted C U négyzet. [[pause 500]]
Síkkondenzátorral W egyenlő egy ketted D E szorozva V, ebből kis w egyenlő egy ketted D skalárszorzat E. [[pause 500]]
W egyenlő egy ketted integrál D skalárszorzat E dé V. [[pause 500]]

<!-- eredeti
### 11. Dipólmomentumra ható erő és forgatónyomaték. Dipólus tere és potenciálja
-->
# Első rész, tizenegyedik tétel. Dipólmomentumra ható erő és forgatónyomaték. Dipólus tere és potenciálja

<!-- eredeti
| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| Q, −Q | a dipólus két töltése | C |
| ℓ (vagy d) | a két töltés távolsága; vektorként a −-tól a + felé mutat | m |
| p | dipólmomentum, p = Qℓ | C·m |
| E | külső térerősség | V/m |
| φ | a dipólus és a tér közti szög | rad |
| M | forgatónyomaték | N·m |
| Eₚ | helyzeti (potenciális) energia | J |
| F | eredő erő | N |
| x | távolság a dipólus tengelyén | m |
| U | potenciál | V |
-->
## Jelölések

A Q és a mínusz Q jel a dipólus két töltését jelenti, mértékegysége a {{coulomb|kulomb}}.

Az el (vagy dé) jel a két töltés távolságát jelenti; vektorként a negatív töltéstől a pozitív felé mutat; mértékegysége a méter.

A pé jel a dipólmomentumot jelenti, pé egyenlő Q el, mértékegysége a {{coulomb|kulomb}} méter. [[pause 500]]

Az E jel a külső térerősséget jelenti, mértékegysége a volt per méter.

A fí jel a dipólus és a tér közti szöget jelenti, mértékegysége a radián.

Az M jel a forgatónyomatékot jelenti, mértékegysége a {{newton|nyúton}} méter.

Az E pé jel a helyzeti (potenciális) energiát jelenti, mértékegysége a {{joule|dzsúl}}.

Az F jel az eredő erőt jelenti, mértékegysége a {{newton|nyúton}}.

Az iksz jel a dipólus tengelyén mért távolságot jelenti, mértékegysége a méter.

Az U jel a potenciált jelenti, mértékegysége a volt.

<!-- eredeti
**Miről szól?** A dipólus egy + és egy − töltés egy kis pálcán. Egyenletes térben a két végét egyforma erővel, de ellentétes irányba húzza a tér: nem mozdul el, csak befordul a tér irányába, mint egy iránytű. Ha a tér nem egyenletes, az egyik végét erősebben húzza, így a dipólus az erősebb tér felé mozdul. Messziről a két töltés majdnem kioltja egymást, ezért a dipólus tere gyorsabban csökken, mint egy ponttöltésé.
-->
## Miről szól

A dipólus egy pozitív és egy negatív töltés egy kis pálcán. Egyenletes térben a két végét egyforma erővel, de ellentétes irányba húzza a tér: nem mozdul el, csak befordul a tér irányába, mint egy iránytű. Ha a tér nem egyenletes, az egyik végét erősebben húzza, így a dipólus az erősebb tér felé mozdul. Messziről a két töltés majdnem kioltja egymást, ezért a dipólus tere gyorsabban csökken, mint egy ponttöltésé.

<!-- eredeti
**Homogén térben.** A két erő: F₊ = QE és F₋ = −QE, az eredő nulla. A középpontra a nyomaték (mindkét erő karja ℓ/2):
-->
## Homogén térben

A két erő: F plusz egyenlő Q E és F mínusz egyenlő mínusz Q E, az eredő nulla. [[pause 500]]
A középpontra a nyomaték (mindkét erő karja el per kettő):

<!-- eredeti
```latex
\vec M = -\frac{\vec\ell}{2}\times(-Q\vec E) + \frac{\vec\ell}{2}\times Q\vec E = Q\vec\ell\times\vec E = \vec p\times\vec E, \qquad M = pE\sin\varphi
```
-->
Az M nyomatékvektor egyenlő mínusz el vektor per kettő vektoriálisan szorozva, zárójelben mínusz Q E vektor, plusz el vektor per kettő vektoriálisan szorozva Q E vektor. [[pause 500]]
Ez egyenlő Q el vektor vektoriálisan szorozva E vektor, vagyis pé vektor vektoriálisan szorozva E vektor. [[pause 500]]
Nagyságára M egyenlő pé E szinusz fí. [[pause 500]]

<!-- eredeti
**Helyzeti energia.** A nyomaték munkája φ₁ és φ₂ között W = pE(cosφ₁ − cosφ₂), ebből:
-->
## Helyzeti energia

A nyomaték munkája fí egy és fí kettő között W egyenlő pé E szorozva, zárójelben koszinusz fí egy mínusz koszinusz fí kettő, ebből: [[pause 500]]

<!-- eredeti
```latex
E_p = -\vec p\vec E
```
-->
Az E pé helyzeti energia egyenlő mínusz pé vektor skalárszorzat E vektor. [[pause 500]]

<!-- eredeti
Ha p és E egyirányú: nyomaték nincs, az energia minimális, **stabil** egyensúly. Ha ellentétes: nyomaték nincs, de az energia maximális, **instabil**.
-->
Ha pé és E egyirányú: nyomaték nincs, az energia minimális, stabil egyensúly. Ha ellentétes: nyomaték nincs, de az energia maximális, instabil.

<!-- eredeti
**Inhomogén térben.** Egy dimenzióban a + töltésnél E + ΔE, a − töltésnél E a tér, ΔE = ℓ·∂E/∂x, így az eredő F = QΔE = p·∂E/∂x. Három dimenzióban, illetve örvénymentes (sztatikus) térben:
-->
## Inhomogén térben

Egy dimenzióban a pozitív töltésnél E plusz delta E, a negatív töltésnél E a tér, delta E egyenlő el szorozva E parciális iksz szerint, így az eredő F egyenlő Q delta E, ami egyenlő pé szorozva E parciális iksz szerint. [[pause 500]]
Három dimenzióban, illetve örvénymentes (sztatikus) térben:

<!-- eredeti
```latex
\vec F = (\vec p\cdot\operatorname{grad})\vec E = \operatorname{grad}(\vec p\vec E)
```
-->
F vektor egyenlő, zárójelben pé vektor skalárszorzat gradiens, szorozva E vektor, ami egyenlő gradiens, zárójelben pé vektor skalárszorzat E vektor. [[pause 500]]

<!-- eredeti
Ez éppen az Eₚ = −p·E energia negatív gradiense. (Ezért vonzza a dörzsölt rúd a polarizált papírdarabot.)
-->
Ez éppen az E pé egyenlő mínusz pé skalárszorzat E energia negatív gradiense. [[pause 500]]
(Ezért vonzza a dörzsölt rúd a polarizált papírdarabot.)

<!-- eredeti
**Dipólus tere és potenciálja a tengelyen** (−Q és +Q egymástól d távolságra, vákuumban). A két ponttöltés terét előjelhelyesen összeadjuk, majd nagy x-re csak a vezető tagot tartjuk meg:
-->
## Dipólus tere és potenciálja a tengelyen

Mínusz Q és plusz Q egymástól dé távolságra, vákuumban. A két ponttöltés terét előjelhelyesen összeadjuk, majd nagy iksz-re csak a vezető tagot tartjuk meg:

<!-- eredeti
```latex
E = kQ\left(\frac{1}{x^2} - \frac{1}{(x+d)^2}\right) = kQ\frac{2xd + d^2}{x^2(x+d)^2} \;\xrightarrow{x\to\infty}\; \frac{2kQd}{x^3} = \frac{2kp}{x^3}
```
-->
E egyenlő ká Q szorozva, zárójelben egy per iksz négyzet mínusz egy per, zárójelben iksz plusz dé, a négyzeten. [[pause 500]]
Ez egyenlő ká Q szorozva egy tört, a számláló kettő iksz dé plusz dé négyzet, a nevező iksz négyzet szorozva, zárójelben iksz plusz dé, a négyzeten. [[pause 500]]
Ha iksz tart végtelenhez, ez tart kettő ká Q dé per iksz köbhöz, vagyis kettő ká pé per iksz köbhöz. [[pause 500]]

<!-- eredeti
```latex
U = kQ\left(\frac1x - \frac{1}{x+d}\right) = \frac{kQd}{x^2 + xd} \;\xrightarrow{x\to\infty}\; \frac{kp}{x^2}
```
-->
U egyenlő ká Q szorozva, zárójelben egy per iksz mínusz egy per, zárójelben iksz plusz dé. [[pause 500]]
Ez egyenlő ká Q dé per, zárójelben iksz négyzet plusz iksz dé. [[pause 500]]
Ha iksz tart végtelenhez, ez tart ká pé per iksz négyzethez. [[pause 500]]

<!-- eredeti
A tér 1/x³, a potenciál 1/x² szerint csökken (ponttöltésnél 1/x² és 1/x). Ellenőrzés: E = −dU/dx = 2kp/x³.
-->
A tér egy per iksz köb, a potenciál egy per iksz négyzet szerint csökken (ponttöltésnél egy per iksz négyzet és egy per iksz). [[pause 500]]
Ellenőrzés: E egyenlő mínusz dé U per dé iksz, ami egyenlő kettő ká pé per iksz köb. [[pause 500]]

## Amit a vizsgán le kell írni

<!-- eredeti
**Vizsgán:** p = Qℓ; homogén térben eredő erő 0, M = p × E levezetve; Eₚ = −p·E, stabil/instabil; inhomogén térben F = grad(p·E); tengelyen E → 2kp/x³, U → kp/x².
-->
Pé egyenlő Q el; homogén térben eredő erő nulla, M egyenlő pé vektoriálisan szorozva E levezetve. [[pause 500]]
E pé egyenlő mínusz pé skalárszorzat E, stabil, illetve instabil. [[pause 500]]
Inhomogén térben F egyenlő gradiens, zárójelben pé skalárszorzat E. [[pause 500]]
Tengelyen E tart kettő ká pé per iksz köbhöz, U tart ká pé per iksz négyzethez. [[pause 500]]


<!-- eredeti
### 12. Elektromos áramsűrűség. Differenciális Ohm-törvény és levezetése
-->
# Első rész, tizenkettedik tétel. Elektromos áramsűrűség. Differenciális {{Ohm|óm}}-törvény és levezetése

<!-- eredeti
| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| I | áramerősség (átfolyó töltés másodpercenként) | A = C/s |
| Q | töltés | C |
| t | idő | s |
| j | áramsűrűség (áram 1 m² keresztmetszeten) | A/m² |
| A, dA | keresztmetszet, felületelem | m² |
| R | ellenállás | Ω |
| ℓ | a vezető hossza | m |
| ρ | fajlagos ellenállás (anyagjellemző) | Ωm |
| σ = 1/ρ | fajlagos vezetőképesség | S/m = 1/(Ωm) |
| U | feszültség a vezető két vége között | V |
| E | térerősség a vezetőben | V/m |
-->
## Jelölések

Az I jel az áramerősséget jelenti, vagyis a másodpercenként átfolyó töltést, mértékegysége az amper, ami kulomb per másodperc.

A Q jel a töltést jelenti, mértékegysége a kulomb.

A t jel az időt jelenti, mértékegysége a másodperc.

A j jel az áramsűrűséget jelenti, vagyis az egy négyzetméter keresztmetszeten átfolyó áramot, mértékegysége az amper per négyzetméter.

Az A és a dé á jel a keresztmetszetet és a felületelemet jelenti, mértékegységük a négyzetméter.

Az R jel az ellenállást jelenti, mértékegysége az óm.

Az el jel a vezető hosszát jelenti, mértékegysége a méter.

A ró jel a fajlagos ellenállást jelenti, ami anyagjellemző, mértékegysége az óm méter.

A szigma jel, amely egyenlő egy per ró, a fajlagos vezetőképességet jelenti, mértékegysége a szímensz per méter, vagyis egy per óm méter. [[pause 500]]

Az U jel a vezető két vége közötti feszültséget jelenti, mértékegysége a volt.

Az E jel a vezetőben lévő térerősséget jelenti, mértékegysége a volt per méter.

<!-- eredeti
**Miről szól?** Az áramerősség az egész vezetőre vonatkozik (mennyi töltés megy át másodpercenként), az áramsűrűség egy pontra (ott mennyire „zsúfolt” az áramlás). A szokásos U = RI csak egyszerű, egyenes vezetőre jó. A differenciális Ohm-törvény ugyanez pontra lebontva: ahol nagyobb a térerősség, ott nagyobb az áramsűrűség, és ez bármilyen alakú vezetőre használható.
-->
## Miről szól

Az áramerősség az egész vezetőre vonatkozik (mennyi töltés megy át másodpercenként), az áramsűrűség egy pontra (ott mennyire „zsúfolt” az áramlás). A szokásos összefüggés, az U feszültség egyenlő az R ellenállás szorozva az I áramerősség, csak egyszerű, egyenes vezetőre jó. [[pause 500]] A differenciális {{Ohm|óm}}-törvény ugyanez pontra lebontva: ahol nagyobb a térerősség, ott nagyobb az áramsűrűség, és ez bármilyen alakú vezetőre használható.

<!-- eredeti
**Áramerősség:** a keresztmetszeten időegység alatt átfolyó nettó töltés. Iránya a pozitív töltések (elképzelt) mozgásának iránya, az elektronokéval ellentétes. Egy időszak alatt átfolyt töltés: Q = ∫I dt.
-->
## Áramerősség

A keresztmetszeten időegység alatt átfolyó nettó töltés. Iránya a pozitív töltések (elképzelt) mozgásának iránya, az elektronokéval ellentétes. Egy időszak alatt átfolyt töltés: a Q töltés egyenlő integrál í dé té. [[pause 500]]

<!-- eredeti
**Áramsűrűség:** az áramlásra merőleges egységnyi felületen átfolyó áram; vektor, a pozitív töltéshordozók mozgásának irányába mutat.
-->
## Áramsűrűség

Az áramlásra merőleges egységnyi felületen átfolyó áram; vektor, a pozitív töltéshordozók mozgásának irányába mutat.

<!-- eredeti
```latex
j = \lim_{A\to0}\frac{I}{A} \qquad I = \int_A\vec j\,d\vec A \quad (\text{egyenletes, merőleges esetben } I = jA)
```
-->
A j áramsűrűség egyenlő limesz á tart nullához í per á. [[pause 500]]

Í egyenlő a jé vektor skalárszorzat dé á vektor integrálja az á felületre. [[pause 500]]

Egyenletes, merőleges esetben í egyenlő jé szorozva á. [[pause 500]]

<!-- eredeti
**Ellenállás és méretek.** Kétszer hosszabb vezető olyan, mint két ugyanolyan sorba kötve (kétszeres R); kétszer vastagabb olyan, mint két párhuzamosan (fele R):
-->
## Ellenállás és méretek

Kétszer hosszabb vezető olyan, mint két ugyanolyan sorba kötve (kétszeres er); kétszer vastagabb olyan, mint két párhuzamosan (fele er):

<!-- eredeti
```latex
R = \rho\frac{\ell}{A}
```
-->
Er egyenlő ró szorozva el per á. [[pause 500]]

<!-- eredeti
**A differenciális Ohm-törvény levezetése.** Vékony, ℓ hosszú, A keresztmetszetű vezető, benne egyenletes tér és áramsűrűség:
-->
## A differenciális {{Ohm|óm}}-törvény levezetése

Vékony, el hosszú, á keresztmetszetű vezető, benne egyenletes tér és áramsűrűség:

<!-- eredeti
1. A két vége közti feszültség U = Eℓ, az áram I = jA.
2. Az ellenállás egyrészt R = U/I = Eℓ/(jA), másrészt R = ρℓ/A.
3. A kettőt egyenlővé téve ℓ/A kiesik: ρ = E/j.
-->
- Első lépés: a két vége közti feszültség ú egyenlő é szorozva el, [[pause 500]] az áram í egyenlő jé szorozva á. [[pause 500]]
- Második lépés: az ellenállás egyrészt er egyenlő ú per í, ami egyenlő é szorozva el, osztva zárójelben jé szorozva á, [[pause 500]] másrészt er egyenlő ró szorozva el per á. [[pause 500]]
- Harmadik lépés: a kettőt egyenlővé téve az el per á kiesik: ró egyenlő é per jé. [[pause 500]]

<!-- eredeti
```latex
\frac{E\ell}{jA} = \rho\frac{\ell}{A} \;\Rightarrow\; \vec E = \rho\,\vec j \quad\Longleftrightarrow\quad \vec j = \sigma\vec E
```
-->
Egy tört, a számláló é szorozva el, a nevező jé szorozva á, egyenlő ró szorozva el per á. [[pause 500]]

Ebből következik, hogy az é vektor egyenlő ró szorozva a jé vektor, [[pause 500]] ami egyenértékű azzal, hogy a jé vektor egyenlő szigma szorozva az é vektor. [[pause 500]]

<!-- eredeti
Ez általánosan is igaz, ez az Ohm-féle anyagegyenlet. Csak közelítés: fémekben az áram melegít, és ettől σ változik; diódára állandó hőmérsékleten sem igaz; szupravezetőben ρ = 0, tér nélkül is folyik áram.
-->
Ez általánosan is igaz, ez az {{Ohm|óm}}-féle anyagegyenlet. Csak közelítés: fémekben az áram melegít, és ettől szigma változik; diódára állandó hőmérsékleten sem igaz; szupravezetőben ró egyenlő nulla, tér nélkül is folyik áram. [[pause 500]]

<!-- eredeti
**Vizsgán:** I és j definíciója, I = ∫j dA; R = ρℓ/A indoklással; a levezetés három lépése; j = σE; korlátok.
-->
## Amit a vizsgán le kell írni

- Í és jé definíciója, í egyenlő integrál jé dé á. [[pause 500]]
- Er egyenlő ró szorozva el per á, indoklással. [[pause 500]]
- A levezetés három lépése.
- Jé egyenlő szigma szorozva é. [[pause 500]]
- Korlátok.

<!-- eredeti
### 13. A kontinuitási egyenlet. Kirchhoff csomóponti törvénye
-->
# Első rész, tizenharmadik tétel. A kontinuitási egyenlet. {{Kirchhoff|kirhhoff}} csomóponti törvénye

<!-- eredeti
| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| j | áramsűrűség | A/m² |
| ρ | térfogati töltéssűrűség | C/m³ |
| H, D | mágneses térerősség, elektromos indukció | A/m, C/m² |
| V, F | egy térrész és az azt körbevevő zárt felület | m³, m² |
| Q | a térrészben lévő töltés | C |
| I | egy ágban folyó áram | A |
-->
## Jelölések

A j jel az áramsűrűséget jelenti, mértékegysége az amper per négyzetméter.

A ró jel a térfogati töltéssűrűséget jelenti, mértékegysége a kulomb per köbméter.

A H és a D jel a mágneses térerősséget és az elektromos indukciót jelenti, mértékegységük az amper per méter, illetve a kulomb per négyzetméter.

A nagy V és a nagy F jel egy térrészt és az azt körbevevő zárt felületet jelenti, mértékegységük a köbméter, illetve a négyzetméter.

A Q jel a térrészben lévő töltést jelenti, mértékegysége a kulomb.

Az I jel egy ágban folyó áramot jelenti, mértékegysége az amper.

<!-- eredeti
**Miről szól?** A töltés nem keletkezik és nem tűnik el. Ha egy térrészben fogy a töltés, akkor az valahol kiáramlott a határán, mint egy kádban: a vízszint csak úgy változhat, ha befolyik vagy kifolyik a víz. Ha minden állandósult, amennyi befolyik, annyi ki is folyik: ez a csomóponti törvény.
-->
## Miről szól

A töltés nem keletkezik és nem tűnik el. Ha egy térrészben fogy a töltés, akkor az valahol kiáramlott a határán, mint egy kádban: a vízszint csak úgy változhat, ha befolyik vagy kifolyik a víz. Ha minden állandósult, amennyi befolyik, annyi ki is folyik: ez a csomóponti törvény.

<!-- eredeti
**Levezetés:**
-->
## Levezetés

<!-- eredeti
1. Az 1. Maxwell-egyenlet mindkét oldalának vesszük a divergenciáját. A bal oldal 0, mert div rot ≡ 0:
-->
Első lépés. Az első {{Maxwell|mekszvel}}-egyenlet mindkét oldalának vesszük a divergenciáját. A bal oldal nulla, mert divergencia rotáció azonosan nulla: [[pause 500]]

<!-- eredeti
```latex
\underbrace{\operatorname{div}\operatorname{rot}\vec H}_{0} = \operatorname{div}\vec j + \frac{\partial}{\partial t}\operatorname{div}\vec D
```
-->
Divergencia rotáció há vektor, ami nulla, egyenlő divergencia jé vektor plusz divergencia dé vektor parciális té szerint. [[pause 500]]

<!-- eredeti
2. A 3. Maxwell-egyenletből div D = ρ, így megkapjuk a **differenciális alakot**:
-->
Második lépés. A harmadik {{Maxwell|mekszvel}}-egyenletből divergencia dé egyenlő ró, [[pause 500]] így megkapjuk a differenciális alakot:

<!-- eredeti
```latex
\operatorname{div}\vec j = -\frac{\partial\rho}{\partial t}
```
-->
Divergencia jé vektor egyenlő mínusz ró parciális té szerint. [[pause 500]]

<!-- eredeti
Jelentése: az áramsűrűség ott forrásos, ahol a töltéssűrűség csökken (onnan áramlik ki a töltés).
-->
Jelentése: az áramsűrűség ott forrásos, ahol a töltéssűrűség csökken (onnan áramlik ki a töltés).

<!-- eredeti
3. Egy álló térfogatra integrálva és a Gauss-Osztrogradszkij tételt használva az **integrális alak**:
-->
Harmadik lépés. Egy álló térfogatra integrálva és a {{Gauss|gausz}}-{{Osztrogradszkij|osztrogradszkij}} tételt használva az integrális alak:

<!-- eredeti
```latex
\oint_F\vec j\,d\vec A = -\frac{d}{dt}\int_V\rho\,dV
```
-->
A jé vektor skalárszorzat dé á vektor zárt felületi integrálja a nagy ef felületre egyenlő mínusz dé per dé té szorozva integrál ró dé vé a nagy vé térfogatra. [[pause 500]]

<!-- eredeti
A zárt felületen kifolyó áram = a bent lévő töltés csökkenésének sebessége.
-->
A zárt felületen kifolyó áram egyenlő a bent lévő töltés csökkenésének sebességével.

<!-- eredeti
4. **Stacionárius esetben** (semmi nem változik időben) a jobb oldal 0. Egy csomópont köré tett zárt felületre:
-->
Negyedik lépés. Stacionárius esetben (semmi nem változik időben) a jobb oldal nulla. Egy csomópont köré tett zárt felületre:

<!-- eredeti
```latex
\oint_f\vec j\,d\vec A = 0 \;\Rightarrow\; \sum I = 0
```
-->
A jé vektor skalárszorzat dé á vektor zárt felületi integrálja a kis ef felületre egyenlő nulla, [[pause 500]] ebből következik, hogy szumma í egyenlő nulla. [[pause 500]]

<!-- eredeti
Ez Kirchhoff csomóponti törvénye.
-->
Ez {{Kirchhoff|kirhhoff}} csomóponti törvénye.

<!-- eredeti
**Vizsgán:** a négy lépés (div, div rot ≡ 0, div D = ρ, Gauss-Osztrogradszkij), a jelentés (töltésmegmaradás), stacionárius esetben ΣI = 0.
-->
## Amit a vizsgán le kell írni

- A négy lépés: divergencia, divergencia rotáció azonosan nulla, divergencia dé egyenlő ró, {{Gauss|gausz}}-{{Osztrogradszkij|osztrogradszkij}}. [[pause 500]]
- A jelentés: töltésmegmaradás.
- Stacionárius esetben szumma í egyenlő nulla. [[pause 500]]

<!-- eredeti
### 14. Elektromos mennyiségek két közeg határán. E és D vonalak törése. Dielektrikum külső térben
-->
# Első rész, tizennegyedik tétel. Elektromos mennyiségek két közeg határán. {{E|é}} és {{D|dé}} vonalak törése. Dielektrikum külső térben

<!-- eredeti
| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| 1, 2 index | az 1-es és a 2-es közegben |  |
| t index | tangenciális: a határfelülettel párhuzamos komponens |  |
| n index | normális: a határfelületre merőleges komponens |  |
| E, D | térerősség, indukció | V/m, C/m² |
| ε₁, ε₂ | a két közeg permittivitása | As/(Vm) |
| η | felületi töltéssűrűség a határon | C/m² |
| α, β | a vonal és a határra merőleges egyenes közti szög az 1-es, illetve 2-es közegben | rad |
-->
## Jelölések

Az egyes és a kettes index azt jelenti, hogy a mennyiség az egyes, illetve a kettes közegben értendő.

A té index a tangenciális, vagyis a határfelülettel párhuzamos komponenst jelöli.

Az en index a normális, vagyis a határfelületre merőleges komponenst jelöli.

Az E és a D jel a térerősséget és az indukciót jelenti, mértékegységük a volt per méter, illetve a kulomb per négyzetméter.

Az epszilon egy és az epszilon kettő a két közeg permittivitását jelenti, mértékegysége az amper szekundum per volt méter.

Az éta jel a határon lévő felületi töltéssűrűséget jelenti, mértékegysége a kulomb per négyzetméter.

Az alfa és a béta jel a vonal és a határra merőleges egyenes közti szöget jelenti az egyes, illetve a kettes közegben, mértékegysége a radián.

<!-- eredeti
**Miről szól?** Két különböző szigetelő találkozásánál a vektorokat felbontjuk a határral párhuzamos és rá merőleges részre. Két szabály dönt el mindent: a párhuzamos E nem ugrik, és a merőleges D nem ugrik (ha nincs a határon töltés). Mivel a két közegben más az ε, a vonalak a határon megtörnek, hasonlóan a fényhez.
-->
## Miről szól

Két különböző szigetelő találkozásánál a vektorokat felbontjuk a határral párhuzamos és rá merőleges részre. Két szabály dönt el mindent: a párhuzamos é nem ugrik, és a merőleges dé nem ugrik (ha nincs a határon töltés). Mivel a két közegben más az epszilon, a vonalak a határon megtörnek, hasonlóan a fényhez.

<!-- eredeti
**Tangenciális komponens.** Veszünk egy lapos téglalap alakú hurkot, ami a határt két oldalról öleli, és felírjuk rá a 2. Maxwell-egyenletet (∮E ds = −dΦ/dt). Ha a hurkot „rálapítjuk” a határra: a rövid oldalak integrálja 0-hoz tart, és a közbezárt felület is, így a B-fluxus is eltűnik. Marad a két hosszú oldal, ellentétes irányban:
-->
## Tangenciális komponens

Veszünk egy lapos téglalap alakú hurkot, ami a határt két oldalról öleli, és felírjuk rá a második {{Maxwell|mekszvel}}-egyenletet, vagyis hogy é skalárszorzat dé es zárt görbe menti integrálja egyenlő mínusz dé nagy fí per dé té. [[pause 500]] Ha a hurkot „rálapítjuk” a határra: a rövid oldalak integrálja nullához tart, és a közbezárt felület is, így a bé-fluxus is eltűnik. Marad a két hosszú oldal, ellentétes irányban:

<!-- eredeti
```latex
\int_A^B\left(\vec E_2 - \vec E_1\right)d\vec s = 0 \;\Rightarrow\; E_{t2} = E_{t1}, \qquad \frac{D_{t2}}{D_{t1}} = \frac{\varepsilon_2}{\varepsilon_1}
```
-->
Integrál á-tól bé-ig, zárójelben é kettő vektor mínusz é egy vektor, skalárszorzat dé es vektor, egyenlő nulla. [[pause 500]]

Ebből következik, hogy é té kettő egyenlő é té egy, [[pause 500]] valamint dé té kettő per dé té egy egyenlő epszilon kettő per epszilon egy. [[pause 500]]

<!-- eredeti
(Dₜ nem folytonos, mert D = εE és ε más.)
-->
Dé té nem folytonos, mert dé egyenlő epszilon szorozva é, és epszilon más. [[pause 500]]

<!-- eredeti
**Normális komponens.** Lapos dobozt teszünk a határra (egyik lapja az 1-es, másik a 2-es közegben), és felírjuk rá a Gauss-törvényt. A dobozt lapítva a palást és a térfogat eltűnik, a bezárt töltésből csak a felületi töltés marad:
-->
## Normális komponens

Lapos dobozt teszünk a határra (egyik lapja az egyes, másik a kettes közegben), és felírjuk rá a {{Gauss|gausz}}-törvényt. A dobozt lapítva a palást és a térfogat eltűnik, a bezárt töltésből csak a felületi töltés marad:

<!-- eredeti
```latex
D_{n2} - D_{n1} = \eta
```
-->
Dé en kettő mínusz dé en egy egyenlő éta. [[pause 500]]

<!-- eredeti
Ha a határon nincs töltés (η = 0), Dₙ folytonos, de Eₙ ugrik:
-->
Ha a határon nincs töltés, vagyis éta egyenlő nulla, dé en folytonos, de é en ugrik: [[pause 500]]

<!-- eredeti
```latex
D_{n1} = D_{n2} \;\Rightarrow\; \varepsilon_1 E_{n1} = \varepsilon_2 E_{n2}
```
-->
Dé en egy egyenlő dé en kettő, [[pause 500]] ebből következik, hogy epszilon egy szorozva é en egy egyenlő epszilon kettő szorozva é en kettő. [[pause 500]]

<!-- eredeti
**Törési törvény** (η = 0). A tangens a párhuzamos és a merőleges komponens hányadosa:
-->
## Törési törvény

Ez az éta egyenlő nulla esetre érvényes. [[pause 500]] A tangens a párhuzamos és a merőleges komponens hányadosa:

<!-- eredeti
```latex
\frac{\operatorname{tg}\alpha}{\operatorname{tg}\beta} = \frac{D_{1t}/D_{1n}}{D_{2t}/D_{2n}} = \frac{D_{1t}}{D_{2t}} = \frac{\varepsilon_1}{\varepsilon_2}
```
-->
Tangens alfa per tangens béta egyenlő egy tört, amelynek számlálója dé egy té per dé egy en, nevezője dé kettő té per dé kettő en. [[pause 500]]

Ez egyenlő dé egy té per dé kettő té, [[pause 500]] ami egyenlő epszilon egy per epszilon kettő. [[pause 500]]

<!-- eredeti
Ugyanez jön ki E-re is: az E és a D vonalak ugyanúgy törnek. A nagyobb ε-ú közegben a vonal jobban elhajlik a merőlegestől.
-->
Ugyanez jön ki é-re is: az é és a dé vonalak ugyanúgy törnek. A nagyobb epszilonú közegben a vonal jobban elhajlik a merőlegestől.

<!-- eredeti
**Dielektrikum külső térben.** Homogén térbe tett szigetelőben a tér csak akkor lesz homogén és eredeti irányú, ha a test ellipszoid (egyik tengelye a térrel párhuzamos); ezt nézzük. A testen nincs szabad töltés, tehát D vonalai folytonosak, viszont polarizációs töltés van, így Eₙ ugrik. A térre merőleges lapoknál D kint és bent egyforma, E bent kisebb; a térrel párhuzamos oldalaknál Eₜ folytonos, ezért kint megritkulnak az E vonalak. Végeredmény: bent E kisebb (**depolarizáció**), a D vonalak viszont beszűrűsödnek a testbe.
-->
## Dielektrikum külső térben

Homogén térbe tett szigetelőben a tér csak akkor lesz homogén és eredeti irányú, ha a test ellipszoid (egyik tengelye a térrel párhuzamos); ezt nézzük. A testen nincs szabad töltés, tehát dé vonalai folytonosak, viszont polarizációs töltés van, így é en ugrik. A térre merőleges lapoknál dé kint és bent egyforma, é bent kisebb; a térrel párhuzamos oldalaknál é té folytonos, ezért kint megritkulnak az é vonalak. Végeredmény: bent é kisebb (depolarizáció), a dé vonalak viszont beszűrűsödnek a testbe.

<!-- eredeti
**Vizsgán:** hurok és doboz rajza; Eₜ₁ = Eₜ₂ (miért tűnik el a fluxus); Dₙ₂ − Dₙ₁ = η; η = 0 esetén ε₁Eₙ₁ = ε₂Eₙ₂; tgα/tgβ = ε₁/ε₂; depolarizáció.
-->
## Amit a vizsgán le kell írni

- Hurok és doboz rajza.
- É té egy egyenlő é té kettő, és hogy miért tűnik el a fluxus. [[pause 500]]
- Dé en kettő mínusz dé en egy egyenlő éta. [[pause 500]]
- Éta egyenlő nulla esetén epszilon egy szorozva é en egy egyenlő epszilon kettő szorozva é en kettő. [[pause 500]]
- Tangens alfa per tangens béta egyenlő epszilon egy per epszilon kettő. [[pause 500]]
- Depolarizáció.

<!-- eredeti
### 15. Áramsűrűség két közeg határán. Áramsűrűség törési törvénye
-->
# Első rész, tizenötödik tétel. Áramsűrűség két közeg határán. Áramsűrűség törési törvénye

<!-- eredeti
| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| j₁, j₂ | áramsűrűség a két vezető közegben | A/m² |
| n, t index | a határra merőleges, illetve vele párhuzamos komponens |  |
| σ₁, σ₂ | a két közeg fajlagos vezetőképessége | S/m |
| E | térerősség | V/m |
| α, β | az áramvonal szöge a merőlegessel az 1-es, illetve 2-es közegben | rad |
| G, C | konduktancia (1/R), kapacitás | S, F |
-->
## Jelölések

A jé egy és a jé kettő az áramsűrűséget jelenti a két vezető közegben, mértékegysége az amper per négyzetméter.

Az en és a té index a határra merőleges, illetve vele párhuzamos komponenst jelöli.

A szigma egy és a szigma kettő a két közeg fajlagos vezetőképességét jelenti, mértékegysége a szímensz per méter.

Az E jel a térerősséget jelenti, mértékegysége a volt per méter.

Az alfa és a béta jel az áramvonal szögét jelenti a merőlegessel az egyes, illetve a kettes közegben, mértékegysége a radián.

A G és a C jel a konduktanciát, vagyis az egy per er mennyiséget, illetve a kapacitást jelenti, mértékegységük a szímensz, illetve a farad. [[pause 500]]

<!-- eredeti
**Miről szól?** Ugyanaz, mint a 14. tétel, csak két vezető határán folyó áramra. Állandósult áramlásnál a töltés nem gyűlhet fel a határon: ami merőlegesen odajön, annak át is kell mennie. A párhuzamos térerősség pedig most is folytonos.
-->
## Miről szól

Ugyanaz, mint a tizennegyedik tétel, csak két vezető határán folyó áramra. Állandósult áramlásnál a töltés nem gyűlhet fel a határon: ami merőlegesen odajön, annak át is kell mennie. A párhuzamos térerősség pedig most is folytonos.

<!-- eredeti
**Normális komponens.** A stacionárius kontinuitási egyenlet (∮j dA = 0) egy határra tett lapos dobozra:
-->
## Normális komponens

A stacionárius kontinuitási egyenlet, vagyis hogy jé skalárszorzat dé á zárt felületi integrálja egyenlő nulla, [[pause 500]] egy határra tett lapos dobozra:

<!-- eredeti
```latex
j_{2n}A - j_{1n}A = 0 \;\Rightarrow\; j_{1n} = j_{2n}
```
-->
Jé kettő en szorozva á mínusz jé egy en szorozva á egyenlő nulla, [[pause 500]] ebből következik, hogy jé egy en egyenlő jé kettő en. [[pause 500]]

<!-- eredeti
**Tangenciális komponens.** Eₜ₁ = Eₜ₂ (14. tétel), és az Ohm-törvény szerint E = j/σ:
-->
## Tangenciális komponens

É té egy egyenlő é té kettő (tizennegyedik tétel), [[pause 500]] és az {{Ohm|óm}}-törvény szerint é egyenlő jé per szigma: [[pause 500]]

<!-- eredeti
```latex
\frac{j_{1t}}{\sigma_1} = \frac{j_{2t}}{\sigma_2}
```
-->
Jé egy té per szigma egy egyenlő jé kettő té per szigma kettő. [[pause 500]]

<!-- eredeti
**Törési törvény:**
-->
## Törési törvény

<!-- eredeti
```latex
\frac{\operatorname{tg}\alpha}{\operatorname{tg}\beta} = \frac{j_{1t}/j_{1n}}{j_{2t}/j_{2n}} = \frac{j_{1t}}{j_{2t}} = \frac{\sigma_1}{\sigma_2}
```
-->
Tangens alfa per tangens béta egyenlő egy tört, amelynek számlálója jé egy té per jé egy en, nevezője jé kettő té per jé kettő en. [[pause 500]]

Ez egyenlő jé egy té per jé kettő té, [[pause 500]] ami egyenlő szigma egy per szigma kettő. [[pause 500]]

<!-- eredeti
Pont olyan, mint a dielektrikumoknál, csak ε helyett σ áll (és D helyett j). Következmény: jó vezetőből (fém) rossz vezetőbe (talaj) az áram szinte merőlegesen lép ki. A hasonlóságot a jegyzet G/σ = C/ε alakban is felírja: ugyanarra az elektróda-elrendezésre a konduktancia és a kapacitás az anyagjellemzővel osztva ugyanaz, csak a geometriától függ.
-->
Pont olyan, mint a dielektrikumoknál, csak epszilon helyett szigma áll (és dé helyett jé). Következmény: jó vezetőből (fém) rossz vezetőbe (talaj) az áram szinte merőlegesen lép ki. A hasonlóságot a jegyzet gé per szigma egyenlő cé per epszilon alakban is felírja: [[pause 500]] ugyanarra az elektróda-elrendezésre a konduktancia és a kapacitás az anyagjellemzővel osztva ugyanaz, csak a geometriától függ.

<!-- eredeti
**Vizsgán:** j₁ₙ = j₂ₙ a stacionárius kontinuitásból; j₁ₜ/σ₁ = j₂ₜ/σ₂; tgα/tgβ = σ₁/σ₂.
-->
## Amit a vizsgán le kell írni

- Jé egy en egyenlő jé kettő en, a stacionárius kontinuitásból. [[pause 500]]
- Jé egy té per szigma egy egyenlő jé kettő té per szigma kettő. [[pause 500]]
- Tangens alfa per tangens béta egyenlő szigma egy per szigma kettő. [[pause 500]]

<!-- eredeti
### 16. A stacionárius áram munkája, teljesítménye, teljesítménysűrűsége
-->
# Első rész, tizenhatodik tétel. A stacionárius áram munkája, teljesítménye, teljesítménysűrűsége

<!-- eredeti
| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| W | a mező munkája (pl. keletkezett hő) | J |
| Q | átfolyt töltés (Q = It) | C |
| U, I, R | feszültség, áram, ellenállás | V, A, Ω |
| t | idő | s |
| P | teljesítmény | W |
| V | a vezető térfogata (Aℓ) | m³ |
| p\_J | teljesítménysűrűség: 1 m³-ben 1 s alatt keletkező hő | W/m³ |
| E, j, ρ, σ | térerősség, áramsűrűség, fajlagos ellenállás, vezetőképesség | V/m, A/m², Ωm, S/m |
-->
## Jelölések

A W jel a mező munkáját jelenti, például a keletkezett hőt, mértékegysége a dzsúl.

A Q jel az átfolyt töltést jelenti, amely egyenlő í szorozva té, mértékegysége a kulomb. [[pause 500]]

Az U, az I és az R jel a feszültséget, az áramot és az ellenállást jelenti, mértékegységük a volt, az amper és az óm.

A t jel az időt jelenti, mértékegysége a másodperc.

A P jel a teljesítményt jelenti, mértékegysége a watt.

A nagy V jel a vezető térfogatát jelenti, amely egyenlő á szorozva el, mértékegysége a köbméter. [[pause 500]]

A pé nagy jé jel a teljesítménysűrűséget jelenti, vagyis az egy köbméterben egy másodperc alatt keletkező hőt, mértékegysége a watt per köbméter.

Az E, a kis j, a ró és a szigma jel a térerősséget, az áramsűrűséget, a fajlagos ellenállást és a vezetőképességet jelenti, mértékegységük a volt per méter, az amper per négyzetméter, az óm méter és a szímensz per méter.

<!-- eredeti
**Miről szól?** A feszültség az egységnyi töltésen végzett munka, így ha t idő alatt Q = It töltés megy át U feszültségen, a mező QU munkát végez. Ez a fogyasztóban hővé, mozgássá, kémiai energiává vagy fénnyé alakul; ha van ellenállás, hő mindig keletkezik. A teljesítménysűrűség azt mondja meg, a vezető melyik pontja mennyire melegszik: ahol sűrűbb az áram, ott (a négyzetével) sokkal jobban.
-->
## Miről szól

A feszültség az egységnyi töltésen végzett munka, így ha té idő alatt kú egyenlő í szorozva té töltés megy át ú feszültségen, a mező kú szorozva ú munkát végez. [[pause 500]] Ez a fogyasztóban hővé, mozgássá, kémiai energiává vagy fénnyé alakul; ha van ellenállás, hő mindig keletkezik. A teljesítménysűrűség azt mondja meg, a vezető melyik pontja mennyire melegszik: ahol sűrűbb az áram, ott (a négyzetével) sokkal jobban.

<!-- eredeti
**Munka és teljesítmény** (Joule-törvény, az U = RI-t beírva):
-->
## Munka és teljesítmény

Ez a {{Joule|dzsúl}}-törvény, az ú egyenlő er szorozva í összefüggést beírva: [[pause 500]]

<!-- eredeti
```latex
W = QU = UIt = I^2Rt = \frac{U^2}{R}t \qquad P = UI = I^2R = \frac{U^2}{R}
```
-->
Dupla vé egyenlő kú szorozva ú, ami egyenlő ú szorozva í szorozva té, ami egyenlő í négyzet szorozva er szorozva té, ami egyenlő ú négyzet per er, szorozva té. [[pause 500]]

Pé egyenlő ú szorozva í, ami egyenlő í négyzet szorozva er, ami egyenlő ú négyzet per er. [[pause 500]]

<!-- eredeti
**Differenciális alak.** Egy homogén drótban leadott teljesítményt elosztjuk a drót térfogatával (U = Eℓ, I = jA, V = Aℓ):
-->
## Differenciális alak

Egy homogén drótban leadott teljesítményt elosztjuk a drót térfogatával, ahol ú egyenlő é szorozva el, í egyenlő kis jé szorozva á, és nagy vé egyenlő á szorozva el: [[pause 500]]

<!-- eredeti
```latex
p_J = \frac{P}{V} = \frac{UI}{A\ell} = \frac{E\ell\cdot jA}{A\ell} = \vec E\vec j = \rho j^2 = \sigma E^2
```
-->
Pé nagy jé egyenlő pé per nagy vé, ami egyenlő ú szorozva í, osztva zárójelben á szorozva el. [[pause 500]]

Ez egyenlő egy törttel, amelynek számlálója é szorozva el szorozva kis jé szorozva á, nevezője á szorozva el. [[pause 500]]

Ez egyenlő az é vektor és a kis jé vektor skalárszorzatával, [[pause 500]] ami egyenlő ró szorozva kis jé négyzet, [[pause 500]] ami egyenlő szigma szorozva é négyzet. [[pause 500]]

<!-- eredeti
Ha az áramlás nem egyenletes, pontonként számolunk és összegzünk: P = ∫p\_J dV.
-->
Ha az áramlás nem egyenletes, pontonként számolunk és összegzünk: pé egyenlő integrál pé nagy jé dé nagy vé. [[pause 500]]

<!-- eredeti
**Vizsgán:** W = QU = UIt; mire alakulhat az energia; Joule-törvény három alakja; P = UI = I²R = U²/R; p\_J levezetése és egysége; inhomogén esetben integrál.
-->
## Amit a vizsgán le kell írni

- Dupla vé egyenlő kú szorozva ú, ami egyenlő ú szorozva í szorozva té. [[pause 500]]
- Mire alakulhat az energia.
- A {{Joule|dzsúl}}-törvény három alakja.
- Pé egyenlő ú szorozva í, ami egyenlő í négyzet szorozva er, ami egyenlő ú négyzet per er. [[pause 500]]
- A pé nagy jé levezetése és egysége.
- Inhomogén esetben integrál.


<!-- eredeti
## 2. rész

### 1. Biot-Savart-törvény, egyenes és körvezető mágneses terének iránya
-->
# Második rész, első tétel. {{Biot|bió}}-{{Savart|szavár}}-törvény, egyenes és körvezető mágneses terének iránya

<!-- eredeti
| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| H | mágneses térerősség | A/m |
| B | mágneses indukció (B = μH) | T = Vs/m² |
| μ = μ₀μᵣ | permeabilitás (μ₀ = 4π·10⁻⁷) | Vs/(Am) |
| j | áramsűrűség | A/m² |
| I | áramerősség | A |
| ds | a vezető egy kis darabja (az áram irányába mutat) | m |
| r | vektor a vizsgált pontból az áramelemhez; r a hossza | m |
| dV | térfogatelem | m³ |
| R | a körvezető (karika) sugara | m |
| z | távolság a karika középpontjától a tengely mentén | m |
| m | a karika mágneses momentuma (IR²π) | Am² |
-->
## Jelölések

- A H jel a mágneses térerősséget jelenti, mértékegysége az amper per méter.
- A B jel a mágneses indukciót jelenti, amely egyenlő mű szorozva há; mértékegysége a tesla, ami egyenlő volt szekundum per négyzetméter. [[pause 500]]
- A mű jel, amely egyenlő mű nulla szorozva mű er, a permeabilitást jelenti, ahol mű nulla egyenlő négy pí szorozva tíz a mínusz hetediken; mértékegysége a volt szekundum per amper méter. [[pause 500]]
- A j jel az áramsűrűséget jelenti, mértékegysége az amper per négyzetméter.
- Az I jel az áramerősséget jelenti, mértékegysége az amper.
- A dé es jel a vezető egy kis darabját jelenti (az áram irányába mutat), mértékegysége a méter.
- A kis r jel a vizsgált pontból az áramelemhez mutató vektort jelenti, kis er pedig a hossza; mértékegysége a méter.
- A dé V jel a térfogatelemet jelenti, mértékegysége a köbméter.
- A nagy R jel a körvezető (karika) sugarát jelenti, mértékegysége a méter.
- A z jel a karika középpontjától a tengely mentén mért távolságot jelenti, mértékegysége a méter.
- Az m jel a karika mágneses momentumát jelenti, amely egyenlő í szorozva nagy er négyzet szorozva pí; mértékegysége az amper négyzetméter. [[pause 500]]

<!-- eredeti
**Miről szól?** Megmondja, hogy egy áramjárta vezető egy adott pontban mekkora és milyen irányú mágneses teret kelt. A vezetőt kis darabokra bontjuk, minden darab hozzájárul a térhez (a távolság négyzetével csökkenően), és ezeket összeadjuk. Az irányt egy vektoriális szorzat adja, ezért a tér mindig merőleges az áramra és a távolság-vektorra is: körbeöleli a vezetőt.
-->
## Miről szól

Megmondja, hogy egy áramjárta vezető egy adott pontban mekkora és milyen irányú mágneses teret kelt. A vezetőt kis darabokra bontjuk, minden darab hozzájárul a térhez (a távolság négyzetével csökkenően), és ezeket összeadjuk. Az irányt egy vektoriális szorzat adja, ezért a tér mindig merőleges az áramra és a távolság-vektorra is: körbeöleli a vezetőt.

<!-- eredeti
**A törvény** (eredetileg mérésből, 1820; a vektorpotenciálos levezetés nem kell):

```latex
\vec B = \frac{\mu}{4\pi}\int\frac{\vec r\times\vec j}{r^3}\,dV \qquad \vec H = \frac{1}{4\pi}\int\frac{\vec r\times\vec j}{r^3}\,dV
```
-->
## A törvény

Eredetileg mérésből származik, ezernyolcszázhúszból; a vektorpotenciálos levezetés nem kell.

A B mágneses indukció vektora egyenlő mű per négy pí, szorozva a következő térfogati integrállal: egy tört, a számláló a kis r vektor vektoriálisan szorozva a j áramsűrűség vektorával, a nevező kis er köb, szorozva dé vé. [[pause 500]]

A H mágneses térerősség vektora egyenlő egy per négy pí, szorozva ugyanezzel az integrállal: egy tört, a számláló kis er vektor vektoriálisan szorozva jé vektor, a nevező kis er köb, szorozva dé vé. [[pause 500]]

<!-- eredeti
Vékony vezetőnél j·dV helyett I·ds írható (j dV = jA ds = I ds), és a vezető teljes hosszára integrálunk:
-->
Vékony vezetőnél jé szorozva dé vé helyett í szorozva dé es írható, mert jé dé vé egyenlő jé szorozva á szorozva dé es, ami egyenlő í dé es, és a vezető teljes hosszára integrálunk. [[pause 500]]

<!-- eredeti
```latex
\vec H = \frac{I}{4\pi}\int\frac{\vec r\times d\vec s}{r^3}
```
-->
Há vektor egyenlő í per négy pí, szorozva integrál, egy tört, a számláló kis er vektor vektoriálisan szorozva dé es vektor, a nevező kis er köb. [[pause 500]]

<!-- eredeti
**Egyenes vezető terének iránya.** Ha az áram felfelé folyik és a pont a vezetőtől jobbra van, minden kis darab tere a lapba befelé mutat, tehát az összeg is. Az erővonalak a vezető körüli koncentrikus körök. **Jobbkéz-szabály:** hüvelykujj az áram irányába, a behajlított ujjak mutatják H körüljárását.
-->
## Egyenes vezető terének iránya

Ha az áram felfelé folyik és a pont a vezetőtől jobbra van, minden kis darab tere a lapba befelé mutat, tehát az összeg is. Az erővonalak a vezető körüli koncentrikus körök. Jobbkéz-szabály: hüvelykujj az áram irányába, a behajlított ujjak mutatják há körüljárását.

<!-- eredeti
**Körvezető tere a tengelyén.** A karika minden darabja ugyanolyan távol van a tengely egy pontjától (r), és r merőleges ds-re, így |r × ds| = r ds. Az egyes darabok terének a tengelyre merőleges részei páronként kioltják egymást, csak a tengely irányú rész marad (szorzó: cos α = R/r). Az integrál a kerület, 2πR:
-->
## Körvezető tere a tengelyén

A karika minden darabja ugyanolyan távol van a tengely egy pontjától (ez a távolság kis er), és kis er merőleges dé es-re, így a kis er vektor vektoriálisan szorozva dé es vektor abszolút értéke egyenlő kis er szorozva dé es. [[pause 500]]
Az egyes darabok terének a tengelyre merőleges részei páronként kioltják egymást, csak a tengely irányú rész marad; a szorzó: koszinusz alfa egyenlő nagy er per kis er. [[pause 500]]
Az integrál a kerület, kettő pí nagy er. [[pause 500]]

<!-- eredeti
```latex
H = \frac{Ir}{4\pi r^3}\cdot\frac{R}{r}\cdot 2\pi R = \frac{IR^2}{2r^3} = \frac{IR^2}{2\left(R^2+z^2\right)^{3/2}}
```
-->
Há egyenlő egy tört, a számláló í szorozva kis er, a nevező négy pí szorozva kis er köb; ezt szorozzuk nagy er per kis er-rel, és kettő pí nagy er-rel. [[pause 500]]
Ez egyenlő í szorozva nagy er négyzet per, zárójelben kettő szorozva kis er köb. [[pause 500]]
Ez pedig egyenlő egy tört, a számláló í szorozva nagy er négyzet, a nevező kettő szorozva a nagy er négyzet plusz zé négyzet összegének háromketted hatványa. [[pause 500]]

<!-- eredeti
A karika közepén (z = 0) H = I/(2R); messze 1/z³ szerint csökken (mint az elektromos dipólusé). Iránya a tengely mentén: ujjak az áram körüljárásának irányába, a hüvelykujj mutatja H-t.
-->
A karika közepén, ahol zé egyenlő nulla, há egyenlő í per, zárójelben kettő szorozva nagy er. [[pause 500]]
Messze egy per zé köb szerint csökken (mint az elektromos dipólusé). [[pause 500]]
Iránya a tengely mentén: ujjak az áram körüljárásának irányába, a hüvelykujj mutatja há-t.

<!-- eredeti
**Vizsgán:** a törvény (B, H, vékony vezető), mit jelent r; egyenes vezető: koncentrikus körök, jobbkéz-szabály; körvezető a tengelyen, középpontban I/(2R).
-->
## Amit a vizsgán le kell írni

A törvény (bé, há, vékony vezető), mit jelent kis er; egyenes vezető: koncentrikus körök, jobbkéz-szabály; körvezető a tengelyen, középpontban há egyenlő í per, zárójelben kettő nagy er. [[pause 500]]

<!-- eredeti
### 2. Ampère-féle gerjesztési törvény. Végtelen egyenes vezető tere
-->
# Második rész, második tétel. {{Ampère|amper}}-féle gerjesztési törvény. Végtelen egyenes vezető tere

<!-- eredeti
| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| H | mágneses térerősség | A/m |
| g, ds | zárt görbe, ívelem | m |
| Iⱼ | a görbe által körülzárt áramok | A |
| j | áramsűrűség | A/m² |
| r | távolság a vezetőtől | m |
-->
## Jelölések

- A H jel a mágneses térerősséget jelenti, mértékegysége az amper per méter.
- A g és a dé es jel a zárt görbét, illetve az ívelemet jelenti, mértékegységük a méter.
- Az I jé jel a görbe által körülzárt áramokat jelenti, mértékegysége az amper.
- A j jel az áramsűrűséget jelenti, mértékegysége az amper per négyzetméter.
- Az r jel a vezetőtől mért távolságot jelenti, mértékegysége a méter.

<!-- eredeti
**Miről szól?** Ha egy zárt görbe mentén összeadjuk, mennyire „sodor” a mágneses tér a görbe irányába, az pont annyi, amennyi áram átfolyik a görbén. Ha a szimmetria miatt a tér a görbe mentén mindenhol egyforma, ebből egyből kijön a tér nagysága (mint a Gauss-törvénynél az elektromos térre).
-->
## Miről szól

Ha egy zárt görbe mentén összeadjuk, mennyire „sodor” a mágneses tér a görbe irányába, az pont annyi, amennyi áram átfolyik a görbén. Ha a szimmetria miatt a tér a görbe mentén mindenhol egyforma, ebből egyből kijön a tér nagysága (mint a {{Gauss|gausz}}-törvénynél az elektromos térre).

<!-- eredeti
**A törvény:**

```latex
\oint_g\vec H\,d\vec s = \sum_j I_j \qquad \operatorname{rot}\vec H = \vec j
```
-->
## A törvény

A H mágneses térerősség vektorának zárt görbe menti integrálja a g görbén, dé es vektor szerint, egyenlő a körülzárt I jé áramok összegével, vagyis szumma jé szerint í jé. [[pause 500]]
Differenciális alakban: rotáció há vektor egyenlő a j áramsűrűség vektorával. [[pause 500]]

<!-- eredeti
Előjel: az a pozitív áram, amelyik a felület normálisának irányában megy át; a görbe körüljárási irányát és a normálist a jobbcsavar-szabály kapcsolja össze. Mágnesezhető anyag jelenlétében is érvényes. A differenciális alak szerint az áram körüli mágneses tér örvényes. Az áramba nemcsak a vezetési (fémben folyó) áram számít, hanem a konvektív is (pl. vákuumban repülő ionok). Időben változó esetben a teljes alak az 1. Maxwell-egyenlet (+ eltolási áram).
-->
Előjel: az a pozitív áram, amelyik a felület normálisának irányában megy át; a görbe körüljárási irányát és a normálist a jobbcsavar-szabály kapcsolja össze. Mágnesezhető anyag jelenlétében is érvényes. A differenciális alak szerint az áram körüli mágneses tér örvényes. Az áramba nemcsak a vezetési (fémben folyó) áram számít, hanem a konvektív is (például vákuumban repülő ionok). Időben változó esetben a teljes alak az első {{Maxwell|mekszvel}}-egyenlet (plusz eltolási áram).

<!-- eredeti
**Végtelen egyenes vezető.** Szimmetria miatt H csak a távolságtól függ, és a vezető körüli körök mentén érintő irányú. Görbének egy r sugarú kört választunk: ezen H állandó, és párhuzamos az ívelemmel, így kiemelhető; a kör hossza 2rπ.
-->
## Végtelen egyenes vezető

Szimmetria miatt há csak a távolságtól függ, és a vezető körüli körök mentén érintő irányú. Görbének egy er sugarú kört választunk: ezen há állandó, és párhuzamos az ívelemmel, így kiemelhető; a kör hossza kettő er pí. [[pause 500]]

<!-- eredeti
```latex
\oint_g\vec H\,d\vec s = H\oint_g ds = H\cdot 2r\pi = I \;\Rightarrow\; H = \frac{I}{2r\pi}
```
-->
Há vektor zárt görbe menti integrálja dé es vektor szerint egyenlő há szorozva dé es zárt görbe menti integráljával, ez egyenlő há szorozva kettő er pí, és ez egyenlő í. [[pause 500]]
Ebből há egyenlő í per, zárójelben kettő er pí. [[pause 500]]

<!-- eredeti
A tér a távolsággal fordítottan arányos.
-->
A tér a távolsággal fordítottan arányos.

<!-- eredeti
**Vizsgán:** ∮H ds = ΣI, előjelezés, jobbcsavar; rot H = j; konvektív áram is számít; egyenes vezető: szimmetria, kör, H = I/(2rπ).
-->
## Amit a vizsgán le kell írni

Há zárt görbe menti integrálja dé es szerint egyenlő szumma í; előjelezés, jobbcsavar; rotáció há egyenlő jé; konvektív áram is számít; egyenes vezető: szimmetria, kör, há egyenlő í per, zárójelben kettő er pí. [[pause 500]]

<!-- eredeti
### 3. Szolenoid és toroid mágneses terének közelítő meghatározása
-->
# Második rész, harmadik tétel. Szolenoid és toroid mágneses terének közelítő meghatározása

<!-- eredeti
| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| N | menetszám | nincs |
| ℓ | a tekercs hossza | m |
| N/ℓ | egységnyi hosszra jutó menetszám | 1/m |
| I | a tekercs árama | A |
| A | a tekercs keresztmetszete | m² |
| x | az integrálási téglalap tekercsen belüli oldalának hossza | m |
| H, B | mágneses térerősség, indukció a tekercsben | A/m, T |
| μ | a tekercs belsejének permeabilitása | Vs/(Am) |
| r | a toroid középvonalának sugara | m |
| R | (vastag) tekercs sugara | m |
-->
## Jelölések

- Az N jel a menetszámot jelenti, mértékegység nélküli.
- Az el jel a tekercs hosszát jelenti, mértékegysége a méter.
- Az en per el hányados az egységnyi hosszra jutó menetszámot jelenti, mértékegysége az egy per méter. [[pause 500]]
- Az I jel a tekercs áramát jelenti, mértékegysége az amper.
- Az A jel a tekercs keresztmetszetét jelenti, mértékegysége a négyzetméter.
- Az x jel az integrálási téglalap tekercsen belüli oldalának hosszát jelenti, mértékegysége a méter.
- A H és a B jel a mágneses térerősséget, illetve az indukciót jelenti a tekercsben, mértékegységük az amper per méter, illetve a tesla.
- A mű jel a tekercs belsejének permeabilitását jelenti, mértékegysége a volt szekundum per amper méter.
- A kis r jel a toroid középvonalának sugarát jelenti, mértékegysége a méter.
- A nagy R jel a (vastag) tekercs sugarát jelenti, mértékegysége a méter.

<!-- eredeti
**Miről szól?** A hosszú, sűrűn tekercselt egyenes tekercs (szolenoid) belsejében a tér közel egyenletes, kívül pedig nagyon gyenge, mert a vonalak egy hatalmas térrészben oszlanak szét. Ezért a gerjesztési törvény egyszerű lesz: csak a tekercs belsején átmenő szakasz számít. A toroid egy körré hajlított szolenoid.
-->
## Miről szól

A hosszú, sűrűn tekercselt egyenes tekercs (szolenoid) belsejében a tér közel egyenletes, kívül pedig nagyon gyenge, mert a vonalak egy hatalmas térrészben oszlanak szét. Ezért a gerjesztési törvény egyszerű lesz: csak a tekercs belsején átmenő szakasz számít. A toroid egy körré hajlított szolenoid.

<!-- eredeti
**Szolenoid.** Egy ABCD téglalapra írjuk fel a gerjesztési törvényt: AB (hossza x) a tekercs belsejében, a tengellyel párhuzamos; DC kint; AD és BC keresztben.
-->
## Szolenoid

Egy á bé cé dé téglalapra írjuk fel a gerjesztési törvényt: az á bé oldal (hossza iksz) a tekercs belsejében, a tengellyel párhuzamos; a dé cé oldal kint; az á dé és a bé cé oldal keresztben.

<!-- eredeti
- DC: kint a tér elhanyagolható, ez a tag 0.
- AD és BC: a tér merőleges a görbére (ellentétes irányúak is), ezek kiesnek.
- AB: a tér egyenletes és párhuzamos, az integrál Hx.
- A körülzárt áram: az x hosszon lévő Nx/ℓ menet, mindegyikben I.
-->
- Dé cé: kint a tér elhanyagolható, ez a tag nulla.
- Á dé és bé cé: a tér merőleges a görbére (ellentétes irányúak is), ezek kiesnek.
- Á bé: a tér egyenletes és párhuzamos, az integrál há szorozva iksz. [[pause 500]]
- A körülzárt áram: az iksz hosszon lévő en szorozva iksz per el menet, mindegyikben í. [[pause 500]]

<!-- eredeti
```latex
Hx = \frac{Nx}{\ell}I \;\Rightarrow\; H = \frac{NI}{\ell}, \qquad B = \mu\frac{NI}{\ell}
```
-->
Há szorozva iksz egyenlő en szorozva iksz per el, szorozva í. [[pause 500]]
Ebből a H mágneses térerősség: há egyenlő en szorozva í per el. [[pause 500]]
A B indukció pedig: bé egyenlő mű szorozva en í per el. [[pause 500]]

<!-- eredeti
Akkor jó, ha a tekercs sokkal hosszabb, mint az átmérője, és bent-kint hasonló a permeabilitás. Vastag tekercs közepén: H = NI/√(4R² + ℓ²), ebből R → 0-ra visszakapjuk NI/ℓ-t, ℓ → 0-ra a karika NI/(2R)-jét.
-->
Akkor jó, ha a tekercs sokkal hosszabb, mint az átmérője, és bent-kint hasonló a permeabilitás. Vastag tekercs közepén: há egyenlő en szorozva í per négyzetgyök, zárójelben négy nagy er négyzet plusz el négyzet. [[pause 500]]
Ebből, ha nagy er tart nullához, visszakapjuk az en í per el értéket, ha pedig el tart nullához, a karika en í per, zárójelben kettő nagy er értékét. [[pause 500]]

<!-- eredeti
**Toroid.** A görbe a toroid középvonalában, egy r sugarú körön fut, végig a tekercsen belül. Hossza 2πr, és mind az N menetet körülveszi:
-->
## Toroid

A görbe a toroid középvonalában, egy kis er sugarú körön fut, végig a tekercsen belül. Hossza kettő pí kis er, és mind az en menetet körülveszi. [[pause 500]]

<!-- eredeti
```latex
H\cdot 2\pi r = NI \;\Rightarrow\; H = \frac{NI}{2\pi r}
```
-->
Há szorozva kettő pí kis er egyenlő en szorozva í. [[pause 500]]
Ebből há egyenlő en í per, zárójelben kettő pí kis er. [[pause 500]]

<!-- eredeti
Itt nincs „kint elhanyagoljuk” hiba, viszont vastag toroidnál a tér nem egyenletes (r függő); vékony toroidra egzakt.
-->
Itt nincs „kint elhanyagoljuk” hiba, viszont vastag toroidnál a tér nem egyenletes (kis er függő); vékony toroidra egzakt.

<!-- eredeti
**Vizsgán:** rajz az ABCD görbével; a négy szakasz indoklása; H = NI/ℓ, B = μNI/ℓ és a feltétel; toroid: kör a középvonalban, H = NI/(2πr).
-->
## Amit a vizsgán le kell írni

Rajz az á bé cé dé görbével; a négy szakasz indoklása; há egyenlő en í per el, bé egyenlő mű en í per el és a feltétel; toroid: kör a középvonalban, há egyenlő en í per, zárójelben kettő pí kis er. [[pause 500]]

<!-- eredeti
### 4. Ampère-erő, Lorentz-erő. Sebességszűrő, ciklotron
-->
# Második rész, negyedik tétel. {{Ampère|amper}}-erő, {{Lorentz|lorenc}}-erő. Sebességszűrő, ciklotron

<!-- eredeti
| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| F | erő | N |
| I | áram a vezetőben | A |
| ℓ | a vezető hossza (vektor: az áram irányába) | m |
| B | mágneses indukció | T = Vs/m² |
| q, Q | a részecske töltése | C |
| v | a részecske sebessége | m/s |
| N | részecskék száma | nincs |
| E | elektromos térerősség | V/m |
| m | a részecske tömege | kg |
| r | körpálya sugara | m |
| T | egy kör ideje (periódusidő) | s |
-->
## Jelölések

- Az F jel az erőt jelenti, mértékegysége a {{newton|nyúton}}.
- Az I jel a vezetőben folyó áramot jelenti, mértékegysége az amper.
- Az el jel a vezető hosszát jelenti (vektorként az áram irányába mutat), mértékegysége a méter.
- A B jel a mágneses indukciót jelenti, mértékegysége a tesla, ami egyenlő volt szekundum per négyzetméter. [[pause 500]]
- A kis q és a nagy Q jel a részecske töltését jelenti, mértékegysége a {{coulomb|kulomb}}.
- A v jel a részecske sebességét jelenti, mértékegysége a méter per szekundum.
- Az N jel a részecskék számát jelenti, mértékegység nélküli.
- Az E jel az elektromos térerősséget jelenti, mértékegysége a volt per méter.
- Az m jel a részecske tömegét jelenti, mértékegysége a kilogramm.
- Az r jel a körpálya sugarát jelenti, mértékegysége a méter.
- A nagy T jel egy kör idejét (periódusidő) jelenti, mértékegysége a másodperc.

<!-- eredeti
**Miről szól?** Mágneses térben az áramjárta vezetőre erő hat (Ampère-erő). Mivel az áram mozgó töltések sokasága, ez tulajdonképpen az egyes mozgó töltésekre ható erők összege (Lorentz-erő). Ez az erő mindig merőleges a sebességre, ezért nem gyorsítja, csak eltéríti a részecskét, körpályára kényszeríti. Ezt használja a sebességszűrő és a ciklotron.
-->
## Miről szól

Mágneses térben az áramjárta vezetőre erő hat ({{Ampère|amper}}-erő). Mivel az áram mozgó töltések sokasága, ez tulajdonképpen az egyes mozgó töltésekre ható erők összege ({{Lorentz|lorenc}}-erő). Ez az erő mindig merőleges a sebességre, ezért nem gyorsítja, csak eltéríti a részecskét, körpályára kényszeríti. Ezt használja a sebességszűrő és a ciklotron.

<!-- eredeti
**Ampère-erő** (egyenes vezető, homogén tér; másképp kis darabokra bontva és összegezve):

```latex
\vec F = I\vec\ell\times\vec B \qquad \vec F = I\int d\vec r\times\vec B
```
-->
## {{Ampère|amper}}-erő

Egyenes vezető és homogén tér esetén, illetve másképp, kis darabokra bontva és összegezve:

Az F erő vektora egyenlő í szorozva el vektor, vektoriálisan szorozva a B mágneses indukció vektorával. [[pause 500]]
Kis darabokra bontva ef vektor egyenlő í szorozva integrál dé er vektor vektoriálisan szorozva bé vektor. [[pause 500]]

<!-- eredeti
**Lorentz-erő levezetése.** Legyen a vezetőben N db q töltésű részecske, mindegyik v sebességgel; Δt idő alatt teszik meg az ℓ hosszat. Ekkor I = Nq/Δt és v = ℓ/Δt, így:
-->
## {{Lorentz|lorenc}}-erő levezetése

Legyen a vezetőben en darab kis kú töltésű részecske, mindegyik vé sebességgel; delta té idő alatt teszik meg az el hosszat. Ekkor í egyenlő en szorozva kis kú per delta té, és vé egyenlő el per delta té, így: [[pause 500]]

<!-- eredeti
```latex
F = BI\ell = BNq\frac{\ell}{\Delta t} = BNqv \;\Rightarrow\; \text{egy részecskére: } F = qvB, \qquad \vec F = q\,\vec v\times\vec B
```
-->
Ef egyenlő bé í el, ami egyenlő bé en kis kú szorozva el per delta té, ami egyenlő bé en kis kú vé. [[pause 500]]
Ebből egy részecskére: ef egyenlő kis kú vé bé. [[pause 500]]
Vektorosan: ef vektor egyenlő kis kú szorozva vé vektor vektoriálisan szorozva bé vektor. [[pause 500]]

<!-- eredeti
A Lorentz-erő munkája a szabad töltésen mindig 0, mert merőleges a sebességre.
-->
A {{Lorentz|lorenc}}-erő munkája a szabad töltésen mindig nulla, mert merőleges a sebességre.

<!-- eredeti
**Sebességszűrő.** Egymásra és a sebességre is merőleges E és B tér; az elektromos erő (qE) és a Lorentz-erő (qvB) ellentétes irányú. Csak az a részecske megy át eltérülés nélkül, amelyiknél a kettő kiegyenlíti egymást:
-->
## Sebességszűrő

Egymásra és a sebességre is merőleges é és bé tér; az elektromos erő (kis kú szorozva é) és a {{Lorentz|lorenc}}-erő (kis kú vé bé) ellentétes irányú. Csak az a részecske megy át eltérülés nélkül, amelyiknél a kettő kiegyenlíti egymást:

<!-- eredeti
```latex
qE = qvB \;\Rightarrow\; v = \frac{E}{B}
```
-->
Kis kú szorozva é egyenlő kis kú szorozva vé bé, ebből vé egyenlő é per bé. [[pause 500]]

<!-- eredeti
A töltés kiesik: töltéstől függetlenül ugyanazt a sebességet választja ki.
-->
A töltés kiesik: töltéstől függetlenül ugyanazt a sebességet választja ki.

<!-- eredeti
**Ciklotron.** Részecskegyorsító: a két D alakú „duáns” között váltakozó feszültség gyorsítja a részecskét, a homogén mágneses tér körpályán tartja. A körmozgáshoz kellő centripetális erőt a Lorentz-erő adja:
-->
## Ciklotron

Részecskegyorsító: a két dé alakú „duáns” között váltakozó feszültség gyorsítja a részecskét, a homogén mágneses tér körpályán tartja. A körmozgáshoz kellő centripetális erőt a {{Lorentz|lorenc}}-erő adja:

<!-- eredeti
```latex
QvB = m\frac{v^2}{r} \;\Rightarrow\; r = \frac{mv}{QB}, \qquad T = \frac{2r\pi}{v} = \frac{2\pi m}{QB}
```
-->
Nagy kú vé bé egyenlő em szorozva vé négyzet per er. [[pause 500]]
Ebből er egyenlő em vé per, zárójelben nagy kú bé. [[pause 500]]
A periódusidő: nagy té egyenlő kettő er pí per vé, ami egyenlő kettő pí em per, zárójelben nagy kú bé. [[pause 500]]

<!-- eredeti
Ahogy gyorsul, egyre nagyobb körön halad. A lényeg: **T nem függ a sebességtől**, ezért állandó frekvenciájú feszültség mindig jókor gyorsít (nemrelativisztikus esetben). Használat: orvosi radioizotópok, anyagvizsgálat, magfizika.
-->
Ahogy gyorsul, egyre nagyobb körön halad. A lényeg: nagy té nem függ a sebességtől, ezért állandó frekvenciájú feszültség mindig jókor gyorsít (nemrelativisztikus esetben). Használat: orvosi radioizotópok, anyagvizsgálat, magfizika.

<!-- eredeti
**Vizsgán:** F = Iℓ × B; Lorentz-erő levezetése az Ampère-erőből; F = qv × B, munkája 0; sebességszűrő v = E/B; ciklotron r és T, és miért fontos, hogy T nem függ v-től.
-->
## Amit a vizsgán le kell írni

Ef egyenlő í el vektoriálisan szorozva bé; {{Lorentz|lorenc}}-erő levezetése az {{Ampère|amper}}-erőből; ef egyenlő kis kú vé vektoriálisan szorozva bé, munkája nulla; sebességszűrő: vé egyenlő é per bé; ciklotron er és nagy té, és miért fontos, hogy nagy té nem függ vé-től. [[pause 500]]

<!-- eredeti
### 5. Áramjárta hurokra ható forgatónyomaték homogén térben. Mágneses dipólmomentum
-->
# Második rész, ötödik tétel. Áramjárta hurokra ható forgatónyomaték homogén térben. Mágneses dipólmomentum

<!-- eredeti
| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| I | áram a hurokban | A |
| a, b | a téglalap alakú hurok oldalai | m |
| A | a hurok területe (ab); vektorként a felületre merőleges | m² |
| B | mágneses indukció | T |
| F | egy oldalra ható erő | N |
| M | forgatónyomaték | N·m |
| m | mágneses dipólmomentum (m = IA) | Am² |
| Eₚ | helyzeti energia | J |
-->
## Jelölések

- Az I jel a hurokban folyó áramot jelenti, mértékegysége az amper.
- A kis a és a kis b jel a téglalap alakú hurok oldalait jelenti, mértékegységük a méter.
- A nagy A jel a hurok területét jelenti, amely egyenlő kis á szorozva kis bé; vektorként a felületre merőleges; mértékegysége a négyzetméter. [[pause 500]]
- A nagy B jel a mágneses indukciót jelenti, mértékegysége a tesla.
- Az F jel az egy oldalra ható erőt jelenti, mértékegysége a {{newton|nyúton}}.
- A nagy M jel a forgatónyomatékot jelenti, mértékegysége a {{newton|nyúton}}méter.
- A kis m jel a mágneses dipólmomentumot jelenti, amely egyenlő í szorozva nagy á; mértékegysége az amper négyzetméter. [[pause 500]]
- Az E pé jel a helyzeti energiát jelenti, mértékegysége a {{joule|dzsúl}}.

<!-- eredeti
**Miről szól?** Egy zárt áramhurokra egyenletes mágneses térben az oldalakra ható erők kioltják egymást, így nem mozdul el, de forgatónyomaték hat rá: befordul, mint egy iránytű. Ezért a hurokhoz (és minden kis mágneshez) egy vektort, a mágneses momentumot rendeljük, ami az elektromos dipólmomentum párja.
-->
## Miről szól

Egy zárt áramhurokra egyenletes mágneses térben az oldalakra ható erők kioltják egymást, így nem mozdul el, de forgatónyomaték hat rá: befordul, mint egy iránytű. Ezért a hurokhoz (és minden kis mágneshez) egy vektort, a mágneses momentumot rendeljük, ami az elektromos dipólmomentum párja.

<!-- eredeti
**Téglalap hurok.** Legyen B párhuzamos a b oldallal. A b oldalakra nem hat erő (párhuzamosak B-vel), a két a oldalra egyenként F = BIa hat, ellentétes irányban: eredő erő 0. A középponton átmenő tengelyre mindkettő ugyanarra forgat, karjuk b/2:
-->
## Téglalap hurok

Legyen nagy bé párhuzamos a kis bé oldallal. A kis bé oldalakra nem hat erő (párhuzamosak nagy bé-vel), a két kis á oldalra egyenként ef egyenlő nagy bé szorozva í szorozva kis á hat, ellentétes irányban: eredő erő nulla. [[pause 500]]
A középponton átmenő tengelyre mindkettő ugyanarra forgat, karjuk kis bé per kettő. [[pause 500]]

<!-- eredeti
```latex
M = 2\cdot BIa\cdot\frac b2 = BIab = BIA
```
-->
Az M forgatónyomaték: nagy em egyenlő kettő szorozva nagy bé í kis á, szorozva kis bé per kettő, ami egyenlő nagy bé í kis á kis bé, vagyis nagy bé í nagy á. [[pause 500]]

<!-- eredeti
Általánosan: homogén térben zárt hurokra nincs eredő erő, a nyomaték pedig nem függ a hurok alakjától:
-->
Általánosan: homogén térben zárt hurokra nincs eredő erő, a nyomaték pedig nem függ a hurok alakjától:

<!-- eredeti
```latex
\vec M = I\vec A\times\vec B
```
-->
Nagy em vektor egyenlő í szorozva nagy á vektor, vektoriálisan szorozva nagy bé vektor. [[pause 500]]

<!-- eredeti
Az A felületvektor irányát az áram körüljárásából a jobbcsavar-szabály adja.
-->
A nagy á felületvektor irányát az áram körüljárásából a jobbcsavar-szabály adja.

<!-- eredeti
**Mágneses dipólmomentum.** Az elektromos p = Qℓ analógiájára:
-->
## Mágneses dipólmomentum

Az elektromos pé egyenlő nagy kú szorozva el analógiájára: [[pause 500]]

<!-- eredeti
```latex
\vec m = I\vec A \qquad \vec M = \vec m\times\vec B \qquad E_p = -\vec m\vec B
```
-->
A kis m mágneses dipólmomentum vektora egyenlő í szorozva nagy á vektor. [[pause 500]]
Nagy em vektor egyenlő kis em vektor vektoriálisan szorozva nagy bé vektor. [[pause 500]]
É pé egyenlő mínusz kis em vektor skalárszorzat nagy bé vektor. [[pause 500]]

<!-- eredeti
Az m vektor hegye az északi, talpa a déli pólus (délről észak felé mutat). Az M = m × B állandó mágnesre (pl. mágnestűre) is érvényes. A nyomaték akkor szűnik meg, ha m ∥ B: a momentum befordul a tér irányába, mert ott minimális az energia. Ezért egy kis áramhurok iránytűként viselkedik. (Eₚ = −m·B a Zeeman-energia.)
-->
A kis em vektor hegye az északi, talpa a déli pólus (délről észak felé mutat). A nagy em egyenlő kis em vektoriálisan szorozva nagy bé összefüggés állandó mágnesre (például mágnestűre) is érvényes. [[pause 500]]
A nyomaték akkor szűnik meg, ha kis em párhuzamos nagy bé-vel: a momentum befordul a tér irányába, mert ott minimális az energia. [[pause 500]]
Ezért egy kis áramhurok iránytűként viselkedik. (Az é pé egyenlő mínusz kis em skalárszorzat nagy bé kifejezés a {{Zeeman|zéman}}-energia.) [[pause 500]]

<!-- eredeti
**Vizsgán:** téglalap hurok rajzzal, erők, eredő erő 0; M = BIA levezetve; M = IA × B; m = IA, egysége, északi-déli pólus; M = m × B; Eₚ = −m·B.
-->
## Amit a vizsgán le kell írni

Téglalap hurok rajzzal, erők, eredő erő nulla; nagy em egyenlő nagy bé í nagy á levezetve; nagy em egyenlő í nagy á vektoriálisan szorozva nagy bé; kis em egyenlő í nagy á, egysége, északi-déli pólus; nagy em egyenlő kis em vektoriálisan szorozva nagy bé; é pé egyenlő mínusz kis em skalárszorzat nagy bé. [[pause 500]]

<!-- eredeti
### 6. Inhomogén mágneses tér (vázlatosan). Mágnesek vonzása és taszítása
-->
# Második rész, hatodik tétel. Inhomogén mágneses tér (vázlatosan). Mágnesek vonzása és taszítása

<!-- eredeti
| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| B, ΔB | mágneses indukció, és mennyivel nagyobb a hurok egyik oldalán | T |
| F, ΔF | erő, erőkülönbség | N |
| I | áram a hurokban | A |
| a, b | a hurok oldalai | m |
| m | mágneses momentum | Am² |
| Eₚ | helyzeti energia | J |
-->
## Jelölések

- A nagy B és a delta nagy B jel a mágneses indukciót jelenti, illetve azt, hogy mennyivel nagyobb a hurok egyik oldalán; mértékegységük a tesla.
- Az F és a delta F jel az erőt, illetve az erőkülönbséget jelenti, mértékegységük a {{newton|nyúton}}.
- Az I jel a hurokban folyó áramot jelenti, mértékegysége az amper.
- A kis a és a kis b jel a hurok oldalait jelenti, mértékegységük a méter.
- Az m jel a mágneses momentumot jelenti, mértékegysége az amper négyzetméter.
- Az E pé jel a helyzeti energiát jelenti, mértékegysége a {{joule|dzsúl}}.

<!-- eredeti
**Miről szól?** Ha a tér nem egyenletes, a hurok egyik oldalára nagyobb erő hat, mint a másikra, így marad egy eredő erő: a hurok (vagy mágnes) mozdulni kezd. Ezzel magyarázható, miért vonzza vagy taszítja egymást két mágnes. Ugyanez a helyzet, mint az elektromos dipólusnál: homogén térben csak forgatónyomaték, inhomogénben erő is.
-->
## Miről szól

Ha a tér nem egyenletes, a hurok egyik oldalára nagyobb erő hat, mint a másikra, így marad egy eredő erő: a hurok (vagy mágnes) mozdulni kezd. Ezzel magyarázható, miért vonzza vagy taszítja egymást két mágnes. Ugyanez a helyzet, mint az elektromos dipólusnál: homogén térben csak forgatónyomaték, inhomogénben erő is.

<!-- eredeti
**Téglalap hurok.** Ugyanaz, mint az 5. tételben, de a jobb oldalon az indukció B + ΔB. Ott az erő F + ΔF, így az eredő (m = abI felhasználásával):
-->
## Téglalap hurok

Ugyanaz, mint az ötödik tételben, de a jobb oldalon az indukció nagy bé plusz delta nagy bé. Ott az erő ef plusz delta ef, így az eredő, felhasználva, hogy em egyenlő kis á szorozva kis bé szorozva í: [[pause 500]]

<!-- eredeti
```latex
\sum F = \Delta F = Ia\,\Delta B = m\frac{\Delta B}{b}
```
-->
Az erők összege egyenlő delta ef, ami egyenlő í szorozva kis á szorozva delta nagy bé, ami egyenlő em szorozva delta nagy bé per kis bé. [[pause 500]]

<!-- eredeti
Az erő a momentummal és a tér változásának meredekségével (gradiensével) arányos. Általános hurokra az Ampère-erőt kell végigintegrálni (F = I∮dr × B), egyszerű pontos képlet nincs. Kis hurokra a közelítés:
-->
Az erő a momentummal és a tér változásának meredekségével (gradiensével) arányos. Általános hurokra az {{Ampère|amper}}-erőt kell végigintegrálni, vagyis ef egyenlő í szorozva zárt görbe menti integrál dé er vektoriálisan szorozva nagy bé; egyszerű pontos képlet nincs. [[pause 500]]
Kis hurokra a közelítés:

<!-- eredeti
```latex
\vec F = \operatorname{grad}\left(\vec m\vec B\right) = -\operatorname{grad}E_p
```
-->
Ef vektor egyenlő gradiens, zárójelben em vektor skalárszorzat nagy bé vektor, ami egyenlő mínusz gradiens é pé. [[pause 500]]

<!-- eredeti
**Vonzás és taszítás.** Egy kör alakú hurok alatt, szimmetrikusan áll egy rúdmágnes, északi pólusa felfelé. A mágnes B vonalai a hurok minden kis darabjánál ferdén, kifelé-felfelé mutatnak. Az egyes darabokra ható Ampère-erők kifelé-lefelé mutatnak; a vízszintes részeik a szimmetria miatt kioltják egymást, a függőleges részek összeadódnak: az eredő erő lefelé, a mágnes felé mutat. A hurok momentuma felfelé mutat, ugyanúgy, mint a mágnesé. Tehát **az azonos irányba álló momentumok vonzzák, az ellentétesek taszítják egymást.** Ellenőrzés a képlettel: m·B pozitív, és lefelé (a pólus felé) nő, ezért az erő lefelé mutat.
-->
## Vonzás és taszítás

Egy kör alakú hurok alatt, szimmetrikusan áll egy rúdmágnes, északi pólusa felfelé. A mágnes nagy bé vonalai a hurok minden kis darabjánál ferdén, kifelé-felfelé mutatnak. Az egyes darabokra ható {{Ampère|amper}}-erők kifelé-lefelé mutatnak; a vízszintes részeik a szimmetria miatt kioltják egymást, a függőleges részek összeadódnak: az eredő erő lefelé, a mágnes felé mutat. A hurok momentuma felfelé mutat, ugyanúgy, mint a mágnesé. Tehát az azonos irányba álló momentumok vonzzák, az ellentétesek taszítják egymást. Ellenőrzés a képlettel: em skalárszorzat nagy bé pozitív, és lefelé (a pólus felé) nő, ezért az erő lefelé mutat. [[pause 500]]

<!-- eredeti
**Vizsgán:** homogén térben csak nyomaték, inhomogénben erő is; ΔF = IaΔB = mΔB/b; F = grad(m·B); a körhurok-rúdmágnes rajza és a következtetés.
-->
## Amit a vizsgán le kell írni

Homogén térben csak nyomaték, inhomogénben erő is; delta ef egyenlő í kis á delta nagy bé, ami egyenlő em delta nagy bé per kis bé; ef egyenlő gradiens, zárójelben em skalárszorzat nagy bé; a körhurok-rúdmágnes rajza és a következtetés. [[pause 500]]

<!-- eredeti
### 7. Mágneses fluxus és Gauss-törvény. Mágneses polarizáció. Mágneses szuszceptibilitás és H
-->
# Második rész, hetedik tétel. Mágneses fluxus és {{Gauss|gausz}}-törvény. Mágneses polarizáció. Mágneses szuszceptibilitás és {{H|há}}

<!-- eredeti
| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| Φ | mágneses indukciófluxus (hány B-vonal megy át a felületen) | Wb = Vs |
| B | mágneses indukció | T = Vs/m² |
| A, dA | felület, felületelem | m² |
| α | B és a felület normálisa közti szög | rad |
| m | egy atom/molekula mágneses momentuma | Am² |
| M | mágnesezettség (mágneses momentum / térfogat) | A/m |
| H | mágneses térerősség | A/m |
| μ₀ | vákuum permeabilitása, 4π·10⁻⁷ | Vs/(Am) |
| χ | mágneses szuszceptibilitás | nincs |
| μᵣ = 1 + χ | relatív permeabilitás | nincs |
| μ = μ₀μᵣ | abszolút permeabilitás | Vs/(Am) |
| T | hőmérséklet (Curie-törvényben) | K |
-->
## Jelölések

- A nagy fí jel a mágneses indukciófluxust jelenti (hány bé-vonal megy át a felületen), mértékegysége a {{weber|véber}}, ami egyenlő volt szekundum.
- A B jel a mágneses indukciót jelenti, mértékegysége a tesla, ami egyenlő volt szekundum per négyzetméter. [[pause 500]]
- Az A és a dé A jel a felületet, illetve a felületelemet jelenti, mértékegységük a négyzetméter.
- Az alfa jel a bé és a felület normálisa közti szöget jelenti, mértékegysége a radián.
- A kis m jel egy atom, illetve molekula mágneses momentumát jelenti, mértékegysége az amper négyzetméter.
- A nagy M jel a mágnesezettséget jelenti (mágneses momentum per térfogat), mértékegysége az amper per méter.
- A H jel a mágneses térerősséget jelenti, mértékegysége az amper per méter.
- A mű nulla jel a vákuum permeabilitását jelenti, értéke négy pí szorozva tíz a mínusz hetediken, mértékegysége a volt szekundum per amper méter. [[pause 500]]
- A khí jel a mágneses szuszceptibilitást jelenti, mértékegység nélküli.
- A mű er jel, amely egyenlő egy plusz khí, a relatív permeabilitást jelenti, mértékegység nélküli. [[pause 500]]
- A mű jel, amely egyenlő mű nulla szorozva mű er, az abszolút permeabilitást jelenti, mértékegysége a volt szekundum per amper méter. [[pause 500]]
- A T jel a hőmérsékletet jelenti ({{Curie|küri}}-törvényben), mértékegysége a kelvin.

<!-- eredeti
**Miről szól?** A fluxus azt méri, mennyi mágneses erővonal megy át egy felületen. Mivel mágneses töltés nincs, a vonalak mindig zártak: egy zárt felületbe ugyanannyi megy be, mint ki. Az anyagban az atomok kis köráramként viselkednek (elektronok keringenek, illetve saját spin), ezek momentumai a térben rendeződhetnek: az anyag felmágneseződik. Ezt méri M, és χ azt, mennyire könnyen. A H vektort úgy vezetjük be, hogy rá egyszerű legyen a gerjesztési törvény.
-->
## Miről szól

A fluxus azt méri, mennyi mágneses erővonal megy át egy felületen. Mivel mágneses töltés nincs, a vonalak mindig zártak: egy zárt felületbe ugyanannyi megy be, mint ki. Az anyagban az atomok kis köráramként viselkednek (elektronok keringenek, illetve saját spin), ezek momentumai a térben rendeződhetnek: az anyag felmágneseződik. Ezt méri nagy em, és khí azt, mennyire könnyen. A há vektort úgy vezetjük be, hogy rá egyszerű legyen a gerjesztési törvény.

<!-- eredeti
**Fluxus és Gauss-törvény.** Homogén térben, illetve általánosan:
-->
## Fluxus és {{Gauss|gausz}}-törvény

Homogén térben, illetve általánosan:

<!-- eredeti
```latex
\Phi = \vec B\vec A = BA\cos\alpha \qquad \Phi = \int_A\vec B\,d\vec A \qquad \oint\vec B\,d\vec A = 0,\quad \operatorname{div}\vec B = 0
```
-->
Homogén térben a nagy fí fluxus egyenlő a B mágneses indukció vektora skalárszorzat az A felület vektora, ami egyenlő bé szorozva á szorozva koszinusz alfa. [[pause 500]]
Általánosan nagy fí egyenlő bé vektor skalárszorzat dé á vektor felületi integrálja az á felületre. [[pause 500]]
Zárt felületre bé vektor skalárszorzat dé á vektor zárt felületi integrálja egyenlő nulla. [[pause 500]]
Differenciális alakban divergencia bé vektor egyenlő nulla. [[pause 500]]

<!-- eredeti
**Mágnesezettség.** Az atom mágneses momentuma lényegében az elektronoké (a magoké sokkal kisebb), két részből: pályamozgás (kis köráram) és saját (spin) momentum. A mágnesezettség az egységnyi térfogatra jutó momentum; állandó mágnesben is délről észak felé mutat. Felfogható úgy, hogy „molekuláris áramok” keltik.
-->
## Mágnesezettség

Az atom mágneses momentuma lényegében az elektronoké (a magoké sokkal kisebb), két részből: pályamozgás (kis köráram) és saját (spin) momentum. A mágnesezettség az egységnyi térfogatra jutó momentum; állandó mágnesben is délről észak felé mutat. Felfogható úgy, hogy „molekuláris áramok” keltik.

<!-- eredeti
```latex
\vec M = \lim_{\Delta V\to0}\frac{\sum\vec m}{\Delta V}
```
-->
Az M mágnesezettség vektora egyenlő limesz delta vé tart nullához, egy tört, a számláló a kis em vektorok összege, a nevező delta vé. [[pause 500]]

<!-- eredeti
**A mágneses térerősség és a szuszceptibilitás.** Definíció, majd a lineáris anyagegyenlet (izotróp anyagban M arányos H-val):
-->
## A mágneses térerősség és a szuszceptibilitás

Definíció, majd a lineáris anyagegyenlet (izotróp anyagban nagy em arányos há-val):

<!-- eredeti
```latex
\vec H = \frac{\vec B}{\mu_0} - \vec M \;\Leftrightarrow\; \vec B = \mu_0\left(\vec H + \vec M\right) \qquad \vec M = \chi\vec H
```
-->
A H mágneses térerősség vektora egyenlő bé vektor per mű nulla, mínusz nagy em vektor. [[pause 500]]
Ez egyenértékű azzal, hogy bé vektor egyenlő mű nulla szorozva, zárójelben há vektor plusz nagy em vektor. [[pause 500]]
A lineáris anyagegyenlet: nagy em vektor egyenlő khí szorozva há vektor. [[pause 500]]

<!-- eredeti
```latex
\vec B = \mu_0\left(\vec H + \chi\vec H\right) = \mu_0(1+\chi)\vec H = \mu_0\mu_r\vec H = \mu\vec H
```
-->
Ebből bé vektor egyenlő mű nulla szorozva, zárójelben há vektor plusz khí há vektor. [[pause 500]]
Ez egyenlő mű nulla szorozva, zárójelben egy plusz khí, szorozva há vektor. [[pause 500]]
Ez egyenlő mű nulla szorozva mű er szorozva há vektor, vagyis mű szorozva há vektor. [[pause 500]]

<!-- eredeti
Ez csak közelítés; kemény ferromágneseknél teljesen rossz.
-->
Ez csak közelítés; kemény ferromágneseknél teljesen rossz.

<!-- eredeti
**Anyagtípusok.** Külső térben két folyamat zajlik: a *diamágneses* (minden atomban indukálódik egy kis momentum, a tér ellen) és a *paramágneses* (a már meglévő atomi momentumok a tér irányába fordulnak, a hőmozgás ellenében).
-->
## Anyagtípusok

Külső térben két folyamat zajlik: a diamágneses (minden atomban indukálódik egy kis momentum, a tér ellen) és a paramágneses (a már meglévő atomi momentumok a tér irányába fordulnak, a hőmozgás ellenében).

<!-- eredeti
| Típus | χ | Viselkedés |
| --- | --- | --- |
| diamágneses | negatív, nagyon kicsi (μᵣ ≈ 0,9999) | atomjainak nincs saját momentuma; a mágnes taszítja (bizmut) |
| paramágneses | pozitív, kicsi (10⁻³...10⁻⁶) | van saját momentum, de tér nélkül rendezetlen; a mágnes gyengén vonzza (alumínium); Curie-törvény: χ \~ 1/T |
| ferromágneses | nem lineáris, nagy | erősen mágnesezhető, megtartja a mágnesességét; telítés, hiszterézis |
-->
- A diamágneses anyag szuszceptibilitása negatív, nagyon kicsi (mű er közelítőleg nulla egész kilencezer-kilencszázkilencvenkilenc tízezred); atomjainak nincs saját momentuma; a mágnes taszítja (bizmut). [[pause 500]]
- A paramágneses anyag szuszceptibilitása pozitív, kicsi (tíz a mínusz harmadikontól tíz a mínusz hatodikonig); van saját momentum, de tér nélkül rendezetlen; a mágnes gyengén vonzza (alumínium); {{Curie|küri}}-törvény: khí arányos egy per té-vel. [[pause 500]]
- A ferromágneses anyag szuszceptibilitása nem lineáris, nagy; erősen mágnesezhető, megtartja a mágnesességét; telítés, hiszterézis.

<!-- eredeti
**Hiszterézisgörbe** (ferromágnes): nulláról a kezdeti görbén haladunk a telítésig; H-t visszaveszük, de B nem ugyanott jön vissza, H = 0-nál marad Bᵣ (**remanens indukció**). Az ellentétes tér, amelynél B = 0, a H\_c **koercítiv térerősség**. Kis H\_c: lágymágnes (trafomag); nagy Bᵣ és H\_c: keménymágnes (állandó mágnes).
-->
## Hiszterézisgörbe

Ferromágnes esetén: nulláról a kezdeti görbén haladunk a telítésig; há-t visszavesszük, de bé nem ugyanott jön vissza, há egyenlő nullánál marad bé er (remanens indukció). [[pause 500]]
Az ellentétes tér, amelynél bé egyenlő nulla, a há cé koercitív térerősség. [[pause 500]]
Kis há cé: lágymágnes (trafomag); nagy bé er és há cé: keménymágnes (állandó mágnes).

<!-- eredeti
**Vizsgán:** Φ definíciója; ∮B dA = 0, div B = 0 és jelentése; az elektron két momentuma; M definíciója; H = B/μ₀ − M; M = χH → B = μ₀(1+χ)H; a három anyagtípus; a hiszterézis fő pontjai.
-->
## Amit a vizsgán le kell írni

Nagy fí definíciója; bé skalárszorzat dé á zárt felületi integrálja egyenlő nulla, divergencia bé egyenlő nulla és jelentése; az elektron két momentuma; nagy em definíciója; há egyenlő bé per mű nulla mínusz nagy em; nagy em egyenlő khí há, ebből bé egyenlő mű nulla szorozva, zárójelben egy plusz khí, szorozva há; a három anyagtípus; a hiszterézis fő pontjai. [[pause 500]]


<!-- eredeti
### 8. Elektromágneses indukció. Neumann-törvény, Faraday-Lenz törvény. Lineáris és váltóáramú generátor
-->
# Második rész, nyolcadik tétel. Elektromágneses indukció. {{Neumann|nojmann}}-törvény, {{Faraday|faradéj}}–{{Lenz|lenc}} törvény. Lineáris és váltóáramú generátor

<!-- eredeti
| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| ε | indukált elektromotoros erő (az indukált „feszültség”) | V |
| E\* | idegen térerősség (a mozgás miatt fellépő) | V/m |
| F\* | a mozgó töltésre ható Lorentz-erő | N |
| q | töltés | C |
| v | a vezető (rúd) sebessége | m/s |
| B | mágneses indukció | T |
| ℓ | a mozgó rúd hossza | m |
| h | a hurok másik oldalának hossza | m |
| A | a hurok (keret) területe | m² |
| Φ | mágneses fluxus a hurkon át | Vs |
| R, I | a kör ellenállása, árama | Ω, A |
| ω | a forgó keret szögsebessége | 1/s |
| N | menetszám | nincs |
| ε₀ | (itt) az elektromotoros erő csúcsértéke | V |
-->
## Jelölések

Az epszilon jel az indukált elektromotoros erőt jelenti (az indukált feszültséget), mértékegysége a volt.

Az E csillag jel az idegen térerősséget jelenti (a mozgás miatt fellépőt), mértékegysége a volt per méter.

Az F csillag jel a mozgó töltésre ható {{Lorentz|lorenc}}-erőt jelenti, mértékegysége a {{newton|nyúton}}.

A kú jel a töltést jelenti, mértékegysége a {{coulomb|kulomb}}.

A vé jel a vezető (rúd) sebességét jelenti, mértékegysége a méter per szekundum.

A bé jel a mágneses indukciót jelenti, mértékegysége a tesla.

Az el jel a mozgó rúd hosszát jelenti, mértékegysége a méter.

A há jel a hurok másik oldalának hosszát jelenti, mértékegysége a méter.

Az á jel a hurok (keret) területét jelenti, mértékegysége a négyzetméter.

A nagy fí jel a hurkon átmenő mágneses fluxust jelenti, mértékegysége a voltszekundum.

Az er és az í jel a kör ellenállását, illetve áramát jelenti, mértékegységük az óm, illetve az amper.

Az omega jel a forgó keret szögsebességét jelenti, mértékegysége az egy per másodperc.

Az en jel a menetszámot jelenti, mértékegység nélküli.

Az epszilon nulla jel itt az elektromotoros erő csúcsértékét jelenti, mértékegysége a volt.

<!-- eredeti
**Miről szól?** Mágneses térrel áramot lehet csinálni. Kétféleképpen: ha a vezetőt mozgatjuk a térben, a benne lévő töltésekre Lorentz-erő hat, ez hajtja őket (mozgási indukció). Ha a vezető áll, de a tér változik, a változó tér elektromos teret kelt, az hajtja a töltéseket (nyugalmi indukció). Mindkettőt ugyanaz a szabály írja le: az indukált feszültség annyi, amilyen gyorsan változik a hurkon átmenő fluxus, és mindig úgy, hogy a változást akadályozza (Lenz).
-->
## Miről szól

Mágneses térrel áramot lehet csinálni. Kétféleképpen: ha a vezetőt mozgatjuk a térben, a benne lévő töltésekre {{Lorentz|lorenc}}-erő hat, ez hajtja őket (mozgási indukció). Ha a vezető áll, de a tér változik, a változó tér elektromos teret kelt, az hajtja a töltéseket (nyugalmi indukció). Mindkettőt ugyanaz a szabály írja le: az indukált feszültség annyi, amilyen gyorsan változik a hurkon átmenő fluxus, és mindig úgy, hogy a változást akadályozza ({{Lenz|lenc}}).

<!-- eredeti
**Mozgási indukció, Neumann-törvény.** A mozgó vezető töltéseire ható Lorentz-erő egy „idegen” térerősségként viselkedik, és a vezető mentén elektromotoros erőt kelt:
-->
## Mozgási indukció, {{Neumann|nojmann}}-törvény

A mozgó vezető töltéseire ható {{Lorentz|lorenc}}-erő egy idegen térerősségként viselkedik, és a vezető mentén elektromotoros erőt kelt.

<!-- eredeti
```latex
\vec F^* = q\,\vec v\times\vec B \qquad \vec E^* = \frac{\vec F^*}{q} = \vec v\times\vec B \qquad \varepsilon_{AB} = \int_A^B\left(\vec v\times\vec B\right)d\vec s
```
-->
Az F csillag vektor egyenlő kú szorozva vé vektor vektoriálisan szorozva bé vektor. [[pause 500]]

Az E csillag vektor egyenlő F csillag vektor per kú, ami egyenlő vé vektor vektoriálisan szorozva bé vektor. [[pause 500]]

Epszilon á bé egyenlő integrál az á ponttól a bé pontig, zárójelben vé vektor vektoriálisan szorozva bé vektor, szorozva dé es vektor. [[pause 500]]

<!-- eredeti
**Lineáris generátor.** Síneken csúszó ℓ hosszú rúd; v, B és a rúd egymásra merőlegesek. Az indukált elektromotoros erő és az áram:
-->
## Lineáris generátor

Síneken csúszó el hosszú rúd; vé, bé és a rúd egymásra merőlegesek. Az indukált elektromotoros erő és az áram:

<!-- eredeti
```latex
\varepsilon = v\ell B \qquad I = \frac{\varepsilon}{R}
```
-->
Epszilon egyenlő vé szorozva el szorozva bé. [[pause 500]]

Í egyenlő epszilon per er. [[pause 500]]

<!-- eredeti
Honnan van az energia? Az indukált áram miatt a rúdra Ampère-erő hat, a mozgással szemben (Lenz). Ezt egy húzóerővel kell legyőzni, és ennek munkája lesz az elektromos energia. A generátor mechanikai munkát alakít elektromossá.
-->
Honnan van az energia? Az indukált áram miatt a rúdra {{Ampère|amper}}-erő hat, a mozgással szemben ({{Lenz|lenc}}). Ezt egy húzóerővel kell legyőzni, és ennek munkája lesz az elektromos energia. A generátor mechanikai munkát alakít elektromossá.

<!-- eredeti
**A fluxus-szabály levezetése.** A hurok területe A = ℓh. A rúd v sebességgel mozog, ezért a terület dA/dt = −ℓv ütemben változik. A fluxus változása:
-->
## A fluxus-szabály levezetése

A hurok területe á egyenlő el szorozva há. [[pause 500]]

A rúd vé sebességgel mozog, ezért a terület dé á per dé té egyenlő mínusz el szorozva vé ütemben változik. [[pause 500]]

A fluxus változása:

<!-- eredeti
```latex
\frac{d\Phi}{dt} = \frac{d(BA)}{dt} = B\frac{dA}{dt} = -B\ell v = -\varepsilon
```
-->
Dé nagy fí per dé té egyenlő dé, zárójelben bé szorozva á, per dé té, ami egyenlő bé szorozva dé á per dé té. [[pause 500]]

Ez egyenlő mínusz bé szorozva el szorozva vé, vagyis egyenlő mínusz epszilon. [[pause 500]]

<!-- eredeti
Általánosan, bármilyen mozgó (akár alakváltozó) zárt hurokra, ez a **Faraday-törvény** (fluxus-szabály):
-->
Általánosan, bármilyen mozgó (akár alakváltozó) zárt hurokra, ez a {{Faraday|faradéj}}-törvény (fluxus-szabály):

<!-- eredeti
```latex
\varepsilon = -\frac{d\Phi}{dt}
```
-->
Epszilon egyenlő mínusz dé nagy fí per dé té. [[pause 500]]

<!-- eredeti
Ez sokszor egyszerűbb, mint a Neumann-törvény. Például látszik belőle, hogy homogén térben egyenesen mozgó keretben nem indukálódik semmi (a fluxus nem változik).
-->
Ez sokszor egyszerűbb, mint a {{Neumann|nojmann}}-törvény. Például látszik belőle, hogy homogén térben egyenesen mozgó keretben nem indukálódik semmi (a fluxus nem változik).

<!-- eredeti
**Nyugalmi indukció.** A fluxus úgy is változhat, hogy a hurok áll, csak B változik. Ilyenkor nem a Lorentz-erő hat, hanem a változó mágneses tér elektromos teret kelt. Ha egy másik tekercs áramának változása okozza, az a kölcsönös indukció; ha a saját áramé, az önindukció (9. tétel). Az összefoglaló alak:
-->
## Nyugalmi indukció

A fluxus úgy is változhat, hogy a hurok áll, csak bé változik. Ilyenkor nem a {{Lorentz|lorenc}}-erő hat, hanem a változó mágneses tér elektromos teret kelt. Ha egy másik tekercs áramának változása okozza, az a kölcsönös indukció; ha a saját áramé, az önindukció (kilencedik tétel). Az összefoglaló alak:

<!-- eredeti
```latex
\oint_g\vec E\,d\vec s = -\frac{d}{dt}\int_F\vec B\,d\vec A
```
-->
Az E vektor skalárszorzat dé es vektor zárt görbe menti integrálja a gé görbére egyenlő mínusz dé per dé té, zárójelben a bé vektor skalárszorzat dé á vektor felületi integrálja az ef felületre. [[pause 500]]

<!-- eredeti
Az indukált elektromos tér örvényes, nem konzervatív (nem a töltések keltik, forrásmentes).
-->
Az indukált elektromos tér örvényes, nem konzervatív (nem a töltések keltik, forrásmentes).

<!-- eredeti
**Lenz-törvény** (a mínusz jel): az indukált áram az őt létrehozó változás ellen hat; ha a fluxus csökken, olyan áram jön létre, amely növelné. Ha fordítva lenne, az indukció erősítené önmagát, és a semmiből energia keletkezne.
-->
## {{Lenz|lenc}}-törvény (a mínusz jel)

Az indukált áram az őt létrehozó változás ellen hat; ha a fluxus csökken, olyan áram jön létre, amely növelné. Ha fordítva lenne, az indukció erősítené önmagát, és a semmiből energia keletkezne.

<!-- eredeti
**Váltakozó áramú generátor.** A területű keret ω szögsebességgel forog homogén B térben; kezdetben a keret síkjára merőleges irány egyirányú B-vel, így a szögük ωt:
-->
## Váltakozó áramú generátor

Á területű keret omega szögsebességgel forog homogén bé térben; kezdetben a keret síkjára merőleges irány egyirányú bé-vel, így a szögük omega szorozva té:

<!-- eredeti
```latex
\Phi = BA\cos\omega t \;\Rightarrow\; \varepsilon = -\frac{d\Phi}{dt} = BA\omega\sin\omega t = \varepsilon_0\sin\omega t
```
-->
Nagy fí egyenlő bé szorozva á szorozva koszinusz omega té. [[pause 500]]

Ebből következik, hogy epszilon egyenlő mínusz dé nagy fí per dé té, ami egyenlő bé szorozva á szorozva omega szorozva szinusz omega té, vagyis egyenlő epszilon nulla szorozva szinusz omega té. [[pause 500]]

<!-- eredeti
Szinuszos váltakozó feszültség. N menetnél minden meneten átmegy a fluxus, így N-szeres:
-->
Szinuszos váltakozó feszültség. En menetnél minden meneten átmegy a fluxus, így en-szeres:

<!-- eredeti
```latex
\varepsilon = NAB\omega\sin\omega t
```
-->
Epszilon egyenlő en szorozva á szorozva bé szorozva omega szorozva szinusz omega té. [[pause 500]]

<!-- eredeti
**Vizsgán:** E\* = v × B, Neumann-törvény; lineáris generátor ε = vℓB és az energiamérleg; a fluxus-szabály levezetése; nyugalmi indukció; Lenz és a mínusz jel oka; váltóáramú generátor.
-->
## Amit a vizsgán le kell írni

E csillag egyenlő vé vektoriálisan szorozva bé, {{Neumann|nojmann}}-törvény; lineáris generátor, epszilon egyenlő vé szorozva el szorozva bé, és az energiamérleg; a fluxus-szabály levezetése; nyugalmi indukció; {{Lenz|lenc}} és a mínusz jel oka; váltóáramú generátor. [[pause 500]]

<!-- eredeti
### 9. Önindukció és önindukciós együttható
-->
# Második rész, kilencedik tétel. Önindukció és önindukciós együttható

<!-- eredeti
| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| L | önindukciós együttható (induktivitás) | H = Vs/A |
| N | menetszám | nincs |
| ℓ | a tekercs hossza | m |
| A | a tekercs keresztmetszete | m² |
| μ | a tekercs belsejének permeabilitása | Vs/(Am) |
| I | a tekercs árama | A |
| H, B | mágneses térerősség és indukció a tekercsben | A/m, T |
| Φₘ | menetfluxus: egyetlen menet fluxusa | Vs |
| Φ | tekercsfluxus: az összes menet fluxusa (NΦₘ) | Vs |
| U | a tekercsben indukált feszültség | V |
| M | kölcsönös indukciós együttható | H |
-->
## Jelölések

A nagy el jel az önindukciós együtthatót (induktivitást) jelenti, mértékegysége a henri, ami egyenlő voltszekundum per amper.

Az en jel a menetszámot jelenti, mértékegység nélküli.

A kis el jel a tekercs hosszát jelenti, mértékegysége a méter.

Az á jel a tekercs keresztmetszetét jelenti, mértékegysége a négyzetméter.

A mű jel a tekercs belsejének permeabilitását jelenti, mértékegysége a voltszekundum per amperméter.

Az í jel a tekercs áramát jelenti, mértékegysége az amper.

A há és a bé jel a mágneses térerősséget és indukciót jelenti a tekercsben, mértékegységük az amper per méter, illetve a tesla.

A nagy fí em jel a menetfluxust jelenti, vagyis egyetlen menet fluxusát, mértékegysége a voltszekundum.

A nagy fí jel a tekercsfluxust jelenti, vagyis az összes menet fluxusát (en szorozva nagy fí em), mértékegysége a voltszekundum.

Az ú jel a tekercsben indukált feszültséget jelenti, mértékegysége a volt.

Az em jel a kölcsönös indukciós együtthatót jelenti, mértékegysége a henri.

<!-- eredeti
**Miről szól?** Ha egy tekercsben változik az áram, változik a saját mágneses tere és a saját fluxusa is, ez pedig magában a tekercsben indukál feszültséget. Lenz miatt ez a feszültség mindig a változás ellen dolgozik: a tekercs „nem szereti”, ha változtatják az áramát. Az L együttható azt mondja meg, mennyire erős ez a hatás.
-->
## Miről szól

Ha egy tekercsben változik az áram, változik a saját mágneses tere és a saját fluxusa is, ez pedig magában a tekercsben indukál feszültséget. {{Lenz|lenc}} miatt ez a feszültség mindig a változás ellen dolgozik: a tekercs nem szereti, ha változtatják az áramát. A nagy el együttható azt mondja meg, mennyire erős ez a hatás.

<!-- eredeti
**Szolenoid L-je.** A tekercsben H = NI/ℓ és B = μNI/ℓ (3. tétel).
-->
## A szolenoid nagy el-je

A tekercsben há egyenlő en szorozva í per kis el, és bé egyenlő mű szorozva en szorozva í per kis el (harmadik tétel). [[pause 500]]

<!-- eredeti
1. Egy menet fluxusa: Φₘ = BA = μ(NA/ℓ)I.
2. A teljes tekercsfluxus N menetre: Φ = NΦₘ = μ(N²A/ℓ)I.
3. Ez arányos az árammal; az arányossági tényező definíció szerint L:

```latex
\Phi = LI \qquad L = \mu\frac{N^2A}{\ell}
```

4. Változó áramnál a Faraday-törvényből az indukált feszültség:

```latex
U = -\frac{d\Phi}{dt} = -L\frac{dI}{dt}
```
-->
- Első lépés. Egy menet fluxusa: nagy fí em egyenlő bé szorozva á, ami egyenlő mű szorozva, zárójelben en szorozva á per kis el, szorozva í. [[pause 500]]
- Második lépés. A teljes tekercsfluxus en menetre: nagy fí egyenlő en szorozva nagy fí em, ami egyenlő mű szorozva, zárójelben en négyzet szorozva á per kis el, szorozva í. [[pause 500]]
- Harmadik lépés. Ez arányos az árammal; az arányossági tényező definíció szerint nagy el: nagy fí egyenlő nagy el szorozva í, és nagy el egyenlő mű szorozva en négyzet szorozva á per kis el. [[pause 500]]
- Negyedik lépés. Változó áramnál a {{Faraday|faradéj}}-törvényből az indukált feszültség: ú egyenlő mínusz dé nagy fí per dé té, ami egyenlő mínusz nagy el szorozva dé í per dé té. [[pause 500]]

<!-- eredeti
Az indukált feszültség arányos az áram változásának gyorsaságával. L a menetszám **négyzetével** nő (ezért van sok menet) és a permeabilitással (ezért tesznek bele vasmagot). Mivel lineáris anyagot tételeztünk fel, vasmagra csak korlátozottan igaz.
-->
Az indukált feszültség arányos az áram változásának gyorsaságával. Nagy el a menetszám négyzetével nő (ezért van sok menet) és a permeabilitással (ezért tesznek bele vasmagot). Mivel lineáris anyagot tételeztünk fel, vasmagra csak korlátozottan igaz.

<!-- eredeti
**Kölcsönös indukció** (kiegészítés): két tekercs közös vasmagon, N₁ és N₂ menettel. Az első árama a másodikban Φ₁₂ = MI₁ fluxust kelt, ahol M = μN₁N₂A/ℓ, és ott U₁₂ = −M dI₁/dt feszültséget indukál.
-->
## Kölcsönös indukció (kiegészítés)

Két tekercs közös vasmagon, en egy és en kettő menettel. Az első árama a másodikban nagy fí egy kettő egyenlő em szorozva í egy fluxust kelt, ahol em egyenlő mű szorozva en egy szorozva en kettő szorozva á per kis el, és ott ú egy kettő egyenlő mínusz em szorozva dé í egy per dé té feszültséget indukál. [[pause 500]]

<!-- eredeti
**Vizsgán:** a jelenség és Lenz; menetfluxus, tekercsfluxus; Φ = LI mint definíció; szolenoidra L = μN²A/ℓ levezetve, egysége; U = −L dI/dt; miért sok menet és vasmag.
-->
## Amit a vizsgán le kell írni

A jelenség és {{Lenz|lenc}}; menetfluxus, tekercsfluxus; nagy fí egyenlő nagy el szorozva í mint definíció; szolenoidra nagy el egyenlő mű szorozva en négyzet szorozva á per kis el levezetve, egysége; ú egyenlő mínusz nagy el szorozva dé í per dé té; miért sok menet és vasmag. [[pause 500]]

<!-- eredeti
### 10. Az általános huroktörvény
-->
# Második rész, tizedik tétel. Az általános huroktörvény

<!-- eredeti
| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| R | a kör teljes ellenállása | Ω |
| C | a kondenzátor kapacitása | F |
| L | a tekercs (és egyben a kör) induktivitása | H |
| ε | az áramforrás elektromotoros ereje | V |
| I | az áram a körben | A |
| Q | a kondenzátor töltése | C |
| dI/dt | az áram változásának gyorsasága | A/s |
| g₁, g₂ | a hurok vezetőben, illetve a kondenzátor lemezei között futó része |  |
-->
## Jelölések

Az er jel a kör teljes ellenállását jelenti, mértékegysége az óm.

A cé jel a kondenzátor kapacitását jelenti, mértékegysége a farad.

Az el jel a tekercs (és egyben a kör) induktivitását jelenti, mértékegysége a henri.

Az epszilon jel az áramforrás elektromotoros erejét jelenti, mértékegysége a volt.

Az í jel az áramot jelenti a körben, mértékegysége az amper.

A kú jel a kondenzátor töltését jelenti, mértékegysége a {{coulomb|kulomb}}.

A dé í per dé té jel az áram változásának gyorsaságát jelenti, mértékegysége az amper per szekundum.

A gé egy és gé kettő jel a hurok vezetőben, illetve a kondenzátor lemezei között futó részét jelenti.

<!-- eredeti
**Miről szól?** A sima Kirchhoff-huroktörvény (ΣU = 0) csak akkor igaz, ha nincs változó mágneses tér. Ha a körben tekercs van és változik az áram, a saját indukció miatt a térerősség körbeintegrálja nem nulla. Ezt úgy kezeljük, hogy a tekercs L·dI/dt tagját is egyfajta feszültségként számoljuk, és így egy soros RLC körre is felírható egy hurokegyenlet.
-->
## Miről szól

A sima {{Kirchhoff|kirhhoff}}-huroktörvény (szumma ú egyenlő nulla) csak akkor igaz, ha nincs változó mágneses tér. Ha a körben tekercs van és változik az áram, a saját indukció miatt a térerősség körbeintegrálja nem nulla. Ezt úgy kezeljük, hogy a tekercs el szorozva dé í per dé té tagját is egyfajta feszültségként számoljuk, és így egy soros er el cé körre is felírható egy hurokegyenlet. [[pause 500]]

<!-- eredeti
**Levezetés:**
-->
## Levezetés

<!-- eredeti
1. A Faraday-törvényt a hurokra felírva, és feltesszük, hogy a kör fluxusát a tekercs adja (Φ = LI):

```latex
\oint_g\vec E\,d\vec s = -\frac{d}{dt}\int_A\vec B\,d\vec A = -L\frac{dI}{dt}
```

2. A bal oldalt két részre bontjuk. A vezető mentén (g₁) a térerősség integrálja IR − ε (mint egyenáramnál), a kondenzátor lemezei között (g₂) pedig a kondenzátor feszültsége, Q/C:

```latex
IR - \varepsilon + \frac{Q}{C} = -L\frac{dI}{dt}
```

3. Átrendezve a huroktörvény általánosítása soros RLC körre:

```latex
L\frac{dI}{dt} + IR + \frac{Q}{C} = \varepsilon
```
-->
- Első lépés. A {{Faraday|faradéj}}-törvényt a hurokra felírva, és feltesszük, hogy a kör fluxusát a tekercs adja (nagy fí egyenlő el szorozva í): az E vektor skalárszorzat dé es vektor zárt görbe menti integrálja a gé görbére egyenlő mínusz dé per dé té, zárójelben a bé vektor skalárszorzat dé á vektor felületi integrálja az á felületre, ami egyenlő mínusz el szorozva dé í per dé té. [[pause 500]]
- Második lépés. A bal oldalt két részre bontjuk. A vezető mentén (gé egy) a térerősség integrálja í szorozva er mínusz epszilon (mint egyenáramnál), a kondenzátor lemezei között (gé kettő) pedig a kondenzátor feszültsége, kú per cé. Így í szorozva er mínusz epszilon plusz kú per cé egyenlő mínusz el szorozva dé í per dé té. [[pause 500]]
- Harmadik lépés. Átrendezve a huroktörvény általánosítása soros er el cé körre: el szorozva dé í per dé té plusz í szorozva er plusz kú per cé egyenlő epszilon. [[pause 500]]

<!-- eredeti
Négy különböző fajta „feszültség”: a tekercsé (saját indukció), az ellenállásé, a kondenzátoré, és a forrásé. Az ε vagy nem elektromos energiát alakít át (elem, napelem), vagy távoli indukcióból származik (erőmű), nem a vizsgált kör saját fluxusváltozásából.
-->
Négy különböző fajta feszültség: a tekercsé (saját indukció), az ellenállásé, a kondenzátoré, és a forrásé. Az epszilon vagy nem elektromos energiát alakít át (elem, napelem), vagy távoli indukcióból származik (erőmű), nem a vizsgált kör saját fluxusváltozásából.

<!-- eredeti
**Vizsgán:** az RLC kör rajza; Faraday-törvény a hurokra, −L dI/dt; a görbe szétbontása; L dI/dt + IR + Q/C = ε; miért nem érvényes itt a sima ΣU = 0.
-->
## Amit a vizsgán le kell írni

Az er el cé kör rajza; {{Faraday|faradéj}}-törvény a hurokra, mínusz el szorozva dé í per dé té; a görbe szétbontása; el szorozva dé í per dé té plusz í szorozva er plusz kú per cé egyenlő epszilon; miért nem érvényes itt a sima szumma ú egyenlő nulla. [[pause 500]]

<!-- eredeti
### 11. Tranziens jelenségek. Az RL és RC kör időállandója
-->
# Második rész, tizenegyedik tétel. Tranziens jelenségek. Az {{RL|er el}} és {{RC|er cé}} kör időállandója

<!-- eredeti
| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| I(t) | az áram az idő függvényében | A |
| I₀ | az áram a kezdőpillanatban (t = 0) | A |
| I∞ | a végső, beállt áram (t → ∞) | A |
| R, C, L | ellenállás, kapacitás, induktivitás | Ω, F, H |
| Q, Q₀ | a kondenzátor töltése, kezdeti töltése | C |
| U₀ | a kondenzátor kezdeti feszültsége (Q₀/C) | V |
| ε₁, ε₂ | a forrás feszültsége az ugrás előtt és után | V |
| τ | időállandó (RC, illetve L/R) | s |
| e | Euler-szám, ≈ 2,718 |  |
-->
## Jelölések

Az í té jel az áramot jelenti az idő függvényében, mértékegysége az amper.

Az í nulla jel az áramot jelenti a kezdőpillanatban (té egyenlő nulla), mértékegysége az amper.

Az í végtelen jel a végső, beállt áramot jelenti (té tart végtelenhez), mértékegysége az amper.

Az er, cé és el jel az ellenállást, a kapacitást és az induktivitást jelenti, mértékegységük az óm, a farad és a henri.

A kú és kú nulla jel a kondenzátor töltését, illetve kezdeti töltését jelenti, mértékegysége a {{coulomb|kulomb}}.

Az ú nulla jel a kondenzátor kezdeti feszültségét jelenti (kú nulla per cé), mértékegysége a volt.

Az epszilon egy és epszilon kettő jel a forrás feszültségét jelenti az ugrás előtt és után, mértékegysége a volt.

A tau jel az időállandót jelenti (er szorozva cé, illetve el per er), mértékegysége a másodperc.

Az é jel az {{Euler|ojler}}-számot jelenti, értéke körülbelül kettő egész hétszáztizennyolc ezred.

<!-- eredeti
**Miről szól?** Ha egy körben hirtelen megváltozik a feszültség (bekapcsolunk, kikapcsolunk), az áram nem ugrik azonnal az új értékre, hanem fokozatosan, exponenciálisan áll be. Ez az átmeneti (tranziens) szakasz. Az időállandó τ megmondja, milyen gyors ez: τ idő alatt az eltérés e-ad részére (kb. 37%-ra) csökken.
-->
## Miről szól

Ha egy körben hirtelen megváltozik a feszültség (bekapcsolunk, kikapcsolunk), az áram nem ugrik azonnal az új értékre, hanem fokozatosan, exponenciálisan áll be. Ez az átmeneti (tranziens) szakasz. Az időállandó, tau megmondja, milyen gyors ez: tau idő alatt az eltérés é-ad részére (körülbelül harminchét százalékra) csökken.

<!-- eredeti
**Kondenzátor kisütése (RC kör).** A feltöltött kondenzátort R ellenálláson keresztül kisütjük. A huroktörvény (nincs forrás):
-->
## Kondenzátor kisütése (er cé kör)

A feltöltött kondenzátort er ellenálláson keresztül kisütjük. A huroktörvény (nincs forrás):

<!-- eredeti
```latex
IR + \frac{Q}{C} = 0, \qquad I = \frac{dQ}{dt}
```
-->
Í szorozva er plusz kú per cé egyenlő nulla, ahol í egyenlő dé kú per dé té. [[pause 500]]

<!-- eredeti
1. Idő szerint deriválva (dQ/dt = I) és átrendezve: dI/dt = −I/(RC).
2. Szétválasztjuk a változókat és integrálunk I₀-tól I-ig, illetve 0-tól t-ig:

```latex
\int_{I_0}^{I}\frac{dI}{I} = -\frac{1}{RC}\int_0^t dt \;\Rightarrow\; \ln\frac{I}{I_0} = -\frac{t}{RC}
```

3. Ebből:

```latex
I(t) = I_0e^{-t/\tau}, \qquad \tau = RC, \qquad I_0 = \frac{U_0}{R}
```
-->
- Első lépés. Idő szerint deriválva (dé kú per dé té egyenlő í) és átrendezve: dé í per dé té egyenlő mínusz í per, zárójelben er szorozva cé. [[pause 500]]
- Második lépés. Szétválasztjuk a változókat és integrálunk í nullától í-ig, illetve nullától té-ig: integrál í nullától í-ig dé í per í egyenlő mínusz egy per er cé szorozva integrál nullától té-ig dé té. Ebből következik, hogy természetes alapú logaritmus í per í nulla egyenlő mínusz té per er cé. [[pause 500]]
- Harmadik lépés. Ebből í té egyenlő í nulla szorozva é a mínusz té per tau-adikon, ahol tau egyenlő er szorozva cé, és í nulla egyenlő ú nulla per er. [[pause 500]]

<!-- eredeti
**Tekercs hirtelen változó feszültségen (RL kör).** A forrás feszültsége t = 0-ban ε₁-ről ε₂-re ugrik (bármelyik lehet 0). Az általános huroktörvény:
-->
## Tekercs hirtelen változó feszültségen (er el kör)

A forrás feszültsége a té egyenlő nulla pillanatban epszilon egyről epszilon kettőre ugrik (bármelyik lehet nulla). Az általános huroktörvény:

<!-- eredeti
```latex
IR - \varepsilon_2 = -L\frac{dI}{dt}
```
-->
Í szorozva er mínusz epszilon kettő egyenlő mínusz el szorozva dé í per dé té. [[pause 500]]

<!-- eredeti
**Kezdeti feltétel:** az áram nem ugorhat hirtelen, mert akkor dI/dt és vele az indukált feszültség végtelen lenne. Tehát t = 0-ban még a régi áram folyik: I₀ = ε₁/R.
-->
## Kezdeti feltétel

Az áram nem ugorhat hirtelen, mert akkor dé í per dé té és vele az indukált feszültség végtelen lenne. Tehát a té egyenlő nulla pillanatban még a régi áram folyik: í nulla egyenlő epszilon egy per er. [[pause 500]]

<!-- eredeti
1. Szétválasztva és integrálva:

```latex
\int_{I_0}^{I}\frac{dI}{\varepsilon_2 - RI} = \frac1L\int_0^t dt \;\Rightarrow\; \varepsilon_2 - RI = \left(\varepsilon_2 - RI_0\right)e^{-\frac RL t}
```

2. R-rel osztva, I∞ = ε₂/R jelöléssel, és τ = L/R bevezetésével:

```latex
I(t) = I_0e^{-t/\tau} + I_\infty\left(1 - e^{-t/\tau}\right), \qquad \tau = \frac{L}{R}
```
-->
- Első lépés. Szétválasztva és integrálva: integrál í nullától í-ig egy tört, a számláló dé í, a nevező epszilon kettő mínusz er szorozva í, ez egyenlő egy per el szorozva integrál nullától té-ig dé té. [[pause 500]] Ebből következik, hogy epszilon kettő mínusz er szorozva í egyenlő, zárójelben epszilon kettő mínusz er szorozva í nulla, szorozva é a mínusz er per el szorozva té-ediken. [[pause 500]]
- Második lépés. Er-rel osztva, í végtelen egyenlő epszilon kettő per er jelöléssel, és tau egyenlő el per er bevezetésével: í té egyenlő í nulla szorozva é a mínusz té per tau-adikon, plusz í végtelen szorozva, zárójelben egy mínusz é a mínusz té per tau-adikon, ahol tau egyenlő el per er. [[pause 500]]

<!-- eredeti
A régi áram exponenciálisan eltűnik, az új ugyanolyan ütemben épül fel. **Kikapcsolás** (I∞ = 0): I = I₀e^(−t/τ). **Bekapcsolás** (I₀ = 0): I = I∞(1 − e^(−t/τ)).
-->
A régi áram exponenciálisan eltűnik, az új ugyanolyan ütemben épül fel. Kikapcsolás (í végtelen egyenlő nulla): í egyenlő í nulla szorozva é a mínusz té per tau-adikon. [[pause 500]] Bekapcsolás (í nulla egyenlő nulla): í egyenlő í végtelen szorozva, zárójelben egy mínusz é a mínusz té per tau-adikon. [[pause 500]]

<!-- eredeti
(Megjegyzés: LC körben ellenállás nélkül szinuszos rezgés jön létre, ellenállással csillapított rezgés.)
-->
Megjegyzés: el cé körben ellenállás nélkül szinuszos rezgés jön létre, ellenállással csillapított rezgés.

<!-- eredeti
**Vizsgán:** mi a tranziens; RC kisütés levezetése, τ = RC és jelentése; RL kör egyenlete, a kezdeti feltétel indoklása, a megoldás, τ = L/R; be- és kikapcsolás.
-->
## Amit a vizsgán le kell írni

Mi a tranziens; er cé kisütés levezetése, tau egyenlő er szorozva cé és jelentése; er el kör egyenlete, a kezdeti feltétel indoklása, a megoldás, tau egyenlő el per er; be- és kikapcsolás. [[pause 500]]

<!-- eredeti
### 12. Tekercs mágneses terének energiája. A mágneses tér energiasűrűsége
-->
# Második rész, tizenkettedik tétel. Tekercs mágneses terének energiája. A mágneses tér energiasűrűsége

<!-- eredeti
| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| W, Wₘ | munka, illetve a tekercsben tárolt mágneses energia | J |
| U | a tekercsben indukált (ellen)feszültség | V |
| dq | egy kis átvitt töltés | C |
| L | induktivitás | H |
| I, I∞ | áram, végső áram | A |
| N, ℓ, A | menetszám, tekercshossz, keresztmetszet | -, m, m² |
| μ | permeabilitás | Vs/(Am) |
| H, B | mágneses térerősség, indukció | A/m, T |
| V | a tekercs belsejének térfogata (Aℓ) | m³ |
| wₘ | mágneses energiasűrűség | J/m³ |
-->
## Jelölések

A dupla vé és a dupla vé em jel a munkát, illetve a tekercsben tárolt mágneses energiát jelenti, mértékegysége a {{joule|dzsúl}}.

Az ú jel a tekercsben indukált ellenfeszültséget jelenti, mértékegysége a volt.

A dé kú jel egy kis átvitt töltést jelent, mértékegysége a {{coulomb|kulomb}}.

A nagy el jel az induktivitást jelenti, mértékegysége a henri.

Az í és í végtelen jel az áramot, illetve a végső áramot jelenti, mértékegysége az amper.

Az en, a kis el és az á jel a menetszámot, a tekercshosszt és a keresztmetszetet jelenti; az en mértékegység nélküli, a kis el mértékegysége a méter, az á mértékegysége a négyzetméter.

A mű jel a permeabilitást jelenti, mértékegysége a voltszekundum per amperméter.

A há és a bé jel a mágneses térerősséget és az indukciót jelenti, mértékegységük az amper per méter, illetve a tesla.

A vé jel a tekercs belsejének térfogatát jelenti (á szorozva kis el), mértékegysége a köbméter.

A kis dupla vé em jel a mágneses energiasűrűséget jelenti, mértékegysége a {{joule|dzsúl}} per köbméter.

<!-- eredeti
**Miről szól?** Amikor bekapcsoljuk a tekercset, az áram növekedése ellenfeszültséget indukál (Lenz), és a forrásnak ez ellenében kell átvinnie a töltéseket. Ez a munka nem vész el: a tekercs mágneses terében tárolódik. Ugyanúgy, ahogy a kondenzátor az elektromos térben tárol energiát (10. tétel, 1. rész), a tekercs a mágnesesben.
-->
## Miről szól

Amikor bekapcsoljuk a tekercset, az áram növekedése ellenfeszültséget indukál ({{Lenz|lenc}}), és a forrásnak ez ellenében kell átvinnie a töltéseket. Ez a munka nem vész el: a tekercs mágneses terében tárolódik. Ugyanúgy, ahogy a kondenzátor az elektromos térben tárol energiát (első rész, tizedik tétel), a tekercs a mágnesesben.

<!-- eredeti
**A munka.** Egy kis dq töltés átvitele az U = L dI/dt ellenfeszültség ellenében, dq = I dt:
-->
## A munka

Egy kis dé kú töltés átvitele az ú egyenlő nagy el szorozva dé í per dé té ellenfeszültség ellenében, ahol dé kú egyenlő í szorozva dé té. [[pause 500]]

<!-- eredeti
```latex
dW = U\,dq = L\frac{dI}{dt}\,I\,dt = LI\,dI
```
-->
Dé dupla vé egyenlő ú szorozva dé kú, ami egyenlő nagy el szorozva dé í per dé té szorozva í szorozva dé té, vagyis egyenlő nagy el szorozva í szorozva dé í. [[pause 500]]

<!-- eredeti
0-tól a végső áramig integrálva (L állandó, lineáris közeg):
-->
Nullától a végső áramig integrálva (nagy el állandó, lineáris közeg):

<!-- eredeti
```latex
W = \int_0^{I_\infty}LI\,dI = L\left[\frac{I^2}{2}\right]_0^{I_\infty} \;\Rightarrow\; W_m = \frac12 LI^2
```
-->
Dupla vé egyenlő integrál nullától í végtelenig nagy el szorozva í dé í, ami egyenlő nagy el szorozva í négyzet per kettő, nullától í végtelenig kiértékelve. [[pause 500]]

Ebből következik, hogy dupla vé em egyenlő egyketted szorozva nagy el szorozva í négyzet. [[pause 500]]

<!-- eredeti
**Energiasűrűség.** Hosszú szolenoidba beírjuk L = μN²A/ℓ-t, és észrevesszük benne H = NI/ℓ-t és B = μNI/ℓ-t:
-->
## Energiasűrűség

Hosszú szolenoidba beírjuk a nagy el egyenlő mű szorozva en négyzet szorozva á per kis el összefüggést, és észrevesszük benne a há egyenlő en szorozva í per kis el és a bé egyenlő mű szorozva en szorozva í per kis el kifejezést. [[pause 500]]

<!-- eredeti
```latex
W_m = \frac12\mu\frac{N^2A}{\ell}I^2 = \frac12\cdot\mu\frac{NI}{\ell}\cdot\frac{NI}{\ell}\cdot A\ell = \frac12 BH\,V
```
-->
Dupla vé em egyenlő egyketted szorozva mű szorozva en négyzet szorozva á per kis el, szorozva í négyzet. [[pause 500]]

Ez egyenlő egyketted szorozva mű szorozva en í per kis el, szorozva en í per kis el, szorozva á szorozva kis el. [[pause 500]]

Ez pedig egyenlő egyketted szorozva bé szorozva há szorozva vé. [[pause 500]]

<!-- eredeti
V = Aℓ a tekercs belsejének térfogata, itt homogén a tér. Térfogattal osztva:
-->
Vé egyenlő á szorozva kis el, a tekercs belsejének térfogata, itt homogén a tér. Térfogattal osztva: [[pause 500]]

<!-- eredeti
```latex
w_m = \frac12\vec B\vec H
```
-->
Kis dupla vé em egyenlő egyketted szorozva bé vektor skalárszorzat há vektor. [[pause 500]]

<!-- eredeti
(Az elektromos w = ½D·E párja.) Megjegyzés: a bekapcsolás nem azért tart ideig, mert az elektronokat nehéz felgyorsítani; ez az energia a mágneses téré, nem az elektronok mozgási energiája.
-->
(Az elektromos kis dupla vé egyenlő egyketted szorozva nagy dé skalárszorzat E párja.) [[pause 500]] Megjegyzés: a bekapcsolás nem azért tart ideig, mert az elektronokat nehéz felgyorsítani; ez az energia a mágneses téré, nem az elektronok mozgási energiája.

<!-- eredeti
**Vizsgán:** miért kell munka a bekapcsoláshoz; dW = LI dI; Wₘ = ½LI²; szolenoidra W = ½BHV; wₘ = ½B·H.
-->
## Amit a vizsgán le kell írni

Miért kell munka a bekapcsoláshoz; dé dupla vé egyenlő nagy el szorozva í szorozva dé í; dupla vé em egyenlő egyketted szorozva nagy el szorozva í négyzet; szolenoidra dupla vé egyenlő egyketted szorozva bé szorozva há szorozva vé; kis dupla vé em egyenlő egyketted szorozva bé skalárszorzat há. [[pause 500]]

<!-- eredeti
### 13. Mágneses mennyiségek két közeg határán. B és H vonalak törése
-->
# Második rész, tizenharmadik tétel. Mágneses mennyiségek két közeg határán. {{B|bé}} és {{H|há}} vonalak törése

<!-- eredeti
| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| 1, 2 index | az 1-es és a 2-es közegben |  |
| t, n index | a határral párhuzamos, illetve rá merőleges komponens |  |
| H, B | mágneses térerősség, indukció | A/m, T |
| μ₁, μ₂ | a két közeg permeabilitása | Vs/(Am) |
| α, β | a vonal és a határra merőleges egyenes közti szög az 1-es, illetve 2-es közegben | rad |
-->
## Jelölések

Az egyes és a kettes index azt jelenti: az egyes és a kettes közegben.

A té és az en index a határral párhuzamos, illetve rá merőleges komponenst jelenti.

A há és a bé jel a mágneses térerősséget és az indukciót jelenti, mértékegységük az amper per méter, illetve a tesla.

A mű egy és mű kettő jel a két közeg permeabilitását jelenti, mértékegysége a voltszekundum per amperméter.

Az alfa és a béta jel a vonal és a határra merőleges egyenes közti szöget jelenti az egyes, illetve a kettes közegben, mértékegysége a radián.

<!-- eredeti
**Miről szól?** Pontosan ugyanaz a módszer és eredmény, mint az elektromos esetnél (1. rész 14. tétel), csak E helyett H, D helyett B és ε helyett μ szerepel. A határral párhuzamos H nem ugrik (ha nincs felületi áram), a merőleges B nem ugrik (mert nincs mágneses töltés). Ezért a vonalak megtörnek.
-->
## Miről szól

Pontosan ugyanaz a módszer és eredmény, mint az elektromos esetnél (első rész, tizennegyedik tétel), csak E helyett há, nagy dé helyett bé és epszilon helyett mű szerepel. A határral párhuzamos há nem ugrik (ha nincs felületi áram), a merőleges bé nem ugrik (mert nincs mágneses töltés). Ezért a vonalak megtörnek.

<!-- eredeti
**Tangenciális komponens.** A határt két oldalról ölelő lapos hurokra az 1. Maxwell-egyenlet: ∮H ds = (átfolyó áram) + d/dt(D fluxusa). A hurkot a határra lapítva a rövid oldalak eltűnnek, és a körbezárt felület is, így a jobb oldal is (feltéve, hogy a határon **nincs felületi áram**):
-->
## Tangenciális komponens

A határt két oldalról ölelő lapos hurokra az első {{Maxwell|mekszvel}}-egyenlet: há skalárszorzat dé es zárt görbe menti integrálja egyenlő az átfolyó áram plusz dé per dé té, zárójelben a nagy dé fluxusa. [[pause 500]] A hurkot a határra lapítva a rövid oldalak eltűnnek, és a körbezárt felület is, így a jobb oldal is (feltéve, hogy a határon nincs felületi áram):

<!-- eredeti
```latex
\int_A^B\left(\vec H_2 - \vec H_1\right)d\vec s = 0 \;\Rightarrow\; H_{t2} = H_{t1}, \qquad \frac{B_{1t}}{B_{2t}} = \frac{\mu_1}{\mu_2}
```
-->
Integrál az á ponttól a bé pontig, zárójelben há kettő vektor mínusz há egy vektor, skalárszorzat dé es vektor, egyenlő nulla. [[pause 500]]

Ebből következik, hogy há té kettő egyenlő há té egy, továbbá bé egy té per bé kettő té egyenlő mű egy per mű kettő. [[pause 500]]

<!-- eredeti
**Normális komponens.** Lapos doboz a határon, a mágneses Gauss-törvény (∮B dA = 0). Lapítva a palást eltűnik, a két lap fluxusa egyenlő és ellentétes:
-->
## Normális komponens

Lapos doboz a határon, a mágneses {{Gauss|gausz}}-törvény (bé skalárszorzat dé á zárt felületi integrálja egyenlő nulla). [[pause 500]] Lapítva a palást eltűnik, a két lap fluxusa egyenlő és ellentétes:

<!-- eredeti
```latex
B_{n2} = B_{n1} \qquad \mu_1H_{1n} = \mu_2H_{2n} \;\Rightarrow\; \frac{H_{1n}}{H_{2n}} = \frac{\mu_2}{\mu_1}
```
-->
Bé en kettő egyenlő bé en egy, és mű egy szorozva há egy en egyenlő mű kettő szorozva há kettő en. [[pause 500]]

Ebből következik, hogy há egy en per há kettő en egyenlő mű kettő per mű egy. [[pause 500]]

<!-- eredeti
(Itt nincs „felületi töltés” tag, mert mágneses töltés nincs.)
-->
(Itt nincs felületi töltés tag, mert mágneses töltés nincs.)

<!-- eredeti
**Törési törvény** (tangens = párhuzamos/merőleges komponens):
-->
## Törési törvény

Tangens egyenlő párhuzamos per merőleges komponens. [[pause 500]]

<!-- eredeti
```latex
\frac{\operatorname{tg}\alpha}{\operatorname{tg}\beta} = \frac{H_{1t}/H_{1n}}{H_{2t}/H_{2n}} = \frac{H_{2n}}{H_{1n}} = \frac{\mu_1}{\mu_2}
```
-->
Tangens alfa per tangens béta egyenlő egy tört, a számláló há egy té per há egy en, a nevező há kettő té per há kettő en. [[pause 500]]

Ez egyenlő há kettő en per há egy en, ami egyenlő mű egy per mű kettő. [[pause 500]]

<!-- eredeti
B-re ugyanez jön ki. Következmény: a nagy μ-jű vasból a vonalak szinte merőlegesen lépnek ki a levegőbe.
-->
Bé-re ugyanez jön ki. Következmény: a nagy mű-jű vasból a vonalak szinte merőlegesen lépnek ki a levegőbe.

<!-- eredeti
**Vizsgán:** hurok és doboz rajza; Hₜ₁ = Hₜ₂ (feltétel: nincs felületi áram); Bₙ₁ = Bₙ₂; tgα/tgβ = μ₁/μ₂.
-->
## Amit a vizsgán le kell írni

Hurok és doboz rajza; há té egy egyenlő há té kettő (feltétel: nincs felületi áram); bé en egy egyenlő bé en kettő; tangens alfa per tangens béta egyenlő mű egy per mű kettő. [[pause 500]]

<!-- eredeti
### 14. A mágneses térmennyiségek forrásai és örvényei
-->
# Második rész, tizennegyedik tétel. A mágneses térmennyiségek forrásai és örvényei

<!-- eredeti
| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| H, B, M | mágneses térerősség, indukció, mágnesezettség | A/m, T, A/m |
| j | makroszkopikus (vezetéki) áramsűrűség | A/m² |
| jₘ | molekuláris (atomon belüli) áramsűrűség | A/m² |
| ρₘ | effektív mágneses töltéssűrűség (északi pólusnál +, délinél −) | A/m² |
| μ₀ | vákuum permeabilitása | Vs/(Am) |
| rot, div | örvényesség, forrásosság |  |
-->
## Jelölések

A há, a bé és az em jel a mágneses térerősséget, az indukciót és a mágnesezettséget jelenti, mértékegységük az amper per méter, a tesla és az amper per méter.

A jé jel a makroszkopikus (vezetéki) áramsűrűséget jelenti, mértékegysége az amper per négyzetméter.

A jé em jel a molekuláris (atomon belüli) áramsűrűséget jelenti, mértékegysége az amper per négyzetméter.

A ró em jel az effektív mágneses töltéssűrűséget jelenti (északi pólusnál pozitív, délinél negatív előjelű), mértékegysége az amper per négyzetméter.

A mű nulla jel a vákuum permeabilitását jelenti, mértékegysége a voltszekundum per amperméter.

A rotáció és a divergencia jel az örvényességet, illetve a forrásosságot jelenti.

<!-- eredeti
**Miről szól?** Összeszedjük, mi kelti a három mágneses mennyiség örvényeit (ami köré „tekerednek”) és forrásait (amiből „kiindulnak”). Az örvényeket áramok keltik, a forrásokat a mágneses pólusok. A B-nek nincs forrása, a H-nak és M-nek viszont a pólusoknál van, ellentétes előjellel. Ebből jön ki a meglepő eredmény: egy állandó mágnes belsejében H és M ellentétes irányú.
-->
## Miről szól

Összeszedjük, mi kelti a három mágneses mennyiség örvényeit (ami köré tekerednek) és forrásait (amiből kiindulnak). Az örvényeket áramok keltik, a forrásokat a mágneses pólusok. A bé-nek nincs forrása, a há-nak és em-nek viszont a pólusoknál van, ellentétes előjellel. Ebből jön ki a meglepő eredmény: egy állandó mágnes belsejében há és em ellentétes irányú.

<!-- eredeti
**Örvények** (stacionárius esetben):
-->
## Örvények (stacionárius esetben)

<!-- eredeti
```latex
\operatorname{rot}\vec H = \vec j \qquad \operatorname{rot}\vec M = \vec j_m \qquad \operatorname{rot}\vec B = \mu_0\operatorname{rot}\left(\vec H + \vec M\right) = \mu_0\left(\vec j + \vec j_m\right)
```
-->
Rotáció há vektor egyenlő jé vektor. [[pause 500]]

Rotáció em vektor egyenlő jé em vektor. [[pause 500]]

Rotáció bé vektor egyenlő mű nulla szorozva rotáció, zárójelben há vektor plusz em vektor, ami egyenlő mű nulla szorozva, zárójelben jé vektor plusz jé em vektor. [[pause 500]]

<!-- eredeti
H örvényeit a vezetékekben folyó áramok, M örvényeit a molekuláris áramok, B-éit mindkettő kelti.
-->
Há örvényeit a vezetékekben folyó áramok, em örvényeit a molekuláris áramok, bé-éit mindkettő kelti.

<!-- eredeti
**Források:**
-->
## Források

<!-- eredeti
```latex
\operatorname{div}\vec M = -\rho_m \qquad \operatorname{div}\vec B = 0 \;\xrightarrow{\ B = \mu_0(H+M)\ }\; \operatorname{div}\vec H = -\operatorname{div}\vec M = \rho_m
```
-->
Divergencia em vektor egyenlő mínusz ró em. [[pause 500]]

Divergencia bé vektor egyenlő nulla. [[pause 500]]

A bé egyenlő mű nulla szorozva, zárójelben há plusz em összefüggés felhasználásával ebből következik, hogy divergencia há vektor egyenlő mínusz divergencia em vektor, ami egyenlő ró em. [[pause 500]]

<!-- eredeti
|  | Örvényét kelti | Forrása |
| --- | --- | --- |
| H | makroszkopikus áram (j) | mágneses pólusok (ρₘ) |
| M | molekuláris áram (jₘ) | pólusok ellentétes előjellel (−ρₘ) |
| B | mindkettő, μ₀(j + jₘ) | nincs |
-->
A há örvényét a makroszkopikus áram (jé) kelti, forrása a mágneses pólusok (ró em).

Az em örvényét a molekuláris áram (jé em) kelti, forrása a pólusok ellentétes előjellel (mínusz ró em).

A bé örvényét mindkettő kelti, vagyis mű nulla szorozva, zárójelben jé plusz jé em; forrása nincs. [[pause 500]]

<!-- eredeti
**Következmény:** egy állandó mágnes két pólusa között H és M vonalai ellentétes irányba futnak. A lineáris M = χH ebből negatív χ-t adna, holott ferromágnesre χ nagy pozitív: nemlineáris anyagnál a szuszceptibilitás nem így értendő (16. tétel). Általában három dolog kelt H teret: az áramok és az eltolási áram (örvényes rész), valamint a mágneses pólusok (forrásos rész).
-->
## Következmény

Egy állandó mágnes két pólusa között há és em vonalai ellentétes irányba futnak. A lineáris em egyenlő khí szorozva há összefüggés ebből negatív khí-t adna, holott ferromágnesre khí nagy pozitív: nemlineáris anyagnál a szuszceptibilitás nem így értendő (tizenhatodik tétel). [[pause 500]] Általában három dolog kelt há teret: az áramok és az eltolási áram (örvényes rész), valamint a mágneses pólusok (forrásos rész).

<!-- eredeti
(Példa a jegyzetből: egyenletesen mágnesezett hasb felső lapján M hirtelen nullára esik, ott rot M ≠ 0, vagyis ott folynak a molekuláris áramok; a póluslapokon viszont M forrásos, de nem örvényes.)
-->
Példa a jegyzetből: egyenletesen mágnesezett hasáb felső lapján em hirtelen nullára esik, ott rotáció em nem egyenlő nulla, vagyis ott folynak a molekuláris áramok; a póluslapokon viszont em forrásos, de nem örvényes. [[pause 500]]

<!-- eredeti
**Vizsgán:** a három rot és a három div egyenlet, div H = ρₘ levezetése; a táblázat; H és M ellentétes a mágnesben; H három forrása.
-->
## Amit a vizsgán le kell írni

A három rotáció és a három divergencia egyenlet, a divergencia há egyenlő ró em összefüggés levezetése; a táblázat; há és em ellentétes a mágnesben; há három forrása. [[pause 500]]


<!-- eredeti
### 15. Lemágnesező tér, állandó mágnesek
-->
# Második rész, tizenötödik tétel. Lemágnesező tér, állandó mágnesek

<!-- eredeti
| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| Hₐ | alkalmazott (külső) mágneses tér | A/m |
| H\_d | lemágnesező tér: a test saját pólusai által keltett tér | A/m |
| H\_in | a tényleges tér az anyag belsejében | A/m |
| M | mágnesezettség | A/m |
| N | lemágnesezési tényező (csak az alaktól függ, 0 és 1 között) | nincs |
| Nₓ, N\_y, N\_z | lemágnesezési tényező a három főtengely irányában | nincs |
| B | mágneses indukció | T |
| μ₀ | vákuum permeabilitása | Vs/(Am) |
-->
## Jelölések

A H á jel az alkalmazott, vagyis külső mágneses teret jelenti, mértékegysége az amper per méter.

A H dé jel a lemágnesező teret jelenti, vagyis a test saját pólusai által keltett teret, mértékegysége az amper per méter.

A H in jel a tényleges teret jelenti az anyag belsejében, mértékegysége az amper per méter.

Az M jel a mágnesezettséget jelenti, mértékegysége az amper per méter.

Az N jel a lemágnesezési tényezőt jelenti, amely csak az alaktól függ, és nulla és egy között van; mértékegység nélküli.

Az N iksz, N ipszilon és N zé jel a lemágnesezési tényezőt jelenti a három főtengely irányában, mértékegység nélküli.

A B jel a mágneses indukciót jelenti, mértékegysége a tesla.

A mű nulla jel a vákuum permeabilitását jelenti, mértékegysége a volt szekundum per amper méter.

<!-- eredeti
**Miről szól?** Ha egy anyagot felmágnesezünk, a két végén mágneses pólusok alakulnak ki, és ezek saját teret keltenek. Ez a saját tér bent mindig a mágnesezettség ellen mutat, tehát gyengíti a teret: ez a lemágnesező tér (ugyanaz, mint a depolarizáció az elektromos esetben). Az, hogy mennyire erős, csak a test alakjától függ: egy hosszú tűben szinte nincs, egy lapos korongban nagyon erős.
-->
## Miről szól

Ha egy anyagot felmágnesezünk, a két végén mágneses pólusok alakulnak ki, és ezek saját teret keltenek. Ez a saját tér bent mindig a mágnesezettség ellen mutat, tehát gyengíti a teret: ez a lemágnesező tér (ugyanaz, mint a depolarizáció az elektromos esetben). Az, hogy mennyire erős, csak a test alakjától függ: egy hosszú tűben szinte nincs, egy lapos korongban nagyon erős.

<!-- eredeti
**A tényleges belső tér.** Mivel a terek összeadhatók, bent az alkalmazott és a saját tér összege van:

```latex
\vec H_{in} = \vec H_a + \vec H_d
```
-->
## A tényleges belső tér

Mivel a terek összeadhatók, bent az alkalmazott és a saját tér összege van:

A H in vektor egyenlő a H á vektor plusz a H dé vektor. [[pause 500]]

<!-- eredeti
Paramágneses vagy lágy ferromágneses anyagban M a külső térrel egyirányú lesz, H\_d pedig ellentétes vele, ezért bent kisebb a tér, mint vákuumban volt: H\_in < Hₐ.
-->
Paramágneses vagy lágy ferromágneses anyagban M a külső térrel egyirányú lesz, H dé pedig ellentétes vele, ezért bent kisebb a tér, mint vákuumban volt: H in kisebb, mint H á. [[pause 500]]

<!-- eredeti
**Lemágnesezési tényező.** Általában a tér a testben nem homogén és nehéz számolni. Ellipszoid alakú testnél viszont (ha egy főtengelye a külső térrel párhuzamos) bent minden homogén, és a lemágnesező tér arányos a mágnesezettséggel:

```latex
\vec H_d = -N\vec M \qquad N_x + N_y + N_z = 1
```
-->
## Lemágnesezési tényező

Általában a tér a testben nem homogén és nehéz számolni. Ellipszoid alakú testnél viszont (ha egy főtengelye a külső térrel párhuzamos) bent minden homogén, és a lemágnesező tér arányos a mágnesezettséggel:

A H dé vektor egyenlő mínusz en szorozva az M vektor. [[pause 500]]
Továbbá N iksz plusz N ipszilon plusz N zé egyenlő egy. [[pause 500]]

<!-- eredeti
Gömbnél a szimmetria miatt mindhárom egyforma, tehát N = 1/3, H\_d = −M/3.
-->
Gömbnél a szimmetria miatt mindhárom egyforma, tehát en egyenlő egy harmad, és H dé egyenlő mínusz M per három. [[pause 500]]

<!-- eredeti
**Gömb alakú állandó mágnes** külső tér nélkül (Hₐ = 0, tehát H\_in = H\_d). A B = μ₀(H + M) képletből:

```latex
\frac{\vec B}{\mu_0} = \vec H_d + \vec M = -\frac13\vec M + \vec M = \frac23\vec M = -2\vec H_d
```
-->
## Gömb alakú állandó mágnes

Gömb alakú állandó mágnes külső tér nélkül: H á egyenlő nulla, tehát H in egyenlő H dé. [[pause 500]]
A bé egyenlő mű nulla szorozva, zárójelben H plusz M képletből:

Bé vektor per mű nulla egyenlő H dé vektor plusz M vektor. [[pause 500]]
Ez egyenlő mínusz egy harmad M vektor plusz M vektor. [[pause 500]]
Ez egyenlő kétharmad M vektor. [[pause 500]]
Ez pedig egyenlő mínusz kettő szorozva H dé vektor. [[pause 500]]

<!-- eredeti
A mágnes belsejében tehát H ellentétes irányú B-vel (és M-mel), és fele akkora. Az északi pólus H-nak forrása, M-nek nyelője, a déli fordítva. A mágnesen kívül (vákuumban) H és B/μ₀ megegyezik.
-->
A mágnes belsejében tehát H ellentétes irányú bé-vel (és M-mel), és fele akkora. Az északi pólus H-nak forrása, M-nek nyelője, a déli fordítva. A mágnesen kívül (vákuumban) H és bé per mű nulla megegyezik. [[pause 500]]

<!-- eredeti
**Határesetek:**
-->
## Határesetek

<!-- eredeti
| Alak | N a hossztengely (x) mentén | N keresztben |
| --- | --- | --- |
| gömb | 1/3 | 1/3 |
| hosszú tű | → 0 | → 1/2 |
| lapos korong (x a vastagság iránya) | → 1 | → 0 |
-->
Gömb esetén en a hossztengely, vagyis az iksz tengely mentén egy harmad, keresztben szintén egy harmad.

Hosszú tű esetén en a hossztengely mentén nullához tart, keresztben egy feléhez tart.

Lapos korong esetén, ahol iksz a vastagság iránya, en a hossztengely mentén egyhez tart, keresztben nullához tart.

<!-- eredeti
Magyarázat (energiaminimum): ha a gömböt x irányban nyújtjuk, a B vonalaknak a test mellett egyre több hely jut, ritkulnak; a határfeltételek miatt ezért a H is ritkul a test mellett és benne is, tehát Nₓ → 0. (Különben a nagyon hosszú test mellett óriási térfogatban lenne erős tér, és divergens lenne az energia.) Lapításnál a nagy lapokon átmenő B-nek kell kicsinek lennie; B = μ₀(M − abs(H)) akkor minimális, ha H = M, vagyis Nₓ = 1.
-->
Magyarázat (energiaminimum): ha a gömböt iksz irányban nyújtjuk, a bé vonalaknak a test mellett egyre több hely jut, ritkulnak; a határfeltételek miatt ezért a H is ritkul a test mellett és benne is, tehát N iksz nullához tart. [[pause 500]]
(Különben a nagyon hosszú test mellett óriási térfogatban lenne erős tér, és divergens lenne az energia.) Lapításnál a nagy lapokon átmenő bé-nek kell kicsinek lennie; bé egyenlő mű nulla szorozva, zárójelben M mínusz H abszolút értéke, és ez akkor minimális, ha H egyenlő M, vagyis N iksz egyenlő egy. [[pause 500]]

<!-- eredeti
**Vizsgán:** a lemágnesező tér fogalma, H\_in = Hₐ + H\_d; miért kisebb bent a tér; H\_d = −NM, ΣN = 1; gömb állandó mágnes: N = 1/3, B/μ₀ = (2/3)M = −2H\_d; tű és korong.
-->
## Amit a vizsgán le kell írni

A lemágnesező tér fogalma, H in egyenlő H á plusz H dé; miért kisebb bent a tér; H dé egyenlő mínusz en szorozva M, és az en tényezők összege egy; gömb állandó mágnes: en egyenlő egy harmad, bé per mű nulla egyenlő kétharmad M, ami egyenlő mínusz kettő szorozva H dé; tű és korong. [[pause 500]]

<!-- eredeti
### 16. A hiszterézisgörbe korrekciója, alakanizotrópia, a szuszceptibilitás értelmezése
-->
# Második rész, tizenhatodik tétel. A hiszterézisgörbe korrekciója, alakanizotrópia, a szuszceptibilitás értelmezése

<!-- eredeti
| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| Hₐ | alkalmazott (mérhető, külső) tér | A/m |
| H\_in | a valódi tér az anyagban | A/m |
| M | mágnesezettség | A/m |
| N | lemágnesezési tényező | nincs |
| χ | szuszceptibilitás | nincs |
| χ\_true | valódi (az anyagra jellemző) szuszceptibilitás, H\_in-hez viszonyítva | nincs |
| χ\_meas | mért szuszceptibilitás, Hₐ-hoz viszonyítva (a minta alakja is benne van) | nincs |
-->
## Jelölések

A H á jel az alkalmazott, vagyis mérhető, külső teret jelenti, mértékegysége az amper per méter.

A H in jel a valódi teret jelenti az anyagban, mértékegysége az amper per méter.

Az M jel a mágnesezettséget jelenti, mértékegysége az amper per méter.

Az N jel a lemágnesezési tényezőt jelenti, mértékegység nélküli.

A khí jel a szuszceptibilitást jelenti, mértékegység nélküli.

A khí {{true|trú}} jel a valódi, az anyagra jellemző szuszceptibilitást jelenti, H in-hez viszonyítva; mértékegység nélküli.

A khí {{meas|méz}} jel a mért szuszceptibilitást jelenti, H á-hoz viszonyítva (a minta alakja is benne van); mértékegység nélküli.

<!-- eredeti
**Miről szól?** A lemágnesező tér miatt ugyanaz az anyag különböző alakú darabokban látszólag különböző mértékben mágnesezhető: egy tűt hosszanti irányban sokkal könnyebb, mint keresztben. Ez az **alakanizotrópia** (nem az anyag, hanem az alak miatt irányfüggő). Ezért amikor mérjük a hiszterézisgörbét (amit a külső tér függvényében tudunk), azt át kell számolni a valódi belső térre, hogy az anyagot jellemezze, ne a minta alakját. Ugyanígy meg kell különböztetni a mért és a valódi szuszceptibilitást.
-->
## Miről szól

A lemágnesező tér miatt ugyanaz az anyag különböző alakú darabokban látszólag különböző mértékben mágnesezhető: egy tűt hosszanti irányban sokkal könnyebb, mint keresztben. Ez az alakanizotrópia (nem az anyag, hanem az alak miatt irányfüggő). Ezért amikor mérjük a hiszterézisgörbét (amit a külső tér függvényében tudunk), azt át kell számolni a valódi belső térre, hogy az anyagot jellemezze, ne a minta alakját. Ugyanígy meg kell különböztetni a mért és a valódi szuszceptibilitást.

<!-- eredeti
**Alakanizotrópia.** A 15. tételből Hₐ = H\_in − H\_d = H\_in + NM. A kezdeti szakaszon a lineáris közelítéssel (M = χH\_in):

```latex
H_a = H_{in} + N\chi H_{in} = (1 + N\chi)\,H_{in}
```
-->
## Alakanizotrópia

A tizenötödik tételből H á egyenlő H in mínusz H dé, ami egyenlő H in plusz en szorozva M. [[pause 500]]
A kezdeti szakaszon a lineáris közelítéssel, ahol M egyenlő khí szorozva H in: [[pause 500]]

H á egyenlő H in plusz en szorozva khí szorozva H in, ami egyenlő, zárójelben egy plusz en khí, szorozva H in. [[pause 500]]

<!-- eredeti
- **Tű hosszban** (N = 0): Hₐ = H\_in, a belső tér egyenlő a külsővel.
- **Tű keresztben** (N = 1/2, pl. χ = 10): Hₐ = (1 + 10/2)H\_in = 6H\_in. Ugyanakkora mágnesezettséghez hatszor nagyobb külső tér kell, azaz keresztben a mért szuszceptibilitás a valódi hatoda. Nagyobb χ-nél még nagyobb az eltérés.
-->
- Tű hosszban, ahol en egyenlő nulla: H á egyenlő H in, a belső tér egyenlő a külsővel. [[pause 500]]
- Tű keresztben, ahol en egyenlő egy fél, és például khí egyenlő tíz: H á egyenlő, zárójelben egy plusz tíz per kettő, szorozva H in, ami hatszor H in. [[pause 500]] Ugyanakkora mágnesezettséghez hatszor nagyobb külső tér kell, azaz keresztben a mért szuszceptibilitás a valódi hatoda. Nagyobb khí-nél még nagyobb az eltérés.

<!-- eredeti
**A hiszterézisgörbe korrekciója.** Az M görbét kétféleképpen rajzolhatjuk: a külső Hₐ függvényében (ezt mérjük) vagy a belső H\_in függvényében. Ha N ≠ 0, a kettő az M = 0 pontokat kivéve eltér. A mértből a H\_in = Hₐ − NM összefüggéssel számoljuk ki a másodikat: ez a korrekció. A szakirodalomban megadott görbe általában már a korrigált, ami az anyagot írja le.
-->
## A hiszterézisgörbe korrekciója

Az M görbét kétféleképpen rajzolhatjuk: a külső H á függvényében (ezt mérjük) vagy a belső H in függvényében. Ha en nem egyenlő nulla, a kettő az M egyenlő nulla pontokat kivéve eltér. [[pause 500]]
A mértből a H in egyenlő H á mínusz en szorozva M összefüggéssel számoljuk ki a másodikat: ez a korrekció. [[pause 500]]
A szakirodalomban megadott görbe általában már a korrigált, ami az anyagot írja le.

<!-- eredeti
**A szuszceptibilitás értelmezése.** Nemlineáris anyagnál az M/H arány nem állandó, ezért inkább a görbe meredekségét használják (differenciális szuszceptibilitás):

```latex
\chi = \frac{dM}{dH}
```
-->
## A szuszceptibilitás értelmezése

Nemlineáris anyagnál az M per H arány nem állandó, ezért inkább a görbe meredekségét használják (differenciális szuszceptibilitás):

Khí egyenlő dé M per dé H. [[pause 500]]

<!-- eredeti
Ez viszont függ attól, hol vagyunk a görbén (pl. ideális állandó mágnes görbéje „kövér téglalap”, a meredekség szinte mindenhol 0). Egyértelműbb az origó körüli érték, és ott is két változat van:

```latex
\chi_{true} = \frac{M}{H_{in}}\bigg|_{M,H\to0} \qquad \chi_{meas} = \frac{M}{H_a}\bigg|_{M,H\to0}
```
-->
Ez viszont függ attól, hol vagyunk a görbén (például ideális állandó mágnes görbéje „kövér téglalap”, a meredekség szinte mindenhol nulla). Egyértelműbb az origó körüli érték, és ott is két változat van:

Khí {{true|trú}} egyenlő M per H in, abban a határesetben, amikor M és H nullához tart. [[pause 500]]
Khí {{meas|méz}} egyenlő M per H á, ugyanebben a határesetben, amikor M és H nullához tart. [[pause 500]]

<!-- eredeti
A kapcsolatuk: H\_in = Hₐ − NM-et beírva és M/Hₐ-val (= χ\_meas) egyszerűsítve:

```latex
\chi_{true} = \frac{M}{H_a - NM} = \frac{\chi_{meas}}{1 - N\chi_{meas}} \qquad\Longleftrightarrow\qquad \chi_{meas} = \frac{\chi_{true}}{1 + N\chi_{true}}
```
-->
A kapcsolatuk: H in egyenlő H á mínusz en szorozva M-et beírva, és M per H á-val, ami egyenlő khí {{meas|méz}}, egyszerűsítve: [[pause 500]]

Khí {{true|trú}} egyenlő egy tört, a számláló M, a nevező H á mínusz en szorozva M. [[pause 500]]
Ez egyenlő egy törttel, a számláló khí {{meas|méz}}, a nevező egy mínusz en szorozva khí {{meas|méz}}. [[pause 500]]
Ezzel egyenértékű, hogy khí {{meas|méz}} egyenlő egy tört, a számláló khí {{true|trú}}, a nevező egy plusz en szorozva khí {{true|trú}}. [[pause 500]]

<!-- eredeti
(A tűs példában χ\_true = 10, N = 1/2 esetén χ\_meas = 10/6, valóban hatoda.)
-->
(A tűs példában khí {{true|trú}} egyenlő tíz, en egyenlő egy fél esetén khí {{meas|méz}} egyenlő tíz per hat, valóban hatoda.) [[pause 500]]

<!-- eredeti
**Vizsgán:** Hₐ = H\_in + NM = (1 + Nχ)H\_in; tű hosszban és keresztben; az alakanizotrópia fogalma; a korrekció lényege; dM/dH; χ\_true és χ\_meas kapcsolata.
-->
## Amit a vizsgán le kell írni

H á egyenlő H in plusz en szorozva M, ami egyenlő, zárójelben egy plusz en khí, szorozva H in; tű hosszban és keresztben; az alakanizotrópia fogalma; a korrekció lényege; dé M per dé H; khí {{true|trú}} és khí {{meas|méz}} kapcsolata. [[pause 500]]

<!-- eredeti
### 17. Mágneses skálarpotenciál. Mágneses körök, soros és párhuzamos kapcsolás
-->
# Második rész, tizenhetedik tétel. Mágneses skálarpotenciál. Mágneses körök, soros és párhuzamos kapcsolás

<!-- eredeti
| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| Uₘ | mágneses skálarpotenciál, „mágneses feszültség” | A |
| H | mágneses térerősség | A/m |
| N, I | a gerjesztő tekercs menetszáma és árama | -, A |
| εₘ = NI | mágneses gerjesztés (magnetomotoros erő), a „forrás” | A |
| Φ | mágneses fluxus, az „áram” szerepében | Vs |
| Rₘ | mágneses ellenállás | A/(Vs) |
| ℓ | egy test hossza a fluxus mentén | m |
| A | a test keresztmetszete | m² |
| μ | permeabilitás | Vs/(Am) |
-->
## Jelölések

Az U em jel a mágneses skálarpotenciált, a „mágneses feszültséget” jelenti, mértékegysége az amper.

A H jel a mágneses térerősséget jelenti, mértékegysége az amper per méter.

Az N és az I jel a gerjesztő tekercs menetszámát és áramát jelenti; a menetszám mértékegység nélküli, az áram mértékegysége az amper.

Az epszilon em jel, amely egyenlő en szorozva í, a mágneses gerjesztést (magnetomotoros erőt), a „forrást” jelenti, mértékegysége az amper.

A nagy fí jel a mágneses fluxust jelenti, az „áram” szerepében, mértékegysége a volt szekundum.

Az R em jel a mágneses ellenállást jelenti, mértékegysége az amper per volt szekundum.

A kézírásos el jel egy test hosszát jelenti a fluxus mentén, mértékegysége a méter.

Az A jel a test keresztmetszetét jelenti, mértékegysége a négyzetméter.

A mű jel a permeabilitást jelenti, mértékegysége a volt szekundum per amper méter.

<!-- eredeti
**Miről szól?** Ahol nincs áram, a mágneses tér örvénymentes, így ugyanúgy rendelhető hozzá potenciál, mint az elektrosztatikus térhez. Ebből egy hasznos analógia jön: a vasmagos mágneses körök úgy számolhatók, mint az áramkörök. A tekercs gerjesztése (NI) a feszültségforrás, a fluxus az áram, a vas és a légrés pedig ellenállások; még Ohm- és Kirchhoff-törvény is van.
-->
## Miről szól

Ahol nincs áram, a mágneses tér örvénymentes, így ugyanúgy rendelhető hozzá potenciál, mint az elektrosztatikus térhez. Ebből egy hasznos analógia jön: a vasmagos mágneses körök úgy számolhatók, mint az áramkörök. A tekercs gerjesztése (en í) a feszültségforrás, a fluxus az áram, a vas és a légrés pedig ellenállások; még {{Ohm|óm}}- és {{Kirchhoff|kirhhoff}}-törvény is van.

<!-- eredeti
**Mágneses skálarpotenciál.** Ha nincs áram és változó elektromos tér, rot H = 0, tehát (potenciálos mezők tétele) létezik Uₘ. Egy P₀ pontban nullának választva:

```latex
\vec H = -\operatorname{grad}U_m \qquad U_m(A) = \int_A^{P_0}\vec H\,d\vec s \qquad \oint\vec H\,d\vec s = \sum U_m = 0
```
-->
## Mágneses skálarpotenciál

Ha nincs áram és változó elektromos tér, rotáció H egyenlő nulla, tehát (potenciálos mezők tétele) létezik U em. [[pause 500]]
Egy pé nulla pontban nullának választva:

A H vektor egyenlő mínusz gradiens U em. [[pause 500]]
U em az A pontban egyenlő integrál A-tól pé nulláig H vektor skalárszorzat dé es vektor. [[pause 500]]
H vektor skalárszorzat dé es vektor zárt görbe menti integrálja egyenlő az U em értékek összegével, ami egyenlő nulla. [[pause 500]]

<!-- eredeti
Ritkábban használják, mint az elektromos feszültséget, mert nincs olyan szemléletes jelentése (nem munka). Ha áram is van, a hurok mentén nem 0 az összeg, hanem a körülzárt gerjesztés (gerjesztési törvény):

```latex
\sum U_m = \varepsilon_m = NI
```
-->
Ritkábban használják, mint az elektromos feszültséget, mert nincs olyan szemléletes jelentése (nem munka). Ha áram is van, a hurok mentén nem nulla az összeg, hanem a körülzárt gerjesztés (gerjesztési törvény):

Az U em értékek összege egyenlő epszilon em, ami egyenlő en szorozva í. [[pause 500]]

<!-- eredeti
**Mágneses ellenállás és Ohm-törvény.** Egy homogén, ℓ hosszú, A keresztmetszetű testben Uₘ = Hℓ és Φ = BA = μHA. A hányadosuk:

```latex
R_m = \frac{U_m}{\Phi} = \frac{H\ell}{\mu HA} = \frac{\ell}{\mu A} \qquad U_{m,i} = R_{m,i}\,\Phi
```
-->
## Mágneses ellenállás és {{Ohm|óm}}-törvény

Egy homogén, el hosszú, á keresztmetszetű testben U em egyenlő H szorozva el, és nagy fí egyenlő bé szorozva á, ami egyenlő mű szorozva H szorozva á. [[pause 500]]
A hányadosuk:

R em egyenlő U em per nagy fí. [[pause 500]]
Ez egyenlő egy törttel, a számláló H szorozva el, a nevező mű szorozva H szorozva á. [[pause 500]]
Ez egyszerűsítve egyenlő el per, zárójelben mű szorozva á. [[pause 500]]
Az i-edik elemre U em i egyenlő R em i szorozva nagy fí. [[pause 500]]

<!-- eredeti
(Pont olyan, mint az R = ρℓ/A, csak ρ helyett 1/μ.)
-->
(Pont olyan, mint az er egyenlő ró szorozva el per á, csak ró helyett egy per mű.) [[pause 500]]

<!-- eredeti
**Csomóponti törvény.** A mágneses Gauss-törvény (∮B dA = 0) miatt egy elágazásba befutó és kifutó fluxusok összege 0 (mint az áramoknál a kontinuitás miatt):

```latex
\sum_k\Phi_k = 0
```
-->
## Csomóponti törvény

A mágneses {{Gauss|gausz}}-törvény (bé skalárszorzat dé á zárt felületi integrálja nulla) miatt egy elágazásba befutó és kifutó fluxusok összege nulla (mint az áramoknál a kontinuitás miatt):

Szumma ká szerint nagy fí ká egyenlő nulla. [[pause 500]]

<!-- eredeti
**Soros és párhuzamos kapcsolás.** Egymáshoz erősített vastestekben ugyanaz a fluxus halad végig (soros kapcsolás), a mágneses feszültségek összeadódnak. Elágazó körben (párhuzamos) a feszültség közös, a fluxus megoszlik:

```latex
\text{soros: } R_{m,eredő} = \sum_n R_{m,n} \qquad \text{párhuzamos: } \frac{1}{R_{m,eredő}} = \sum_n\frac{1}{R_{m,n}}
```
-->
## Soros és párhuzamos kapcsolás

Egymáshoz erősített vastestekben ugyanaz a fluxus halad végig (soros kapcsolás), a mágneses feszültségek összeadódnak. Elágazó körben (párhuzamos) a feszültség közös, a fluxus megoszlik:

Soros kapcsolásnál az eredő R em egyenlő szumma en szerint R em en. [[pause 500]]
Párhuzamos kapcsolásnál egy per eredő R em egyenlő szumma en szerint egy per R em en. [[pause 500]]

<!-- eredeti
**Légrés:** a levegő permeabilitása nagyságrendekkel kisebb a vasénál, ezért még egy vékony légrés is nagyon megnöveli a kör mágneses ellenállását, és sokkal nagyobb áram kell ugyanakkora fluxushoz. (A légrésnél pólusok jelennek meg, amelyek lemágnesező teret keltenek.)
-->
## Légrés

A levegő permeabilitása nagyságrendekkel kisebb a vasénál, ezért még egy vékony légrés is nagyon megnöveli a kör mágneses ellenállását, és sokkal nagyobb áram kell ugyanakkora fluxushoz. (A légrésnél pólusok jelennek meg, amelyek lemágnesező teret keltenek.)

<!-- eredeti
**Vizsgán:** rot H = 0 feltétele, H = −grad Uₘ, ΣUₘ = 0 illetve NI; az analógia (NI ↔ feszültség, Φ ↔ áram); Rₘ = ℓ/(μA) levezetve; mágneses Ohm-törvény; ΣΦ = 0; soros és párhuzamos eredő; légrés hatása.
-->
## Amit a vizsgán le kell írni

A rotáció H egyenlő nulla feltétele, H egyenlő mínusz gradiens U em, az U em értékek összege nulla, illetve en í; az analógia (en í megfelel a feszültségnek, nagy fí megfelel az áramnak); R em egyenlő el per, zárójelben mű á, levezetve; mágneses {{Ohm|óm}}-törvény; a nagy fí értékek összege nulla; soros és párhuzamos eredő; légrés hatása. [[pause 500]]

<!-- eredeti
### 18. Elektromágneses hullámok szigetelőkben. A homogén hullámegyenlet
-->
# Második rész, tizennyolcadik tétel. Elektromágneses hullámok szigetelőkben. A homogén hullámegyenlet

<!-- eredeti
| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| E, D | elektromos térerősség, indukció | V/m, C/m² |
| H, B | mágneses térerősség, indukció | A/m, T |
| ε, μ | a közeg permittivitása és permeabilitása | As/(Vm), Vs/(Am) |
| j, ρ | áramsűrűség, töltéssűrűség (itt mindkettő 0) | A/m², C/m³ |
| Δ | Laplace-operátor: ∂²/∂x² + ∂²/∂y² + ∂²/∂z² (vektorra komponensenként) | 1/m² |
| ∂²/∂t² | második derivált az idő szerint | 1/s² |
-->
## Jelölések

Az E jel az elektromos térerősséget jelenti, mértékegysége a volt per méter.

A D jel az elektromos indukciót jelenti, mértékegysége a kulomb per négyzetméter.

A H jel a mágneses térerősséget jelenti, mértékegysége az amper per méter.

A B jel a mágneses indukciót jelenti, mértékegysége a tesla.

Az epszilon jel a közeg permittivitását jelenti, mértékegysége az amper szekundum per volt méter.

A mű jel a közeg permeabilitását jelenti, mértékegysége a volt szekundum per amper méter.

A j jel az áramsűrűséget jelenti, mértékegysége az amper per négyzetméter; itt értéke nulla.

A ró jel a töltéssűrűséget jelenti, mértékegysége a kulomb per köbméter; itt értéke szintén nulla.

A nagy delta jel a {{Laplace|laplasz}}-operátort jelenti: dé négyzet per dé iksz négyzet plusz dé négyzet per dé ipszilon négyzet plusz dé négyzet per dé zé négyzet, vektorra komponensenként; mértékegysége az egy per négyzetméter.

A dé négyzet per dé té négyzet jel a második deriváltat jelenti az idő szerint, mértékegysége az egy per szekundum négyzet.

<!-- eredeti
**Miről szól?** A Maxwell-egyenletekből kijön, hogy léteznek elektromágneses hullámok. A változó elektromos tér mágneses teret kelt (1. ME), a változó mágneses tér elektromosat (2. ME), és így egymást fenntartva terjednek. Ha a két egyenletet összefűzzük, mindkét térre egy-egy hullámegyenlet adódik, ugyanolyan alakú, mint egy rezgő húré.
-->
## Miről szól

A {{Maxwell|mekszvel}}-egyenletekből kijön, hogy léteznek elektromágneses hullámok. A változó elektromos tér mágneses teret kelt (első {{Maxwell|mekszvel}}-egyenlet), a változó mágneses tér elektromosat (második {{Maxwell|mekszvel}}-egyenlet), és így egymást fenntartva terjednek. Ha a két egyenletet összefűzzük, mindkét térre egy-egy hullámegyenlet adódik, ugyanolyan alakú, mint egy rezgő húré.

<!-- eredeti
**Feltételek:** vákuum vagy homogén, izotróp, lineáris szigetelő: nincs áram és töltés (j = 0, ρ = 0), D = εE és B = μH. Ekkor az első két Maxwell-egyenlet:

```latex
\operatorname{rot}\vec H = \frac{\partial\vec D}{\partial t} \qquad \operatorname{rot}\vec E = -\frac{\partial\vec B}{\partial t}
```
-->
## Feltételek

Vákuum vagy homogén, izotróp, lineáris szigetelő: nincs áram és töltés, vagyis j egyenlő nulla és ró egyenlő nulla, továbbá D egyenlő epszilon szorozva E, és bé egyenlő mű szorozva H. [[pause 500]]
Ekkor az első két {{Maxwell|mekszvel}}-egyenlet:

Rotáció H vektor egyenlő dé D vektor per dé té. [[pause 500]]
Rotáció E vektor egyenlő mínusz dé B vektor per dé té. [[pause 500]]

<!-- eredeti
**Levezetés a mágneses térre:**
-->
## Levezetés a mágneses térre

<!-- eredeti
1. Az első egyenlet rotációját vesszük (a hely és idő szerinti deriválás felcserélhető):

```latex
\operatorname{rot}\operatorname{rot}\vec H = \frac{\partial}{\partial t}\operatorname{rot}\vec D
```

2. A bal oldalra az azonosság: rot rot v = grad div v − Δv. A 4. ME szerint div B = 0, így div H = 0, az első tag kiesik.
3. A jobb oldalon D = εE, majd a 2. ME:

```latex
-\Delta\vec H = \varepsilon\frac{\partial}{\partial t}\operatorname{rot}\vec E = \varepsilon\frac{\partial}{\partial t}\left(-\frac{\partial\vec B}{\partial t}\right) = -\varepsilon\mu\frac{\partial^2\vec H}{\partial t^2}
```

4. Megkaptuk a hullámegyenletet a mágneses térre; ugyanígy (a 2. ME-ből indulva) az elektromosra:

```latex
\Delta\vec H = \varepsilon\mu\frac{\partial^2\vec H}{\partial t^2} \qquad\qquad \Delta\vec E = \varepsilon\mu\frac{\partial^2\vec E}{\partial t^2}
```
-->
- Első lépés. Az első egyenlet rotációját vesszük (a hely és idő szerinti deriválás felcserélhető): rotáció rotáció H vektor egyenlő a rotáció D vektor idő szerinti parciális deriváltjával. [[pause 500]]
- Második lépés. A bal oldalra az azonosság: rotáció rotáció vé egyenlő gradiens divergencia vé mínusz {{Laplace|laplasz}} vé. [[pause 500]] A negyedik {{Maxwell|mekszvel}}-egyenlet szerint divergencia bé egyenlő nulla, így divergencia H egyenlő nulla, az első tag kiesik. [[pause 500]]
- Harmadik lépés. A jobb oldalon D egyenlő epszilon szorozva E, majd a második {{Maxwell|mekszvel}}-egyenlet: [[pause 500]] Mínusz {{Laplace|laplasz}} H vektor egyenlő epszilon szorozva a rotáció E vektor idő szerinti parciális deriváltjával. [[pause 500]] Ez egyenlő epszilon szorozva a zárójelben álló mínusz dé B vektor per dé té idő szerinti parciális deriváltjával. [[pause 500]] Ez pedig egyenlő mínusz epszilon mű szorozva dé négyzet H vektor per dé té négyzet. [[pause 500]]
- Negyedik lépés. Megkaptuk a hullámegyenletet a mágneses térre; ugyanígy (a második {{Maxwell|mekszvel}}-egyenletből indulva) az elektromosra: [[pause 500]] {{Laplace|laplasz}} H vektor egyenlő epszilon mű szorozva dé négyzet H vektor per dé té négyzet. [[pause 500]] {{Laplace|laplasz}} E vektor egyenlő epszilon mű szorozva dé négyzet E vektor per dé té négyzet. [[pause 500]]

<!-- eredeti
Komponensenként kiírva pl. az x komponensre:

```latex
\frac{\partial^2 H_x}{\partial x^2} + \frac{\partial^2 H_x}{\partial y^2} + \frac{\partial^2 H_x}{\partial z^2} = \varepsilon\mu\frac{\partial^2 H_x}{\partial t^2}
```
-->
Komponensenként kiírva például az iksz komponensre:

Dé négyzet H iksz per dé iksz négyzet plusz dé négyzet H iksz per dé ipszilon négyzet plusz dé négyzet H iksz per dé zé négyzet egyenlő epszilon mű szorozva dé négyzet H iksz per dé té négyzet. [[pause 500]]

<!-- eredeti
A „homogén” itt azt jelenti, hogy az egyenletben nincs forrástag: a vizsgált helyen nincsenek töltések és áramok, a hullám nem itt keletkezik, csak áthalad. (Nem azonos azzal, hogy maga a közeg homogén, bár azt is feltettük.)
-->
A „homogén” itt azt jelenti, hogy az egyenletben nincs forrástag: a vizsgált helyen nincsenek töltések és áramok, a hullám nem itt keletkezik, csak áthalad. (Nem azonos azzal, hogy maga a közeg homogén, bár azt is feltettük.)

<!-- eredeti
**Vizsgán:** a feltételek; az 1. és 2. ME; a négy lépés (rot, azonosság és div H = 0, behelyettesítés); ΔH = εμ∂²H/∂t² és ΔE = εμ∂²E/∂t²; mit jelent itt a homogén.
-->
## Amit a vizsgán le kell írni

A feltételek; az első és a második {{Maxwell|mekszvel}}-egyenlet; a négy lépés (rotáció, azonosság és divergencia H egyenlő nulla, behelyettesítés); {{Laplace|laplasz}} H egyenlő epszilon mű szorozva dé négyzet H per dé té négyzet, és {{Laplace|laplasz}} E egyenlő epszilon mű szorozva dé négyzet E per dé té négyzet; mit jelent itt a homogén. [[pause 500]]

<!-- eredeti
### 19. Síkhullám megoldás, a fénysebesség. Transzverzalitás, Poynting-vektor
-->
# Második rész, tizenkilencedik tétel. Síkhullám megoldás, a fénysebesség. Transzverzalitás, {{Poynting|pojnting}}-vektor

<!-- eredeti
| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| E₀, H₀ | a térerősségek amplitúdója (csúcsértéke) | V/m, A/m |
| f | frekvencia | Hz = 1/s |
| λ | hullámhossz | m |
| c | terjedési sebesség (vákuumban a fénysebesség) | m/s |
| ω = 2πf | körfrekvencia | 1/s |
| k = 2π/λ | hullámszám (vektorként a terjedés irányába mutat) | 1/m |
| r | helyvektor | m |
| ε₀, μ₀ | vákuum permittivitása és permeabilitása | As/(Vm), Vs/(Am) |
| εᵣ, μᵣ | relatív permittivitás és permeabilitás | nincs |
| S | Poynting-vektor (energiaáramlás sűrűsége) | W/m² |
-->
## Jelölések

Az E nulla és a H nulla jel a térerősségek amplitúdóját, vagyis csúcsértékét jelenti; E nulla mértékegysége a volt per méter, H nulla mértékegysége az amper per méter.

Az f jel a frekvenciát jelenti, mértékegysége a hertz, ami egy per szekundum.

A lambda jel a hullámhosszt jelenti, mértékegysége a méter.

A c jel a terjedési sebességet jelenti (vákuumban a fénysebességet), mértékegysége a méter per szekundum.

Az omega jel, amely egyenlő kettő pí szorozva ef, a körfrekvenciát jelenti, mértékegysége az egy per szekundum.

A k jel, amely egyenlő kettő pí per lambda, a hullámszámot jelenti (vektorként a terjedés irányába mutat), mértékegysége az egy per méter.

Az r jel a helyvektort jelenti, mértékegysége a méter.

Az epszilon nulla és a mű nulla jel a vákuum permittivitását és permeabilitását jelenti; epszilon nulla mértékegysége az amper szekundum per volt méter, mű nulla mértékegysége a volt szekundum per amper méter.

Az epszilon er és a mű er jel a relatív permittivitást és permeabilitást jelenti, mértékegység nélküli.

Az S jel a {{Poynting|pojnting}}-vektort, vagyis az energiaáramlás sűrűségét jelenti, mértékegysége a watt per négyzetméter.

<!-- eredeti
**Miről szól?** A hullámegyenletnek megoldása a jól ismert szinuszos síkhullám. Ha visszahelyettesítjük, kijön, milyen gyorsan terjed: a közeg ε-jától és μ-jétől függ, vákuumban pont a fénysebesség. Az E és H egymásra és a terjedés irányára is merőleges (transzverzális hullám). A hullám energiát szállít, ennek áramlását és irányát a Poynting-vektor adja meg.
-->
## Miről szól

A hullámegyenletnek megoldása a jól ismert szinuszos síkhullám. Ha visszahelyettesítjük, kijön, milyen gyorsan terjed: a közeg epszilonjától és műjétől függ, vákuumban pont a fénysebesség. Az E és H egymásra és a terjedés irányára is merőleges (transzverzális hullám). A hullám energiát szállít, ennek áramlását és irányát a {{Poynting|pojnting}}-vektor adja meg.

<!-- eredeti
**Síkhullám megoldás.** Pozitív x irányba haladó hullám:

```latex
E = E_0\sin\left(2\pi\left(ft - \frac{x}{\lambda}\right)\right) \qquad H = H_0\sin\left(2\pi\left(ft - \frac{x}{\lambda}\right)\right)
```
-->
## Síkhullám megoldás

Pozitív iksz irányba haladó hullám:

E egyenlő E nulla szorozva szinusz, zárójelben kettő pí szorozva, zárójelben ef té mínusz iksz per lambda. [[pause 500]]
H egyenlő H nulla szorozva szinusz, zárójelben kettő pí szorozva, zárójelben ef té mínusz iksz per lambda. [[pause 500]]

<!-- eredeti
Visszahelyettesítve a hullámegyenletbe (a kétszeri x szerinti deriválás (2π/λ)²-et, a kétszeri t szerinti (2πf)²-et hoz ki):

```latex
\frac{1}{\lambda^2f^2} = \varepsilon\mu
```
-->
Visszahelyettesítve a hullámegyenletbe (a kétszeri iksz szerinti deriválás kettő pí per lambda négyzetét, a kétszeri té szerinti kettő pí ef négyzetét hozza ki):

Egy per, zárójelben lambda négyzet szorozva ef négyzet, egyenlő epszilon szorozva mű. [[pause 500]]

<!-- eredeti
**Fénysebesség.** A terjedési sebesség c = fλ, ebből:

```latex
c = f\lambda = \frac{1}{\sqrt{\varepsilon\mu}} \qquad c_0 = \frac{1}{\sqrt{\varepsilon_0\mu_0}} = 3\cdot10^8\,\frac{\mathrm m}{\mathrm s} \qquad \frac{c_0}{c_{közeg}} = \sqrt{\varepsilon_r\mu_r}
```
-->
## Fénysebesség

A terjedési sebesség cé egyenlő ef szorozva lambda, ebből: [[pause 500]]

Cé egyenlő ef lambda, ami egyenlő egy per négyzetgyök epszilon mű. [[pause 500]]
Cé nulla egyenlő egy per négyzetgyök epszilon nulla mű nulla, ami háromszor tíz a nyolcadikon méter per szekundum. [[pause 500]]
Cé nulla per cé közeg egyenlő négyzetgyök epszilon er szorozva mű er. [[pause 500]]

<!-- eredeti
A vákuumbeli érték az ismert állandókból (ε₀ = 1/(4π·9·10⁹), μ₀ = 4π·10⁻⁷) kiszámolható, és egyezik a mért fénysebességgel. Anyagban lassabb (minél nagyobb εᵣμᵣ, annál lassabb). Más alakban, illetve tetszőleges irányba haladó hullámra:

```latex
E = E_0\sin(\omega t - kx) \qquad \vec E = \vec E_0\sin\left(\omega t - \vec k\vec r\right) \qquad \vec H = \vec H_0\sin\left(\omega t - \vec k\vec r\right)
```
-->
A vákuumbeli érték az ismert állandókból kiszámolható, ahol epszilon nulla egyenlő egy per, zárójelben négy pí szorozva kilenc szorozva tíz a kilencediken, és mű nulla egyenlő négy pí szorozva tíz a mínusz hetediken; és egyezik a mért fénysebességgel. [[pause 500]]
Anyagban lassabb (minél nagyobb epszilon er szorozva mű er, annál lassabb). Más alakban, illetve tetszőleges irányba haladó hullámra:

E egyenlő E nulla szorozva szinusz, zárójelben omega té mínusz ká iksz. [[pause 500]]
E vektor egyenlő E nulla vektor szorozva szinusz, zárójelben omega té mínusz ká vektor skalárszorzat er vektor. [[pause 500]]
H vektor egyenlő H nulla vektor szorozva szinusz, zárójelben omega té mínusz ká vektor skalárszorzat er vektor. [[pause 500]]

<!-- eredeti
Az azonos fázisú pontok síkokat alkotnak, ezért síkhullám.
-->
Az azonos fázisú pontok síkokat alkotnak, ezért síkhullám.

<!-- eredeti
**Transzverzalitás.** Az E és a H merőleges a terjedés irányára, és egymásra is (pl. E az x, H az y tengely mentén rezeg, a hullám z irányba megy). Nem függetlenül, hanem együtt terjednek, és az elektromos és mágneses energiasűrűség egyenlő:

```latex
\mu H^2 = \varepsilon E^2 \qquad \frac{E}{H} = \sqrt{\frac{\mu_0}{\varepsilon_0}} \approx 377\,\Omega
```
-->
## Transzverzalitás

Az E és a H merőleges a terjedés irányára, és egymásra is (például E az iksz, H az ipszilon tengely mentén rezeg, a hullám zé irányba megy). Nem függetlenül, hanem együtt terjednek, és az elektromos és mágneses energiasűrűség egyenlő:

Mű szorozva H négyzet egyenlő epszilon szorozva E négyzet. [[pause 500]]
E per H egyenlő négyzetgyök mű nulla per epszilon nulla, ami közelítőleg háromszázhetvenhét óm. [[pause 500]]

<!-- eredeti
A 377 Ω a vákuum hullámellenállása (impedanciája).
-->
A háromszázhetvenhét óm a vákuum hullámellenállása (impedanciája).

<!-- eredeti
**Poynting-vektor.** Megadja, mennyi energia megy át 1 m²-en 1 s alatt (pillanatnyi érték), és az energiaáramlás irányába mutat. Az időátlaga (a hullám intenzitása) az amplitúdókkal:

```latex
\vec S = \vec E\times\vec H \qquad S_{átlag} = \frac12 E_0H_0
```
-->
## {{Poynting|pojnting}}-vektor

Megadja, mennyi energia megy át egy négyzetméteren egy szekundum alatt (pillanatnyi érték), és az energiaáramlás irányába mutat. Az időátlaga (a hullám intenzitása) az amplitúdókkal:

Az S vektor egyenlő E vektor vektoriálisan szorozva H vektor. [[pause 500]]
S átlag egyenlő egy fél szorozva E nulla szorozva H nulla. [[pause 500]]

<!-- eredeti
Vákuumban a sugárzás c sebességgel terjed, energiát és impulzust szállít; c minden frekvencián ugyanaz, ezért f és λ fordítottan arányos.
-->
Vákuumban a sugárzás cé sebességgel terjed, energiát és impulzust szállít; cé minden frekvencián ugyanaz, ezért ef és lambda fordítottan arányos.

<!-- eredeti
**Vizsgán:** síkhullám alakja; behelyettesítve 1/(λ²f²) = εμ; c = 1/√(εμ), vákuumban 3·10⁸ m/s; ω, k alak; transzverzalitás rajzzal; μH² = εE², 377 Ω; S = E × H, S\_átlag = ½E₀H₀.
-->
## Amit a vizsgán le kell írni

Síkhullám alakja; behelyettesítve egy per, zárójelben lambda négyzet ef négyzet, egyenlő epszilon mű; cé egyenlő egy per négyzetgyök epszilon mű, vákuumban háromszor tíz a nyolcadikon méter per szekundum; omega, ká alak; transzverzalitás rajzzal; mű H négyzet egyenlő epszilon E négyzet, háromszázhetvenhét óm; S egyenlő E vektoriálisan szorozva H, S átlag egyenlő egy fél E nulla H nulla. [[pause 500]]

<!-- eredeti
### 20. Az energiatétel elektromágneses térben
-->
# Második rész, huszadik tétel. Az energiatétel elektromágneses térben

<!-- eredeti
| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| S = E × H | Poynting-vektor | W/m² |
| w\_EM | az elektromágneses tér energiasűrűsége (½εE² + ½μH²) | J/m³ |
| W\_EM | a teljes térenergia egy V térfogatban | J |
| j | áramsűrűség | A/m² |
| jᵥ | vezetési áramsűrűség | A/m² |
| ρv | konvektív áram (mozgó töltések, pl. ionok) | A/m² |
| Eᵢ | idegen (pl. kémiai, a forrásban ható) térerősség | V/m |
| σ | fajlagos vezetőképesség | S/m |
| v | a vezető vagy töltés sebessége | m/s |
| V, f | térfogat, az azt határoló zárt felület | m³, m² |
-->
## Jelölések

Az S jel, amely egyenlő E vektoriálisan szorozva H, a {{Poynting|pojnting}}-vektort jelenti, mértékegysége a watt per négyzetméter.

A kis w E M jel az elektromágneses tér energiasűrűségét jelenti, ami egy fél epszilon E négyzet plusz egy fél mű H négyzet; mértékegysége a {{Joule|dzsúl}} per köbméter.

A nagy W E M jel a teljes térenergiát jelenti egy V térfogatban, mértékegysége a {{Joule|dzsúl}}.

A j jel az áramsűrűséget jelenti, mértékegysége az amper per négyzetméter.

A j vé jel a vezetési áramsűrűséget jelenti, mértékegysége az amper per négyzetméter.

A ró vé jel a konvektív áramot jelenti (mozgó töltések, például ionok), mértékegysége az amper per négyzetméter.

Az E í jel az idegen (például kémiai, a forrásban ható) térerősséget jelenti, mértékegysége a volt per méter.

A szigma jel a fajlagos vezetőképességet jelenti, mértékegysége a {{siemens|szímensz}} per méter.

A v jel a vezető vagy töltés sebességét jelenti, mértékegysége a méter per szekundum.

A nagy V jel a térfogatot jelenti, mértékegysége a köbméter; az f jel az azt határoló zárt felületet jelenti, mértékegysége a négyzetméter.

<!-- eredeti
**Miről szól?** Az elektromágneses tér energiájára vonatkozó mérleg, mint egy pénztárca: egy térrészben a tér energiája akkor csökken, ha energia áramlik ki a határán (ezt a Poynting-vektor méri), vagy ha a tér munkát végez a töltéseken (pl. Joule-hő keletkezik). Az áramforrások pedig növelik. Ez az energiamegmaradás az elektromágneses térre.
-->
## Miről szól

Az elektromágneses tér energiájára vonatkozó mérleg, mint egy pénztárca: egy térrészben a tér energiája akkor csökken, ha energia áramlik ki a határán (ezt a {{Poynting|pojnting}}-vektor méri), vagy ha a tér munkát végez a töltéseken (például {{Joule|dzsúl}}-hő keletkezik). Az áramforrások pedig növelik. Ez az energiamegmaradás az elektromágneses térre.

<!-- eredeti
**Levezetés:**
-->
## Levezetés

<!-- eredeti
1. Az 1. Maxwell-egyenletet szorozzuk −E-vel, a 2.-at H-val:

```latex
-\vec E\operatorname{rot}\vec H = -\vec E\frac{\partial\vec D}{\partial t} - \vec E\vec j \qquad \vec H\operatorname{rot}\vec E = -\vec H\frac{\partial\vec B}{\partial t}
```

2. Összeadjuk, és a bal oldalra az azonosságot használjuk: H rot E − E rot H = div(E × H).
3. Lineáris, időben állandó anyagban az időderiváltak energiasűrűség-változásként írhatók:

```latex
\vec H\frac{\partial\vec B}{\partial t} = \frac{\partial}{\partial t}\left(\frac12\mu H^2\right) \qquad \vec E\frac{\partial\vec D}{\partial t} = \frac{\partial}{\partial t}\left(\frac12\varepsilon E^2\right)
```

4. Így az **energiatétel differenciális alakja**:

```latex
\operatorname{div}\vec S + \frac{\partial w_{EM}}{\partial t} = -\vec E\vec j, \qquad w_{EM} = \frac12\varepsilon E^2 + \frac12\mu H^2
```
-->
- Első lépés. Az első {{Maxwell|mekszvel}}-egyenletet szorozzuk mínusz E-vel, a másodikat H-val: [[pause 500]] Mínusz E vektor szorozva rotáció H vektor egyenlő mínusz E vektor szorozva dé D vektor per dé té, mínusz E vektor skalárszorzat j vektor. [[pause 500]] H vektor szorozva rotáció E vektor egyenlő mínusz H vektor szorozva dé B vektor per dé té. [[pause 500]]
- Második lépés. Összeadjuk, és a bal oldalra az azonosságot használjuk: H rotáció E mínusz E rotáció H egyenlő divergencia, zárójelben E vektoriálisan szorozva H. [[pause 500]]
- Harmadik lépés. Lineáris, időben állandó anyagban az időderiváltak energiasűrűség-változásként írhatók: [[pause 500]] H vektor szorozva dé B vektor per dé té egyenlő az egy fél mű H négyzet idő szerinti parciális deriváltjával. [[pause 500]] E vektor szorozva dé D vektor per dé té egyenlő az egy fél epszilon E négyzet idő szerinti parciális deriváltjával. [[pause 500]]
- Negyedik lépés. Így az energiatétel differenciális alakja: [[pause 500]] Divergencia S vektor plusz dé kis w E M per dé té egyenlő mínusz E vektor skalárszorzat j vektor. [[pause 500]] Ahol kis w E M egyenlő egy fél epszilon E négyzet plusz egy fél mű H négyzet. [[pause 500]]

<!-- eredeti
Ideális szigetelőben (j = 0) ez egy kontinuitási egyenlet az energiára: ami beáramlik, az a tér energiáját növeli.
-->
Ideális szigetelőben, ahol j egyenlő nulla, ez egy kontinuitási egyenlet az energiára: ami beáramlik, az a tér energiáját növeli. [[pause 500]]

<!-- eredeti
5. Térfogatra integrálva (Gauss-Osztrogradszkij), az **integrális alak**:

```latex
\frac{dW_{EM}}{dt} = -\oint_f\vec S\,d\vec A - \int_V\vec j\vec E\,dV
```
-->
- Ötödik lépés. Térfogatra integrálva ({{Gauss|gausz}}–Osztrogradszkij), az integrális alak: [[pause 500]] Dé nagy W E M per dé té egyenlő mínusz az S vektor skalárszorzat dé A vektor zárt felületi integrálja az f felületre, mínusz a j vektor skalárszorzat E vektor dé V térfogati integrálja a V térfogatra. [[pause 500]]

<!-- eredeti
Az első tag a felületen kilépő energia, a második a tér által a töltéseken végzett munka.
-->
Az első tag a felületen kilépő energia, a második a tér által a töltéseken végzett munka.

<!-- eredeti
**Az áramos tag szétbontása.** Az áram vezetési (jᵥ) és konvektív (ρv) részből áll. Az Ohm-törvény a mozgási és az idegen térrel: jᵥ = σ(E + v × B + Eᵢ), ebből E-t kifejezve és beírva:

```latex
\frac{dW_{EM}}{dt} = -\oint_f\vec S\,d\vec A + \int_V\left[\vec j_v\vec E_i - \frac{j_v^2}{\sigma} - \vec v\left(\vec j_v\times\vec B\right) - \rho\vec E\vec v\right]dV
```
-->
## Az áramos tag szétbontása

Az áram vezetési (j vé) és konvektív (ró vé) részből áll. Az {{Ohm|óm}}-törvény a mozgási és az idegen térrel: j vé egyenlő szigma szorozva, zárójelben E plusz vé vektoriálisan szorozva bé plusz E í; ebből E-t kifejezve és beírva: [[pause 500]]

Dé nagy W E M per dé té egyenlő mínusz az S vektor skalárszorzat dé A vektor zárt felületi integrálja az f felületre, plusz egy térfogati integrál a V térfogatra. [[pause 500]]
Az integrál alatt szögletes zárójelben négy tag áll: j vé vektor skalárszorzat E í vektor, mínusz j vé négyzet per szigma, mínusz vé vektor skalárszorzat, zárójelben j vé vektor vektoriálisan szorozva bé vektor, végül mínusz ró szorozva E vektor skalárszorzat vé vektor; a szögletes zárójel után dé V áll. [[pause 500]]

<!-- eredeti
A zárójel tagjai (teljesítménysűrűségek):
-->
A zárójel tagjai (teljesítménysűrűségek):

<!-- eredeti
1. jᵥEᵢ: az áramforrások (elem, napelem) munkája, növeli a tér energiáját.
2. −jᵥ²/σ: a Joule-hő, mindig csökkenti.
3. −v(jᵥ × B): az Ampère-erő munkája a mozgó vezetőn; motornál csökkenti, generátornál növeli a tér energiáját.
4. −ρE·v: az elektromos tér munkája a mozgó töltéseken, előjele a szögtől függ.
-->
- Első tag, j vé szorozva E í: az áramforrások (elem, napelem) munkája, növeli a tér energiáját. [[pause 500]]
- Második tag, mínusz j vé négyzet per szigma: a {{Joule|dzsúl}}-hő, mindig csökkenti. [[pause 500]]
- Harmadik tag, mínusz vé szorozva, zárójelben j vé vektoriálisan szorozva bé: az {{Ampère|amper}}-erő munkája a mozgó vezetőn; motornál csökkenti, generátornál növeli a tér energiáját. [[pause 500]]
- Negyedik tag, mínusz ró szorozva E skalárszorzat vé: az elektromos tér munkája a mozgó töltéseken, előjele a szögtől függ. [[pause 500]]

<!-- eredeti
**Vizsgán:** a két ME szorzása és összeadása; az azonosság; az időderiváltak átírása; div S + ∂w/∂t = −E·j és a tagok jelentése; integrális alak; a zárójeles tagok jelentése.
-->
## Amit a vizsgán le kell írni

A két {{Maxwell|mekszvel}}-egyenlet szorzása és összeadása; az azonosság; az időderiváltak átírása; divergencia S plusz dé kis w per dé té egyenlő mínusz E skalárszorzat j, és a tagok jelentése; integrális alak; a zárójeles tagok jelentése. [[pause 500]]


