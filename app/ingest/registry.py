"""Kiterjesztés alapján választ importert (L1-08)."""

from __future__ import annotations

from pathlib import Path

from app.ingest.base import Document, Importer, ImportError
from app.ingest.docx import DocxImporter
from app.ingest.epub import EpubImporter
from app.ingest.markdown import MarkdownImporter
from app.ingest.pdf import PdfImporter

IMPORTERS: list[Importer] = [PdfImporter(), DocxImporter(), EpubImporter(), MarkdownImporter()]


def importer_for(path: Path) -> Importer:
    for imp in IMPORTERS:
        if imp.can_handle(path):
            return imp
    raise ImportError(f"Nem támogatott formátum: {path.name}. Támogatott: PDF, DOCX, EPUB, Markdown, .tts.md.")


def load_document(path: Path) -> Document:
    return importer_for(Path(path)).load(Path(path))
