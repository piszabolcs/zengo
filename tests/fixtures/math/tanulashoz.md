# Tételek tanuláshoz

Minden tétel így épül fel: egy táblázat a benne szereplő jelekről (mit jelent, mi a mértékegysége), egy rövid, hétköznapi magyarázat arról, miről szól, majd a jegyzet tartalma képletekkel és levezetéssel, számpéldák nélkül. A végén egy sor arról, mit kell a vizsgán mindenképp leírni.

## 1. rész

### 1. Elektromos alapmennyiségek: térerősség, polarizáció, indukcióvektor, szuszceptibilitás

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

**Miről szól?** A térerősség megmondja, mekkora és milyen irányú erő hatna egy pontba tett pici pozitív töltésre. Ha szigetelőt teszünk a térbe, a molekulái kicsit „megnyúlnak” vagy befordulnak: az anyag polarizálódik. Ezt méri P, és κ azt, mennyire könnyen történik meg. A D vektort azért találták ki, mert vele a Gauss-törvényben csak az általunk odavitt (szabad) töltések szerepelnek, a polarizációs töltésekkel nem kell külön foglalkozni.

**Térerősség.** A próbatöltésre ható erő arányos a töltéssel (F = qE), a hányadosuk már csak a teret jellemzi. Ponttöltésre a Coulomb-törvényből:

```latex
\vec E = \frac{\vec F}{q} \qquad E = k\frac{Q}{r^2}
```

**Polarizáció jelensége.** Két fajtája van:

- *Indukált:* a tér széthúzza a molekula pozitív és negatív töltésközéppontját, így az is dipólus lesz, amelyik eddig nem volt az. Minden anyagban megtörténik.
- *Rendeződési (orientációs):* a már eleve dipólus molekulákat a tér beforítja a saját irányába. Minél hidegebb az anyag, annál jobban sikerül (a hőmozgás zavarja), tehát erősen hőmérsékletfüggő.

Polarizálódás után inhomogén térben erő is hat a testre: ezért vonzza a dörzsölt üvegrúd a papírfecnit.

**Polarizációvektor és szuszceptibilitás.** Egy kis térfogatban összeadjuk a molekulák dipólmomentumait, és elosztjuk a térfogattal. A legtöbb anyagban ez arányos a térerősséggel (lineáris anyagegyenlet):

```latex
\vec P = \lim_{\Delta V\to 0}\frac{\sum\vec p}{\Delta V} \qquad \vec P = \kappa\,\varepsilon_0\,\vec E
```

Vákuumban κ = 0, anyagban általában κ > 0. Nem mindig igaz: nagy térben átütés lehet, anizotróp kristályban P és E nem párhuzamos (κ tenzor).

**Indukcióvektor.** Definíció szerint, majd a lineáris közelítést beírva:

```latex
\vec D = \varepsilon_0\vec E + \vec P = \varepsilon_0\vec E + \kappa\varepsilon_0\vec E = \varepsilon_0(1+\kappa)\vec E = \varepsilon_0\varepsilon_r\vec E = \varepsilon\vec E, \qquad \varepsilon_r = 1+\kappa
```

**Fluxus és Gauss-törvény (II. alaptörvény).** A fluxus azt számolja, hány D-vonal megy át egy felületen (α a D és a felület normálisa közti szög): Ψ = ∫D dA, kicsiben ΔΨ = DΔA cos α. Ha egy Q ponttöltés köré r sugarú gömböt teszünk, D = Q/(4πr²) mindenhol merőleges a gömbre, így a fluxus D·4πr² = Q, a sugártól függetlenül: ahol kétszer akkora a sugár, négyszer akkora a felület, és negyed akkora a D. Ez bármilyen zárt felületre igaz, ami a töltést körbezárja (ami nincs bent, annak vonalai be is mennek, ki is jönnek, összesen 0):

```latex
\oint_f\vec D\,d\vec A = Q \qquad \operatorname{div}\vec D = \rho
```

**Ki minek a forrása?**

| Vektor | Forrása | Egyenlet |
| --- | --- | --- |
| D | csak a szabad töltések | div D = ρ |
| P | a polarizációs töltések (ellentétes előjellel) | div(−P) = ρ′ |
| E | mindkettő | div E = (ρ + ρ′)/ε₀ |

(Az E sort a felső kettő összeadásából kapjuk, mert E = (D − P)/ε₀.)

**Vizsgán:** E = F/q; a kétféle polarizáció; P definíciója; P = κε₀E; D = ε₀E + P → D = ε₀εᵣE, εᵣ = 1 + κ; a források táblázata.

### 2. A Maxwell-egyenletek teljes rendszere

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

**Miről szól?** Négy törvény arról, hogy mi hozza létre az elektromos és a mágneses teret. Az elméletben ezeket alaptételnek (axiómának) vesszük, és belőlük vezetünk le mindent. A leghíresebb következményük az elektromágneses hullámok létezése. Mindegyik kétféleképpen írható: integrálisan (egy egész görbére vagy felületre) és differenciálisan (egy pontra).

**1. Ampère-Maxwell-féle gerjesztési törvény:** áram és időben változó elektromos tér köré örvényes mágneses tér alakul ki. (A ∂D/∂t tag az eltolási áram.)

```latex
\oint_g\vec H\,d\vec s = \sum_k I_k + \frac{d}{dt}\int_F\vec D\,d\vec A \qquad \operatorname{rot}\vec H = \vec j + \frac{\partial\vec D}{\partial t}
```

**2. Faraday-féle indukciótörvény:** időben változó mágneses tér köré örvényes elektromos tér alakul ki.

```latex
\oint_g\vec E\,d\vec s = -\frac{d}{dt}\int_F\vec B\,d\vec A \qquad \operatorname{rot}\vec E = -\frac{\partial\vec B}{\partial t}
```

**3. Elektromos Gauss-törvény:** az elektromos tér forrásai a töltések.

```latex
\oint_f\vec D\,d\vec A = Q \qquad \operatorname{div}\vec D = \rho
```

**4. Mágneses Gauss-törvény:** nincs mágneses töltés, a B vonalak mindig zártak.

```latex
\oint_f\vec B\,d\vec A = 0 \qquad \operatorname{div}\vec B = 0
```

**Anyagegyenletek.** A megoldáshoz kell még, hogy az anyagban hogyan függ össze D és E, B és H, j és E:

```latex
\vec D = \varepsilon_0\varepsilon_r\vec E \qquad \vec B = \mu_0\mu_r\vec H \qquad \vec j = \sigma\vec E
```

A Maxwell-egyenletek egzakt természettörvények, az anyagegyenletek csak közelítések, bizonyos anyagokra jók (pl. a ferromágnesességet és az állandó mágneseket nem írják le).

**Vizsgán:** mind a négy egyenlet mindkét alakban, a nevükkel; mindegyikhez egy mondat jelentés; az anyagegyenletek, és hogy ezek közelítések.

### 3. Gauss-Osztrogradszkij és Stokes tétel. Az integrális és differenciális alak ekvivalenciája

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

**Miről szól?** A két tétel híd a „nagyban” és a „kicsiben” leírás között. *Gauss-Osztrogradszkij:* ami egy zárt felületen összesen kifá (fluxus), az pont a bent lévő források összege, mint amikor egy szobából kifolyó víz megegyezik a bent lévő locsolók hozamával. *Stokes:* egy zárt út mentén összegzett „sodrás” (cirkuláció) pont a körbezárt felületen lévő kis örvények összege. Ezekkel lehet a Maxwell-egyenleteket integrálisból differenciális alakra átírni és vissza.

**A differenciáloperátorok** (Függelék): a gradiens egy skálar leggyorsabb növekedésének irányába mutat; a divergencia a forrásosságot, a rotáció az örvényességet méri.

```latex
\operatorname{div}\vec v = \partial_x v_x + \partial_y v_y + \partial_z v_z \qquad \operatorname{rot}\vec v = \begin{pmatrix}\partial_y v_z - \partial_z v_y\\ \partial_z v_x - \partial_x v_z\\ \partial_x v_y - \partial_y v_x\end{pmatrix}
```

Fontos azonosságok: rot grad φ ≡ 0 (gradiensnek nincs örvénye) és div rot v ≡ 0 (örvénynek nincs forrása).

**Gauss-Osztrogradszkij tétel** (F a V térfogat zárt határa, a normális kifelé mutat):

```latex
\oint_F\vec v\,d\vec A = \int_V\operatorname{div}\vec v\,dV
```

**Stokes-tétel** (a g zárt görbe az F felület pereme; a körüljárás és a normális jobbkéz-szabály szerint):

```latex
\oint_g\vec v\,d\vec s = \int_F\operatorname{rot}\vec v\,d\vec A
```

**Ekvivalencia, az 1. Maxwell-egyenleten bemutatva:**

1. Integrális alak, az áramot áramsűrűséggel írva (I = ∫j dA):

```latex
\oint_g\vec H\,d\vec s = \int_F\vec j\,d\vec A + \frac{d}{dt}\int_F\vec D\,d\vec A
```

2. A bal oldalra Stokes-tétel: ∮H ds = ∫rot H dA.
3. Ha a felület nem mozog, a d/dt bevihető az integrál alá, ott ∂/∂t lesz:

```latex
\int_F\operatorname{rot}\vec H\,d\vec A = \int_F\left(\vec j + \frac{\partial\vec D}{\partial t}\right)d\vec A
```

4. Ez **bármilyen** felületre igaz, ezért a két oldalon az integrandusok is egyenlők: rot H = j + ∂D/∂t.

A 2. egyenletnél ugyanígy. A Gauss-törvényeknél a Stokes helyett a Gauss-Osztrogradszkij tétel kell:

```latex
\oint_f\vec D\,d\vec A = \int_V\operatorname{div}\vec D\,dV = Q = \int_V\rho\,dV \;\Rightarrow\; \operatorname{div}\vec D = \rho
```

Visszafelé ugyanezek a lépések fordítva.

**Vizsgán:** a két tétel képlettel és hogy mi a görbe, felület, térfogat; div és rot jelentése; az 1. ME átalakítása a négy lépéssel; Gauss-törvényeknél a divergencia-tétel.

### 4. Skálarpotenciál. Kirchhoff huroktörvénye

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

**Miről szól?** Ha semmi nem változik időben (elektrosztatika), az elektromos tér olyan, mint a gravitáció: két pont között mindegy, merre viszünk egy töltést, a munka ugyanannyi. Ezért minden ponthoz rendelhetünk egy számot, a potenciált (mint a tengerszint feletti magasság), és a térerősség a „lejtő lefelé” irány. Ha körbemész és visszajössz, ugyanott vagy: ez a huroktörvény.

**I. alaptörvény.** A 2. Maxwell-egyenletben sztatikában ∂B/∂t = 0, ezért a mező konzervatív (örvénymentes):

```latex
\oint_g\vec E\,d\vec s = 0 \quad\Longleftrightarrow\quad \operatorname{rot}\vec E = 0
```

(Az egyenáram mágneses tere is állandó, tehát rá is igaz.) A potenciálos mezők tétele szerint ez három egyenértékű állítás: rot v = 0; bármely zárt görbére ∮v ds = 0 (az integrál független az úttól); létezik U, hogy v = ±grad U.

**Munka, feszültség, potenciál.** A feszültség az egységnyi töltésen végzett munka; homogén térben egyszerűen U = Ed.

```latex
W_{AB} = \int_A^B q\vec E\,d\vec r \qquad U_{AB} = \frac{W_{AB}}{q} = \int_A^B\vec E\,d\vec r = U(A) - U(B)
```

A potenciál az egységnyi töltésre jutó helyzeti energia (U = Eₚ/q), csak egy állandó erejéig meghatározott. Szokásos választás, hogy a végtelenben 0, ekkor a pont potenciálja az a munka, amit a mező végez, amíg egységnyi pozitív töltést onnan a végtelenbe visz:

