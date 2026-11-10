"""EPUB importer: gerinc sorrend, nav/NCX címek, lábjegyzetek, borító, előzék kihagyása (L1-04)."""

from __future__ import annotations

import posixpath
import re
import warnings
from pathlib import Path

from bs4 import BeautifulSoup, Tag

from app.ingest.base import BlockBuilder, Document, ImportError, clean_text, title_from_filename

FOOTNOTE_TYPES = {"footnote", "endnote", "rearnote", "note"}
FOOTNOTE_ROLES = {"doc-footnote", "doc-endnote", "doc-endnotes"}
NOTEREF_TYPES = {"noteref"}
NOTEREF_ROLES = {"doc-noteref"}
SKIP_LANDMARKS = {"toc", "copyright-page", "landmarks", "loi", "lot"}
BLOCK_TAGS = ["h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "blockquote", "figcaption", "img", "table", "dd",
              "dt", "pre"]


def _types(el: Tag) -> set[str]:
    return set((el.get("epub:type") or "").split())


def _role(el: Tag) -> str:
    return (el.get("role") or "").strip()


def _base(href: str) -> str:
    return posixpath.normpath(href.split("#", 1)[0])


class EpubImporter:
    def can_handle(self, path: Path) -> bool:
        return path.suffix.lower() == ".epub"

    def load(self, path: Path) -> Document:
        import ebooklib
        from ebooklib import epub

        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                book = epub.read_epub(str(path), options={"ignore_ncx": False})
        except Exception as e:
            raise ImportError(f"A fájl nem nyitható meg: {e}") from e

        title = self._meta(book, "title") or title_from_filename(path)
        author = self._meta(book, "creator")
        titles = self._toc_titles(book.toc)
        skip = self._skipped_hrefs(book)
        doc_warnings: list[str] = []

        bb = BlockBuilder()
        footnotes: list[str] = []
        for idref, _linear in book.spine:
            item = book.get_item_with_id(idref)
            if item is None or item.get_type() != ebooklib.ITEM_DOCUMENT:
                continue
            href = _base(item.get_name())
            if href in skip or isinstance(item, epub.EpubNav) or "nav" in (getattr(item, "properties", []) or []):
                continue
            soup = BeautifulSoup(item.get_content(), "lxml")
            if soup.body is None:
                continue
            self._strip_noterefs(soup)
            doc_notes = self._extract_footnotes(soup)
            first_heading = soup.body.find(["h1", "h2"])
            chapter_title = titles.get(href) or (clean_text(first_heading.get_text(" ")) if first_heading else "")
            elements = [el for el in soup.body.find_all(BLOCK_TAGS)
                        if not any(p.name in BLOCK_TAGS for p in el.parents if isinstance(p, Tag))]
            texts = [clean_text(el.get_text(" ")) for el in elements if el.name not in ("img", "table")]
            if not any(texts):
                footnotes.extend(doc_notes)  # külön jegyzetfájl (pl. endnotes.xhtml)
                continue
            if chapter_title:
                bb.add("heading", chapter_title, level=1)
            title_used = False
            seen_text = False
            for el in elements:
                name = el.name
                if name == "img":
                    bb.add("figure", el.get("alt") or "")
                    continue
                if name == "table":
                    bb.add("figure", "")
                    continue
                text = clean_text(el.get_text(" "))
                if not text:
                    continue
                if name in ("h1", "h2", "h3", "h4", "h5", "h6"):
                    # a dokumentum első, szöveg előtti címe maga a fejezetcím (a nav-beli alakja eltérhet)
                    if not title_used and chapter_title and (text.lower() == chapter_title.lower()
                                                             or (not seen_text and name in ("h1", "h2"))):
                        title_used = True
                        continue
                    level = {"h1": 2, "h2": 2, "h3": 3}.get(name, 3)
                    bb.add("heading", text, level=level)
                elif name == "figcaption":
                    bb.add("figure", text)
                else:
                    bb.add("paragraph", text)
                seen_text = True
            for fn in doc_notes:
                bb.add("footnote", fn)
        for fn in footnotes:
            bb.add("footnote", fn)
        return Document(title=title, author=author, source_path=str(path), blocks=bb.blocks,
                        cover_image=self._cover(book), warnings=doc_warnings)

    @staticmethod
    def _meta(book, name: str) -> str | None:
        vals = book.get_metadata("DC", name)
        return clean_text(vals[0][0]) if vals and vals[0][0] else None

    def _toc_titles(self, toc) -> dict[str, str]:
        out: dict[str, str] = {}

        def walk(entries) -> None:
            for e in entries:
                if isinstance(e, tuple):
                    section, children = e
                    if getattr(section, "href", None):
                        out.setdefault(_base(section.href), clean_text(section.title or ""))
                    walk(children)
                elif getattr(e, "href", None):
                    out.setdefault(_base(e.href), clean_text(e.title or ""))

        walk(toc)
        return {k: v for k, v in out.items() if v}

    def _skipped_hrefs(self, book) -> set[str]:
        """A nav `landmarks` részében toc / copyright-page típusú dokumentumok."""
        import ebooklib

        skip: set[str] = set()
        for item in book.get_items_of_type(ebooklib.ITEM_NAVIGATION):
            skip.add(_base(item.get_name()))
        for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            props = getattr(item, "properties", []) or []
            if "nav" not in props and not item.get_name().endswith(("nav.xhtml", "nav.html")):
                continue
            skip.add(_base(item.get_name()))
            soup = BeautifulSoup(item.get_content(), "lxml")
            nav_dir = posixpath.dirname(item.get_name())
            for nav in soup.find_all("nav"):
                if "landmarks" not in _types(nav):
                    continue
                for a in nav.find_all("a", href=True):
                    if _types(a) & SKIP_LANDMARKS:
                        skip.add(_base(posixpath.join(nav_dir, a["href"])))
        for ref in getattr(book, "guide", []) or []:
            if ref.get("type") in ("toc", "copyright-page") and ref.get("href"):
                skip.add(_base(ref["href"]))
        return skip

    @staticmethod
    def _strip_noterefs(soup: BeautifulSoup) -> None:
        for a in list(soup.find_all(True)):
            if not isinstance(a, Tag) or a.attrs is None:
                continue
            if _types(a) & NOTEREF_TYPES or _role(a) in NOTEREF_ROLES:
                a.decompose()
        # gyakori jelöletlen alak: <a href="#fn1"><sup>1</sup></a> vagy <sup><a href="#fn1">1</a></sup>
        for sup in list(soup.find_all("sup")):
            if sup.attrs is None:
                continue
            if re.fullmatch(r"\s*[\d*†‡]+\s*", sup.get_text() or "") and (
                    sup.find("a", href=re.compile("#")) or (sup.parent and sup.parent.name == "a")):
                target = sup.parent if sup.parent and sup.parent.name == "a" else sup
                target.decompose()

    @staticmethod
    def _extract_footnotes(soup: BeautifulSoup) -> list[str]:
        out: list[str] = []
        for el in list(soup.find_all(True)):
            if not isinstance(el, Tag) or el.attrs is None:
                continue
            if _types(el) & FOOTNOTE_TYPES or _role(el) in FOOTNOTE_ROLES:
                text = clean_text(el.get_text(" "))
                if text:
                    out.append(text)
                el.decompose()
        return out

    @staticmethod
    def _cover(book) -> bytes | None:
        import ebooklib

        meta = book.get_metadata("OPF", "cover")
        if meta:
            cid = meta[0][1].get("content") if len(meta[0]) > 1 else None
            item = book.get_item_with_id(cid) if cid else None
            if item is not None and item.get_type() in (ebooklib.ITEM_IMAGE, ebooklib.ITEM_COVER):
                return item.get_content()
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_COVER:
                return item.get_content()
            if "cover-image" in (getattr(item, "properties", []) or []):
                return item.get_content()
        for item in book.get_items_of_type(ebooklib.ITEM_IMAGE):
            if "cover" in item.get_name().lower():
                return item.get_content()
        return None
