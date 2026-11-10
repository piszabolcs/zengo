# Kidolgozott példák

Minden példa: a forrás részlete, majd a belőle készült forgatókönyv. A forgatókönyvek átmennek a
Felolvasó validátorán, hiba és figyelmeztetés nélkül.

## 1. Villamosságtani tétel jelölésszótárral

Forrás:

> **3. tétel. A fajlagos ellenállás**
> Jelölések: R – ellenállás [Ω], ρ – fajlagos ellenállás [Ω·m], l – a vezető hossza [m],
> A – a vezető keresztmetszete [m²].
> Egy homogén vezető ellenállása: R = ρ·l/A. (3.1)
> Például egy 2 m hosszú, 0,5 mm² keresztmetszetű rézvezetőre (ρ = 1,7·10⁻⁸ Ω·m) R ≈ 0,068 Ω.

Forgatókönyv:

```text
---
format: ttsmd/1
title: Villamosságtan jegyzet, harmadik tétel
author: Ismeretlen
language: hu
source: villamossagtan.pdf
symbols:
  R: er, ellenállás
  rho: ró, fajlagos ellenállás
  l: el, a vezető hossza
  A: á, a vezető keresztmetszete
---

<!-- eredeti
**3. tétel. A fajlagos ellenállás**
-->
# Harmadik tétel. A fajlagos ellenállás

<!-- eredeti
Jelölések: R – ellenállás [Ω], ρ – fajlagos ellenállás [Ω·m], l – a vezető hossza [m],
A – a vezető keresztmetszete [m²].
-->
Jelölések: er az ellenállás, mértékegysége óm. Ró a fajlagos ellenállás, mértékegysége óm szorozva méter. El a vezető hossza méterben, á pedig a vezető keresztmetszete négyzetméterben.

<!-- eredeti
Egy homogén vezető ellenállása: $R = ho \cdot l / A$. (3.1)
-->
Egy homogén vezető ellenállása: az R ellenállás egyenlő ró szorozva l per A. [[pause 500]]
Ez a harmadik tétel első képlete.

<!-- eredeti
Például egy 2 m hosszú, 0,5 mm² keresztmetszetű rézvezetőre (ρ = 1,7·10⁻⁸ Ω·m) R ≈ 0,068 Ω.
-->
Például egy kétméteres, fél négyzetmilliméter keresztmetszetű rézvezetőre, ahol ró egyenlő egy egész hét tized szorozva tíz a mínusz nyolcadikon óm méter, er közelítőleg egyenlő nulla egész hatvannyolc ezred óm. [[pause 500]]
```

## 2. Differenciálegyenlet összetett törttel

Forrás:

> Az RC-kör kondenzátorfeszültsége: u_C(t) = U₀·(1 − e^(−t/RC)).
> Az időállandó τ = RC.

Forgatókönyv:

```text
---
format: ttsmd/1
title: Átmeneti jelenségek
language: hu
---

# Az RC-kör bekapcsolása

Az er cé kör kondenzátorfeszültsége: u cé té-ben egyenlő U nulla szorozva, zárójelben egy mínusz e a mínusz té per er cé-ediken. [[pause 500]]

Az időállandó: tau egyenlő er szorozva cé. [[pause 500]]
```

## 3. Integrál és határérték

Forrás:

> Gauss-törvény: ∮_A E·dA = Q/ε₀.
> A derivált definíciója: f′(x) = lim_{h→0} (f(x+h) − f(x))/h.

Forgatókönyv:

```text
---
format: ttsmd/1
title: Fizika kettő
language: hu
---

# A Gauss-törvény

{{Gauss|gausz}}-törvény: E skalárszorzat dé A zárt felületi integrálja az A felületre egyenlő Q per epszilon nulla. [[pause 500]]

## A derivált

A derivált definíciója: f vessző x egyenlő limesz há tart nullához egy tört, a számláló f, zárójelben x plusz há, mínusz f x, a nevező há. [[pause 500]]
```

## 4. Szumma és vektorok

Forrás:

> Kirchhoff I. törvénye: Σ_{k=1}^{n} I_k = 0.
> Az erő: **F** = q(**E** + **v** × **B**).

Forgatókönyv:

```text
---
format: ttsmd/1
title: Elektrodinamika
language: hu
---

# Kirchhoff törvényei

{{Kirchhoff|kirhhoff}} első törvénye: szumma ká egyenlő egytől en-ig I ká egyenlő nulla. [[pause 500]]
Vagyis a csomópontba befolyó és onnan kifolyó áramok előjeles összege nulla.

## A Lorentz-erő

Az F erővektor egyenlő q szorozva, zárójelben E vektor plusz vé vektor vektoriálisan szorozva bé vektor. [[pause 500]]
```

## 5. Könyvfejezet lábjegyzettel és ábrával

Forrás:

> **II. fejezet – Az első tavasz**
> 1848. március 15-én a város csendes volt.¹ Az ablakból a ködös utcát figyelte.
> *2. ábra: A belváros térképe 1850 körül*
> ¹ A korabeli napló szerint.

Forgatókönyv:

```text
---
format: ttsmd/1
title: A régi város
author: Ismeretlen
language: hu
---

# Második fejezet. Az első tavasz

Ezernyolcszáznegyvennyolc március tizenötödikén a város csendes volt. Az ablakból a ködös utcát figyelte.

Ábra: a belváros térképe ezernyolcszázötven körül.
```