```latex
U(P) = \int_P^\infty\vec E\,d\vec r \qquad \vec E = -\operatorname{grad}U
```

Ponttöltésre:

```latex
U(r) = \int_r^\infty\frac{kQ}{r^2}\,dr = kQ\left[-\frac1r\right]_r^\infty = \frac{kQ}{r}
```

Pozitív töltésre az alacsonyabb potenciál felé hat erő. Az azonos potenciálú pontok ekvipotenciális felületet alkotnak (ponttöltésnél gömbök); ezen mozogva nincs munka, és E merőleges rájuk.

**Kirchhoff huroktörvénye.** A konzervativitásból bármely zárt hurokra:

```latex
\sum U = 0
```

Csak akkor igaz, ha rot E = 0. Ha B időben változik, ez a feszültség-fogalom nem működik (ezt a 2. részben az általános huroktörvény kezeli).

**Vizsgán:** I. alaptörvény és honnan jön; munka, feszültség, potenciál definíciója; U(∞) = 0; ponttöltés potenciálja levezetve; E = −grad U; ΣU = 0 és mikor nem igaz.

### 5. Vezetők az elektrosztatikus mezőben. Csúcshatás

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

**Miről szól?** A fémben szabadon mozgó elektronok vannak. Ha bent tér lenne, mozognának, áram folyna. Addig rendeződnek át, amíg a saját terük kioltja a teret, ezért nyugalomban a fém belsejében nincs tér. A töltés a felületre megy, de nem egyenletesen: a hegyes részeken sűrűbb, ott erősebb a tér (csúcshatás).

**Vezető sztatikus állapotban.**

- Bent E = 0, különben a szabad töltések mozognának.
- Ezért bármely két pont közt a feszültség 0: a vezető **ekvipotenciális**. Üreges vezetőre is igaz, ha az üregben nincs töltés: zárt fémburokba (Faraday-kalitka) nem hatol be a tér. Erre épül az elektrosztatikai árnyékolás.
- Eₜ a határon folytonos, bent 0, tehát kívül sincs tangenciális tér: a tér a vezető körül **merőleges a felületre**.
- Bent E = 0 → D = 0 → (div D = ρ miatt) ρ = 0: a vezetőre vitt töltés a **külső felületre** húzódik.
- A határfeltételből (Dₙ₂ − Dₙ₁ = η, bent Dₙ₁ = 0) a felület mellett a szigetelőben Dₙ = η.

**Csúcshatás.** Két különböző méretű fémgömböt vezetékkel összekötünk, így egy vezetőként azonos potenciálra kerülnek. Gömb potenciálja kQ/(sugár), a töltés pedig η · felület:

```latex
k\frac{Q_1}{r} = k\frac{Q_2}{R} \;\Rightarrow\; \frac{\eta_1\,4\pi r^2}{r} = \frac{\eta_2\,4\pi R^2}{R} \;\Rightarrow\; \frac{\eta_1}{\eta_2} = \frac{R}{r}
```

A kisebb gömbön sűrűbb a töltés, fordított arányban a sugárral. Általánosan: a csúcsokon (kis görbületi sugár) nagyobb a töltéssűrűség és így a tér. Pontos képlet a görbületre nincs. Ezért hegyes a villámhárító, és ezért lekerekítettek a nagyfeszültségű elektródák.

**Vizsgán:** miért E = 0 bent; ekvipotenciális, Faraday-kalitka; tér merőleges a felületre; ρ = 0, töltés a felületen, Dₙ = η; csúcshatás két gömbbel, η₁/η₂ = R/r.

### 6-8. Gömb, henger és sík tere és potenciálja (a testen kívül)

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

**Miről szól mindhárom?** Ugyanaz a trükk háromszor. A Gauss-törvény (∮D dA = Q) bármilyen zárt felületre igaz, de általában nehéz kiintegrálni. Ha viszont a szimmetriát kihasználva olyan képzeletbeli felületet (Gauss-felületet) választunk, amelyen D **mindenhol ugyanakkora** és **merőleges a felületre**, akkor az integrál egyszerű szorzás lesz: D · (felület) = bezárt töltés. Ebből kifejezzük D-t, elosztjuk ε-nal és megvan E. A potenciálhoz E-t kell integrálni.

**6. Gömbszimmetrikus töltéseloszlás** (ponttöltés, töltött gömb vagy gömbhéj)

- *Szimmetria:* D sugárirányú, nagysága csak r-től függ.
- *Gauss-felület:* a testtel koncentrikus, r sugarú gömb. Ezen D mindenhol ugyanakkora és merőleges rá. Felülete 4πr².

```latex
\oint\vec D\,d\vec A = D\cdot 4\pi r^2 = Q \;\Rightarrow\; E = \frac{D}{\varepsilon} = \frac{1}{4\pi\varepsilon}\frac{Q}{r^2}
```

Ez a Coulomb-törvény, a 3. Maxwell-egyenletből levezetve. Nem használtuk ki, hogy a töltés pontszerű, csak a gömbszimmetriát: **kívülről bármilyen gömbszimmetrikus test úgy látszik, mintha minden töltése a középpontban lenne.** A tér 1/r² szerint csökken (kétszer messzebb negyed akkora), mert a vonalak egyre nagyobb gömbfelületen oszlanak el. Potenciál (nulla a végtelenben):

```latex
U(r) = \int_r^\infty E\,dr = \frac{Q}{4\pi\varepsilon}\int_r^\infty\frac{dr}{r^2} = \frac{1}{4\pi\varepsilon}\frac{Q}{r}
```

Ebből: egy R sugarú, Q töltésű fémgömb potenciálja U = kQ/R.

**7. Hengerszimmetrikus töltéseloszlás** (hosszú egyenes töltött szál vagy henger)

- *Szimmetria:* a szál a z tengely, a térnek nincs z irányú része, sugárirányban mutat kifelé.
- *Gauss-felület:* a szállal koaxiális, r sugarú, h magas henger. Az alap- és fedőlapon a tér a lappal párhuzamos, ott nincs fluxus. Csak a palást számít, annak területe 2πrh. A bezárt töltés a h hosszú szálszakaszé: λh.

```latex
D\cdot 2\pi r h = \lambda h \;\Rightarrow\; E = \frac{\lambda}{2\pi\varepsilon r} = \frac{2k\lambda}{r}
```

A tér 1/r szerint csökken (kétszer messzebb fele akkora), mert a vonalak csak „oldalra”, egyre nagyobb palástra oszlanak el. **Potenciál:** itt nem lehet a végtelenben a nulla, mert az 1/r integrálja (ln) végtelen lenne; vékony szálnál magán a szálon sem, mert ott a tér végtelen. Ezért egy tetszőleges R₀ távolságban választjuk a nullát:

```latex
U(r) = \int_r^{R_0}\frac{2k\lambda}{r}\,dr = 2k\lambda\ln\frac{R_0}{r}
```

**8. Végtelen töltött sík**

- *Szimmetria:* a tér merőleges a síkra, mindkét oldalon kifelé mutat.
- *Gauss-felület:* a síkot átszúró kis henger, A területű alap- és fedőlappal a sík két oldalán, egyforma távol. A paláston nincs fluxus (a tér párhuzamos vele), a **két** lapon egyaránt kilép, ezért van 2-es szorzó. A bezárt töltés ηA.

```latex
2\varepsilon EA = \eta A \;\Rightarrow\; E = \frac{\eta}{2\varepsilon}
```

A tér **nem függ a távolságtól**, mert a vonalak párhuzamosak, nem tudnak szétszóródni. Ez addig igaz, amíg sokkal közelebb vagyunk a laphoz, mint annak mérete. **Potenciál:** a nullszint a síkon; a pozitív lap taszítja a pozitív töltést, tehát tőle távolodva mindkét irányban lineárisan csökken:

```latex
U(z) = -\frac{\eta}{2\varepsilon}\,\lvert z\rvert
```

**Összehasonlítás:**

|  | Gauss-felület | Mekkora felületen van fluxus | E távolságfüggése |
| --- | --- | --- | --- |
| gömb | koncentrikus gömb | 4πr² (az egész gömb) | 1/r² |
| henger | koaxiális henger | 2πrh (csak a palást) | 1/r |
| sík | átszúró kis henger | 2A (csak a két lap) | nem függ |

**Vizsgán** (mindháromnál): szimmetria-érv, a Gauss-felület rajza és hogy hol nincs fluxus; a Gauss-törvény beírva; E kifejezve; potenciál integrálással és a nullszint választása.

### 9. Kapacitás. Síkkondenzátor kapacitása. Dielektrikummal töltött kondenzátor

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

**Miről szól?** Ha egy vezetőre kétszer annyi töltést viszünk, minden kétszeres lesz, a potenciálja is. A töltés és a feszültség aránya tehát állandó, ez a kapacitás: megmutatja, mennyi töltés „fér el” 1 V feszültségnél. A kondenzátor két közeli lemez: a közelség miatt kis feszültséghez is sok töltés tartozik. Ha szigetelőt teszünk közé, az polarizálódik és gyengíti a teret, így ugyanannyi töltéshez még kisebb feszültség kell: nő a kapacitás.

**Definíció.** Lineáris közegben a potenciál egyenesen arányos a töltéssel, a hányados állandó (csak a geometriától és az anyagtól függ):

```latex
C = \frac{Q}{U}
```

Magányos R sugarú gömbre U = kQ/R, így C = 4πε₀R; ez hétköznapi testeknél nagyon kicsi. Növelni úgy lehet, hogy közel teszünk egy másik (pl. földelt) vezetőt: a tér rövidebb útra integrálódik, kisebb a feszültség. A kondenzátor két, szigetelővel elválasztott vezető (fegyverzet), a töltésük ellentetten egyenlő.

**Síkkondenzátor** (feltétel: d sokkal kisebb a lemezek méreténél):

1. A két ellentétes töltésű lemez tere (8. tétel) a lemezek között összeadódik, kívül kioltja egymást. A lemezek között: D = η.
2. Ebből a térerősség E = η/(ε₀εᵣ), homogén.
3. A feszültség U = Ed = ηd/(ε₀εᵣ).
4. A kapacitás (Q = ηA):

```latex
C = \frac{Q}{U} = \frac{\eta A}{\dfrac{\eta d}{\varepsilon_0\varepsilon_r}} = \varepsilon_0\varepsilon_r\frac{A}{d}
```

Ha d nem elég kicsi, a vonalak a széleken kiszóródnak, és a képlet pontatlan.

**Dielektrikummal töltött kondenzátor.** A képletből látszik, hogy a kapacitás εᵣ-szeresre nő a vákuumhoz képest:

```latex
C = \varepsilon_r C_0
```

Oka: ugyanaz a szabad töltés ugyanakkora D-t hoz létre (D = η), de a polarizációs töltések miatt E = D/(ε₀εᵣ) kisebb, így U is kisebb.

(Kiegészítés: gömbkondenzátor C = 4πε r₁r₂/(r₂ − r₁), hengerkondenzátor C = 2πεh/ln(r₂/r₁).)

**Vizsgán:** C = Q/U és miért állandó; kondenzátor fogalma; síkkondenzátor levezetése (D = η → E → U → C); C = εᵣC₀ és miért.

### 10. Síkkondenzátor feltöltésének munkája. Az elektromos tér energiája és energiasűrűsége

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

**Miről szól?** A kondenzátort apránként töltjük: az első adagot szinte ingyen viszük át, de minél több töltés van már rajta, annál nagyobb feszültség ellenében kell vinni a következőt. Átlagosan a végső feszültség felén dolgozunk, innen az ½. A befektetett munka a lemezek közötti **térben** tárolódik; a tér minden köbméterének van energiája.

