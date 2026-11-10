import tomllib

import pytest

from app.config import Config, Paths
from app.engines.manager import EngineManager
from app.engines.protocol import EngineCrashed, EngineError, EngineTimeout
from app.storage.db import Database
from app.ttsmd.validator import validate_text

VALID = """---
format: ttsmd/1
title: Villamosságtan jegyzet
author: Ismeretlen
language: hu
source: elektro_jegyzet.pdf
voice: f5-alap            # opcionális, hangprofil id
symbols:                   # opcionális
  R: er, ellenállás
  rho: ró, fajlagos ellenállás
---

# Első tétel. Az ellenállás

## A fajlagos ellenállás

Az R ellenállás egyenlő ró szorozva l per A. [[pause 500]]
Ahol l a vezeték hossza, A pedig a keresztmetszete.

{{Kirchhoff|kirhhoff}} első törvénye szerint ennyi.

<!-- megjegyzés, nem olvasódik fel -->

- első elem
- második elem
"""


# --- L7-01 konfiguráció ---

def test_config_first_start_creates_dirs(tmp_path):
    paths = Paths(tmp_path / "c", tmp_path / "d")
    cfg = Config.load(paths)
    assert paths.config_file.exists()
    for d in (paths.projects_dir, paths.cache_dir, paths.logs_dir, paths.models_dir, paths.voices_dir):
        assert d.is_dir()
    data = tomllib.loads(paths.config_file.read_text(encoding="utf-8"))
    assert data["pauses"]["sentence"] == 350
    assert cfg["qa"]["device"] == "cpu"


def test_config_persists_changes(tmp_path):
    paths = Paths(tmp_path / "c", tmp_path / "d")
    Config.load(paths).update({"export": {"speed": 1.2}})
    cfg = Config.load(paths)
    assert cfg["export"]["speed"] == 1.2
    assert cfg["export"]["formats"] == ["mp3", "m4b"]


# --- L7-02 SQLite ---

def test_db_schema_created_and_idempotent(tmp_path):
    db = Database(tmp_path / "x.db")
    tables = {r["name"] for r in db.query("SELECT name FROM sqlite_master WHERE type='table'")}
    assert {"projects", "voices", "jobs", "chunks", "cache_entries", "lexicon", "schema_version"} <= tables
    assert db.one("PRAGMA journal_mode")[0] == "wal"
    before = db.query("SELECT * FROM schema_version")
    assert db.migrate() == 1
    assert len(db.query("SELECT * FROM schema_version")) == len(before) == 1


# --- L3-01 parser és validátor ---

def test_valid_script_parses():
    script, report = validate_text(VALID)
    assert report.errors == []
    assert script.front_matter["symbols"]["R"] == "er, ellenállás"
    assert script.front_matter["voice"] == "f5-alap"
    kinds = [b.kind for b in script.blocks]
    assert kinds == ["chapter", "h2", "paragraph", "paragraph", "list_item", "list_item"]
    para = script.blocks[2]
    assert "[[pause 500]]" in para.text and para.text.endswith("keresztmetszete.")
    assert script.blocks[4].text == "első elem"


def test_crlf_accepted():
    _, report = validate_text(VALID.replace("\n", "\r\n"))
    assert report.errors == []


@pytest.mark.parametrize("text,needle", [
    ("# Cím\n\nSzöveg.", "Hiányzó front matter"),
    ("---\nformat: ttsmd/2\ntitle: X\nlanguage: hu\n---\n# A\n", "Ismeretlen formátum"),
    ("---\nformat: ttsmd/1\nlanguage: hu\n---\n# A\n", "title"),
    ("---\nformat: ttsmd/1\ntitle: X\nlanguage: hu\n---\nCsak szöveg.\n", "Nincs egyetlen # fejezet"),
    ("---\nformat: ttsmd/1\ntitle: X\nlanguage: hu\n---\n# A\n\nSzöveg [[speed 2]].\n", "Ismeretlen direktíva"),
    ("---\nformat: ttsmd/1\ntitle: X\nlanguage: hu\n---\n# A\n\nSzöveg {{abc|def.\n", "Lezáratlan {{"),
    ("---\nformat: ttsmd/1\ntitle: X\nlanguage: hu\n---\n# A\n\n#### Mély\n", "Túl mély"),
    ("---\nformat: ttsmd/1\ntitle: X\nlanguage: hu\n---\n# A\n\nX [[pause 20000]]\n", "0 és 10000"),
])
def test_invalid_scripts(text, needle):
    _, report = validate_text(text)
    assert any(needle in e.message for e in report.errors), report.errors


def test_error_line_numbers():
    text = "---\nformat: ttsmd/1\ntitle: X\nlanguage: hu\n---\n# A\n\nJó.\n\nRossz [[foo]].\n"
    _, report = validate_text(text)
    assert report.errors[0].line == 10


def test_warnings_math_suspect_and_symbols():
    text = ("---\nformat: ttsmd/1\ntitle: X\nlanguage: hu\n---\n# A\n\n<!-- MATH_SUSPECT -->\n"
            "Az R = ρ·l/A képlet \\frac{a}{b}.\n")
    _, report = validate_text(text)
    msgs = " ".join(w.message for w in report.warnings)
    assert report.errors == []
    assert "MATH_SUSPECT" in msgs and "LaTeX" in msgs and "Matematikai" in msgs
    assert report.warnings[0].line == 8


# --- L4-01, L4-02 dummy motor és manager ---

VOICE = {"id": "dummy-test", "ref_audio_path": None, "ref_text": None, "params": {}}


def test_dummy_info_and_synthesize(config, tmp_path):
    m = EngineManager(config)
    try:
        info = m.info("dummy")
        assert info.engine_id == "dummy" and info.sample_rate == 24000
        out = tmp_path / "a.wav"
        res = m.synthesize("dummy", VOICE, "c1", "Helló világ, ez egy teszt.", {}, out)
        assert out.exists() and res.duration_s > 1.0
    finally:
        m.shutdown_all()


def test_manager_restarts_killed_worker(config, tmp_path):
    m = EngineManager(config)
    try:
        w1 = m.get("dummy")
        w1.kill()
        w2 = m.get("dummy")
        assert w2 is not w1 and w2.alive
        res = m.synthesize("dummy", VOICE, "c2", "Újra működik.", {}, tmp_path / "b.wav")
        assert res.ok
    finally:
        m.shutdown_all()


def test_manager_timeout_and_crash(config, tmp_path):
    m = EngineManager(config)
    try:
        with pytest.raises(EngineTimeout):
            m.synthesize("dummy", VOICE, "c3", "HANGTESZT", {}, tmp_path / "c.wav", timeout=2)
        with pytest.raises(EngineCrashed):
            m.synthesize("dummy", VOICE, "c4", "CRASHTESZT", {}, tmp_path / "d.wav", timeout=10)
        with pytest.raises(EngineError) as ei:
            m.synthesize("dummy", VOICE, "c5", "OOMTESZT", {}, tmp_path / "e.wav")
        assert ei.value.is_oom
        assert m.synthesize("dummy", VOICE, "c6", "Rendben.", {}, tmp_path / "f.wav").ok
    finally:
        m.shutdown_all()
