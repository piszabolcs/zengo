"""Közös `Document` modell és `Importer` protokoll (6.1, 8.2, L1-01)."""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path
from typing import Literal, Protocol

from pydantic import BaseModel, Field

BlockType = Literal["heading", "paragraph", "footnote", "figure"]

MATH_FONT_HINTS = ("Math", "Symbol", "CMMI", "CMSY", "Cambria Math")
MATH_CHAR_RE = re.compile("[∀-⋿Α-Ωα-ω\U0001d400-\U0001d7ff]")
NORMAL_PUNCT = set(".,;:!?…-–—()[]\"'„“”«»‘’/%&§")


class ImportError(Exception):
    """A fájl nem nyitható meg (jelszavas, sérült, ismeretlen formátum)."""


class Block(BaseModel):
    id: str
    type: BlockType
    level: int | None = None
    text: str
    page: int | None = None
    math_suspect: bool = False


class Document(BaseModel):
    title: str
    author: str | None = None
    source_path: str
    blocks: list[Block] = Field(default_factory=list)
    cover_image: bytes | None = None
    warnings: list[str] = Field(default_factory=list)


class Importer(Protocol):
    def can_handle(self, path: Path) -> bool: ...

    def load(self, path: Path) -> Document: ...


class BlockBuilder:
    """Egyedi azonosítójú blokkok gyűjtése."""

    def __init__(self) -> None:
        self.blocks: list[Block] = []

    def add(self, type_: BlockType, text: str, level: int | None = None, page: int | None = None,
            math_suspect: bool = False) -> Block | None:
        text = clean_text(text)
        if not text and type_ != "figure":
            return None
        b = Block(id=f"b{len(self.blocks) + 1}", type=type_, level=level if type_ == "heading" else None,
                  text=text, page=page, math_suspect=math_suspect or (type_ != "figure" and is_math_text(text)))
        self.blocks.append(b)
        return b


def clean_text(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    text = text.replace("­", "").replace("ﬁ", "fi").replace("ﬂ", "fl")
    return re.sub(r"\s+", " ", text).strip()


def is_math_text(text: str) -> bool:
    """Képletgyanú: >15% nem betű/szám/írásjel karakter, vagy matematikai Unicode karakter."""
    if not text:
        return False
    if MATH_CHAR_RE.search(text) or "$" in text and re.search(r"\$[^$]+\$", text):
        return True
    chars = [c for c in text if not c.isspace()]
    if len(chars) < 4:
        return False
    odd = sum(1 for c in chars if not (c.isalnum() or c in NORMAL_PUNCT))
    return odd / len(chars) > 0.15


def is_math_font(name: str) -> bool:
    return any(h.lower() in (name or "").lower() for h in MATH_FONT_HINTS)


def title_from_filename(path: Path) -> str:
    name = path.name
    for suffix in (".tts.md", ".markdown", ".md", ".pdf", ".docx", ".epub"):
        if name.lower().endswith(suffix):
            name = name[: -len(suffix)]
            break
    return re.sub(r"[_]+", " ", name).strip() or "Névtelen"
