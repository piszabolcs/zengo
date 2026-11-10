"""A Claude skill csomagolása claude.ai-ra feltölthető zip-be (L10-03).

Használat:  uv run python scripts/package_skill.py [kimeneti.zip]
A `references/ttsmd-format.md` mindig a `docs/ttsmd-format.md` aktuális másolata lesz.
"""

from __future__ import annotations

import shutil
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO / "claude-skill" / "felolvaso-elokeszito"


def package(out: Path) -> Path:
    shutil.copyfile(REPO / "docs" / "ttsmd-format.md", SKILL_DIR / "references" / "ttsmd-format.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(SKILL_DIR.rglob("*")):
            if f.is_file():
                # a SKILL.md a zip gyökerébe kerül
                z.write(f, f.relative_to(SKILL_DIR).as_posix())
    return out


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO / "dist" / "felolvaso-elokeszito.zip"
    print(package(target))
