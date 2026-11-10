import re
import zipfile

from app.normalize.hu import normalize
from app.ttsmd.validator import validate_text
from scripts.package_skill import SKILL_DIR, package

REFS = SKILL_DIR / "references"


def test_math_reading_covers_every_symbol():
    """L10-01: a 6.10 / 5. pont minden szimbóluma szerepel."""
    text = (REFS / "math-reading-hu.md").read_text(encoding="utf-8")
    for sym in ["=", "≈", "≠", "<", "≤", "+", "-", "·", "×", "a/b", "x²", "x³", "xⁿ", "√x", "x_i", "Δx", "dx/dt",
                "∂f/∂x", "∫ f dx", "∫_a^b", "∮", "∬_A", "Σ_{i=1}^{n}", "lim_{x→0}", "∞", "|x|", "∇·E", "∇×E", "E·dA"]:
        assert sym in text, sym
    for word in ["ró", "epszilon", "mű", "fí", "omega", "nagy omega", "U nulla", "I be", "R ki", "számláló",
                 "zárójelben", "E vektor"]:
        assert word in text, word
    assert (REFS / "ttsmd-format.md").read_text(encoding="utf-8").startswith("# Felolvasási forgatókönyv")


def test_examples_validate_without_warnings():
    """L10-02: az öt példa forgatókönyve hiba és figyelmeztetés nélkül átmegy a validátoron."""
    md = (REFS / "examples.md").read_text(encoding="utf-8")
    scripts = re.findall(r"```text\n(.*?)```", md, re.DOTALL)
    assert len(scripts) == 5
    for s in scripts:
        _, report = validate_text(s, normalize)
        assert report.errors == [] and report.warnings == [], (s[:80], report)
    assert "az R ellenállás egyenlő ró szorozva l per A" in scripts[0]


def test_skill_frontmatter_and_zip(tmp_path):
    """L10-03: a zip a SKILL.md-t a gyökérben tartalmazza."""
    skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert skill.startswith("---\nname: felolvaso-elokeszito\ndescription: ")
    out = package(tmp_path / "skill.zip")
    names = zipfile.ZipFile(out).namelist()
    assert "SKILL.md" in names
    assert {"references/ttsmd-format.md", "references/math-reading-hu.md", "references/examples.md"} <= set(names)