**A feltöltés munkája.** Közbülső állapotban a töltés q, a feszültség u = q/C. Egy kis Δq átvitelének munkája ΔW = uΔq (a feszültség az egységnyi töltésen végzett munka). 0-tól Q-ig összegezve:

```latex
\Delta W = \frac{q}{C}\Delta q \;\Rightarrow\; W = \frac1C\int_0^Q q\,dq = \frac{Q^2}{2C} = \frac12 QU = \frac12 CU^2
```

**Energiasűrűség.** Síkkondenzátorban a tér homogén. Beírjuk, hogy Q = ηA, U = Ed, D = η és V = Ad:

```latex
W = \frac12 QU = \frac12\eta A\cdot Ed = \frac12 DE\cdot Ad = \frac12 DE\cdot V
```

Az energiasűrűség az 1 m³-re jutó energia, w = W/V:

```latex
w = \frac12\vec D\vec E \;\left(= \frac12\varepsilon E^2\right)
```

Ez általánosan is igaz (nem csak kondenzátorban, nem csak sztatikusan). Ha a tér nem homogén, pontonként számolunk és összegzünk:

```latex
W = \int_V w\,dV = \frac12\int_V\vec D\vec E\,dV
```

**Másik út: a lemezek közti erőből.** Ha F = QE-t írnánk E = η/ε₀-lal, kétszer többet kapnánk a valóságosnál: a tér felét a lemez maga kelti, az önmagára nem hat. Helyesen F = QE/2 = Q²/(2ε₀A), ami nem függ d-től. Állandó töltésnél 0-ról d távolságra széthúzva a lemezeket: W = Fd = Q²d/(2ε₀A) = Q²/(2C), ugyanaz.

**Vizsgán:** feltöltés kis adagokban, ΔW = (q/C)Δq, integrálás; W = Q²/2C = ½QU = ½CU²; síkkondenzátorral W = ½DE·V → w = ½D·E; W = ½∫D·E dV.

### 11. Dipólmomentumra ható erő és forgatónyomaték. Dipólus tere és potenciálja

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

**Miről szól?** A dipólus egy + és egy − töltés egy kis pálcán. Egyenletes térben a két végét egyforma erővel, de ellentétes irányba húzza a tér: nem mozdul el, csak befordul a tér irányába, mint egy iránytű. Ha a tér nem egyenletes, az egyik végét erősebben húzza, így a dipólus az erősebb tér felé mozdul. Messziről a két töltés majdnem kioltja egymást, ezért a dipólus tere gyorsabban csökken, mint egy ponttöltésé.

**Homogén térben.** A két erő: F₊ = QE és F₋ = −QE, az eredő nulla. A középpontra a nyomaték (mindkét erő karja ℓ/2):

```latex
\vec M = -\frac{\vec\ell}{2}\times(-Q\vec E) + \frac{\vec\ell}{2}\times Q\vec E = Q\vec\ell\times\vec E = \vec p\times\vec E, \qquad M = pE\sin\varphi
```

**Helyzeti energia.** A nyomaték munkája φ₁ és φ₂ között W = pE(cosφ₁ − cosφ₂), ebből:

```latex
E_p = -\vec p\vec E
```

Ha p és E egyirányú: nyomaték nincs, az energia minimális, **stabil** egyensúly. Ha ellentétes: nyomaték nincs, de az energia maximális, **instabil**.

**Inhomogén térben.** Egy dimenzióban a + töltésnél E + ΔE, a − töltésnél E a tér, ΔE = ℓ·∂E/∂x, így az eredő F = QΔE = p·∂E/∂x. Három dimenzióban, illetve örvénymentes (sztatikus) térben:

```latex
\vec F = (\vec p\cdot\operatorname{grad})\vec E = \operatorname{grad}(\vec p\vec E)
```

Ez éppen az Eₚ = −p·E energia negatív gradiense. (Ezért vonzza a dörzsölt rúd a polarizált papírdarabot.)

**Dipólus tere és potenciálja a tengelyen** (−Q és +Q egymástól d távolságra, vákuumban). A két ponttöltés terét előjelhelyesen összeadjuk, majd nagy x-re csak a vezető tagot tartjuk meg:

```latex
E = kQ\left(\frac{1}{x^2} - \frac{1}{(x+d)^2}\right) = kQ\frac{2xd + d^2}{x^2(x+d)^2} \;\xrightarrow{x\to\infty}\; \frac{2kQd}{x^3} = \frac{2kp}{x^3}
```

```latex
U = kQ\left(\frac1x - \frac{1}{x+d}\right) = \frac{kQd}{x^2 + xd} \;\xrightarrow{x\to\infty}\; \frac{kp}{x^2}
```

A tér 1/x³, a potenciál 1/x² szerint csökken (ponttöltésnél 1/x² és 1/x). Ellenőrzés: E = −dU/dx = 2kp/x³.

**Vizsgán:** p = Qℓ; homogén térben eredő erő 0, M = p × E levezetve; Eₚ = −p·E, stabil/instabil; inhomogén térben F = grad(p·E); tengelyen E → 2kp/x³, U → kp/x².

### 12. Elektromos áramsűrűség. Differenciális Ohm-törvény és levezetése

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

**Miről szól?** Az áramerősség az egész vezetőre vonatkozik (mennyi töltés megy át másodpercenként), az áramsűrűség egy pontra (ott mennyire „zsúfolt” az áramlás). A szokásos U = RI csak egyszerű, egyenes vezetőre jó. A differenciális Ohm-törvény ugyanez pontra lebontva: ahol nagyobb a térerősség, ott nagyobb az áramsűrűség, és ez bármilyen alakú vezetőre használható.

**Áramerősség:** a keresztmetszeten időegység alatt átfolyó nettó töltés. Iránya a pozitív töltések (elképzelt) mozgásának iránya, az elektronokéval ellentétes. Egy időszak alatt átfolyt töltés: Q = ∫I dt.

**Áramsűrűség:** az áramlásra merőleges egységnyi felületen átfolyó áram; vektor, a pozitív töltéshordozók mozgásának irányába mutat.

```latex
j = \lim_{A\to0}\frac{I}{A} \qquad I = \int_A\vec j\,d\vec A \quad (\text{egyenletes, merőleges esetben } I = jA)
```

**Ellenállás és méretek.** Kétszer hosszabb vezető olyan, mint két ugyanolyan sorba kötve (kétszeres R); kétszer vastagabb olyan, mint két párhuzamosan (fele R):

```latex
R = \rho\frac{\ell}{A}
```

**A differenciális Ohm-törvény levezetése.** Vékony, ℓ hosszú, A keresztmetszetű vezető, benne egyenletes tér és áramsűrűség:

1. A két vége közti feszültség U = Eℓ, az áram I = jA.
2. Az ellenállás egyrészt R = U/I = Eℓ/(jA), másrészt R = ρℓ/A.
3. A kettőt egyenlővé téve ℓ/A kiesik: ρ = E/j.

```latex
\frac{E\ell}{jA} = \rho\frac{\ell}{A} \;\Rightarrow\; \vec E = \rho\,\vec j \quad\Longleftrightarrow\quad \vec j = \sigma\vec E
```

Ez általánosan is igaz, ez az Ohm-féle anyagegyenlet. Csak közelítés: fémekben az áram melegít, és ettől σ változik; diódára állandó hőmérsékleten sem igaz; szupravezetőben ρ = 0, tér nélkül is folyik áram.

**Vizsgán:** I és j definíciója, I = ∫j dA; R = ρℓ/A indoklással; a levezetés három lépése; j = σE; korlátok.

### 13. A kontinuitási egyenlet. Kirchhoff csomóponti törvénye

| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| j | áramsűrűség | A/m² |
| ρ | térfogati töltéssűrűség | C/m³ |
| H, D | mágneses térerősség, elektromos indukció | A/m, C/m² |
| V, F | egy térrész és az azt körbevevő zárt felület | m³, m² |
| Q | a térrészben lévő töltés | C |
| I | egy ágban folyó áram | A |

**Miről szól?** A töltés nem keletkezik és nem tűnik el. Ha egy térrészben fogy a töltés, akkor az valahol kiáramlott a határán, mint egy kádban: a vízszint csak úgy változhat, ha befolyik vagy kifolyik a víz. Ha minden állandósult, amennyi befolyik, annyi ki is folyik: ez a csomóponti törvény.

**Levezetés:**

1. Az 1. Maxwell-egyenlet mindkét oldalának vesszük a divergenciáját. A bal oldal 0, mert div rot ≡ 0:

```latex
\underbrace{\operatorname{div}\operatorname{rot}\vec H}_{0} = \operatorname{div}\vec j + \frac{\partial}{\partial t}\operatorname{div}\vec D
```

2. A 3. Maxwell-egyenletből div D = ρ, így megkapjuk a **differenciális alakot**:

```latex
\operatorname{div}\vec j = -\frac{\partial\rho}{\partial t}
```

Jelentése: az áramsűrűség ott forrásos, ahol a töltéssűrűség csökken (onnan áramlik ki a töltés).

3. Egy álló térfogatra integrálva és a Gauss-Osztrogradszkij tételt használva az **integrális alak**:

```latex
\oint_F\vec j\,d\vec A = -\frac{d}{dt}\int_V\rho\,dV
```

A zárt felületen kifolyó áram = a bent lévő töltés csökkenésének sebessége.

4. **Stacionárius esetben** (semmi nem változik időben) a jobb oldal 0. Egy csomópont köré tett zárt felületre:

```latex
\oint_f\vec j\,d\vec A = 0 \;\Rightarrow\; \sum I = 0
```

Ez Kirchhoff csomóponti törvénye.

**Vizsgán:** a négy lépés (div, div rot ≡ 0, div D = ρ, Gauss-Osztrogradszkij), a jelentés (töltésmegmaradás), stacionárius esetben ΣI = 0.

### 14. Elektromos mennyiségek két közeg határán. E és D vonalak törése. Dielektrikum külső térben

| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| 1, 2 index | az 1-es és a 2-es közegben |  |
| t index | tangenciális: a határfelülettel párhuzamos komponens |  |
| n index | normális: a határfelületre merőleges komponens |  |
| E, D | térerősség, indukció | V/m, C/m² |
| ε₁, ε₂ | a két közeg permittivitása | As/(Vm) |
| η | felületi töltéssűrűség a határon | C/m² |
| α, β | a vonal és a határra merőleges egyenes közti szög az 1-es, illetve 2-es közegben | rad |

**Miről szól?** Két különböző szigetelő találkozásánál a vektorokat felbontjuk a határral párhuzamos és rá merőleges részre. Két szabály dönt el mindent: a párhuzamos E nem ugrik, és a merőleges D nem ugrik (ha nincs a határon töltés). Mivel a két közegben más az ε, a vonalak a határon megtörnek, hasonlóan a fényhez.

**Tangenciális komponens.** Veszünk egy lapos téglalap alakú hurkot, ami a határt két oldalról öleli, és felírjuk rá a 2. Maxwell-egyenletet (∮E ds = −dΦ/dt). Ha a hurkot „rálapítjuk” a határra: a rövid oldalak integrálja 0-hoz tart, és a közbezárt felület is, így a B-fluxus is eltűnik. Marad a két hosszú oldal, ellentétes irányban:

```latex
\int_A^B\left(\vec E_2 - \vec E_1\right)d\vec s = 0 \;\Rightarrow\; E_{t2} = E_{t1}, \qquad \frac{D_{t2}}{D_{t1}} = \frac{\varepsilon_2}{\varepsilon_1}
```

(Dₜ nem folytonos, mert D = εE és ε más.)

**Normális komponens.** Lapos dobozt teszünk a határra (egyik lapja az 1-es, másik a 2-es közegben), és felírjuk rá a Gauss-törvényt. A dobozt lapítva a palást és a térfogat eltűnik, a bezárt töltésből csak a felületi töltés marad:

