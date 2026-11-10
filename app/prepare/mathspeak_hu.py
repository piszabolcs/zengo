"""Szabályalapú magyar képletfelolvasó: LaTeX és Unicode képlet -> AST -> kimondható mondat.

A szabályok forrása `claude-skill/felolvaso-elokeszito/references/math-reading-hu.md`. Amit a parser
nem ért (ismeretlen parancs, karakter, szerkezet), arra `MathSpeakError`-t dob: a hívó ilyenkor
`MATH_SUSPECT` jelölést tesz, nem talál ki felolvasást.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

from app.normalize.hu import LETTER_NAMES, cardinal, decimal_words, ordinal
from app.normalize.suffix_hu import BACK, ROUND, apply_suffix, word_harmony


class MathSpeakError(Exception):
    """A képlet nem olvasható fel biztonságosan szabályokkal."""


# --- jelkészletek ---

GREEK = {
    "α": "alfa", "β": "béta", "γ": "gamma", "δ": "delta", "ε": "epszilon", "ϵ": "epszilon", "ζ": "dzéta",
    "η": "éta", "θ": "théta", "ϑ": "théta", "ι": "ióta", "κ": "kappa", "λ": "lambda", "μ": "mű", "µ": "mű",
    "ν": "nű", "ξ": "kszí", "ο": "omikron", "π": "pí", "ρ": "ró", "ϱ": "ró", "σ": "szigma", "ς": "szigma",
    "τ": "tau", "υ": "üpszilon", "φ": "fí", "ϕ": "fí", "χ": "khí", "ψ": "pszí", "ω": "omega",
    "Γ": "nagy gamma", "Δ": "delta", "Θ": "nagy théta", "Λ": "nagy lambda", "Ξ": "nagy kszí", "Π": "nagy pí",
    "Σ": "nagy szigma", "Υ": "nagy üpszilon", "Φ": "nagy fí", "Ψ": "nagy pszí", "Ω": "nagy omega",
    "ℓ": "el", "ħ": "há vonás",
}
GREEK_CMDS = {
    "alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ", "epsilon": "ε", "varepsilon": "ε", "zeta": "ζ",
    "eta": "η", "theta": "θ", "vartheta": "ϑ", "iota": "ι", "kappa": "κ", "lambda": "λ", "mu": "μ", "nu": "ν",
    "xi": "ξ", "pi": "π", "rho": "ρ", "varrho": "ρ", "sigma": "σ", "varsigma": "σ", "tau": "τ",
    "upsilon": "υ", "phi": "φ", "varphi": "φ", "chi": "χ", "psi": "ψ", "omega": "ω", "Gamma": "Γ",
    "Delta": "Δ", "Theta": "Θ", "Lambda": "Λ", "Xi": "Ξ", "Pi": "Π", "Sigma": "Σ", "Upsilon": "Υ",
    "Phi": "Φ", "Psi": "Ψ", "Omega": "Ω", "ell": "ℓ", "hbar": "ħ",
}
FUNCS = {
    "sin": "szinusz", "cos": "koszinusz", "tg": "tangens", "tan": "tangens", "ctg": "kotangens",
    "cot": "kotangens", "ln": "természetes alapú logaritmus", "log": "logaritmus",
    "lg": "tízes alapú logaritmus", "exp": "exponenciális", "div": "divergencia", "rot": "rotáció",
    "curl": "rotáció", "grad": "gradiens", "sinh": "szinusz hiperbolikusz", "sh": "szinusz hiperbolikusz",
    "cosh": "koszinusz hiperbolikusz", "ch": "koszinusz hiperbolikusz", "arcsin": "arkusz szinusz",
    "arccos": "arkusz koszinusz", "arctg": "arkusz tangens", "arctan": "arkusz tangens", "max": "maximum",
    "min": "minimum", "det": "determináns", "sgn": "szignum", "Re": "valós rész", "Im": "képzetes rész",
}
# Unicode betűsorban csak ezeket vesszük függvénynévnek ("Im" lehet I·m is)
UNICODE_FUNCS = set(FUNCS) - {"Re", "Im", "sh", "ch", "min", "max", "det", "lg"}
SUB_WORDS = {"max": "maximum", "min": "minimum", "eff": "effektív", "átl": "átlag"}
REL_WORDS = {
    "=": "egyenlő", "≈": "közelítőleg egyenlő", "≠": "nem egyenlő", "<": "kisebb, mint", ">": "nagyobb, mint",
    "≤": "kisebb vagy egyenlő", "≥": "nagyobb vagy egyenlő", "≡": "azonosan egyenlő", "∝": "arányos",
    "∼": "arányos", "→": "nyíl", "⇒": "ebből következik", "⇔": "akkor és csak akkor",
    "∥": "párhuzamos", "⊥": "merőleges", "↔": "megfelel",
}
ADD_WORDS = {"+": "plusz", "-": "mínusz", "±": "plusz-mínusz", "∓": "mínusz-plusz"}
LATEX_SYMBOLS = {
    "cdot": "·", "times": "×", "pm": "±", "mp": "∓", "infty": "∞", "to": "→", "rightarrow": "→",
    "Rightarrow": "⇒", "implies": "⇒", "Leftrightarrow": "⇔", "iff": "⇔", "Longleftrightarrow": "⇔",
    "longrightarrow": "→", "Longrightarrow": "⇒", "leftrightarrow": "⇔", "leq": "≤", "le": "≤", "geq": "≥",
    "ge": "≥", "neq": "≠", "ne": "≠", "approx": "≈", "equiv": "≡", "sim": "∼", "propto": "∝",
    "partial": "∂", "nabla": "∇", "int": "∫", "iint": "∬", "iiint": "∭", "oint": "∮", "oiint": "∯",
    "sum": "∑", "prod": "∏", "ldots": "…", "cdots": "…", "dots": "…", "circ": "°", "degree": "°", "%": "%",
    "vert": "|", "lvert": "|", "rvert": "|", "|": "‖", "Vert": "‖", "{": "(", "}": ")", "lbrace": "(",
    "rbrace": ")", "lbrack": "[", "rbrack": "]", "sqrt": "√",
}
IGNORED_CMDS = {"displaystyle", "textstyle", "limits", "nolimits", "left", "right", "big", "Big", "bigg",
                "Bigg", "bigl", "bigr", "Bigl", "Bigr", "biggl", "biggr", ",", ";", ":", "!", " "}
SEP_CMDS = {"qquad", "quad", "\\"}
ACCENT_CMDS = {"vec": "vec", "overrightarrow": "vec", "mathbf": "vec", "boldsymbol": "vec", "bm": "vec",
               "hat": "kalap", "widehat": "kalap", "bar": "átlag", "overline": "felülvonás", "dot": "pont",
               "ddot": "két pont", "tilde": "hullám", "widetilde": "hullám"}
FRAC_CMDS = {"frac", "dfrac", "tfrac", "cfrac"}
TEXT_CMDS = {"text", "textrm", "mbox", "mathrm", "operatorname", "mathit", "textit", "mathcal", "mathsf"}

SUPERSCRIPTS = dict(zip("⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿⁱ", "0123456789+-=()ni"))
SUBSCRIPTS = dict(zip("₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑₒₓₕₖₗₘₙₚₛₜᵢᵣᵤᵥⱼ", "0123456789+-=()aeoxhklmnpstiruvj"))
VEC_MARK = "⃗"
VULGAR = {"½": ("1", "2"), "⅓": ("1", "3"), "⅔": ("2", "3"), "¼": ("1", "4"), "¾": ("3", "4")}
HU_ACCENTED = set("áéíóöőúüűÁÉÍÓÖŐÚÜŰ")
PRIMES = {"′": 1, "″": 2, "'": 1}
MINUS_CHARS = "-−–"
REL_CHARS = "=≈≠<>≤≥≡∝∼~→⇒⇔∥⊥↔"
MUL_CHARS = "·⋅×∙"
BIG_OPS = {"∫": "int", "∬": "iint", "∭": "iiint", "∮": "oint", "∯": "oiint", "∑": "sum", "∏": "prod"}

LINE_DIFFS = {"s", "l", "ℓ", "r"}
SURFACE_DIFFS = {"A", "F", "f", "S"}
VOLUME_DIFFS = {"V", "τ"}

FRACTION_NAMES = {2: "ketted", 3: "harmad", 4: "negyed", 5: "ötöd", 6: "hatod", 7: "heted", 8: "nyolcad",
                  9: "kilenced", 10: "tized"}
LETTER_NAME_SET = set(LETTER_NAMES.values())


@dataclass
class Ctx:
    """Felolvasási környezet: azok a latin betűk, amelyek kis- és nagybetűvel is szerepelnek."""
    both_cases: set[str] = field(default_factory=set)


# --- lexer ---

@dataclass
class Tok:
    kind: str  # num, letter, word, text, op, rel, lp, rp, lb, rb, sub, sup, prime, vec, accent, frac,
    #            sqrt, big, lim, diff, partial, nabla, inf, sep, ellipsis, abs, norm, postfix
    value: str = ""


def _math_alnum(ch: str) -> str:
    """Matematikai betűváltozat (𝐸, 𝑥) -> alap betű."""
    if 0x1D400 <= ord(ch) <= 0x1D7FF:
        return unicodedata.normalize("NFKC", ch)
    return ch


class Lexer:
    def __init__(self, src: str):
        self.s = "".join(_math_alnum(c) for c in unicodedata.normalize("NFC", src))
        self.i = 0
        self.toks: list[Tok] = []

    def run(self) -> list[Tok]:
        s = self.s
        while self.i < len(s):
            ch = s[self.i]
            if ch.isspace() or ch == "&":
                self.i += 1
            elif ch == "\\":
                self._command()
            elif ch in "0123456789":
                self._number()
            elif ch in VULGAR:
                a, b = VULGAR[ch]
                self.toks += [Tok("frac"), Tok("num", a), Tok("num", b)]
                self.i += 1
            elif ch in SUPERSCRIPTS or ch in SUBSCRIPTS:
                self._script(ch in SUPERSCRIPTS)
            elif ch.isalpha() and ch not in GREEK and (ch.isascii() or ch in HU_ACCENTED):
                self._letters()
            elif ch in GREEK:
                self.toks.append(Tok("letter", ch))
                self.i += 1
            else:
                self._symbol(ch)
        return self.toks

    def _number(self) -> None:
        m = re.match(r"\d+(?:(?:,|\.|\{,\})\d+)?", self.s[self.i:])
        assert m
        self.toks.append(Tok("num", m.group(0).replace("{,}", ",").replace(".", ",")))
        self.i += m.end()

    def _script(self, sup: bool) -> None:
        table = SUPERSCRIPTS if sup else SUBSCRIPTS
        j = self.i
        while j < len(self.s) and self.s[j] in table:
            j += 1
        inner = "".join(table[c] for c in self.s[self.i:j])
        self.toks.append(Tok("sup" if sup else "sub"))
        self.toks.append(Tok("lb"))
        self.toks.extend(Lexer(inner).run())
        self.toks.append(Tok("rb"))
        self.i = j

    def _letters(self) -> None:
        m = re.match(r"[A-Za-záéíóöőúüűÁÉÍÓÖŐÚÜŰ]+", self.s[self.i:])
        assert m
        run = m.group(0)
        self.i += len(run)
        if run in UNICODE_FUNCS or run == "lim":
            self.toks.append(Tok("lim" if run == "lim" else "word", run))
            return
        if not run.isascii():
            self.toks.append(Tok("text", run))  # ékezetes szó (index: "eredő")
            return
        k = 0
        while k < len(run):
            ch = run[k]
            nxt = run[k + 1] if k + 1 < len(run) else (self.s[self.i] if self.i < len(self.s) else "")
            # differenciál: "dA", "dΦ", "d\vec A", és a "d/dt" számlálója
            if ch == "d" and (nxt.isalpha() or nxt == "\\" or nxt in GREEK or (nxt == "/" and k + 1 == len(run))):
                self.toks.append(Tok("diff"))
            else:
                self.toks.append(Tok("letter", ch))
            k += 1

    def _group_text(self) -> str:
        s = self.s
        while self.i < len(s) and s[self.i].isspace():
            self.i += 1
        if self.i >= len(s) or s[self.i] != "{":
            if self.i < len(s):
                self.i += 1
                return s[self.i - 1]
            raise MathSpeakError("Hiányzó argumentum")
        depth, j = 0, self.i
        while j < len(s):
            if s[j] == "{":
                depth += 1
            elif s[j] == "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        if depth:
            raise MathSpeakError("Lezáratlan kapcsos zárójel")
        text = s[self.i + 1:j]
        self.i = j + 1
        return text

    def _command(self) -> None:
        s = self.s
        m = re.match(r"\\([A-Za-z]+|.)", s[self.i:])
        if not m:
            raise MathSpeakError("Magányos backslash")
        name = m.group(1)
        self.i += m.end()
        if name in ("left", "right") and self.i < len(s) and s[self.i] == ".":
            self.i += 1
            return
        if name in SEP_CMDS:
            self.toks.append(Tok("sep"))
        elif name in IGNORED_CMDS:
            return
        elif name in GREEK_CMDS:
            self.toks.append(Tok("letter", GREEK_CMDS[name]))
        elif name in FUNCS:
            self.toks.append(Tok("word", name))
        elif name == "lim":
            self.toks.append(Tok("lim", name))
        elif name in FRAC_CMDS:
            self.toks.append(Tok("frac"))
            # \frac12: két egyjegyű argumentum
            m2 = re.match(r"\s*(\d)(\d)?", s[self.i:])
            if m2:
                self.toks.append(Tok("num", m2.group(1)))
                if m2.group(2):
                    self.toks.append(Tok("num", m2.group(2)))
                self.i += m2.end()
        elif name in ("xrightarrow", "xRightarrow"):
            note = self._group_text()
            self.toks.append(Tok("rel", "⇒"))
            self.toks.append(Tok("note", note))
        elif name == "underbrace":
            self.toks.append(Tok("underbrace"))
        elif name in ACCENT_CMDS:
            self.toks.append(Tok("accent", ACCENT_CMDS[name]))
        elif name == "prime":
            self.toks.append(Tok("prime", "1"))
        elif name in TEXT_CMDS:
            text = self._group_text().strip()
            if name == "mathrm" and text == "d":
                self.toks.append(Tok("diff"))
            elif name in ("mathrm", "operatorname", "mathit", "mathcal", "mathsf") and text in FUNCS:
                self.toks.append(Tok("word", text))
            elif name in ("mathrm", "mathit", "mathcal", "mathsf") and re.fullmatch(r"[A-Za-z]", text):
                self.toks.append(Tok("letter", text))
            elif re.fullmatch(r"[^\W\d_]*(?:[ .,:-]+[^\W\d_]*)*", text):
                if text:
                    self.toks.append(Tok("text", text))
            else:
                raise MathSpeakError(f"Nem kezelt szöveg: {text}")
        elif name in LATEX_SYMBOLS:
            self._symbol(LATEX_SYMBOLS[name], advance=False)
        else:
            raise MathSpeakError(f"Ismeretlen parancs: \\{name}")

    def _symbol(self, ch: str, advance: bool = True) -> None:
        if advance:
            self.i += 1
        t = self.toks
        if ch in "([":
            t.append(Tok("lp", ch))
        elif ch in ")]":
            t.append(Tok("rp", ch))
        elif ch == "{":
            t.append(Tok("lb"))
        elif ch == "}":
            t.append(Tok("rb"))
        elif ch in "+±∓" or ch in MINUS_CHARS:
            t.append(Tok("op", "-" if ch in MINUS_CHARS else ch))
        elif ch == "*":
            t.append(Tok("star"))
        elif ch in MUL_CHARS:
            t.append(Tok("op", "×" if ch == "×" else "·"))
        elif ch == "/":
            t.append(Tok("op", "/"))
        elif ch in REL_CHARS:
            t.append(Tok("rel", "∼" if ch == "~" else ch))
        elif ch == "^":
            t.append(Tok("sup"))
        elif ch == "_":
            t.append(Tok("sub"))
            # zárójel nélküli szóindex (Unicode jegyzetben: H_in, χ_meas)
            m = re.match(r"[A-Za-záéíóöőúüű]{2,}", self.s[self.i:]) if advance else None
            if m and re.search("[aáeéiíoóöőuúüű]", m.group(0)):
                t.append(Tok("text", m.group(0)))
                self.i += m.end()
        elif ch in PRIMES:
            t.append(Tok("prime", str(PRIMES[ch])))
        elif ch == VEC_MARK:
            t.append(Tok("vec"))
        elif ch in BIG_OPS:
            t.append(Tok("big", BIG_OPS[ch]))
        elif ch == "√":
            t.append(Tok("sqrt", "2"))
        elif ch == "∛":
            t.append(Tok("sqrt", "3"))
        elif ch == "∂":
            t.append(Tok("partial"))
        elif ch == "∇":
            t.append(Tok("nabla"))
        elif ch == "∞":
            t.append(Tok("inf"))
        elif ch == "…":
            t.append(Tok("ellipsis"))
        elif ch == "|":
            t.append(Tok("abs"))
        elif ch == "‖":
            t.append(Tok("norm"))
        elif ch in "°%!":
            t.append(Tok("postfix", ch))
        elif ch in ",;":
            t.append(Tok("sep", ch))
        elif ch == ".":
            return  # mondatzáró pont a képlet végén
        else:
            raise MathSpeakError(f"Ismeretlen jel: {ch!r}")


def tokenize(src: str) -> list[Tok]:
    toks = Lexer(src).run()
    # a Σ betű a képletekben szinte mindig összegjel
    toks = [Tok("big", "sum") if t.kind == "letter" and t.value == "Σ" else t for t in toks]
    # reláció körüli térköz (\quad\Longleftrightarrow\quad) nem választ el képleteket
    out: list[Tok] = []
    for i, t in enumerate(toks):
        if t.kind == "sep" and t.value == "" and (
                (out and out[-1].kind == "rel") or (i + 1 < len(toks) and toks[i + 1].kind == "rel")):
            continue
        out.append(t)
    return out


# --- AST ---

@dataclass
class Num:
    text: str


@dataclass
class Sym:
    base: str
    vec: bool = False
    mods: list[str] = field(default_factory=list)
    primes: int = 0
    sub: object | None = None


@dataclass
class Text:
    text: str


@dataclass
class Diff:
    arg: object | None
    partial: bool = False
    order: object | None = None


@dataclass
class Pow:
    base: object
    exp: object


@dataclass
class Frac:
    num: object
    den: object


@dataclass
class Sqrt:
    arg: object
    index: str = "2"


@dataclass
class Paren:
    inner: object
    kind: str = "("


@dataclass
class Neg:
    op: str
    inner: object


@dataclass
class Sum:
    items: list  # [(op, node)]; az első op lehet "" vagy előjel


@dataclass
class Prod:
    items: list  # [(op, node)]; op: "" (egymás mellé írt), "·", "×"


@dataclass
class Func:
    name: str
    arg: object | None
    sup: object | None = None
    sub: object | None = None


@dataclass
class BigOp:
    kind: str
    lower: object | None
    upper: object | None
    body: object | None


@dataclass
class Lim:
    sub: object | None
    body: object


@dataclass
class Rel:
    first: object | None
    rest: list  # [(op, node)]


@dataclass
class Atom:
    """Szóként kimondott jel: végtelen, és így tovább, nabla."""
    words: str


@dataclass
class Eval:
    """Helyettesítési érték: [F]_a^b."""
    inner: object
    lower: object
    upper: object


@dataclass
class Under:
    """Aláhúzott rész megjegyzéssel (underbrace)."""
    inner: object
    note: object | None


@dataclass
class SubList:
    """Vesszővel tagolt index: R_{m,i}."""
    items: list


@dataclass
class Apply:
    """Függvényérték egy pontban: U(r)."""
    fn: object
    arg: object


@dataclass
class Delta:
    """Δ előtag: delta x."""
    inner: object


@dataclass
class Postfix:
    inner: object
    op: str


# --- parser ---

FACTOR_START = {"num", "letter", "word", "text", "lp", "lb", "frac", "sqrt", "accent", "big", "lim", "diff",
                "partial", "nabla", "inf", "ellipsis", "abs", "norm"}


class Parser:
    def __init__(self, toks: list[Tok]):
        self.t = toks
        self.i = 0
        self.abs_depth = 0

    def peek(self, k: int = 0) -> Tok | None:
        j = self.i + k
        return self.t[j] if j < len(self.t) else None

    def take(self, kind: str | None = None) -> Tok:
        tok = self.peek()
        if tok is None or (kind and tok.kind != kind):
            raise MathSpeakError(f"Váratlan vég vagy jel: {tok.kind if tok else 'vége'} (várt: {kind})")
        self.i += 1
        return tok

    def at(self, kind: str, value: str | None = None) -> bool:
        tok = self.peek()
        return tok is not None and tok.kind == kind and (value is None or tok.value == value)

    # formula_list := relation (sep relation)*
    def formulas(self) -> list:
        out = []
        while self.peek() is not None:
            if self.at("sep"):
                self.i += 1
                continue
            out.append(self.relation())
            if self.peek() is not None and not self.at("sep"):
                raise MathSpeakError(f"Fel nem dolgozott jel: {self.peek().kind}")
        if not out:
            raise MathSpeakError("Üres képlet")
        return out

    def relation(self):
        first = None
        if not self.at("rel"):
            first = self.expr()
        rest = []
        while self.at("rel"):
            op = self.take().value
            if self.at("note"):
                note = Parser(tokenize(self.take().value)).relation()
                rest.append((("⇒", note), self.expr()))
                continue
            rest.append((op, self.expr()))
        if first is not None and not rest:
            return first
        return Rel(first, rest)

    def expr(self):
        items = []
        if self.at("op") and self.peek().value in ADD_WORDS:
            items.append((self.take().value, self.term()))
        else:
            items.append(("", self.term()))
        while self.at("op") and self.peek().value in ADD_WORDS:
            op = self.take().value
            items.append((op, self.term()))
        if len(items) == 1:
            op, node = items[0]
            return Neg(op, node) if op else node
        return Sum(items)

    def _starts_factor(self) -> bool:
        tok = self.peek()
        if tok is None:
            return False
        if tok.kind == "abs":
            return self.abs_depth == 0
        return tok.kind in FACTOR_START

    def term(self):
        items = [("", self.factor())]
        while True:
            tok = self.peek()
            if tok is None:
                break
            if (tok.kind == "op" and tok.value in ("·", "×")) or tok.kind == "star":
                self.i += 1
                tok = Tok("op", "·") if tok.kind == "star" else tok
                if self.at("op", "-"):  # a·(−b) írásmód zárójel nélkül
                    self.i += 1
                    items.append((tok.value, Neg("-", self.factor())))
                else:
                    items.append((tok.value, self.factor()))
            elif tok.kind == "op" and tok.value == "/":
                self.i += 1
                den = self.factor()
                if isinstance(den, Num):
                    # Q²/2C, Q/4πr²: a számmal kezdődő nevező a mögé írt tényezőket is magába foglalja
                    tail = [("", den)]
                    while self.peek() is not None and self.peek().kind in ("letter", "num", "sqrt"):
                        tail.append(("", self.factor()))
                    den = den if len(tail) == 1 else Prod(tail)
                if isinstance(items[-1][1], Diff) and isinstance(den, Diff):
                    # p·∂E/∂x: a derivált csak a differenciálból áll
                    items[-1] = (items[-1][0], Frac(items[-1][1], den))
                else:
                    num = items[0][1] if len(items) == 1 else Prod(items)
                    items = [("", Frac(num, den))]
            elif self._starts_factor():
                items.append(("", self.factor()))
            else:
                break
        return items[0][1] if len(items) == 1 else Prod(items)

    def factor(self):
        if self.at("op", "-") or self.at("op", "+"):
            op = self.take().value
            return Neg(op, self.factor())
        return self.postfix(self.primary())

    def script_arg(self):
        if self.at("postfix", "°"):
            self.take()
            return Postfix(Text(""), "°")
        if self.at("star"):
            self.take()
            return Text("csillag")
        if (self.at("lb") and self.peek(1) is not None and self.peek(1).kind == "op"
                and self.peek(1).value in ADD_WORDS and self.peek(2) is not None and self.peek(2).kind == "rb"):
            self.i += 3  # előjel-index: F₊, F₋
            return Text(ADD_WORDS[self.t[self.i - 2].value])
        if self.at("lb"):
            self.take()
            items = [("", self.relation() if not self.at("rb") else Text(""))]
            while self.at("sep", ","):  # többrészes index: R_{m,i}
                self.take()
                items.append(("", self.relation()))
            self.take("rb")
            return items[0][1] if len(items) == 1 else SubList([n for _, n in items])
        if self.at("op", "-"):
            self.take()
            return Neg("-", self.primary())
        return self.primary()

    def postfix(self, node):
        while True:
            if self.at("sub"):
                self.take()
                sub = self.script_arg()
                if isinstance(node, Paren) and node.kind == "[" and self.at("sup"):
                    self.take()
                    node = Eval(node.inner, sub, self.script_arg())
                elif isinstance(node, Sym) and node.sub is None:
                    node.sub = sub
                elif isinstance(node, Pow) and isinstance(node.base, Sym) and node.base.sub is None:
                    node.base.sub = sub
                else:
                    raise MathSpeakError("Index nem jelhez kapcsolódik")
            elif self.at("sup"):
                self.take()
                if self.at("prime"):
                    primes = int(self.take().value)
                    if not isinstance(node, Sym):
                        raise MathSpeakError("Vessző nem jelhez kapcsolódik")
                    node.primes += primes
                    continue
                if self.at("lb") and self.peek(1) and self.peek(1).kind == "prime":
                    self.take()
                    primes = 0
                    while self.at("prime"):
                        primes += int(self.take().value)
                    self.take("rb")
                    if not isinstance(node, Sym):
                        raise MathSpeakError("Vessző nem jelhez kapcsolódik")
                    node.primes += primes
                    continue
                if self.at("star") and isinstance(node, Sym):
                    self.take()
                    node.mods.append("csillag")
                    continue
                node = Pow(node, self.script_arg())
            elif self.at("prime"):
                primes = int(self.take().value)
                if not isinstance(node, Sym):
                    raise MathSpeakError("Vessző nem jelhez kapcsolódik")
                node.primes += primes
            elif self.at("star") and isinstance(node, Sym) and not (
                    self.peek(1) is not None and self.peek(1).kind in FACTOR_START):
                self.take()
                node.mods.append("csillag")
            elif self.at("vec"):
                self.take()
                if not isinstance(node, Sym):
                    raise MathSpeakError("Vektorjel nem jelhez kapcsolódik")
                node.vec = True
            elif self.at("postfix"):
                node = Postfix(node, self.take().value)
            elif (isinstance(node, Sym) and not node.vec and self.at("lp", "(") and self.peek(2) is not None
                  and self.peek(1).kind in ("letter", "num", "inf") and self.peek(2).kind == "rp"):
                # függvényérték: U(r) -> ú er-ben
                self.take()
                arg = self.primary()
                self.take("rp")
                node = Apply(node, arg)
            else:
                return node

    def group(self):
        """Kötelező `{...}` csoport vagy egyetlen elem (LaTeX argumentum)."""
        if self.at("lb"):
            self.take()
            node = self.relation()
            self.take("rb")
            return node
        return self.postfix(self.primary())

    def limits(self) -> tuple[object | None, object | None]:
        lower = upper = None
        for _ in range(2):
            if self.at("sub") and lower is None:
                self.take()
                lower = self.script_arg()
            elif self.at("sup") and upper is None:
                self.take()
                upper = self.script_arg()
        return lower, upper

    def primary(self):
        tok = self.peek()
        if tok is None:
            raise MathSpeakError("Hiányzó operandus")
        k = tok.kind
        if k == "num":
            self.i += 1
            return Num(tok.value)
        if k == "letter":
            self.i += 1
            nxt = self.peek()
            if tok.value == "Δ" and nxt is not None and nxt.kind in ("letter", "accent"):
                return Delta(self.postfix(self.primary()))
            return Sym(tok.value)
        if k == "text":
            self.i += 1
            return Text(tok.value)
        if k == "lp":
            self.i += 1
            inner = self.relation()
            close = self.take("rp")
            return Paren(inner, "(" if close.value == ")" else "[")
        if k == "lb":
            self.i += 1
            inner = self.relation()
            self.take("rb")
            return inner
        if k in ("abs", "norm"):
            self.i += 1
            self.abs_depth += 1
            inner = self.expr()
            self.abs_depth -= 1
            self.take(k)
            return Paren(inner, "|")
        if k == "frac":
            self.i += 1
            return Frac(self.group(), self.group())
        if k == "sqrt":
            self.i += 1
            index = tok.value
            if self.at("lp", "["):
                self.take()
                idx = self.take("num").value
                self.take("rp")
                index = idx
            return Sqrt(self.group(), index)
        if k == "accent":
            self.i += 1
            node = self.group()
            if not isinstance(node, Sym):
                raise MathSpeakError("Ékezet nem egyetlen jelen")
            if tok.value == "vec":
                node.vec = True
            else:
                node.mods.append(tok.value)
            return node
        if k == "word":
            self.i += 1
            sub = sup = None
            for _ in range(2):
                if self.at("sup") and sup is None:
                    self.take()
                    sup = self.script_arg()
                elif self.at("sub") and sub is None:
                    self.take()
                    sub = self.script_arg()
            arg = self.factor() if self._starts_factor() else None
            if arg is not None and _is_atomic(arg) and not isinstance(arg, Paren):
                items = [("", arg)]
                while self.peek() is not None and self.peek().kind in ("letter", "num"):
                    items.append(("", self.postfix(self.primary())))
                if len(items) > 1:
                    arg = Prod(items)
            return Func(tok.value, arg, sup, sub)
        if k == "big":
            self.i += 1
            lower, upper = self.limits()
            if not self._starts_factor():
                raise MathSpeakError("Integrál vagy összeg operandus nélkül")
            return BigOp(tok.value, lower, upper, self.term())
        if k == "lim":
            self.i += 1
            sub = None
            if self.at("sub"):
                self.take()
                sub = self.script_arg()
            return Lim(sub, self.term())
        if k == "partial" and self.peek(1) is not None and self.peek(1).kind == "sub":
            self.i += 2  # \partial_x v -> v parciális x szerint
            var = self.script_arg()
            return Frac(Diff(self.factor(), partial=True), Diff(var, partial=True))
        if k in ("diff", "partial"):
            self.i += 1
            order = None
            if self.at("sup"):
                self.take()
                order = self.script_arg()
            arg = None
            if self.peek() is not None and self.peek().kind in ("letter", "accent", "lb"):
                arg = self.postfix(self.primary())
            return Diff(arg, partial=(k == "partial"), order=order)
        if k == "nabla":
            self.i += 1
            if self.at("op", "·"):
                self.i += 1
                return Func("div", self.factor())
            if self.at("op", "×"):
                self.i += 1
                return Func("rot", self.factor())
            if self.at("sup"):
                self.take()
                exp = self.script_arg()
                if not (isinstance(exp, Num) and exp.text == "2"):
                    raise MathSpeakError("Ismeretlen nabla-hatvány")
                return Func("laplace", self.factor() if self._starts_factor() else None)
            if self._starts_factor():
                return Func("grad", self.factor())
            return Atom("nabla")
        if k == "underbrace":
            self.i += 1
            inner = self.group()
            note = None
            if self.at("sub"):
                self.take()
                note = self.script_arg()
            return Under(inner, note)
        if k == "inf":
            self.i += 1
            return Atom("végtelen")
        if k == "ellipsis":
            self.i += 1
            return Atom("és így tovább")
        raise MathSpeakError(f"Váratlan jel: {k}")


def parse_formulas(src: str) -> list:
    toks = tokenize(src)
    return Parser(toks).formulas()


# --- toldalékok ---

def _art(word: str) -> str:
    return "az" if word[:1].lower() in "aáeéiíoóöőuúüű" else "a"


def _lengthen(word: str) -> str:
    if word.endswith("a"):
        return word[:-1] + "á"
    if word.endswith("e"):
        return word[:-1] + "é"
    return word


def suffixed(words: list[str], kind: str) -> list[str]:
    """Az utolsó szóra rag: kind = tól, ig, hoz, ra. Betűnévhez kötőjellel ("á-tól")."""
    if not words:
        raise MathSpeakError("Üres határ")
    words = " ".join(words).split(" ")
    *head, last = words
    if last == ",":
        raise MathSpeakError("Összetett határ")
    h = word_harmony(last)
    forms = {"tól": ("tól", "től", "től"), "hoz": ("hoz", "hez", "höz"), "ra": ("ra", "re", "re"),
             "ban": ("ban", "ben", "ben"),
             "ig": ("ig", "ig", "ig")}[kind]
    suf = forms[0] if h == BACK else (forms[2] if h == ROUND else forms[1])
    if last in LETTER_NAME_SET or re.fullmatch(r"[a-z]", last):
        return head + [f"{last}-{suf}"]
    if re.fullmatch(r"[a-záéíóöőúüű]+", last) and last not in GREEK.values():
        return head + [apply_suffix(last, suf)]
    return head + [_lengthen(last) + suf]


def exponent_word(n: int) -> str:
    """Hatványkitevő ragos sorszámneve: 9 -> kilencediken, 3 -> harmadikon, 1 -> egyediken."""
    base = {1: "egyedik", 2: "második"}.get(n) or ordinal(n)
    return base + ("on" if word_harmony(base) == BACK else "en")


# --- felolvasás ---

def _letter(ch: str, ctx: Ctx, with_case: bool = True) -> str:
    if ch in GREEK:
        return GREEK[ch]
    if ch.isascii() and ch.isalpha():
        name = LETTER_NAMES[ch.upper()]
        if with_case and ch.upper() in ctx.both_cases:
            return ("nagy " if ch.isupper() else "kis ") + name
        return name
    raise MathSpeakError(f"Ismeretlen betű: {ch}")


def _plain_letters(node) -> str | None:
    """Ha az index csupa egyszerű betű (pl. `ki`, `max`, `AB`), a betűk sora."""
    if isinstance(node, Sym) and not (node.vec or node.mods or node.primes or node.sub):
        return node.base
    if isinstance(node, Text):
        return node.text
    if isinstance(node, Prod) and all(op == "" for op, _ in node.items):
        parts = [_plain_letters(n) for _, n in node.items]
        if all(p and len(p) == 1 for p in parts):
            return "".join(parts)  # type: ignore[arg-type]
    return None


def _speak_sub(node, ctx: Ctx) -> list[str]:
    if isinstance(node, Num):
        if "," not in node.text and len(node.text) > 1:
            return [cardinal(int(d)) for d in node.text]
        return _num(node.text)
    letters = _plain_letters(node)
    if letters is not None:
        if isinstance(node, Text) or (len(letters) >= 2 and letters.islower()
                                      and re.search("[aáeéiíoóöőuúüű]", letters)):
            return [SUB_WORDS.get(letters, letters)]
        return [_letter(c, ctx, with_case=False) for c in letters if c != " "]
    if isinstance(node, Prod) and all(op == "" for op, _ in node.items):
        return [w for _, n in node.items for w in _speak_sub(n, ctx)]
    if isinstance(node, SubList):
        return [w for n in node.items for w in _speak_sub(n, ctx)]
    return speak_node(node, ctx)


def _num(text: str) -> list[str]:
    if "," in text:
        a, b = text.split(",", 1)
        return [decimal_words(a, b)]
    return [cardinal(int(text))]


def _is_atomic(node) -> bool:
    if isinstance(node, (Num, Sym, Text, Atom, Apply)):
        return True
    if isinstance(node, Delta):
        return _is_atomic(node.inner)
    if isinstance(node, Pow):
        return _is_atomic(node.base) and isinstance(node.exp, (Num, Sym))
    if isinstance(node, Func):
        return node.arg is None or _is_atomic(node.arg)
    if isinstance(node, Diff):
        return node.arg is None or isinstance(node.arg, Sym)
    if isinstance(node, Paren):
        return node.kind == "|" and _is_atomic(node.inner)
    if isinstance(node, Neg):
        return _is_atomic(node.inner)
    return False


def _is_simple_product(node) -> bool:
    if _is_atomic(node):
        return True
    if isinstance(node, Prod):
        return all(_is_atomic(n) or (isinstance(n, Sqrt) and _is_simple_product(_strip_paren(n.arg)))
                   for _, n in node.items)
    if isinstance(node, Sqrt):
        return _is_simple_product(_strip_paren(node.arg))
    return False


def _strip_paren(node):
    return node.inner if isinstance(node, Paren) and node.kind in "([" else node


def _is_vector(node) -> bool:
    if isinstance(node, Sym):
        return node.vec
    if isinstance(node, Diff):
        return isinstance(node.arg, Sym) and node.arg.vec
    if isinstance(node, Pow):
        return _is_vector(node.base)
    if isinstance(node, Func):
        return node.name in ("rot", "curl", "grad")
    if isinstance(node, (Paren, Neg)):
        return _is_vector(node.inner)
    if isinstance(node, Sum):
        return any(_is_vector(n) for _, n in node.items)
    if isinstance(node, Prod):
        return sum(1 for _, n in node.items if _is_vector(n)) == 1 and all(op == "" for op, _ in node.items)
    return False


def _deriv(frac: Frac, ctx: Ctx) -> tuple[list[str], bool] | None:
    """Derivált felismerése. (szavak, operátor-e: utána jön az operandus)."""
    num, den = frac.num, frac.den
    if isinstance(num, Sym) and num.base == "d" and not (num.sub or num.vec or num.mods or num.primes):
        num = Diff(None)
    if (isinstance(num, Prod) and len(num.items) == 2 and isinstance(num.items[0][1], Sym)
            and num.items[0][1].base == "d" and isinstance(num.items[1][1], Paren)):
        num = Diff(num.items[1][1])
    # d²x/dt²: a "d²" a lexerben d betű négyzete, a nevező "dt²" pedig dt négyzete
    if (isinstance(num, Prod) and len(num.items) == 2 and isinstance(num.items[0][1], Pow)
            and isinstance(num.items[0][1].base, Sym) and num.items[0][1].base.base == "d"
            and isinstance(den, Diff) and isinstance(den.arg, Pow)):
        num = Diff(num.items[1][1], order=num.items[0][1].exp)
        den = Diff(den.arg.base, order=den.arg.exp)
    if not isinstance(den, Diff) or den.arg is None:
        return None
    var = speak_node(den.arg, ctx)
    order = None
    if den.order is not None:
        order = den.order
    if (isinstance(num, Diff) and num.partial and den.partial and isinstance(num.order, Num)
            and num.order.text == "2" and isinstance(den.arg, Pow) and isinstance(den.arg.exp, Num)
            and den.arg.exp.text == "2"):
        prefix = [] if num.arg is None else speak_node(num.arg, ctx)
        tail = ["deriváltja"] if num.arg is not None else []
        return prefix + ["második", "parciális"] + tail + speak_node(den.arg.base, ctx) + ["szerint"], \
            num.arg is None
    if isinstance(num, Diff) and num.partial == den.partial:
        if den.partial:
            prefix = [] if num.arg is None else speak_node(num.arg, ctx)
            if order is not None:
                if not (isinstance(order, Num) and order.text == "2"):
                    raise MathSpeakError("Ismeretlen parciális derivált rend")
                return prefix + ["második", "parciális"] + var + ["szerint"], num.arg is None
            return prefix + ["parciális"] + var + ["szerint"], num.arg is None
        sq = ["négyzet"] if order is not None else []
        if order is not None and not (isinstance(order, Num) and order.text == "2"):
            raise MathSpeakError("Ismeretlen derivált rend")
        head = ["dé"] + sq + ([] if num.arg is None else speak_node(num.arg, ctx))
        return head + ["per", "dé"] + var + sq, num.arg is None
    return None


def _paren_words(inner, ctx: Ctx) -> list[str]:
    if _is_atomic(inner):
        return speak_node(inner, ctx)
    return [",", "zárójelben"] + speak_node(inner, ctx) + [","]


def _frac(node: Frac, ctx: Ctx) -> list[str]:
    d = _deriv(node, ctx)
    if d is not None:
        return d[0]
    num, den = _strip_paren(node.num), _strip_paren(node.den)
    if (isinstance(num, Num) and isinstance(den, Num) and "," not in num.text + den.text
            and int(den.text) in FRACTION_NAMES):
        return [cardinal(int(num.text)), FRACTION_NAMES[int(den.text)]]
    n_words, d_words = speak_node(num, ctx), speak_node(den, ctx)
    if _is_simple_product(num) and _is_atomic(den):
        return n_words + ["per"] + d_words
    if _is_simple_product(num) and _is_simple_product(den):
        return n_words + ["per", ",", "zárójelben"] + d_words + [","]
    if _is_simple_product(num) and isinstance(den, Pow) and isinstance(den.base, Paren):
        return n_words + ["per"] + d_words
    return ["egy tört", ",", "a számláló"] + n_words + [",", "a nevező"] + d_words + [","]


def _pow(node: Pow, ctx: Ctx) -> list[str]:
    base = node.base
    if isinstance(base, Paren) and base.kind in "([":
        b = [",", "zárójelben"] + speak_node(base.inner, ctx) + [","]
    else:
        b = speak_node(base, ctx)
    e = _strip_paren(node.exp)
    if isinstance(e, Num) and "," not in e.text:
        n = int(e.text)
        if n == 2:
            return b + ["négyzet"]
        if n == 3:
            return b + ["köb"]
        w = exponent_word(n)
        return b + [_art(w), w]
    if isinstance(e, Neg) and e.op == "-" and isinstance(e.inner, Num) and "," not in e.inner.text:
        return b + ["a", "mínusz", exponent_word(int(e.inner.text))]
    if isinstance(e, Sym) and not e.sub and not e.vec:
        name = _letter(e.base, ctx, with_case=False)
        if e.base in GREEK:
            w = name + ("adikon" if word_harmony(name) == BACK else "ediken")
        else:
            w = f"{name}-{'adikon' if word_harmony(name) == BACK else 'ediken'}"
        return b + [_art(w), w]
    if isinstance(e, Postfix) and e.op == "°":
        return b + ["fok"]
    ew = speak_node(e, ctx)
    return b + [_art(ew[0] if ew[0] != "," else ew[1]), *ew, "hatványon", ","]


def _diff_class(body) -> str:
    """Az integrál mértéke: line / surface / volume / ''."""
    items = body.items if isinstance(body, Prod) else [("", body)]
    for _, n in reversed(items):
        if isinstance(n, Diff) and isinstance(n.arg, Sym):
            b = n.arg.base
            if b in LINE_DIFFS:
                return "line"
            if b in SURFACE_DIFFS:
                return "surface"
            if b in VOLUME_DIFFS:
                return "volume"
            return ""
    return ""


def _bound(node, ctx: Ctx, kind: str) -> list[str]:
    words = speak_node(node, ctx)
    if "," in words:
        raise MathSpeakError("Összetett határ")
    return suffixed(words, kind)


def _bigop(node: BigOp, ctx: Ctx) -> list[str]:
    body = speak_node(node.body, ctx)
    if node.kind in ("sum", "prod"):
        head = ["szumma" if node.kind == "sum" else "produktum"]
        lo = node.lower
        if isinstance(lo, Rel) and lo.first is not None and len(lo.rest) == 1 and lo.rest[0][0] == "=":
            head += speak_node(lo.first, ctx) + ["egyenlő"] + _bound(lo.rest[0][1], ctx, "tól")
            if node.upper is not None:
                head += _bound(node.upper, ctx, "ig")
        elif lo is not None:
            head += speak_node(lo, ctx) + ["szerint"]
            if node.upper is not None:
                raise MathSpeakError("Összeg felső határral, de változó nélkül")
        return head + body
    cls = _diff_class(node.body)
    if node.kind == "oint":
        head = ["zárt felületi integrál"] if cls == "surface" else ["zárt görbe menti integrál"]
    elif node.kind == "oiint":
        head = ["zárt felületi integrál"]
    elif node.kind == "iint":
        head = ["felületi integrál"]
    elif node.kind == "iiint":
        head = ["térfogati integrál"]
    else:
        head = ["integrál"]
    if node.lower is not None and node.upper is not None:
        head += _bound(node.lower, ctx, "tól") + _bound(node.upper, ctx, "ig") + [","]
    elif node.upper is not None:
        head += _bound(node.upper, ctx, "ig") + [","]
    elif node.lower is not None:
        dom = speak_node(node.lower, ctx)
        if "," in dom:
            raise MathSpeakError("Összetett integrálási tartomány")
        closed = node.kind in ("oint", "oiint")
        noun = {"line": "görbére", "surface": "zárt felületre" if closed else "felületre",
                "volume": "térfogatra"}.get(cls, "tartományra")
        head += [_art(dom[0]), *dom, noun, ","]
    return head + body + [","]


def _lim(node: Lim, ctx: Ctx) -> list[str]:
    head = ["limesz"]
    s = node.sub
    if isinstance(s, Rel) and s.first is not None and len(s.rest) == 1 and s.rest[0][0] == "→":
        head += speak_node(s.first, ctx) + ["tart"] + _bound(s.rest[0][1], ctx, "hoz")
    elif s is not None:
        raise MathSpeakError("Ismeretlen limesz-index")
    return head + [","] + speak_node(node.body, ctx)


def _func(node: Func, ctx: Ctx) -> list[str]:
    if node.name == "laplace":
        words = ["nabla négyzet"]
    else:
        words = [FUNCS[node.name]]
    if node.sub is not None:
        words = speak_node(node.sub, ctx) + ["alapú"] + words
    if node.sup is not None:
        if isinstance(node.sup, Num) and node.sup.text == "2":
            words += ["négyzet"]
        else:
            words = _pow(Pow(Text(" ".join(words)), node.sup), ctx)
    if node.arg is None:
        return words
    arg = node.arg
    if isinstance(arg, Prod) and all(op == "" and _is_atomic(n) for op, n in arg.items):
        return words + [w for _, n in arg.items for w in speak_node(n, ctx)]
    if isinstance(arg, Paren) and arg.kind == "(":
        inner = arg.inner
        if _is_atomic(inner):
            return words + speak_node(inner, ctx)
        return words + [",", "zárójelben"] + speak_node(inner, ctx) + [","]
    return words + speak_node(arg, ctx)


def _juxtaposed(prev, n) -> bool:
    """Egymás mellé írt tényezők "szorozva" nélkül: négy pí, egy ketted Q, í végtelen, szöveg."""
    if isinstance(prev, Text) or isinstance(n, Text):
        return True
    if isinstance(prev, Frac) and isinstance(prev.num, Num) and isinstance(prev.den, Num):
        return True
    if isinstance(prev, Num) and isinstance(n, (Sym, Pow, Func, Sqrt)):
        return True
    return isinstance(prev, Sym) and isinstance(n, Atom) and n.words == "végtelen"


def _prod(node: Prod, ctx: Ctx) -> list[str]:
    out: list[str] = []
    prev = None
    for op, n in node.items:
        if prev is not None:
            if isinstance(prev, Frac) and _deriv(prev, ctx) and _deriv(prev, ctx)[1]:  # type: ignore[index]
                out.append(",")
            elif op == "·" and (_is_vector(prev) or _is_vector(n) or (isinstance(n, Diff) and not n.partial)):
                out.append("skalárszorzat")
            elif op == "×" and (_is_vector(prev) or _is_vector(n)):
                out.append("vektoriálisan szorozva")
            elif op == "" and isinstance(n, Diff):
                if _is_vector(prev) and _is_vector(n):
                    out.append("skalárszorzat")
                elif isinstance(prev, (Frac, BigOp)):
                    out.append(",")
            elif op == "" and _is_vector(prev) and _is_vector(n):
                out.append("skalárszorzat")
            elif not (op == "" and _juxtaposed(prev, n)):
                out.append("szorozva")
        if isinstance(n, Paren) and n.kind in "([":
            out += _paren_words(n.inner, ctx)
        else:
            out += speak_node(n, ctx)
        prev = n
    return out


def _rel(node: Rel, ctx: Ctx) -> list[str]:
    out = [] if node.first is None else speak_node(node.first, ctx)
    prev = None
    for op, n in node.rest:
        if isinstance(op, tuple):
            out += [",", "ebből, ha"] + speak_node(op[1], ctx) + [",", "ezt kapjuk:"] + speak_node(n, ctx)
            prev = "⇒"
            continue
        if node.first is None and prev is None and op == "≈":
            word = "közelítőleg"
        elif op == "→" and len(node.rest) == 1 and node.first is not None:
            words = speak_node(n, ctx)
            if _is_atomic(n) and "," not in words:
                out += ["tart"] + suffixed(words, "hoz")
            else:  # E → 2kp/x³: é tart a ... értékhez
                out += ["tart", _art(words[0] if words[0] != "," else words[1]), *words, "értékhez"]
            prev = op
            continue
        elif op == "⇔":
            out += [",", "ami egyenértékű azzal, hogy"] + speak_node(n, ctx)
            prev = "⇒"
            continue
        elif op in ("→", "⇒"):
            word = None
        else:
            word = REL_WORDS[op]
        if word is None:
            out += [",", "ebből következik, hogy"]
        elif prev is not None and prev not in ("→", "⇒"):
            out += [",", "ami", word]
        else:
            out.append(word)
        out += speak_node(n, ctx)
        prev = op
    return out


def speak_node(node, ctx: Ctx) -> list[str]:
    if isinstance(node, Num):
        return _num(node.text)
    if isinstance(node, Sym):
        words = [_letter(node.base, ctx)]
        if node.sub is not None:
            words += _speak_sub(node.sub, ctx)
        if node.primes:
            words.append("vessző" if node.primes == 1 else "két vessző")
        words += node.mods
        if node.vec:
            words.append("vektor")
        return words
    if isinstance(node, Text):
        return [node.text] if node.text else []
    if isinstance(node, Atom):
        return [node.words]
    if isinstance(node, Delta):
        return ["delta"] + speak_node(node.inner, ctx)
    if isinstance(node, Apply):
        return speak_node(node.fn, ctx) + _bound(node.arg, ctx, "ban")
    if isinstance(node, Eval):
        inner = speak_node(node.inner, ctx)
        return ([",", _art(inner[0])] + inner + ["kifejezés"] + _bound(node.lower, ctx, "tól")
                + _bound(node.upper, ctx, "ig") + ["vett helyettesítési értéke", ","])
    if isinstance(node, Under):
        note = [] if node.note is None else [",", "ami"] + speak_node(node.note, ctx) + [","]
        return speak_node(node.inner, ctx) + note
    if isinstance(node, Diff):
        head = ["parciális"] if node.partial else ["dé"]
        if node.order is not None:
            if not (isinstance(node.order, Num) and node.order.text == "2"):
                raise MathSpeakError("Ismeretlen differenciál rend")
            head.append("négyzet")
        return head + ([] if node.arg is None else speak_node(node.arg, ctx))
    if isinstance(node, Pow):
        return _pow(node, ctx)
    if isinstance(node, Frac):
        return _frac(node, ctx)
    if isinstance(node, Sqrt):
        name = {"2": "négyzetgyök", "3": "köbgyök"}.get(node.index)
        if name is None:
            name = f"{ordinal(int(node.index))} gyök"
        inner = _strip_paren(node.arg)
        if _is_simple_product(inner):
            # a gyök alatti szorzat egybeolvasva: "négyzetgyök el cé"
            words = []
            for w in (speak_node(inner, ctx)):
                if w != "szorozva":
                    words.append(w)
            return [name] + words
        return [name, "alatt"] + speak_node(inner, ctx) + [","]
    if isinstance(node, Paren):
        if node.kind == "|":
            if _is_atomic(node.inner):
                return speak_node(node.inner, ctx) + ["abszolút értéke"]
            return [",", "zárójelben"] + speak_node(node.inner, ctx) + [",", "abszolút értéke"]
        return _paren_words(node.inner, ctx)
    if isinstance(node, Neg):
        inner = node.inner
        if isinstance(inner, Paren) and inner.kind in "([" and _is_atomic(inner.inner):
            inner = inner.inner
        return [ADD_WORDS[node.op]] + speak_node(inner, ctx)
    if isinstance(node, Sum):
        out: list[str] = []
        for op, n in node.items:
            if op:
                out.append(ADD_WORDS[op])
            out += speak_node(n, ctx)
        return out
    if isinstance(node, Prod):
        return _prod(node, ctx)
    if isinstance(node, Func):
        return _func(node, ctx)
    if isinstance(node, BigOp):
        return _bigop(node, ctx)
    if isinstance(node, Lim):
        return _lim(node, ctx)
    if isinstance(node, Rel):
        return _rel(node, ctx)
    if isinstance(node, Postfix):
        word = {"°": "fok", "%": "százalék", "!": "faktoriális"}[node.op]
        return speak_node(node.inner, ctx) + [word]
    raise MathSpeakError(f"Ismeretlen csomópont: {type(node).__name__}")


def join_words(words: list[str]) -> str:
    text = " ".join(w for w in words if w)
    text = re.sub(r"\s+,", ",", text)
    text = re.sub(r",(\s*,)+", ",", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip(" ,")


SPOKEN_OK_RE = re.compile(r"^[a-záéíóöőúüűA-ZÁÉÍÓÖŐÚÜŰ ,:\-]+$")


def _check(text: str) -> str:
    if not text or not SPOKEN_OK_RE.match(text):
        raise MathSpeakError(f"Nem tiszta kimenet: {text!r}")
    return text


def speak(src: str, ctx: Ctx | None = None) -> list[str]:
    """Képlet (vagy `\\qquad`-dal elválasztott képletsor) -> kimondható mondatok listája."""
    ctx = ctx or Ctx()
    return [_check(join_words(speak_node(f, ctx))) for f in parse_formulas(src)]


UNIT_TAIL_RE = re.compile(r"^(.*[\d⁰-⁹])\s+([A-Za-zΩµμ°%/·²³⁻¹()]+)$")


def speak_one(src: str, ctx: Ctx | None = None) -> str:
    m = UNIT_TAIL_RE.match(src.strip())
    if m and speak_unit(m.group(2)) not in (None, "nincs"):
        # szám után mértékegység: 3·10⁸ m/s
        return speak_one(m.group(1), ctx) + " " + speak_unit(m.group(2))  # type: ignore[operator]
    parts = speak(src, ctx)
    if len(parts) != 1:
        return ", ".join(parts)
    return parts[0]


def letters_in(src: str) -> set[str]:
    """A képletben jelként használt latin betűk (a kis/nagy betű megkülönböztetéséhez)."""
    out: set[str] = set()

    def walk(n) -> None:
        if isinstance(n, Sym):
            if n.base.isascii():
                out.add(n.base)
            return
        if isinstance(n, (list, tuple)):
            for x in n:
                walk(x)
            return
        if hasattr(n, "__dataclass_fields__"):
            for f in n.__dataclass_fields__:
                if f == "sub" and isinstance(n, Sym):
                    continue
                walk(getattr(n, f))

    try:
        walk(parse_formulas(src))
    except MathSpeakError:
        pass
    return out


def both_cases(letters: set[str]) -> set[str]:
    return {c for c in letters if c.isupper() and c.lower() in letters}


def sentence(text: str) -> str:
    text = text.strip()
    if not text:
        return text
    return text[0].upper() + text[1:] + ("" if text.endswith((".", "!", "?")) else ".")


# --- mértékegységek ---

UNIT_NAMES = {
    "V": "volt", "A": "amper", "Ω": "óm", "W": "watt", "J": "{{joule|dzsúl}}", "C": "{{coulomb|kulomb}}",
    "F": "farad", "H": "henri", "T": "tesla", "Wb": "{{weber|véber}}", "S": "{{siemens|zímensz}}",
    "N": "{{newton|nyúton}}", "Pa": "pascal", "K": "kelvin", "s": "szekundum", "m": "méter",
    "g": "gramm", "kg": "kilogramm", "Hz": "hertz", "eV": "elektronvolt", "mol": "mól", "cd": "kandela",
    "kΩ": "kiloóm", "MΩ": "megaóm", "mA": "milliamper", "µA": "mikroamper", "μA": "mikroamper",
    "mV": "millivolt", "kV": "kilovolt", "mW": "milliwatt", "kW": "kilowatt", "kJ": "kilojoule",
    "mH": "millihenri", "µH": "mikrohenri", "μH": "mikrohenri", "µF": "mikrofarad", "μF": "mikrofarad",
    "nF": "nanofarad", "pF": "pikofarad", "mT": "millitesla", "kHz": "kilohertz", "MHz": "megahertz",
    "GHz": "gigahertz", "ms": "milliszekundum", "µs": "mikroszekundum", "μs": "mikroszekundum",
    "ns": "nanoszekundum", "km": "kilométer", "cm": "centiméter", "mm": "milliméter", "nm": "nanométer",
    "°C": "celsius-fok", "%": "százalék", "°": "fok", "rad": "radián",
}
_UNIT_KEYS = sorted(UNIT_NAMES, key=len, reverse=True)
_NO_UNIT = {"nincs", "–", "-", "—", "1", "egység nélküli", "dimenzió nélküli"}


def speak_unit(src: str) -> str | None:
    """Mértékegység-kifejezés kiolvasva (`Vm/(As)` -> volt méter per amper szekundum); None, ha nem az."""
    s = src.strip()
    if not s:
        return None
    if s.lower() in _NO_UNIT:
        return "nincs"
    parts = [p.strip() for p in s.split("=")]
    spoken = [_unit_expr(p) for p in parts]
    if any(x is None for x in spoken):
        return None
    out = spoken[0]
    for x in spoken[1:]:
        out += f", ami egyenlő {x}"
    return out


def _unit_expr(s: str) -> str | None:
    words: list[str] = []
    i = 0
    s = s.replace("·", " ").replace("⋅", " ").replace("*", " ")
    while i < len(s):
        ch = s[i]
        if ch.isspace() or ch in "()":
            i += 1
            continue
        if ch == "/":
            words.append("per")
            i += 1
            continue
        if ch == "1" and (i + 1 == len(s) or s[i + 1] in "/ "):
            words.append("egy")
            i += 1
            continue
        m = re.match(r"[a-záéíóöőúüű]{3,}", s[i:])
        if m and not any(s.startswith(k, i) and len(k) >= len(m.group(0)) for k in _UNIT_KEYS):
            words.append(m.group(0))  # szóval leírt rész, pl. "(mező)/m"
            i += m.end()
            continue
        for k in _UNIT_KEYS:
            if s.startswith(k, i):
                i += len(k)
                exp = ""
                while i < len(s) and s[i] in SUPERSCRIPTS:
                    exp += SUPERSCRIPTS[s[i]]
                    i += 1
                name = UNIT_NAMES[k]
                if exp in ("2", "3") and name in ("méter", "centiméter", "milliméter", "kilométer"):
                    name = ("négyzet" if exp == "2" else "köb") + name
                elif exp == "2":
                    name += " négyzet"
                elif exp == "3":
                    name += " köb"
                elif exp:
                    return None
                words.append(name)
                break
        else:
            return None
    if not words or words[0] == "per" or words[-1] == "per":
        return None
    if len(words) == 1 and words[0] == "szekundum":
        return "másodperc"
    return " ".join(words)
