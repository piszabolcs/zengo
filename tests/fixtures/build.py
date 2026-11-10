"""Tesztdokumentumok generálása (PDF, DOCX, EPUB), hogy ne kelljen bináris fájlt tárolni a repóban."""

from __future__ import annotations

import os
from pathlib import Path

FONTS = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"
ARIAL = FONTS / "arial.ttf"
ARIAL_BOLD = FONTS / "arialbd.ttf"
CAMBRIA_MATH = FONTS / "cambria.ttc"

LOREM = [
    "A villamos áram a töltéshordozók rendezett mozgása, amelyet a vezető két vége",
    "között fennálló feszültség hoz létre. Az áramerősség mértékegysége az amper, a",
    "feszültségé a volt. A jelenség megértéséhez először a vezetők szerkezetét kell",
    "megvizsgálnunk, majd a töltések mozgását leíró törvényeket.",
]


def _page(doc, w=595, h=842):
    page = doc.new_page(width=w, height=h)
    page.insert_font(fontname="AR", fontfile=str(ARIAL))
    page.insert_font(fontname="ARB", fontfile=str(ARIAL_BOLD))
    return page


def _lines(page, x, y, lines, size=11, font="AR", leading=1.35):
    for ln in lines:
        page.insert_text((x, y), ln, fontsize=size, fontname=font)
        y += size * leading
    return y


def make_pdf_book(path: Path, with_toc: bool = False) -> Path:
    """4 oldalas könyv élőfejjel, oldalszámmal, lábjegyzettel, felső indexszel és elválasztással."""
    import pymupdf

    doc = pymupdf.open()
    for pno in range(1, 5):
        page = _page(doc)
        page.insert_text((40, 30), "Minta Könyv – Villamosságtan alapjai", fontsize=8, fontname="AR")
        page.insert_text((290, 815), f"- {pno} -", fontsize=9, fontname="AR")
        y = 80
        if pno == 1:
            page.insert_text((40, y), "Első fejezet", fontsize=18, fontname="ARB")
            y += 40
            y = _lines(page, 40, y, LOREM)
            y += 14
            page.insert_text((40, y), "Ez a mondat lábjegyzetre hivatkozik", fontsize=11, fontname="AR")
            ref_x = 40 + pymupdf.get_text_length("Ez a mondat lábjegyzetre hivatkozik", fontname="helv", fontsize=11)
            page.insert_text((ref_x + 2, y - 4), "1", fontsize=7, fontname="AR")
            page.insert_text((ref_x + 8, y), ", és itt folytatódik a szöveg.", fontsize=11, fontname="AR")
            y += 11 * 1.35 + 14
            y = _lines(page, 40, y, ["A hosszú szavak a sor végén néha elvá-",
                                     "lasztva jelennek meg, ezt össze kell vonni."])
            page.insert_text((40, 740), "1 Ez egy lábjegyzet szövege, ami nem olvasódik fel.", fontsize=8,
                             fontname="AR")
        elif pno == 2:
            y = _lines(page, 40, y, LOREM)
            y += 14
            _lines(page, 40, y, ["A második oldal második bekezdése, amely szintén a törzsszöveg része."])
        elif pno == 3:
            page.insert_text((40, y), "Második fejezet", fontsize=18, fontname="ARB")
            y += 40
            y = _lines(page, 40, y, LOREM[:2])
            y += 20
            page.insert_text((40, y), "Alfejezet", fontsize=14, fontname="ARB")
            y += 28
            _lines(page, 40, y, LOREM[2:])
        else:
            _lines(page, 40, y, ["Az utolsó oldal rövid szövege zárja a könyvet."])
    if with_toc:
        doc.set_toc([[1, "Első fejezet", 1], [1, "Második fejezet", 3], [2, "Alfejezet", 3]])
    doc.set_metadata({"title": "Minta Könyv", "author": "Teszt Szerző"})
    doc.save(str(path))
    return path


def make_pdf_two_columns(path: Path) -> Path:
    import pymupdf

    doc = pymupdf.open()
    page = _page(doc, w=595, h=842)
    page.insert_text((60, 90), "Kéthasábos cikk", fontsize=20, fontname="ARB")
    left = ["Bal hasáb első bekezdése, ami", "több sorból áll és itt", "fejeződik be."]
    right = ["Jobb hasáb első bekezdése,", "amelyet a bal hasáb után", "kell felolvasni."]
    y = 150
    for i in range(3):
        _lines(page, 60, y, [f"{i + 1}. " + left[0], *left[1:]])
        _lines(page, 320, y, [f"{i + 1}. " + right[0], *right[1:]])
        y += 90
    # képletes blokk
    page.insert_text((60, 600), "Az R = ρ · l / A összefüggés ∑ és ∫ jelekkel.", fontsize=11, fontname="AR")
    doc.save(str(path))
    return path