```latex
D_{n2} - D_{n1} = \eta
```

Ha a határon nincs töltés (η = 0), Dₙ folytonos, de Eₙ ugrik:

```latex
D_{n1} = D_{n2} \;\Rightarrow\; \varepsilon_1 E_{n1} = \varepsilon_2 E_{n2}
```

**Törési törvény** (η = 0). A tangens a párhuzamos és a merőleges komponens hányadosa:

```latex
\frac{\operatorname{tg}\alpha}{\operatorname{tg}\beta} = \frac{D_{1t}/D_{1n}}{D_{2t}/D_{2n}} = \frac{D_{1t}}{D_{2t}} = \frac{\varepsilon_1}{\varepsilon_2}
```

Ugyanez jön ki E-re is: az E és a D vonalak ugyanúgy törnek. A nagyobb ε-ú közegben a vonal jobban elhajlik a merőlegestől.

**Dielektrikum külső térben.** Homogén térbe tett szigetelőben a tér csak akkor lesz homogén és eredeti irányú, ha a test ellipszoid (egyik tengelye a térrel párhuzamos); ezt nézzük. A testen nincs szabad töltés, tehát D vonalai folytonosak, viszont polarizációs töltés van, így Eₙ ugrik. A térre merőleges lapoknál D kint és bent egyforma, E bent kisebb; a térrel párhuzamos oldalaknál Eₜ folytonos, ezért kint megritkulnak az E vonalak. Végeredmény: bent E kisebb (**depolarizáció**), a D vonalak viszont beszűrűsödnek a testbe.

**Vizsgán:** hurok és doboz rajza; Eₜ₁ = Eₜ₂ (miért tűnik el a fluxus); Dₙ₂ − Dₙ₁ = η; η = 0 esetén ε₁Eₙ₁ = ε₂Eₙ₂; tgα/tgβ = ε₁/ε₂; depolarizáció.

### 15. Áramsűrűség két közeg határán. Áramsűrűség törési törvénye

| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| j₁, j₂ | áramsűrűség a két vezető közegben | A/m² |
| n, t index | a határra merőleges, illetve vele párhuzamos komponens |  |
| σ₁, σ₂ | a két közeg fajlagos vezetőképessége | S/m |
| E | térerősség | V/m |
| α, β | az áramvonal szöge a merőlegessel az 1-es, illetve 2-es közegben | rad |
| G, C | konduktancia (1/R), kapacitás | S, F |

**Miről szól?** Ugyanaz, mint a 14. tétel, csak két vezető határán folyó áramra. Állandósult áramlásnál a töltés nem gyűlhet fel a határon: ami merőlegesen odajön, annak át is kell mennie. A párhuzamos térerősség pedig most is folytonos.

**Normális komponens.** A stacionárius kontinuitási egyenlet (∮j dA = 0) egy határra tett lapos dobozra:

```latex
j_{2n}A - j_{1n}A = 0 \;\Rightarrow\; j_{1n} = j_{2n}
```

**Tangenciális komponens.** Eₜ₁ = Eₜ₂ (14. tétel), és az Ohm-törvény szerint E = j/σ:

```latex
\frac{j_{1t}}{\sigma_1} = \frac{j_{2t}}{\sigma_2}
```

**Törési törvény:**

```latex
\frac{\operatorname{tg}\alpha}{\operatorname{tg}\beta} = \frac{j_{1t}/j_{1n}}{j_{2t}/j_{2n}} = \frac{j_{1t}}{j_{2t}} = \frac{\sigma_1}{\sigma_2}
```

Pont olyan, mint a dielektrikumoknál, csak ε helyett σ áll (és D helyett j). Következmény: jó vezetőből (fém) rossz vezetőbe (talaj) az áram szinte merőlegesen lép ki. A hasonlóságot a jegyzet G/σ = C/ε alakban is felírja: ugyanarra az elektróda-elrendezésre a konduktancia és a kapacitás az anyagjellemzővel osztva ugyanaz, csak a geometriától függ.

**Vizsgán:** j₁ₙ = j₂ₙ a stacionárius kontinuitásból; j₁ₜ/σ₁ = j₂ₜ/σ₂; tgα/tgβ = σ₁/σ₂.

### 16. A stacionárius áram munkája, teljesítménye, teljesítménysűrűsége

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

**Miről szól?** A feszültség az egységnyi töltésen végzett munka, így ha t idő alatt Q = It töltés megy át U feszültségen, a mező QU munkát végez. Ez a fogyasztóban hővé, mozgássá, kémiai energiává vagy fénnyé alakul; ha van ellenállás, hő mindig keletkezik. A teljesítménysűrűség azt mondja meg, a vezető melyik pontja mennyire melegszik: ahol sűrűbb az áram, ott (a négyzetével) sokkal jobban.

**Munka és teljesítmény** (Joule-törvény, az U = RI-t beírva):

```latex
W = QU = UIt = I^2Rt = \frac{U^2}{R}t \qquad P = UI = I^2R = \frac{U^2}{R}
```

**Differenciális alak.** Egy homogén drótban leadott teljesítményt elosztjuk a drót térfogatával (U = Eℓ, I = jA, V = Aℓ):

```latex
p_J = \frac{P}{V} = \frac{UI}{A\ell} = \frac{E\ell\cdot jA}{A\ell} = \vec E\vec j = \rho j^2 = \sigma E^2
```

Ha az áramlás nem egyenletes, pontonként számolunk és összegzünk: P = ∫p\_J dV.

**Vizsgán:** W = QU = UIt; mire alakulhat az energia; Joule-törvény három alakja; P = UI = I²R = U²/R; p\_J levezetése és egysége; inhomogén esetben integrál.

## 2. rész

### 1. Biot-Savart-törvény, egyenes és körvezető mágneses terének iránya

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

**Miről szól?** Megmondja, hogy egy áramjárta vezető egy adott pontban mekkora és milyen irányú mágneses teret kelt. A vezetőt kis darabokra bontjuk, minden darab hozzájárul a térhez (a távolság négyzetével csökkenően), és ezeket összeadjuk. Az irányt egy vektoriális szorzat adja, ezért a tér mindig merőleges az áramra és a távolság-vektorra is: körbeöleli a vezetőt.

**A törvény** (eredetileg mérésből, 1820; a vektorpotenciálos levezetés nem kell):

```latex
\vec B = \frac{\mu}{4\pi}\int\frac{\vec r\times\vec j}{r^3}\,dV \qquad \vec H = \frac{1}{4\pi}\int\frac{\vec r\times\vec j}{r^3}\,dV
```

Vékony vezetőnél j·dV helyett I·ds írható (j dV = jA ds = I ds), és a vezető teljes hosszára integrálunk:

```latex
\vec H = \frac{I}{4\pi}\int\frac{\vec r\times d\vec s}{r^3}
```

**Egyenes vezető terének iránya.** Ha az áram felfelé folyik és a pont a vezetőtől jobbra van, minden kis darab tere a lapba befelé mutat, tehát az összeg is. Az erővonalak a vezető körüli koncentrikus körök. **Jobbkéz-szabály:** hüvelykujj az áram irányába, a behajlított ujjak mutatják H körüljárását.

**Körvezető tere a tengelyén.** A karika minden darabja ugyanolyan távol van a tengely egy pontjától (r), és r merőleges ds-re, így |r × ds| = r ds. Az egyes darabok terének a tengelyre merőleges részei páronként kioltják egymást, csak a tengely irányú rész marad (szorzó: cos α = R/r). Az integrál a kerület, 2πR:

```latex
H = \frac{Ir}{4\pi r^3}\cdot\frac{R}{r}\cdot 2\pi R = \frac{IR^2}{2r^3} = \frac{IR^2}{2\left(R^2+z^2\right)^{3/2}}
```

A karika közepén (z = 0) H = I/(2R); messze 1/z³ szerint csökken (mint az elektromos dipólusé). Iránya a tengely mentén: ujjak az áram körüljárásának irányába, a hüvelykujj mutatja H-t.

**Vizsgán:** a törvény (B, H, vékony vezető), mit jelent r; egyenes vezető: koncentrikus körök, jobbkéz-szabály; körvezető a tengelyen, középpontban I/(2R).

### 2. Ampère-féle gerjesztési törvény. Végtelen egyenes vezető tere

| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| H | mágneses térerősség | A/m |
| g, ds | zárt görbe, ívelem | m |
| Iⱼ | a görbe által körülzárt áramok | A |
| j | áramsűrűség | A/m² |
| r | távolság a vezetőtől | m |

**Miről szól?** Ha egy zárt görbe mentén összeadjuk, mennyire „sodor” a mágneses tér a görbe irányába, az pont annyi, amennyi áram átfolyik a görbén. Ha a szimmetria miatt a tér a görbe mentén mindenhol egyforma, ebből egyből kijön a tér nagysága (mint a Gauss-törvénynél az elektromos térre).

**A törvény:**

```latex
\oint_g\vec H\,d\vec s = \sum_j I_j \qquad \operatorname{rot}\vec H = \vec j
```

Előjel: az a pozitív áram, amelyik a felület normálisának irányában megy át; a görbe körüljárási irányát és a normálist a jobbcsavar-szabály kapcsolja össze. Mágnesezhető anyag jelenlétében is érvényes. A differenciális alak szerint az áram körüli mágneses tér örvényes. Az áramba nemcsak a vezetési (fémben folyó) áram számít, hanem a konvektív is (pl. vákuumban repülő ionok). Időben változó esetben a teljes alak az 1. Maxwell-egyenlet (+ eltolási áram).

**Végtelen egyenes vezető.** Szimmetria miatt H csak a távolságtól függ, és a vezető körüli körök mentén érintő irányú. Görbének egy r sugarú kört választunk: ezen H állandó, és párhuzamos az ívelemmel, így kiemelhető; a kör hossza 2rπ.

```latex
\oint_g\vec H\,d\vec s = H\oint_g ds = H\cdot 2r\pi = I \;\Rightarrow\; H = \frac{I}{2r\pi}
```

A tér a távolsággal fordítottan arányos.

**Vizsgán:** ∮H ds = ΣI, előjelezés, jobbcsavar; rot H = j; konvektív áram is számít; egyenes vezető: szimmetria, kör, H = I/(2rπ).

### 3. Szolenoid és toroid mágneses terének közelítő meghatározása

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

**Miről szól?** A hosszú, sűrűn tekercselt egyenes tekercs (szolenoid) belsejében a tér közel egyenletes, kívül pedig nagyon gyenge, mert a vonalak egy hatalmas térrészben oszlanak szét. Ezért a gerjesztési törvény egyszerű lesz: csak a tekercs belsején átmenő szakasz számít. A toroid egy körré hajlított szolenoid.

**Szolenoid.** Egy ABCD téglalapra írjuk fel a gerjesztési törvényt: AB (hossza x) a tekercs belsejében, a tengellyel párhuzamos; DC kint; AD és BC keresztben.

- DC: kint a tér elhanyagolható, ez a tag 0.
- AD és BC: a tér merőleges a görbére (ellentétes irányúak is), ezek kiesnek.
- AB: a tér egyenletes és párhuzamos, az integrál Hx.
- A körülzárt áram: az x hosszon lévő Nx/ℓ menet, mindegyikben I.

```latex
Hx = \frac{Nx}{\ell}I \;\Rightarrow\; H = \frac{NI}{\ell}, \qquad B = \mu\frac{NI}{\ell}
```

Akkor jó, ha a tekercs sokkal hosszabb, mint az átmérője, és bent-kint hasonló a permeabilitás. Vastag tekercs közepén: H = NI/√(4R² + ℓ²), ebből R → 0-ra visszakapjuk NI/ℓ-t, ℓ → 0-ra a karika NI/(2R)-jét.

