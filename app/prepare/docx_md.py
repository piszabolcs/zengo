"""DOCX -> Markdown a képletes előkészítéshez: címsorok, félkövér bevezetők, táblázatok, listák,
OMML képletek LaTeX-ként (`$...$`, önálló képletsor `$$...$$`)."""

from __future__ import annotations

from pathlib import Path

from lxml import etree

from app.ingest.docx import M, W, _heading_level, _q, _style_name

ACCENTS = {"⃗": "\\vec", "→": "\\vec", "^": "\\hat", "̂": "\\hat", "¯": "\\bar", "̄": "\\bar", "˙": "\\dot",
           "̇": "\\dot", "~": "\\tilde", "̃": "\\tilde"}
NARY = {"∫": "\\int", "∬": "\\iint", "∭": "\\iiint", "∮": "\\oint", "∯": "\\oiint", "∑": "\\sum", "∏": "\\prod"}


def _val(el, path: str, default: str = "") -> str:
    found = el.find(path, {"m": M})
    if found is None:
        return default
    return found.get(_q(M, "val"), default)


def _kids(el, tag: str):
    return el.find(f"m:{tag}", {"m": M})


def omml_to_latex(el) -> str:
    """OMML (`m:oMath`) részfa -> LaTeX. Ismeretlen elem: `\\unsupported` (a képletolvasó elutasítja)."""
    tag = etree.QName(el).localname

    def sub(name: str) -> str:
        child = _kids(el, name)
        return "" if child is None else omml_to_latex(child)

    if tag in ("oMath", "e", "num", "den", "sub", "sup", "deg", "lim", "fName", "box", "borderBox"):
        return "".join(omml_to_latex(c) for c in el if etree.QName(c).localname not in ("rPr", "ctrlPr")
                       and not etree.QName(c).localname.endswith("Pr"))
    if tag == "oMathPara":
        return " \\qquad ".join(omml_to_latex(c) for c in el if etree.QName(c).localname == "oMath")
    if tag == "r":
        return "".join(t.text or "" for t in el.iter(_q(M, "t")))
    if tag == "f":
        return f"\\frac{{{sub('num')}}}{{{sub('den')}}}"
    if tag == "sSup":
        return f"{{{sub('e')}}}^{{{sub('sup')}}}"
    if tag == "sSub":
        return f"{{{sub('e')}}}_{{{sub('sub')}}}"
    if tag == "sSubSup":
        return f"{{{sub('e')}}}_{{{sub('sub')}}}^{{{sub('sup')}}}"
    if tag == "rad":
        deg = sub("deg").strip()
        return f"\\sqrt[{deg}]{{{sub('e')}}}" if deg else f"\\sqrt{{{sub('e')}}}"
    if tag == "nary":
        chr_ = _val(el, "m:naryPr/m:chr", "∫")
        cmd = NARY.get(chr_)
        if cmd is None:
            return "\\unsupported"
        lo, hi = sub("sub").strip(), sub("sup").strip()
        return cmd + (f"_{{{lo}}}" if lo else "") + (f"^{{{hi}}}" if hi else "") + f" {{{sub('e')}}}"
    if tag == "d":
        beg = _val(el, "m:dPr/m:begChr", "(")
        end = _val(el, "m:dPr/m:endChr", ")")
        sep = _val(el, "m:dPr/m:sepChr", ",")
        inner = sep.join(omml_to_latex(c) for c in el if etree.QName(c).localname == "e")
        return f"{beg or ''}{inner}{end or ''}"
    if tag == "func":
        return f"{sub('fName')} {sub('e')}"
    if tag == "acc":
        chr_ = _val(el, "m:accPr/m:chr", "̂")
        cmd = ACCENTS.get(chr_)
        return f"{cmd}{{{sub('e')}}}" if cmd else "\\unsupported"
    if tag == "bar":
        return f"\\overline{{{sub('e')}}}"
    if tag == "limLow":
        return f"{{{sub('e')}}}_{{{sub('lim')}}}"
    if tag == "limUpp":
        return f"{{{sub('e')}}}^{{{sub('lim')}}}"
    if tag == "groupChr":
        return sub("e")
    if tag == "eqArr":
        return " \\qquad ".join(omml_to_latex(c) for c in el if etree.QName(c).localname == "e")
    if tag.endswith("Pr"):
        return ""
    return "\\unsupported"


