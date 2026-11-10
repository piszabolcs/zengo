"""A forgatókönyvhöz és a tagoláshoz tartozó pydantic modellek (8.2)."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class Issue(BaseModel):
    line: int
    message: str


class ValidationReport(BaseModel):
    errors: list[Issue] = Field(default_factory=list)
    warnings: list[Issue] = Field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


ScriptBlockKind = Literal["chapter", "h2", "h3", "paragraph", "list_item"]


class ScriptBlock(BaseModel):
    """A forgatókönyv egy blokkja: cím, bekezdés vagy listaelem.

    A bekezdés szövege tartalmazhat `[[pause N]]` direktívát és `{{írott|kiejtés}}` jelölést,
    ezeket a normalizáló és a tagoló értelmezi. Az `original` az előtte álló
    `<!-- eredeti ... -->` megjegyzés tartalma (a felhasználó eredeti szövege, az olvasónézethez).
    """

    id: str
    kind: ScriptBlockKind
    text: str
    line: int
    end_line: int
    chapter_index: int
    original: str | None = None


class Script(BaseModel):
    front_matter: dict[str, Any] = Field(default_factory=dict)
    blocks: list[ScriptBlock] = Field(default_factory=list)
    math_suspect_lines: list[int] = Field(default_factory=list)

    @property
    def title(self) -> str:
        return str(self.front_matter.get("title", ""))

    def chapters(self) -> list[ScriptBlock]:
        return [b for b in self.blocks if b.kind == "chapter"]


class Chunk(BaseModel):
    chunk_id: str
    chapter_index: int
    block_id: str
    seq: int
    text: str
    pause_after_ms: int


class ChapterPlan(BaseModel):
    index: int
    title: str
    chunks: list[Chunk] = Field(default_factory=list)


class ChunkPlan(BaseModel):
    chapters: list[ChapterPlan] = Field(default_factory=list)

    def all_chunks(self) -> list[Chunk]:
        return [c for ch in self.chapters for c in ch.chunks]