def make_docx(path: Path) -> Path:
    import docx
    from docx.opc.constants import CONTENT_TYPE as CT
    from docx.opc.constants import RELATIONSHIP_TYPE as RT
    from docx.opc.packuri import PackURI
    from docx.opc.part import Part
    from docx.oxml import parse_xml

    W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    M = "http://schemas.openxmlformats.org/officeDocument/2006/math"
    d = docx.Document()
    d.core_properties.title = "DOCX jegyzet"
    d.core_properties.author = "Docx Szerző"
    d.add_heading("Első fejezet", level=1)
    p = d.add_paragraph("Ez a bekezdés lábjegyzetre hivatkozik")
    p._p.append(parse_xml(f'<w:r xmlns:w="{W}"><w:footnoteReference w:id="1"/></w:r>'))
    p.add_run(" és folytatódik.")
    d.add_heading("Alfejezet", level=2)
    m = d.add_paragraph("A képlet: ")
    m._p.append(parse_xml(
        f'<m:oMath xmlns:m="{M}"><m:r><m:t>R=</m:t></m:r><m:f><m:num><m:r><m:t>ρl</m:t></m:r></m:num>'
        f'<m:den><m:r><m:t>A</m:t></m:r></m:den></m:f></m:oMath>'))
    m.add_run(" ahol R az ellenállás.")
    d.add_heading("Második fejezet", level=1)
    d.add_paragraph("A második fejezet szövege.")
    footnotes = (
        f'<w:footnotes xmlns:w="{W}">'
        '<w:footnote w:type="separator" w:id="-1"><w:p><w:r><w:separator/></w:r></w:p></w:footnote>'
        '<w:footnote w:type="continuationSeparator" w:id="0"><w:p><w:r><w:continuationSeparator/></w:r></w:p>'
        '</w:footnote>'
        '<w:footnote w:id="1"><w:p><w:r><w:t>Ez a DOCX lábjegyzet szövege.</w:t></w:r></w:p></w:footnote>'
        '</w:footnotes>').encode()
    part = Part(PackURI("/word/footnotes.xml"), CT.WML_FOOTNOTES, footnotes, d.part.package)
    d.part.relate_to(part, RT.FOOTNOTES)
    d.save(str(path))
    return path


def make_epub(path: Path) -> Path:
    import pymupdf
    from ebooklib import epub

    book = epub.EpubBook()
    book.set_identifier("felolvaso-teszt")
    book.set_title("EPUB Regény")
    book.set_language("hu")
    book.add_author("Epub Író")
    pix = pymupdf.Pixmap(pymupdf.csRGB, pymupdf.IRect(0, 0, 60, 80), False)
    pix.set_rect(pix.irect, (200, 30, 30))
    book.set_cover("cover.jpg", pix.tobytes("jpg"))

    copyright_page = epub.EpubHtml(title="Impresszum", file_name="copyright.xhtml", lang="hu")
    copyright_page.content = "<html><body><p>Minden jog fenntartva. ISBN 978-963-000-000-0</p></body></html>"
    c1 = epub.EpubHtml(title="Első fejezet: Kezdet", file_name="c1.xhtml", lang="hu")
    c1.content = (
        '<html xmlns:epub="http://www.idpf.org/2007/ops"><body><h1>Első fejezet</h1>'
        '<p>Egyszer volt, hol nem volt<a epub:type="noteref" href="#fn1">1</a>, egy kis falu.</p>'
        '<p>A második bekezdés<sup><a href="#fn2">2</a></sup> itt folytatódik.</p>'
        '<aside epub:type="footnote" id="fn1"><p>Ez az első lábjegyzet.</p></aside>'
        '<aside role="doc-footnote" id="fn2"><p>Ez a második lábjegyzet.</p></aside>'
        "</body></html>")
    c2 = epub.EpubHtml(title="Második fejezet", file_name="c2.xhtml", lang="hu")
    c2.content = ("<html><body><h2>Második fejezet</h2><h3>Egy alcím</h3>"
                  "<p>A második fejezet szövege.</p></body></html>")
    for c in (copyright_page, c1, c2):
        book.add_item(c)
    book.toc = [epub.Link("c1.xhtml", "Első fejezet: Kezdet", "c1"), epub.Link("c2.xhtml", "Második fejezet", "c2")]
    book.guide = [{"href": "copyright.xhtml", "title": "Impresszum", "type": "copyright-page"}]
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ["nav", copyright_page, c1, c2]
    epub.write_epub(str(path), book)
    return path


MARKDOWN = """---
title: Markdown jegyzet
author: Md Szerző
---

# Első fejezet

Ez egy bekezdés lábjegyzettel[^1], ami **félkövér** szót is tartalmaz.

## Alszakasz

Itt egy képlet: $R = \\rho \\frac{l}{A}$ a szövegben.

$$
U = R \\cdot I
$$

```python
print("kód nem olvasódik fel")
```

# Második fejezet

- első elem
- második elem

[^1]: Ez a markdown lábjegyzet.
"""


def make_markdown(path: Path) -> Path:
    path.write_text(MARKDOWN, encoding="utf-8")
    return path