def _cell_text(el) -> str:
    return " ".join(paragraph_md(p)[0] for p in el.iter(_q(W, "p"))).replace("|", "\\|").strip()


def paragraph_md(p) -> tuple[str, bool]:
    """Bekezdés Markdown-szövege (félkövér `**`, képlet `$...$`), és hogy önálló képletsor-e."""
    parts: list[str] = []
    only_math = True
    has_math = False
    bold_open = False

    def close_bold() -> None:
        nonlocal bold_open
        if bold_open:
            parts.append("**")
            bold_open = False

    for child in p.iter():
        tag = child.tag
        if tag in (_q(M, "oMath"),):
            if child.getparent() is not None and child.getparent().tag == _q(M, "oMathPara"):
                continue
            close_bold()
            parts.append(f"${omml_to_latex(child)}$")
            has_math = True
        elif tag == _q(M, "oMathPara"):
            close_bold()
            parts.append(f"$${omml_to_latex(child)}$$")
            has_math = True
        elif tag == _q(W, "r") and child.getparent() is not None and not _in_math(child):
            text = "".join(t.text or "" for t in child.iter(_q(W, "t")))
            if not text:
                continue
            bold = child.find(f"{_q(W, 'rPr')}/{_q(W, 'b')}") is not None and \
                child.find(f"{_q(W, 'rPr')}/{_q(W, 'b')}").get(_q(W, "val"), "1") not in ("0", "false")
            if bold and not bold_open:
                parts.append("**")
                bold_open = True
            elif not bold and bold_open:
                close_bold()
            parts.append(text)
            if text.strip():
                only_math = False
    close_bold()
    text = "".join(parts).replace("** **", " ").replace("****", "")
    return text, has_math and only_math


def _in_math(el) -> bool:
    par = el.getparent()
    while par is not None:
        if par.tag in (_q(M, "oMath"), _q(M, "oMathPara")):
            return True
        par = par.getparent()
    return False


def docx_to_markdown(path: Path) -> str:
    import docx

    d = docx.Document(str(path))
    styles = {s.style_id: s.name for s in d.styles if s.style_id}
    out: list[str] = []
    for el in d.element.body.iterchildren():
        if el.tag == _q(W, "p"):
            text, display = paragraph_md(el)
            if not text.strip():
                continue
            level = _heading_level(_style_name(el, styles))
            if level:
                out += ["#" * level + " " + text.replace("**", "").strip(), ""]
            elif display:
                body = text.strip().strip("$")
                out += ["```latex", body, "```", ""]
            elif el.find(f"{_q(W, 'pPr')}/{_q(W, 'numPr')}") is not None:
                out += [f"- {text.strip()}"]
            else:
                out += [text.strip(), ""]
        elif el.tag == _q(W, "tbl"):
            rows = [[_cell_text(tc) for tc in tr.iter(_q(W, "tc"))] for tr in el.iter(_q(W, "tr"))]
            if not rows:
                continue
            width = max(len(r) for r in rows)
            rows = [r + [""] * (width - len(r)) for r in rows]
            out += ["", "| " + " | ".join(rows[0]) + " |", "|" + " --- |" * width]
            out += ["| " + " | ".join(r) + " |" for r in rows[1:]]
            out.append("")
    return "\n".join(out) + "\n"


def docx_has_math(path: Path) -> bool:
    import zipfile

    try:
        with zipfile.ZipFile(path) as z:
            return b"<m:oMath" in z.read("word/document.xml")
    except (OSError, KeyError, zipfile.BadZipFile):
        return False