**Toroid.** A görbe a toroid középvonalában, egy r sugarú körön fut, végig a tekercsen belül. Hossza 2πr, és mind az N menetet körülveszi:

```latex
H\cdot 2\pi r = NI \;\Rightarrow\; H = \frac{NI}{2\pi r}
```

Itt nincs „kint elhanyagoljuk” hiba, viszont vastag toroidnál a tér nem egyenletes (r függő); vékony toroidra egzakt.

**Vizsgán:** rajz az ABCD görbével; a négy szakasz indoklása; H = NI/ℓ, B = μNI/ℓ és a feltétel; toroid: kör a középvonalban, H = NI/(2πr).

### 4. Ampère-erő, Lorentz-erő. Sebességszűrő, ciklotron

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

**Miről szól?** Mágneses térben az áramjárta vezetőre erő hat (Ampère-erő). Mivel az áram mozgó töltések sokasága, ez tulajdonképpen az egyes mozgó töltésekre ható erők összege (Lorentz-erő). Ez az erő mindig merőleges a sebességre, ezért nem gyorsítja, csak eltéríti a részecskét, körpályára kényszeríti. Ezt használja a sebességszűrő és a ciklotron.

**Ampère-erő** (egyenes vezető, homogén tér; másképp kis darabokra bontva és összegezve):

```latex
\vec F = I\vec\ell\times\vec B \qquad \vec F = I\int d\vec r\times\vec B
```

**Lorentz-erő levezetése.** Legyen a vezetőben N db q töltésű részecske, mindegyik v sebességgel; Δt idő alatt teszik meg az ℓ hosszat. Ekkor I = Nq/Δt és v = ℓ/Δt, így:

```latex
F = BI\ell = BNq\frac{\ell}{\Delta t} = BNqv \;\Rightarrow\; \text{egy részecskére: } F = qvB, \qquad \vec F = q\,\vec v\times\vec B
```

A Lorentz-erő munkája a szabad töltésen mindig 0, mert merőleges a sebességre.

**Sebességszűrő.** Egymásra és a sebességre is merőleges E és B tér; az elektromos erő (qE) és a Lorentz-erő (qvB) ellentétes irányú. Csak az a részecske megy át eltérülés nélkül, amelyiknél a kettő kiegyenlíti egymást:

```latex
qE = qvB \;\Rightarrow\; v = \frac{E}{B}
```

A töltés kiesik: töltéstől függetlenül ugyanazt a sebességet választja ki.

**Ciklotron.** Részecskegyorsító: a két D alakú „duáns” között váltakozó feszültség gyorsítja a részecskét, a homogén mágneses tér körpályán tartja. A körmozgáshoz kellő centripetális erőt a Lorentz-erő adja:

```latex
QvB = m\frac{v^2}{r} \;\Rightarrow\; r = \frac{mv}{QB}, \qquad T = \frac{2r\pi}{v} = \frac{2\pi m}{QB}
```

Ahogy gyorsul, egyre nagyobb körön halad. A lényeg: **T nem függ a sebességtől**, ezért állandó frekvenciájú feszültség mindig jókor gyorsít (nemrelativisztikus esetben). Használat: orvosi radioizotópok, anyagvizsgálat, magfizika.

**Vizsgán:** F = Iℓ × B; Lorentz-erő levezetése az Ampère-erőből; F = qv × B, munkája 0; sebességszűrő v = E/B; ciklotron r és T, és miért fontos, hogy T nem függ v-től.

### 5. Áramjárta hurokra ható forgatónyomaték homogén térben. Mágneses dipólmomentum

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

**Miről szól?** Egy zárt áramhurokra egyenletes mágneses térben az oldalakra ható erők kioltják egymást, így nem mozdul el, de forgatónyomaték hat rá: befordul, mint egy iránytű. Ezért a hurokhoz (és minden kis mágneshez) egy vektort, a mágneses momentumot rendeljük, ami az elektromos dipólmomentum párja.

**Téglalap hurok.** Legyen B párhuzamos a b oldallal. A b oldalakra nem hat erő (párhuzamosak B-vel), a két a oldalra egyenként F = BIa hat, ellentétes irányban: eredő erő 0. A középponton átmenő tengelyre mindkettő ugyanarra forgat, karjuk b/2:

```latex
M = 2\cdot BIa\cdot\frac b2 = BIab = BIA
```

Általánosan: homogén térben zárt hurokra nincs eredő erő, a nyomaték pedig nem függ a hurok alakjától:

```latex
\vec M = I\vec A\times\vec B
```

Az A felületvektor irányát az áram körüljárásából a jobbcsavar-szabály adja.

**Mágneses dipólmomentum.** Az elektromos p = Qℓ analógiájára:

```latex
\vec m = I\vec A \qquad \vec M = \vec m\times\vec B \qquad E_p = -\vec m\vec B
```

Az m vektor hegye az északi, talpa a déli pólus (délről észak felé mutat). Az M = m × B állandó mágnesre (pl. mágnestűre) is érvényes. A nyomaték akkor szűnik meg, ha m ∥ B: a momentum befordul a tér irányába, mert ott minimális az energia. Ezért egy kis áramhurok iránytűként viselkedik. (Eₚ = −m·B a Zeeman-energia.)

**Vizsgán:** téglalap hurok rajzzal, erők, eredő erő 0; M = BIA levezetve; M = IA × B; m = IA, egysége, északi-déli pólus; M = m × B; Eₚ = −m·B.

### 6. Inhomogén mágneses tér (vázlatosan). Mágnesek vonzása és taszítása

| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| B, ΔB | mágneses indukció, és mennyivel nagyobb a hurok egyik oldalán | T |
| F, ΔF | erő, erőkülönbség | N |
| I | áram a hurokban | A |
| a, b | a hurok oldalai | m |
| m | mágneses momentum | Am² |
| Eₚ | helyzeti energia | J |

**Miről szól?** Ha a tér nem egyenletes, a hurok egyik oldalára nagyobb erő hat, mint a másikra, így marad egy eredő erő: a hurok (vagy mágnes) mozdulni kezd. Ezzel magyarázható, miért vonzza vagy taszítja egymást két mágnes. Ugyanez a helyzet, mint az elektromos dipólusnál: homogén térben csak forgatónyomaték, inhomogénben erő is.

**Téglalap hurok.** Ugyanaz, mint az 5. tételben, de a jobb oldalon az indukció B + ΔB. Ott az erő F + ΔF, így az eredő (m = abI felhasználásával):

```latex
\sum F = \Delta F = Ia\,\Delta B = m\frac{\Delta B}{b}
```

Az erő a momentummal és a tér változásának meredekségével (gradiensével) arányos. Általános hurokra az Ampère-erőt kell végigintegrálni (F = I∮dr × B), egyszerű pontos képlet nincs. Kis hurokra a közelítés:

```latex
\vec F = \operatorname{grad}\left(\vec m\vec B\right) = -\operatorname{grad}E_p
```

**Vonzás és taszítás.** Egy kör alakú hurok alatt, szimmetrikusan áll egy rúdmágnes, északi pólusa felfelé. A mágnes B vonalai a hurok minden kis darabjánál ferdén, kifelé-felfelé mutatnak. Az egyes darabokra ható Ampère-erők kifelé-lefelé mutatnak; a vízszintes részeik a szimmetria miatt kioltják egymást, a függőleges részek összeadódnak: az eredő erő lefelé, a mágnes felé mutat. A hurok momentuma felfelé mutat, ugyanúgy, mint a mágnesé. Tehát **az azonos irányba álló momentumok vonzzák, az ellentétesek taszítják egymást.** Ellenőrzés a képlettel: m·B pozitív, és lefelé (a pólus felé) nő, ezért az erő lefelé mutat.

**Vizsgán:** homogén térben csak nyomaték, inhomogénben erő is; ΔF = IaΔB = mΔB/b; F = grad(m·B); a körhurok-rúdmágnes rajza és a következtetés.

### 7. Mágneses fluxus és Gauss-törvény. Mágneses polarizáció. Mágneses szuszceptibilitás és H

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

**Miről szól?** A fluxus azt méri, mennyi mágneses erővonal megy át egy felületen. Mivel mágneses töltés nincs, a vonalak mindig zártak: egy zárt felületbe ugyanannyi megy be, mint ki. Az anyagban az atomok kis köráramként viselkednek (elektronok keringenek, illetve saját spin), ezek momentumai a térben rendeződhetnek: az anyag felmágneseződik. Ezt méri M, és χ azt, mennyire könnyen. A H vektort úgy vezetjük be, hogy rá egyszerű legyen a gerjesztési törvény.

**Fluxus és Gauss-törvény.** Homogén térben, illetve általánosan:

```latex
\Phi = \vec B\vec A = BA\cos\alpha \qquad \Phi = \int_A\vec B\,d\vec A \qquad \oint\vec B\,d\vec A = 0,\quad \operatorname{div}\vec B = 0
```

**Mágnesezettség.** Az atom mágneses momentuma lényegében az elektronoké (a magoké sokkal kisebb), két részből: pályamozgás (kis köráram) és saját (spin) momentum. A mágnesezettség az egységnyi térfogatra jutó momentum; állandó mágnesben is délről észak felé mutat. Felfogható úgy, hogy „molekuláris áramok” keltik.

```latex
\vec M = \lim_{\Delta V\to0}\frac{\sum\vec m}{\Delta V}
```

**A mágneses térerősség és a szuszceptibilitás.** Definíció, majd a lineáris anyagegyenlet (izotróp anyagban M arányos H-val):

```latex
\vec H = \frac{\vec B}{\mu_0} - \vec M \;\Leftrightarrow\; \vec B = \mu_0\left(\vec H + \vec M\right) \qquad \vec M = \chi\vec H
```

```latex
\vec B = \mu_0\left(\vec H + \chi\vec H\right) = \mu_0(1+\chi)\vec H = \mu_0\mu_r\vec H = \mu\vec H
```

Ez csak közelítés; kemény ferromágneseknél teljesen rossz.

**Anyagtípusok.** Külső térben két folyamat zajlik: a *diamágneses* (minden atomban indukálódik egy kis momentum, a tér ellen) és a *paramágneses* (a már meglévő atomi momentumok a tér irányába fordulnak, a hőmozgás ellenében).

| Típus | χ | Viselkedés |
| --- | --- | --- |
| diamágneses | negatív, nagyon kicsi (μᵣ ≈ 0,9999) | atomjainak nincs saját momentuma; a mágnes taszítja (bizmut) |
| paramágneses | pozitív, kicsi (10⁻³...10⁻⁶) | van saját momentum, de tér nélkül rendezetlen; a mágnes gyengén vonzza (alumínium); Curie-törvény: χ \~ 1/T |
| ferromágneses | nem lineáris, nagy | erősen mágnesezhető, megtartja a mágnesességét; telítés, hiszterézis |

**Hiszterézisgörbe** (ferromágnes): nulláról a kezdeti görbén haladunk a telítésig; H-t visszaveszük, de B nem ugyanott jön vissza, H = 0-nál marad Bᵣ (**remanens indukció**). Az ellentétes tér, amelynél B = 0, a H\_c **koercítiv térerősség**. Kis H\_c: lágymágnes (trafomag); nagy Bᵣ és H\_c: keménymágnes (állandó mágnes).

**Vizsgán:** Φ definíciója; ∮B dA = 0, div B = 0 és jelentése; az elektron két momentuma; M definíciója; H = B/μ₀ − M; M = χH → B = μ₀(1+χ)H; a három anyagtípus; a hiszterézis fő pontjai.

### 8. Elektromágneses indukció. Neumann-törvény, Faraday-Lenz törvény. Lineáris és váltóáramú generátor

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

