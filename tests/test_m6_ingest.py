import pytest
from fastapi.testclient import TestClient

from app.ingest.base import Block, Document, ImportError
from app.ingest.registry import importer_for, load_document
from app.main import create_app
from app.prepare.rule_based import prepare
from app.state import AppState
from app.ttsmd.validator import validate_text
from tests.fixtures.build import (
    ARIAL,
    make_docx,
    make_epub,
    make_markdown,
    make_pdf_book,
    make_pdf_two_columns,
)

needs_arial = pytest.mark.skipif(not ARIAL.exists(), reason="Arial betűtípus kell a teszt-PDF-hez")


def body_text(doc: Document) -> str:
    return " ".join(b.text for b in doc.blocks if b.type in ("paragraph", "heading"))


# L1-01
def test_document_roundtrip():
    doc = Document(title="T", author=None, source_path="x.pdf", cover_image=b"\x01\x02",
                   blocks=[Block(id="b1", type="heading", level=1, text="Cím", page=1),
                           Block(id="b2", type="paragraph", text="Szöveg", math_suspect=True)])
    again = Document.model_validate_json(doc.model_dump_json())
    assert again == doc


# L1-02
def test_markdown_importer(tmp_path):
    doc = load_document(make_markdown(tmp_path / "jegyzet.md"))
    assert doc.title == "Markdown jegyzet" and doc.author == "Md Szerző"
    heads = [(b.level, b.text) for b in doc.blocks if b.type == "heading"]
    assert heads == [(1, "Első fejezet"), (2, "Alszakasz"), (1, "Második fejezet")]
    fns = [b for b in doc.blocks if b.type == "footnote"]
    assert [b.text for b in fns] == ["Ez a markdown lábjegyzet."]
    # a lábjegyzet a hivatkozó bekezdés után áll, a hivatkozás eltűnt
    idx = doc.blocks.index(fns[0])
    assert doc.blocks[idx - 1].text.startswith("Ez egy bekezdés lábjegyzettel,")
    assert "[^1]" not in body_text(doc)
    math = [b for b in doc.blocks if b.math_suspect]
    assert any("\\rho" in b.text for b in math) and any("U = R" in b.text for b in math)
    assert "kód nem olvasódik" not in body_text(doc)
    assert "első elem" in body_text(doc)


# L1-03
def test_docx_importer(tmp_path):
    doc = load_document(make_docx(tmp_path / "jegyzet.docx"))
    assert doc.title == "DOCX jegyzet" and doc.author == "Docx Szerző"
    heads = [(b.level, b.text) for b in doc.blocks if b.type == "heading"]
    assert heads == [(1, "Első fejezet"), (2, "Alfejezet"), (1, "Második fejezet")]
    assert [b.text for b in doc.blocks if b.type == "footnote"] == ["Ez a DOCX lábjegyzet szövege."]
    para = next(b for b in doc.blocks if "hivatkozik" in b.text)
    assert para.text == "Ez a bekezdés lábjegyzetre hivatkozik és folytatódik."
    formula = next(b for b in doc.blocks if "képlet" in b.text)
    assert formula.math_suspect and "[képlet: R=ρlA]" in formula.text


# L1-04
def test_epub_importer(tmp_path):
    doc = load_document(make_epub(tmp_path / "regeny.epub"))
    assert doc.title == "EPUB Regény" and doc.author == "Epub Író"
    heads = [(b.level, b.text) for b in doc.blocks if b.type == "heading"]
    # a fejezetcím a nav-ból jön, a dokumentum azonos h-címe nem duplikálódik
    assert heads == [(1, "Első fejezet: Kezdet"), (1, "Második fejezet"), (3, "Egy alcím")]
    text = body_text(doc)
    assert "Egyszer volt, hol nem volt , egy kis falu." in text or "Egyszer volt, hol nem volt, egy kis falu." in text
    assert "1" not in text.replace("Első", "")
    assert "Minden jog fenntartva" not in text
    assert [b.text for b in doc.blocks if b.type == "footnote"] == ["Ez az első lábjegyzet.",
                                                                    "Ez a második lábjegyzet."]
    assert doc.cover_image and doc.cover_image[:2] == b"\xff\xd8"


# L1-05, L1-06
@needs_arial
def test_pdf_headings_and_filtering(tmp_path):
    doc = load_document(make_pdf_book(tmp_path / "konyv.pdf"))
    assert doc.title == "Minta Könyv" and doc.author == "Teszt Szerző"
    heads = [(b.level, b.text) for b in doc.blocks if b.type == "heading"]
    assert heads == [(1, "Első fejezet"), (1, "Második fejezet"), (2, "Alfejezet")]
    text = body_text(doc)
    assert "Minta Könyv – Villamosságtan" not in text      # élőfej
    assert "- 1 -" not in text and "- 3 -" not in text      # oldalszám
    assert "lábjegyzet szövege" not in text                  # lábjegyzet nem a törzsben
    assert "hivatkozik, és itt folytatódik" in text          # a felső indexes hivatkozás törölve
    assert "elválasztva jelennek meg" in text                # elválasztás javítva
    fns = [b for b in doc.blocks if b.type == "footnote"]
    assert len(fns) == 1 and "Ez egy lábjegyzet szövege" in fns[0].text
    paras = [b for b in doc.blocks if b.type == "paragraph"]
    assert any(p.text.startswith("A villamos áram") and p.text.endswith("törvényeket.") for p in paras)


