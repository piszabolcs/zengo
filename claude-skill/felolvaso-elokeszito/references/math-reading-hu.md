# Magyar képletfelolvasás

Cél: a hallgató fejben fel tudja írni a képletet. Minden képlet teljes, kiolvasható magyar mondat.

## Alapelvek

1. A képletet mondatba ágyazd: „Az R ellenállás egyenlő ró szorozva l per A.”
2. A műveleti sorrendet a szórend és a szünet mutassa; ahol kétértelmű, mondd ki a zárójelet
   („szorozva zárójelben a plusz bé”), vagy bontsd részekre („a számláló …, a nevező …”).
3. Képlet után mindig `[[pause 500]]`.
4. Szimbólum első előfordulása a jelölésszótár szerinti teljes alakkal („az R ellenállás”),
   utána a betűnévvel („er”), kivéve ha az érthetőség a teljes alakot kívánja.
5. Számok és mértékegységek betűvel: „tizenkét volt”, „négy egész hét tized milliamper”.

## Műveletek és relációk

| Jel | Felolvasás |
|---|---|
| `=` | egyenlő |
| `≈` | közelítőleg egyenlő |
| `≠` | nem egyenlő |
| `<` | kisebb, mint |
| `>` | nagyobb, mint |
| `≤` | kisebb vagy egyenlő |
| `≥` | nagyobb vagy egyenlő |
| `+` | plusz |
| `-` | mínusz |
| `±` | plusz-mínusz |
| `·` / `×` | szorozva |
| `a/b` | a per b |
| összetett tört | „egy tört, a számláló …, a nevező …” |
| `x²` | x négyzet |
| `x³` | x köb |
| `xⁿ` | x az n-ediken |
| `x⁻¹` | x a mínusz egyediken |
| `√x` | négyzetgyök x |
| `∛x` | köbgyök x |
| `x_i` | x i (index: „x i”, „U nulla”, „I be”, „R ki”) |
| `Δx` | delta x |
| `dx/dt` | dé x per dé té |
| `d²x/dt²` | dé négyzet x per dé té négyzet |
| `∂f/∂x` | f parciális x szerint |
| `∫ f dx` | integrál f dé x |
| `∫_a^b` | integrál a-tól b-ig |
| `∮` | zárt görbe menti integrál |
| `∬_A … dA` | felületi integrál az A felületre |
| `Σ_{i=1}^{n}` | szumma i egyenlő egytől n-ig |
| `Π` (szorzat) | produktum |
| `lim_{x→0}` | limesz x tart nullához |
| `→` | tart (határértéknél), nyíl (egyébként) |
| `∞` | végtelen |
| vektor (félkövér vagy nyíl: **E**, `E⃗`) | E vektor |
| `|x|` | x abszolút értéke |
| `∇·E` | divergencia E |
| `∇×E` | rotáció E |
| `∇f` | gradiens f |
| `E·dA` | E skalárszorzat dé A |
| `a×b` (vektori) | a vektoriálisan szorozva bé |
| `f(x)` | f x (függvény: „f, x-nek a függvénye”, ha szükséges) |
| `sin x`, `cos x`, `tg x` | szinusz x, koszinusz x, tangens x |
| `ln x`, `log x` | természetes alapú logaritmus x, logaritmus x |
| `e^x` | e az x-ediken |
| `%` | százalék |
| `°` | fok |

## Görög betűk

| Betű | Név | Betű | Név |
|---|---|---|---|
| α | alfa | ν | nű |
| β | béta | ξ | kszí |
| γ | gamma | π | pí |
| δ, Δ | delta, nagy delta | ρ | ró |
| ε | epszilon | σ, Σ | szigma, nagy szigma |
| ζ | dzéta | τ | tau |
| η | éta | φ, Φ | fí, nagy fí |
| θ | théta | χ | khí |
| κ | kappa | ψ, Ψ | pszí, nagy pszí |
| λ | lambda | ω, Ω | omega, nagy omega |
| μ | mű | | |

## Latin betűk kiejtése (betűnévként)

a: á, b: bé, c: cé, d: dé, e: é, f: ef, g: gé, h: há, i: í, j: jé, k: ká, l: el, m: em, n: en,
o: ó, p: pé, q: kú, r: er, s: es, t: té, u: ú, v: vé, w: dupla vé, x: iksz, y: ipszilon, z: zé.
Kis- és nagybetű különbsége csak akkor hangozzék el („nagy U”, „kis u”), ha a képletben mindkettő szerepel.

## Mértékegységek

V volt, A amper, Ω óm, kΩ kiloóm, W watt, J joule (dzsúl), C coulomb (kulomb), F farad,
µF mikrofarad, H henri, T tesla, Wb weber (véber), Hz hertz, s másodperc, ms milliszekundum,
m méter, cm centiméter, mm milliméter, kg kilogramm, N newton (nyúton), Pa pascal, K kelvin,
°C celsius-fok. Összetett egység: „méter per szekundum”, „volt per méter”, „amper per négyzetméter”.

## Példák

| Képlet | Felolvasás |
|---|---|
| `R = ρ·l/A` | az R ellenállás egyenlő ró szorozva l per A |
| `U = R·I` | U egyenlő er szorozva í |
| `P = U²/R` | P egyenlő U négyzet per er |
| `Q = C·U` | Q egyenlő cé szorozva U |
| `f = 1/(2π√(LC))` | f egyenlő egy per, zárójelben kettő pí szorozva négyzetgyök el cé |
| `∮ E·dl = −dΦ/dt` | E skalárszorzat dé el zárt görbe menti integrálja egyenlő mínusz dé nagy fí per dé té |
| `Σ_{k=1}^{n} I_k = 0` | szumma k egyenlő egytől n-ig I ká egyenlő nulla |
| `lim_{x→0} sin x / x = 1` | limesz x tart nullához szinusz x per x egyenlő egy |