**Miről szól?** Mágneses térrel áramot lehet csinálni. Kétféleképpen: ha a vezetőt mozgatjuk a térben, a benne lévő töltésekre Lorentz-erő hat, ez hajtja őket (mozgási indukció). Ha a vezető áll, de a tér változik, a változó tér elektromos teret kelt, az hajtja a töltéseket (nyugalmi indukció). Mindkettőt ugyanaz a szabály írja le: az indukált feszültség annyi, amilyen gyorsan változik a hurkon átmenő fluxus, és mindig úgy, hogy a változást akadályozza (Lenz).

**Mozgási indukció, Neumann-törvény.** A mozgó vezető töltéseire ható Lorentz-erő egy „idegen” térerősségként viselkedik, és a vezető mentén elektromotoros erőt kelt:

```latex
\vec F^* = q\,\vec v\times\vec B \qquad \vec E^* = \frac{\vec F^*}{q} = \vec v\times\vec B \qquad \varepsilon_{AB} = \int_A^B\left(\vec v\times\vec B\right)d\vec s
```

**Lineáris generátor.** Síneken csúszó ℓ hosszú rúd; v, B és a rúd egymásra merőlegesek. Az indukált elektromotoros erő és az áram:

```latex
\varepsilon = v\ell B \qquad I = \frac{\varepsilon}{R}
```

Honnan van az energia? Az indukált áram miatt a rúdra Ampère-erő hat, a mozgással szemben (Lenz). Ezt egy húzóerővel kell legyőzni, és ennek munkája lesz az elektromos energia. A generátor mechanikai munkát alakít elektromossá.

**A fluxus-szabály levezetése.** A hurok területe A = ℓh. A rúd v sebességgel mozog, ezért a terület dA/dt = −ℓv ütemben változik. A fluxus változása:

```latex
\frac{d\Phi}{dt} = \frac{d(BA)}{dt} = B\frac{dA}{dt} = -B\ell v = -\varepsilon
```

Általánosan, bármilyen mozgó (akár alakváltozó) zárt hurokra, ez a **Faraday-törvény** (fluxus-szabály):

```latex
\varepsilon = -\frac{d\Phi}{dt}
```

Ez sokszor egyszerűbb, mint a Neumann-törvény. Például látszik belőle, hogy homogén térben egyenesen mozgó keretben nem indukálódik semmi (a fluxus nem változik).

**Nyugalmi indukció.** A fluxus úgy is változhat, hogy a hurok áll, csak B változik. Ilyenkor nem a Lorentz-erő hat, hanem a változó mágneses tér elektromos teret kelt. Ha egy másik tekercs áramának változása okozza, az a kölcsönös indukció; ha a saját áramé, az önindukció (9. tétel). Az összefoglaló alak:

```latex
\oint_g\vec E\,d\vec s = -\frac{d}{dt}\int_F\vec B\,d\vec A
```

Az indukált elektromos tér örvényes, nem konzervatív (nem a töltések keltik, forrásmentes).

**Lenz-törvény** (a mínusz jel): az indukált áram az őt létrehozó változás ellen hat; ha a fluxus csökken, olyan áram jön létre, amely növelné. Ha fordítva lenne, az indukció erősítené önmagát, és a semmiből energia keletkezne.

**Váltakozó áramú generátor.** A területű keret ω szögsebességgel forog homogén B térben; kezdetben a keret síkjára merőleges irány egyirányú B-vel, így a szögük ωt:

```latex
\Phi = BA\cos\omega t \;\Rightarrow\; \varepsilon = -\frac{d\Phi}{dt} = BA\omega\sin\omega t = \varepsilon_0\sin\omega t
```

Szinuszos váltakozó feszültség. N menetnél minden meneten átmegy a fluxus, így N-szeres:

```latex
\varepsilon = NAB\omega\sin\omega t
```

**Vizsgán:** E\* = v × B, Neumann-törvény; lineáris generátor ε = vℓB és az energiamérleg; a fluxus-szabály levezetése; nyugalmi indukció; Lenz és a mínusz jel oka; váltóáramú generátor.

### 9. Önindukció és önindukciós együttható

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

**Miről szól?** Ha egy tekercsben változik az áram, változik a saját mágneses tere és a saját fluxusa is, ez pedig magában a tekercsben indukál feszültséget. Lenz miatt ez a feszültség mindig a változás ellen dolgozik: a tekercs „nem szereti”, ha változtatják az áramát. Az L együttható azt mondja meg, mennyire erős ez a hatás.

**Szolenoid L-je.** A tekercsben H = NI/ℓ és B = μNI/ℓ (3. tétel).

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

Az indukált feszültség arányos az áram változásának gyorsaságával. L a menetszám **négyzetével** nő (ezért van sok menet) és a permeabilitással (ezért tesznek bele vasmagot). Mivel lineáris anyagot tételeztünk fel, vasmagra csak korlátozottan igaz.

**Kölcsönös indukció** (kiegészítés): két tekercs közös vasmagon, N₁ és N₂ menettel. Az első árama a másodikban Φ₁₂ = MI₁ fluxust kelt, ahol M = μN₁N₂A/ℓ, és ott U₁₂ = −M dI₁/dt feszültséget indukál.

**Vizsgán:** a jelenség és Lenz; menetfluxus, tekercsfluxus; Φ = LI mint definíció; szolenoidra L = μN²A/ℓ levezetve, egysége; U = −L dI/dt; miért sok menet és vasmag.

### 10. Az általános huroktörvény

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

**Miről szól?** A sima Kirchhoff-huroktörvény (ΣU = 0) csak akkor igaz, ha nincs változó mágneses tér. Ha a körben tekercs van és változik az áram, a saját indukció miatt a térerősség körbeintegrálja nem nulla. Ezt úgy kezeljük, hogy a tekercs L·dI/dt tagját is egyfajta feszültségként számoljuk, és így egy soros RLC körre is felírható egy hurokegyenlet.

**Levezetés:**

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

Négy különböző fajta „feszültség”: a tekercsé (saját indukció), az ellenállásé, a kondenzátoré, és a forrásé. Az ε vagy nem elektromos energiát alakít át (elem, napelem), vagy távoli indukcióból származik (erőmű), nem a vizsgált kör saját fluxusváltozásából.

**Vizsgán:** az RLC kör rajza; Faraday-törvény a hurokra, −L dI/dt; a görbe szétbontása; L dI/dt + IR + Q/C = ε; miért nem érvényes itt a sima ΣU = 0.

### 11. Tranziens jelenségek. Az RL és RC kör időállandója

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

**Miről szól?** Ha egy körben hirtelen megváltozik a feszültség (bekapcsolunk, kikapcsolunk), az áram nem ugrik azonnal az új értékre, hanem fokozatosan, exponenciálisan áll be. Ez az átmeneti (tranziens) szakasz. Az időállandó τ megmondja, milyen gyors ez: τ idő alatt az eltérés e-ad részére (kb. 37%-ra) csökken.

**Kondenzátor kisütése (RC kör).** A feltöltött kondenzátort R ellenálláson keresztül kisütjük. A huroktörvény (nincs forrás):

```latex
IR + \frac{Q}{C} = 0, \qquad I = \frac{dQ}{dt}
```

1. Idő szerint deriválva (dQ/dt = I) és átrendezve: dI/dt = −I/(RC).
2. Szétválasztjuk a változókat és integrálunk I₀-tól I-ig, illetve 0-tól t-ig:

```latex
\int_{I_0}^{I}\frac{dI}{I} = -\frac{1}{RC}\int_0^t dt \;\Rightarrow\; \ln\frac{I}{I_0} = -\frac{t}{RC}
```

3. Ebből:

```latex
I(t) = I_0e^{-t/\tau}, \qquad \tau = RC, \qquad I_0 = \frac{U_0}{R}
```

**Tekercs hirtelen változó feszültségen (RL kör).** A forrás feszültsége t = 0-ban ε₁-ről ε₂-re ugrik (bármelyik lehet 0). Az általános huroktörvény:

```latex
IR - \varepsilon_2 = -L\frac{dI}{dt}
```

**Kezdeti feltétel:** az áram nem ugorhat hirtelen, mert akkor dI/dt és vele az indukált feszültség végtelen lenne. Tehát t = 0-ban még a régi áram folyik: I₀ = ε₁/R.

1. Szétválasztva és integrálva:

```latex
\int_{I_0}^{I}\frac{dI}{\varepsilon_2 - RI} = \frac1L\int_0^t dt \;\Rightarrow\; \varepsilon_2 - RI = \left(\varepsilon_2 - RI_0\right)e^{-\frac RL t}
```

2. R-rel osztva, I∞ = ε₂/R jelöléssel, és τ = L/R bevezetésével:

```latex
I(t) = I_0e^{-t/\tau} + I_\infty\left(1 - e^{-t/\tau}\right), \qquad \tau = \frac{L}{R}
```

A régi áram exponenciálisan eltűnik, az új ugyanolyan ütemben épül fel. **Kikapcsolás** (I∞ = 0): I = I₀e^(−t/τ). **Bekapcsolás** (I₀ = 0): I = I∞(1 − e^(−t/τ)).

(Megjegyzés: LC körben ellenállás nélkül szinuszos rezgés jön létre, ellenállással csillapított rezgés.)

**Vizsgán:** mi a tranziens; RC kisütés levezetése, τ = RC és jelentése; RL kör egyenlete, a kezdeti feltétel indoklása, a megoldás, τ = L/R; be- és kikapcsolás.

### 12. Tekercs mágneses terének energiája. A mágneses tér energiasűrűsége

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

**Miről szól?** Amikor bekapcsoljuk a tekercset, az áram növekedése ellenfeszültséget indukál (Lenz), és a forrásnak ez ellenében kell átvinnie a töltéseket. Ez a munka nem vész el: a tekercs mágneses terében tárolódik. Ugyanúgy, ahogy a kondenzátor az elektromos térben tárol energiát (10. tétel, 1. rész), a tekercs a mágnesesben.

**A munka.** Egy kis dq töltés átvitele az U = L dI/dt ellenfeszültség ellenében, dq = I dt:

```latex
dW = U\,dq = L\frac{dI}{dt}\,I\,dt = LI\,dI
```

0-tól a végső áramig integrálva (L állandó, lineáris közeg):

```latex
W = \int_0^{I_\infty}LI\,dI = L\left[\frac{I^2}{2}\right]_0^{I_\infty} \;\Rightarrow\; W_m = \frac12 LI^2
```

**Energiasűrűség.** Hosszú szolenoidba beírjuk L = μN²A/ℓ-t, és észrevesszük benne H = NI/ℓ-t és B = μNI/ℓ-t:

```latex
W_m = \frac12\mu\frac{N^2A}{\ell}I^2 = \frac12\cdot\mu\frac{NI}{\ell}\cdot\frac{NI}{\ell}\cdot A\ell = \frac12 BH\,V
```

V = Aℓ a tekercs belsejének térfogata, itt homogén a tér. Térfogattal osztva:

```latex
w_m = \frac12\vec B\vec H
```

(Az elektromos w = ½D·E párja.) Megjegyzés: a bekapcsolás nem azért tart ideig, mert az elektronokat nehéz felgyorsítani; ez az energia a mágneses téré, nem az elektronok mozgási energiája.

**Vizsgán:** miért kell munka a bekapcsoláshoz; dW = LI dI; Wₘ = ½LI²; szolenoidra W = ½BHV; wₘ = ½B·H.

### 13. Mágneses mennyiségek két közeg határán. B és H vonalak törése

| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| 1, 2 index | az 1-es és a 2-es közegben |  |
| t, n index | a határral párhuzamos, illetve rá merőleges komponens |  |
| H, B | mágneses térerősség, indukció | A/m, T |
| μ₁, μ₂ | a két közeg permeabilitása | Vs/(Am) |
| α, β | a vonal és a határra merőleges egyenes közti szög az 1-es, illetve 2-es közegben | rad |