@needs_arial
def test_pdf_toc_overrides_heuristics(tmp_path):
    doc = load_document(make_pdf_book(tmp_path / "konyv.pdf", with_toc=True))
    heads = [(b.level, b.text) for b in doc.blocks if b.type == "heading"]
    assert heads == [(1, "Első fejezet"), (1, "Második fejezet"), (2, "Alfejezet")]


# L1-07
@needs_arial
def test_pdf_two_columns_and_math(tmp_path):
    doc = load_document(make_pdf_two_columns(tmp_path / "cikk.pdf"))
    paras = [b.text for b in doc.blocks if b.type == "paragraph"]
    order = [p[:6] for p in paras if p.startswith(("1. ", "2. ", "3. "))]
    lefts = [i for i, p in enumerate(paras) if "Bal hasáb" in p]
    rights = [i for i, p in enumerate(paras) if "Jobb hasáb" in p]
    assert len(lefts) == 3 and len(rights) == 3, order
    assert max(lefts) < min(rights)
    math = [b for b in doc.blocks if "összefüggés" in b.text]
    assert math and math[0].math_suspect


# L1-08
def test_registry(tmp_path):
    assert type(importer_for(tmp_path / "a.PDF")).__name__ == "PdfImporter"
    assert type(importer_for(tmp_path / "a.epub")).__name__ == "EpubImporter"
    assert type(importer_for(tmp_path / "a.md")).__name__ == "MarkdownImporter"
    with pytest.raises(ImportError, match="Nem támogatott"):
        importer_for(tmp_path / "a.odt")
    bad = tmp_path / "hibas.pdf"
    bad.write_bytes(b"nem pdf")
    with pytest.raises(ImportError, match="nem nyitható meg"):
        load_document(bad)


# L2-01..L2-03
def test_rule_based_epub_novel(tmp_path):
    doc = load_document(make_epub(tmp_path / "regeny.epub"))
    text, _warnings = prepare(doc)
    script, report = validate_text(text)
    assert report.errors == []
    assert [c.text for c in script.chapters()] == ["Első fejezet: Kezdet", "Második fejezet"]
    assert "lábjegyzet" not in text.lower()
    assert 'author: "Epub Író"' in text and "language: hu" in text


def test_rule_based_footnote_and_figure_switches():
    doc = Document(title="K", source_path="k.pdf", blocks=[
        Block(id="1", type="heading", level=1, text="Fejezet"),
        Block(id="2", type="paragraph", text="Szöveg."),
        Block(id="3", type="figure", text="1. ábra: Kapcsolási rajz"),
        Block(id="4", type="footnote", text="Lábjegyzet szöveg."),
        Block(id="5", type="heading", level=1, text="Üres fejezet"),
    ])
    off, w_off = prepare(doc)
    assert "Lábjegyzet szöveg" not in off and "Ábra:" not in off
    assert any("Üres fejezet" in w for w in w_off)
    on, _ = prepare(doc, read_footnotes=True, read_figure_captions=True)
    assert "## Lábjegyzetek\n\nLábjegyzet szöveg." in on
    assert "Ábra: 1. ábra: Kapcsolási rajz" in on
    assert validate_text(on)[1].errors == []


def test_rule_based_heading_promotion_and_math_warning():
    doc = Document(title="Cím nélkül", source_path="Szerző Név - A könyv.pdf", blocks=[
        Block(id="1", type="heading", level=2, text="Egy"),
        Block(id="2", type="heading", level=3, text="Egy-egy"),
        Block(id="3", type="paragraph", text="Az R = ρ·l/A képlet.", math_suspect=True),
        Block(id="4", type="paragraph", text="[[nem direktíva]] és {{nem kiejtés}}"),
    ])
    text, warnings = prepare(doc)
    script, report = validate_text(text)
    assert report.errors == [], report.errors
    assert [c.text for c in script.chapters()] == ["Egy"]
    assert "## Egy-egy" in text and "<!-- MATH_SUSPECT -->" in text
    assert any("1 képletgyanús blokk" in w for w in warnings)
    nodoc = Document(title="Puszta szöveg", source_path="x.md",
                     blocks=[Block(id="1", type="paragraph", text="Csak szöveg.")])
    t2, _ = prepare(nodoc)
    assert validate_text(t2)[0].chapters()[0].text == "Puszta szöveg"


def test_pdf_book_acceptance_via_api(config, tmp_path):
    """6.1 elfogadás: a törzsben nincs oldalszám, élőfej, lábjegyzet és hivatkozás; MATH figyelmeztetés."""
    if not ARIAL.exists():
        pytest.skip("Arial kell")
    pdf = make_pdf_book(tmp_path / "konyv.pdf")
    two = make_pdf_two_columns(tmp_path / "cikk.pdf")
    with TestClient(create_app(AppState(config), start_queue=False)) as client:
        r = client.post("/api/projects", files={"file": ("konyv.pdf", pdf.read_bytes(), "application/pdf")})
        assert r.status_code == 200, r.text
        pid = r.json()["project"]["id"]
        script = client.get(f"/api/projects/{pid}/script").json()["script_text"]
        assert "# Első fejezet" in script and "## Alfejezet" in script
        assert "Villamosságtan alapjai" not in script and "lábjegyzet szövege" not in script
        r = client.post("/api/projects", files={"file": ("cikk.pdf", two.read_bytes(), "application/pdf")},
                        data={"read_footnotes": "true"})
        assert any("képletgyanús" in w for w in r.json()["project"]["warnings"])
        r = client.post("/api/projects", files={"file": ("x.odt", b"x", "application/octet-stream")})
        assert r.status_code == 400