**Miről szól?** Pontosan ugyanaz a módszer és eredmény, mint az elektromos esetnél (1. rész 14. tétel), csak E helyett H, D helyett B és ε helyett μ szerepel. A határral párhuzamos H nem ugrik (ha nincs felületi áram), a merőleges B nem ugrik (mert nincs mágneses töltés). Ezért a vonalak megtörnek.

**Tangenciális komponens.** A határt két oldalról ölelő lapos hurokra az 1. Maxwell-egyenlet: ∮H ds = (átfolyó áram) + d/dt(D fluxusa). A hurkot a határra lapítva a rövid oldalak eltűnnek, és a körbezárt felület is, így a jobb oldal is (feltéve, hogy a határon **nincs felületi áram**):

```latex
\int_A^B\left(\vec H_2 - \vec H_1\right)d\vec s = 0 \;\Rightarrow\; H_{t2} = H_{t1}, \qquad \frac{B_{1t}}{B_{2t}} = \frac{\mu_1}{\mu_2}
```

**Normális komponens.** Lapos doboz a határon, a mágneses Gauss-törvény (∮B dA = 0). Lapítva a palást eltűnik, a két lap fluxusa egyenlő és ellentétes:

```latex
B_{n2} = B_{n1} \qquad \mu_1H_{1n} = \mu_2H_{2n} \;\Rightarrow\; \frac{H_{1n}}{H_{2n}} = \frac{\mu_2}{\mu_1}
```

(Itt nincs „felületi töltés” tag, mert mágneses töltés nincs.)

**Törési törvény** (tangens = párhuzamos/merőleges komponens):

```latex
\frac{\operatorname{tg}\alpha}{\operatorname{tg}\beta} = \frac{H_{1t}/H_{1n}}{H_{2t}/H_{2n}} = \frac{H_{2n}}{H_{1n}} = \frac{\mu_1}{\mu_2}
```

B-re ugyanez jön ki. Következmény: a nagy μ-jű vasból a vonalak szinte merőlegesen lépnek ki a levegőbe.

**Vizsgán:** hurok és doboz rajza; Hₜ₁ = Hₜ₂ (feltétel: nincs felületi áram); Bₙ₁ = Bₙ₂; tgα/tgβ = μ₁/μ₂.

### 14. A mágneses térmennyiségek forrásai és örvényei

| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| H, B, M | mágneses térerősség, indukció, mágnesezettség | A/m, T, A/m |
| j | makroszkopikus (vezetéki) áramsűrűség | A/m² |
| jₘ | molekuláris (atomon belüli) áramsűrűség | A/m² |
| ρₘ | effektív mágneses töltéssűrűség (északi pólusnál +, délinél −) | A/m² |
| μ₀ | vákuum permeabilitása | Vs/(Am) |
| rot, div | örvényesség, forrásosság |  |

**Miről szól?** Összeszedjük, mi kelti a három mágneses mennyiség örvényeit (ami köré „tekerednek”) és forrásait (amiből „kiindulnak”). Az örvényeket áramok keltik, a forrásokat a mágneses pólusok. A B-nek nincs forrása, a H-nak és M-nek viszont a pólusoknál van, ellentétes előjellel. Ebből jön ki a meglepő eredmény: egy állandó mágnes belsejében H és M ellentétes irányú.

**Örvények** (stacionárius esetben):

```latex
\operatorname{rot}\vec H = \vec j \qquad \operatorname{rot}\vec M = \vec j_m \qquad \operatorname{rot}\vec B = \mu_0\operatorname{rot}\left(\vec H + \vec M\right) = \mu_0\left(\vec j + \vec j_m\right)
```

H örvényeit a vezetékekben folyó áramok, M örvényeit a molekuláris áramok, B-éit mindkettő kelti.

**Források:**

```latex
\operatorname{div}\vec M = -\rho_m \qquad \operatorname{div}\vec B = 0 \;\xrightarrow{\ B = \mu_0(H+M)\ }\; \operatorname{div}\vec H = -\operatorname{div}\vec M = \rho_m
```

|  | Örvényét kelti | Forrása |
| --- | --- | --- |
| H | makroszkopikus áram (j) | mágneses pólusok (ρₘ) |
| M | molekuláris áram (jₘ) | pólusok ellentétes előjellel (−ρₘ) |
| B | mindkettő, μ₀(j + jₘ) | nincs |

**Következmény:** egy állandó mágnes két pólusa között H és M vonalai ellentétes irányba futnak. A lineáris M = χH ebből negatív χ-t adna, holott ferromágnesre χ nagy pozitív: nemlineáris anyagnál a szuszceptibilitás nem így értendő (16. tétel). Általában három dolog kelt H teret: az áramok és az eltolási áram (örvényes rész), valamint a mágneses pólusok (forrásos rész).

(Példa a jegyzetből: egyenletesen mágnesezett hasb felső lapján M hirtelen nullára esik, ott rot M ≠ 0, vagyis ott folynak a molekuláris áramok; a póluslapokon viszont M forrásos, de nem örvényes.)

**Vizsgán:** a három rot és a három div egyenlet, div H = ρₘ levezetése; a táblázat; H és M ellentétes a mágnesben; H három forrása.

### 15. Lemágnesező tér, állandó mágnesek

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

**Miről szól?** Ha egy anyagot felmágnesezünk, a két végén mágneses pólusok alakulnak ki, és ezek saját teret keltenek. Ez a saját tér bent mindig a mágnesezettség ellen mutat, tehát gyengíti a teret: ez a lemágnesező tér (ugyanaz, mint a depolarizáció az elektromos esetben). Az, hogy mennyire erős, csak a test alakjától függ: egy hosszú tűben szinte nincs, egy lapos korongban nagyon erős.

**A tényleges belső tér.** Mivel a terek összeadhatók, bent az alkalmazott és a saját tér összege van:

```latex
\vec H_{in} = \vec H_a + \vec H_d
```

Paramágneses vagy lágy ferromágneses anyagban M a külső térrel egyirányú lesz, H\_d pedig ellentétes vele, ezért bent kisebb a tér, mint vákuumban volt: H\_in < Hₐ.

**Lemágnesezési tényező.** Általában a tér a testben nem homogén és nehéz számolni. Ellipszoid alakú testnél viszont (ha egy főtengelye a külső térrel párhuzamos) bent minden homogén, és a lemágnesező tér arányos a mágnesezettséggel:

```latex
\vec H_d = -N\vec M \qquad N_x + N_y + N_z = 1
```

Gömbnél a szimmetria miatt mindhárom egyforma, tehát N = 1/3, H\_d = −M/3.

**Gömb alakú állandó mágnes** külső tér nélkül (Hₐ = 0, tehát H\_in = H\_d). A B = μ₀(H + M) képletből:

```latex
\frac{\vec B}{\mu_0} = \vec H_d + \vec M = -\frac13\vec M + \vec M = \frac23\vec M = -2\vec H_d
```

A mágnes belsejében tehát H ellentétes irányú B-vel (és M-mel), és fele akkora. Az északi pólus H-nak forrása, M-nek nyelője, a déli fordítva. A mágnesen kívül (vákuumban) H és B/μ₀ megegyezik.

**Határesetek:**

| Alak | N a hossztengely (x) mentén | N keresztben |
| --- | --- | --- |
| gömb | 1/3 | 1/3 |
| hosszú tű | → 0 | → 1/2 |
| lapos korong (x a vastagság iránya) | → 1 | → 0 |

Magyarázat (energiaminimum): ha a gömböt x irányban nyújtjuk, a B vonalaknak a test mellett egyre több hely jut, ritkulnak; a határfeltételek miatt ezért a H is ritkul a test mellett és benne is, tehát Nₓ → 0. (Különben a nagyon hosszú test mellett óriási térfogatban lenne erős tér, és divergens lenne az energia.) Lapításnál a nagy lapokon átmenő B-nek kell kicsinek lennie; B = μ₀(M − abs(H)) akkor minimális, ha H = M, vagyis Nₓ = 1.

**Vizsgán:** a lemágnesező tér fogalma, H\_in = Hₐ + H\_d; miért kisebb bent a tér; H\_d = −NM, ΣN = 1; gömb állandó mágnes: N = 1/3, B/μ₀ = (2/3)M = −2H\_d; tű és korong.

### 16. A hiszterézisgörbe korrekciója, alakanizotrópia, a szuszceptibilitás értelmezése

| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| Hₐ | alkalmazott (mérhető, külső) tér | A/m |
| H\_in | a valódi tér az anyagban | A/m |
| M | mágnesezettség | A/m |
| N | lemágnesezési tényező | nincs |
| χ | szuszceptibilitás | nincs |
| χ\_true | valódi (az anyagra jellemző) szuszceptibilitás, H\_in-hez viszonyítva | nincs |
| χ\_meas | mért szuszceptibilitás, Hₐ-hoz viszonyítva (a minta alakja is benne van) | nincs |

**Miről szól?** A lemágnesező tér miatt ugyanaz az anyag különböző alakú darabokban látszólag különböző mértékben mágnesezhető: egy tűt hosszanti irányban sokkal könnyebb, mint keresztben. Ez az **alakanizotrópia** (nem az anyag, hanem az alak miatt irányfüggő). Ezért amikor mérjük a hiszterézisgörbét (amit a külső tér függvényében tudunk), azt át kell számolni a valódi belső térre, hogy az anyagot jellemezze, ne a minta alakját. Ugyanígy meg kell különböztetni a mért és a valódi szuszceptibilitást.

**Alakanizotrópia.** A 15. tételből Hₐ = H\_in − H\_d = H\_in + NM. A kezdeti szakaszon a lineáris közelítéssel (M = χH\_in):

```latex
H_a = H_{in} + N\chi H_{in} = (1 + N\chi)\,H_{in}
```

- **Tű hosszban** (N = 0): Hₐ = H\_in, a belső tér egyenlő a külsővel.
- **Tű keresztben** (N = 1/2, pl. χ = 10): Hₐ = (1 + 10/2)H\_in = 6H\_in. Ugyanakkora mágnesezettséghez hatszor nagyobb külső tér kell, azaz keresztben a mért szuszceptibilitás a valódi hatoda. Nagyobb χ-nél még nagyobb az eltérés.

**A hiszterézisgörbe korrekciója.** Az M görbét kétféleképpen rajzolhatjuk: a külső Hₐ függvényében (ezt mérjük) vagy a belső H\_in függvényében. Ha N ≠ 0, a kettő az M = 0 pontokat kivéve eltér. A mértből a H\_in = Hₐ − NM összefüggéssel számoljuk ki a másodikat: ez a korrekció. A szakirodalomban megadott görbe általában már a korrigált, ami az anyagot írja le.

**A szuszceptibilitás értelmezése.** Nemlineáris anyagnál az M/H arány nem állandó, ezért inkább a görbe meredekségét használják (differenciális szuszceptibilitás):

```latex
\chi = \frac{dM}{dH}
```

Ez viszont függ attól, hol vagyunk a görbén (pl. ideális állandó mágnes görbéje „kövér téglalap”, a meredekség szinte mindenhol 0). Egyértelműbb az origó körüli érték, és ott is két változat van:

```latex
\chi_{true} = \frac{M}{H_{in}}\bigg|_{M,H\to0} \qquad \chi_{meas} = \frac{M}{H_a}\bigg|_{M,H\to0}
```

A kapcsolatuk: H\_in = Hₐ − NM-et beírva és M/Hₐ-val (= χ\_meas) egyszerűsítve:

```latex
\chi_{true} = \frac{M}{H_a - NM} = \frac{\chi_{meas}}{1 - N\chi_{meas}} \qquad\Longleftrightarrow\qquad \chi_{meas} = \frac{\chi_{true}}{1 + N\chi_{true}}
```

(A tűs példában χ\_true = 10, N = 1/2 esetén χ\_meas = 10/6, valóban hatoda.)

**Vizsgán:** Hₐ = H\_in + NM = (1 + Nχ)H\_in; tű hosszban és keresztben; az alakanizotrópia fogalma; a korrekció lényege; dM/dH; χ\_true és χ\_meas kapcsolata.

### 17. Mágneses skálarpotenciál. Mágneses körök, soros és párhuzamos kapcsolás

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

**Miről szól?** Ahol nincs áram, a mágneses tér örvénymentes, így ugyanúgy rendelhető hozzá potenciál, mint az elektrosztatikus térhez. Ebből egy hasznos analógia jön: a vasmagos mágneses körök úgy számolhatók, mint az áramkörök. A tekercs gerjesztése (NI) a feszültségforrás, a fluxus az áram, a vas és a légrés pedig ellenállások; még Ohm- és Kirchhoff-törvény is van.

**Mágneses skálarpotenciál.** Ha nincs áram és változó elektromos tér, rot H = 0, tehát (potenciálos mezők tétele) létezik Uₘ. Egy P₀ pontban nullának választva:

```latex
\vec H = -\operatorname{grad}U_m \qquad U_m(A) = \int_A^{P_0}\vec H\,d\vec s \qquad \oint\vec H\,d\vec s = \sum U_m = 0
```

Ritkábban használják, mint az elektromos feszültséget, mert nincs olyan szemléletes jelentése (nem munka). Ha áram is van, a hurok mentén nem 0 az összeg, hanem a körülzárt gerjesztés (gerjesztési törvény):

```latex
\sum U_m = \varepsilon_m = NI
```

**Mágneses ellenállás és Ohm-törvény.** Egy homogén, ℓ hosszú, A keresztmetszetű testben Uₘ = Hℓ és Φ = BA = μHA. A hányadosuk:

```latex
R_m = \frac{U_m}{\Phi} = \frac{H\ell}{\mu HA} = \frac{\ell}{\mu A} \qquad U_{m,i} = R_{m,i}\,\Phi
```

(Pont olyan, mint az R = ρℓ/A, csak ρ helyett 1/μ.)

**Csomóponti törvény.** A mágneses Gauss-törvény (∮B dA = 0) miatt egy elágazásba befutó és kifutó fluxusok összege 0 (mint az áramoknál a kontinuitás miatt):

```latex
\sum_k\Phi_k = 0
```

**Soros és párhuzamos kapcsolás.** Egymáshoz erősített vastestekben ugyanaz a fluxus halad végig (soros kapcsolás), a mágneses feszültségek összeadódnak. Elágazó körben (párhuzamos) a feszültség közös, a fluxus megoszlik:

```latex
\text{soros: } R_{m,eredő} = \sum_n R_{m,n} \qquad \text{párhuzamos: } \frac{1}{R_{m,eredő}} = \sum_n\frac{1}{R_{m,n}}
```

**Légrés:** a levegő permeabilitása nagyságrendekkel kisebb a vasénál, ezért még egy vékony légrés is nagyon megnöveli a kör mágneses ellenállását, és sokkal nagyobb áram kell ugyanakkora fluxushoz. (A légrésnél pólusok jelennek meg, amelyek lemágnesező teret keltenek.)

**Vizsgán:** rot H = 0 feltétele, H = −grad Uₘ, ΣUₘ = 0 illetve NI; az analógia (NI ↔ feszültség, Φ ↔ áram); Rₘ = ℓ/(μA) levezetve; mágneses Ohm-törvény; ΣΦ = 0; soros és párhuzamos eredő; légrés hatása.

### 18. Elektromágneses hullámok szigetelőkben. A homogén hullámegyenlet

| Jel | Mit jelent | Mértékegység |
| --- | --- | --- |
| E, D | elektromos térerősség, indukció | V/m, C/m² |
| H, B | mágneses térerősség, indukció | A/m, T |
| ε, μ | a közeg permittivitása és permeabilitása | As/(Vm), Vs/(Am) |
| j, ρ | áramsűrűség, töltéssűrűség (itt mindkettő 0) | A/m², C/m³ |
| Δ | Laplace-operátor: ∂²/∂x² + ∂²/∂y² + ∂²/∂z² (vektorra komponensenként) | 1/m² |
| ∂²/∂t² | második derivált az idő szerint | 1/s² |

**Miről szól?** A Maxwell-egyenletekből kijön, hogy léteznek elektromágneses hullámok. A változó elektromos tér mágneses teret kelt (1. ME), a változó mágneses tér elektromosat (2. ME), és így egymást fenntartva terjednek. Ha a két egyenletet összefűzzük, mindkét térre egy-egy hullámegyenlet adódik, ugyanolyan alakú, mint egy rezgő húré.

**Feltételek:** vákuum vagy homogén, izotróp, lineáris szigetelő: nincs áram és töltés (j = 0, ρ = 0), D = εE és B = μH. Ekkor az első két Maxwell-egyenlet:

```latex
\operatorname{rot}\vec H = \frac{\partial\vec D}{\partial t} \qquad \operatorname{rot}\vec E = -\frac{\partial\vec B}{\partial t}
```

**Levezetés a mágneses térre:**

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

Komponensenként kiírva pl. az x komponensre:

```latex
\frac{\partial^2 H_x}{\partial x^2} + \frac{\partial^2 H_x}{\partial y^2} + \frac{\partial^2 H_x}{\partial z^2} = \varepsilon\mu\frac{\partial^2 H_x}{\partial t^2}
```

A „homogén” itt azt jelenti, hogy az egyenletben nincs forrástag: a vizsgált helyen nincsenek töltések és áramok, a hullám nem itt keletkezik, csak áthalad. (Nem azonos azzal, hogy maga a közeg homogén, bár azt is feltettük.)

**Vizsgán:** a feltételek; az 1. és 2. ME; a négy lépés (rot, azonosság és div H = 0, behelyettesítés); ΔH = εμ∂²H/∂t² és ΔE = εμ∂²E/∂t²; mit jelent itt a homogén.

### 19. Síkhullám megoldás, a fénysebesség. Transzverzalitás, Poynting-vektor

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

**Miről szól?** A hullámegyenletnek megoldása a jól ismert szinuszos síkhullám. Ha visszahelyettesítjük, kijön, milyen gyorsan terjed: a közeg ε-jától és μ-jétől függ, vákuumban pont a fénysebesség. Az E és H egymásra és a terjedés irányára is merőleges (transzverzális hullám). A hullám energiát szállít, ennek áramlását és irányát a Poynting-vektor adja meg.

**Síkhullám megoldás.** Pozitív x irányba haladó hullám:

```latex
E = E_0\sin\left(2\pi\left(ft - \frac{x}{\lambda}\right)\right) \qquad H = H_0\sin\left(2\pi\left(ft - \frac{x}{\lambda}\right)\right)
```

Visszahelyettesítve a hullámegyenletbe (a kétszeri x szerinti deriválás (2π/λ)²-et, a kétszeri t szerinti (2πf)²-et hoz ki):

```latex
\frac{1}{\lambda^2f^2} = \varepsilon\mu
```

**Fénysebesség.** A terjedési sebesség c = fλ, ebből:

```latex
c = f\lambda = \frac{1}{\sqrt{\varepsilon\mu}} \qquad c_0 = \frac{1}{\sqrt{\varepsilon_0\mu_0}} = 3\cdot10^8\,\frac{\mathrm m}{\mathrm s} \qquad \frac{c_0}{c_{közeg}} = \sqrt{\varepsilon_r\mu_r}
```

A vákuumbeli érték az ismert állandókból (ε₀ = 1/(4π·9·10⁹), μ₀ = 4π·10⁻⁷) kiszámolható, és egyezik a mért fénysebességgel. Anyagban lassabb (minél nagyobb εᵣμᵣ, annál lassabb). Más alakban, illetve tetszőleges irányba haladó hullámra:

```latex
E = E_0\sin(\omega t - kx) \qquad \vec E = \vec E_0\sin\left(\omega t - \vec k\vec r\right) \qquad \vec H = \vec H_0\sin\left(\omega t - \vec k\vec r\right)
```

Az azonos fázisú pontok síkokat alkotnak, ezért síkhullám.

**Transzverzalitás.** Az E és a H merőleges a terjedés irányára, és egymásra is (pl. E az x, H az y tengely mentén rezeg, a hullám z irányba megy). Nem függetlenül, hanem együtt terjednek, és az elektromos és mágneses energiasűrűség egyenlő:

```latex
\mu H^2 = \varepsilon E^2 \qquad \frac{E}{H} = \sqrt{\frac{\mu_0}{\varepsilon_0}} \approx 377\,\Omega
```

A 377 Ω a vákuum hullámellenállása (impedanciája).

**Poynting-vektor.** Megadja, mennyi energia megy át 1 m²-en 1 s alatt (pillanatnyi érték), és az energiaáramlás irányába mutat. Az időátlaga (a hullám intenzitása) az amplitúdókkal:

```latex
\vec S = \vec E\times\vec H \qquad S_{átlag} = \frac12 E_0H_0
```

Vákuumban a sugárzás c sebességgel terjed, energiát és impulzust szállít; c minden frekvencián ugyanaz, ezért f és λ fordítottan arányos.

**Vizsgán:** síkhullám alakja; behelyettesítve 1/(λ²f²) = εμ; c = 1/√(εμ), vákuumban 3·10⁸ m/s; ω, k alak; transzverzalitás rajzzal; μH² = εE², 377 Ω; S = E × H, S\_átlag = ½E₀H₀.

### 20. Az energiatétel elektromágneses térben

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

**Miről szól?** Az elektromágneses tér energiájára vonatkozó mérleg, mint egy pénztárca: egy térrészben a tér energiája akkor csökken, ha energia áramlik ki a határán (ezt a Poynting-vektor méri), vagy ha a tér munkát végez a töltéseken (pl. Joule-hő keletkezik). Az áramforrások pedig növelik. Ez az energiamegmaradás az elektromágneses térre.

**Levezetés:**

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

Ideális szigetelőben (j = 0) ez egy kontinuitási egyenlet az energiára: ami beáramlik, az a tér energiáját növeli.

5. Térfogatra integrálva (Gauss-Osztrogradszkij), az **integrális alak**:

```latex
\frac{dW_{EM}}{dt} = -\oint_f\vec S\,d\vec A - \int_V\vec j\vec E\,dV
```

Az első tag a felületen kilépő energia, a második a tér által a töltéseken végzett munka.

**Az áramos tag szétbontása.** Az áram vezetési (jᵥ) és konvektív (ρv) részből áll. Az Ohm-törvény a mozgási és az idegen térrel: jᵥ = σ(E + v × B + Eᵢ), ebből E-t kifejezve és beírva:

```latex
\frac{dW_{EM}}{dt} = -\oint_f\vec S\,d\vec A + \int_V\left[\vec j_v\vec E_i - \frac{j_v^2}{\sigma} - \vec v\left(\vec j_v\times\vec B\right) - \rho\vec E\vec v\right]dV
```

A zárójel tagjai (teljesítménysűrűségek):

1. jᵥEᵢ: az áramforrások (elem, napelem) munkája, növeli a tér energiáját.
2. −jᵥ²/σ: a Joule-hő, mindig csökkenti.
3. −v(jᵥ × B): az Ampère-erő munkája a mozgó vezetőn; motornál csökkenti, generátornál növeli a tér energiáját.
4. −ρE·v: az elektromos tér munkája a mozgó töltéseken, előjele a szögtől függ.

**Vizsgán:** a két ME szorzása és összeadása; az azonosság; az időderiváltak átírása; div S + ∂w/∂t = −E·j és a tagok jelentése; integrális alak; a zárójeles tagok jelentése.
