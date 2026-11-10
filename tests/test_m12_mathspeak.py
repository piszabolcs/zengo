"""M12: szabályalapú magyar képletfelolvasás (app/prepare/mathspeak_hu.py, math_prose.py, math_doc.py)."""

import json
from pathlib import Path

import httpx
import pytest
from fastapi.testclient import TestClient

from app.ingest.registry import load_document
from app.jobs.runner import GpuGate
from app.main import create_app
from app.normalize.hu import Normalizer
from app.prepare.math_doc import accusative, prepare_markdown
from app.prepare.math_llm import LlmFallback, acceptable, build_prompt, examples, fallback_for
from app.prepare.math_prose import verbalize_prose
from app.prepare.math_report import report
from app.prepare.mathspeak_hu import Ctx, MathSpeakError, speak, speak_one, speak_unit
from app.prepare.rule_based import prepare
from app.state import AppState
from app.ttsmd.validator import validate_text
from tests.conftest import FIXTURES

MATH = FIXTURES / "math"
NOTE = MATH / "tanulashoz.md"
REFERENCE = MATH / "elektrodinamika-tanulashoz.tts.md"


def _golden() -> list[tuple[str, str]]:
    rows = []
    for line in (MATH / "golden_hu.tsv").read_text(encoding="utf-8").splitlines():
        if line and not line.startswith("#"):
            formula, expected = line.split("\t")
            rows.append((formula, expected))
    return rows


def _clean(text: str) -> bool:
    """A kimondott szöveg a validátor szerint figyelmeztetés nélküli (nincs számjegy, jel, LaTeX)."""
    script = f"---\nformat: ttsmd/1\ntitle: x\nlanguage: hu\n---\n\n# x\n\n{text}\n"
    _, rep = validate_text(script, Normalizer().normalize)
    return not rep.errors and not rep.warnings


GOLDEN = _golden()


def test_golden_set_size():
    assert len(GOLDEN) >= 60


@pytest.mark.parametrize(("formula", "expected"), GOLDEN, ids=[f[:40] for f, _ in GOLDEN])
def test_golden_formula(formula, expected):
    if expected == "MATH_SUSPECT":
        with pytest.raises(MathSpeakError):
            speak_one(formula)
        return
    spoken = speak_one(formula)
    assert spoken == expected
    assert _clean(spoken + ".")


@pytest.mark.parametrize(("formula", "expected"), [
    ("R = ρ·l/A", "er egyenlő ró szorozva el per á"),
    ("P = U²/R", "pé egyenlő ú négyzet per er"),
    ("f = 1/(2π√(LC))", "ef egyenlő egy per, zárójelben kettő pí szorozva négyzetgyök el cé"),
    (r"\sum_{k=1}^{n} I_k = 0", "szumma ká egyenlő egytől en-ig í ká egyenlő nulla"),
    (r"\lim_{x\to 0} \sin x / x = 1", "limesz iksz tart nullához, szinusz iksz per iksz egyenlő egy"),
    ("x⁻¹ + xⁿ", "iksz a mínusz egyediken plusz iksz az en-ediken"),
    (r"\int_a^b f\,dx", "integrál á-tól bé-ig, ef dé iksz"),
    ("∂f/∂x", "ef parciális iksz szerint"),
    (r"\frac{d^2x}{dt^2}", "dé négyzet iksz per dé té négyzet"),
    ("∇·E", "divergencia é"),
    ("∇×E", "rotáció é"),
    ("∇f", "gradiens ef"),
    ("|x| ≤ 3", "iksz abszolút értéke kisebb vagy egyenlő három"),
    ("8,85·10⁻¹²", "nyolc egész nyolcvanöt század szorozva tíz a mínusz tizenkettediken"),
    ("U(r) = kQ/r", "ú er-ben egyenlő ká szorozva kú per er"),
    (r"\varepsilon_r = 1+\kappa", "epszilon er egyenlő egy plusz kappa"),
    ("(ρ + ρ′)/ε₀", "egy tört, a számláló ró plusz ró vessző, a nevező epszilon nulla"),
])
def test_math_reading_rules(formula, expected):
    assert speak_one(formula) == expected


def test_case_context_and_unparsable():
    assert speak_one("q = Q", Ctx({"Q"})) == "kis kú egyenlő nagy kú"
    assert speak(r"\vec E = \frac{\vec F}{q} \qquad E = k\frac{Q}{r^2}") == [
        "é vektor egyenlő ef vektor per kú", "é egyenlő ká szorozva kú per er négyzet"]
    for bad in (r"\begin{pmatrix}a\end{pmatrix}", r"\unknowncmd x", "a ⊗ b", ""):
        with pytest.raises(MathSpeakError):
            speak_one(bad)


def test_units_and_accusative():
    assert speak_unit("N") == "{{newton|nyúton}}"
    assert speak_unit("V/m = N/C") == "volt per méter, ami egyenlő {{newton|nyúton}} per {{coulomb|kulomb}}"
    assert speak_unit("Vm/(As)") == "volt méter per amper szekundum"
    assert speak_unit("C/m³") == "{{coulomb|kulomb}} per köbméter"
    assert speak_unit("nincs") == "nincs"
    assert speak_unit("a mezőé") is None
    assert [accusative(w) for w in ("erő", "töltés", "térerősség", "indukció", "polarizációvektor",
                                    "felület", "momentuma")] == [
        "erőt", "töltést", "térerősséget", "indukciót", "polarizációvektort", "felületet", "momentumát"]


def test_prose_formulas():
    r = verbalize_prose("A próbatöltésre ható erő arányos a töltéssel (F = qE), a hányadosuk állandó. "
                        "Vákuumban κ = 0, a D-vonal sűrűsége ε-szeres.", Ctx(), [])
    assert r.text == ("A próbatöltésre ható erő arányos a töltéssel (ef egyenlő kú szorozva é), a hányadosuk "
                      "állandó. Vákuumban kappa egyenlő nulla, a D-vonal sűrűsége epszilon-szeres.")
    assert r.formulas == 3 and not r.suspects
    r = verbalize_prose("Itt $A = \\begin{pmatrix}1\\end{pmatrix}$ van.", Ctx(), [])
    assert r.formulas == 0  # helyőrző nélkül a $ szöveg marad: a dokumentum-szint dolgozza fel


def test_markdown_note_structure():
    md = ("# Jegyzet\n\n| Jel | Mit jelent | Mértékegység |\n| --- | --- | --- |\n| F | erő | N |\n"
          "| ε₀ | vákuum permittivitása, ≈ 8,85·10⁻¹² | As/(Vm) |\n\n"
          "**Térerősség.** A próbatöltésre ható erő (F = qE):\n\n```latex\nE = k\\frac{Q}{r^2}\n```\n\n"
          "**Mátrix.** Ezt nem érti:\n\n```latex\nA = \\begin{pmatrix}1 & 2\\end{pmatrix}\n```\n")
    text, warnings, st = prepare_markdown(md, "Jegyzet", "Ismeretlen", "jegyzet.md")
    script, rep = validate_text(text, Normalizer().normalize)
    assert rep.errors == []
    assert [w.message for w in rep.warnings] == ["Képletgyanús blokk (MATH_SUSPECT): ellenőrizd a felolvasást."]
    assert "## Jelölések" in text and "## Térerősség" in text and "## Mátrix" in text
    assert "Az ef jel az erőt jelenti, mértékegysége a {{newton|nyúton}}." in text
    assert ("Az epszilon nulla jel a vákuum permittivitását jelenti, értéke közelítőleg nyolc egész nyolcvanöt "
            "század szorozva tíz a mínusz tizenkettediken, mértékegysége amper szekundum per volt méter. "
            "[[pause 500]]") in text
    assert "É egyenlő ká szorozva nagy kú per er négyzet. [[pause 500]]" in text  # q is szerepel
    assert "<!-- eredeti\n**Térerősség.** A próbatöltésre ható erő (F = qE):\n\n```latex" in text
    assert text.count("<!-- MATH_SUSPECT -->") == 1
    assert st.formulas == 6 and st.spoken == 5 and len(st.suspects) == 1
    assert any("1 képletgyanús blokk" in w for w in warnings)
    # az eredeti a következő blokkhoz tartozik (olvasónézet)
    assert any(b.original and "Térerősség" in b.original for b in script.blocks)


def test_tanulashoz_coverage_against_reference():
    """Teljes jegyzet: 0 validátorhiba, csak MATH_SUSPECT figyelmeztetés, lefedettség és referencia-egyezés."""
    r = report(NOTE.read_text(encoding="utf-8"), REFERENCE.read_text(encoding="utf-8"), "tanulashoz.md")
    assert r["errors"] == 0
    assert r["other_warnings"] == []
    assert r["formulas"] > 900
    assert r["coverage"] >= 0.99
    assert len(r["suspects"]) <= 5
    assert r["compared_parts"] >= 100 and r["similarity"] >= 0.75
    text = r["script"]
    assert "# Első rész. Első. Elektromos alapmennyiségek" in text
    assert text.count("<!-- eredeti") > 300
    assert "A nagy ef jel az erőt jelenti" in text


def test_ui_import_of_formula_note(config):
    st = AppState(config)
    st.repo.upsert_voice("dummy-test", "Dummy", "dummy", None, None, {})
    with TestClient(create_app(st, start_queue=False)) as client:
        r = client.post("/api/projects", files={"file": ("tanulashoz.md", NOTE.read_bytes(), "text/markdown")})
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["report"]["errors"] == []
        project = st.repo.get_project(body["project"]["id"])
        text = st.repo.read_script(project)
        assert "[[pause 500]]" in text and "<!-- eredeti" in text
        assert any("képlet, ebből" in w for w in project["warnings"])


def _docx_with_math(path: Path) -> Path:
    import docx
    from docx.oxml import parse_xml

    d = docx.Document()
    d.add_heading("Ellenállás", level=1)
    p = d.add_paragraph()
    run = p.add_run("Fajlagos ellenállás.")
    run.bold = True
    p.add_run(" Az ellenállás képlete:")
    m = ('<m:oMathPara xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
         '<m:oMath><m:r><m:t>R=</m:t></m:r><m:r><m:t>ρ</m:t></m:r><m:f><m:num><m:r><m:t>l</m:t></m:r>'
         '</m:num><m:den><m:r><m:t>A</m:t></m:r></m:den></m:f></m:oMath></m:oMathPara>')
    para = d.add_paragraph()
    para._p.append(parse_xml(m))
    d.add_paragraph("Szövegben is: ")._p.append(parse_xml(
        '<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
        '<m:sSup><m:e><m:r><m:t>U</m:t></m:r></m:e><m:sup><m:r><m:t>2</m:t></m:r></m:sup></m:sSup>'
        '<m:r><m:t>/R</m:t></m:r></m:oMath>'))
    t = d.add_table(rows=2, cols=3)
    for i, c in enumerate(("Jel", "Mit jelent", "Mértékegység")):
        t.cell(0, i).text = c
    for i, c in enumerate(("R", "ellenállás", "Ω")):
        t.cell(1, i).text = c
    d.save(str(path))
    return path


def test_docx_with_omml(tmp_path):
    doc = load_document(_docx_with_math(tmp_path / "jegyzet.docx"))
    text, warnings = prepare(doc)
    _, rep = validate_text(text, Normalizer().normalize)
    assert rep.errors == [] and rep.warnings == [], rep.warnings
    assert "## Fajlagos ellenállás" in text
    assert "Er egyenlő ró szorozva el per á. [[pause 500]]" in text
    assert "ú négyzet per er" in text
    assert "Az er jel az ellenállást jelenti, mértékegysége a óm." in text or "ellenállást jelenti" in text
    assert any("képlet, ebből" in w for w in warnings)


def test_plain_markdown_keeps_old_path():
    from app.ingest.base import Block, Document

    doc = Document(title="Regény", source_path="nincs.md", blocks=[Block(id="1", type="paragraph", text="Szia.")])
    text, warnings = prepare(doc)
    assert "<!-- eredeti" not in text and warnings == []


# --- helyi nyelvi modell tartalék ---

def _transport(answer: str, calls: list):
    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(json.loads(request.content))
        return httpx.Response(200, json={"response": answer})
    return httpx.MockTransport(handler)


def test_llm_prompt_and_validation():
    shots = examples()
    assert ("R = ρ·l/A", "az R ellenállás egyenlő ró szorozva l per A") in shots
    prompt = build_prompt("x ⊗ y", shots)
    assert prompt.endswith("Képlet: x ⊗ y\nFelolvasás:")
    assert acceptable("iksz tenzorszorozva ipszilon")
    assert not acceptable("x ⊗ y")
    assert not acceptable("iksz egyenlő 3")


def test_llm_fallback_accepts_only_clean_answers():
    calls: list = []
    ok = LlmFallback({"enabled": True}, None, httpx.Client(transport=_transport(
        "<think>...</think>Felolvasás: iksz tenzorszorozva ipszilon", calls)))
    assert ok("x ⊗ y") == "iksz tenzorszorozva ipszilon"
    assert calls[0]["model"] == "qwen3:8b" and calls[0]["stream"] is False
    bad = LlmFallback({"enabled": True}, None, httpx.Client(transport=_transport("x ⊗ y = 2", [])))
    assert bad("x ⊗ y") is None
    md = "# K\n\nA szorzat: $x \\otimes y$ itt.\n"
    text, _, st = prepare_markdown(md, "K", "I", "k.md", fallback=ok)
    assert st.llm == 1 and "iksz tenzorszorozva ipszilon" in text and "MATH_SUSPECT" not in text
    text, _, st = prepare_markdown(md, "K", "I", "k.md", fallback=bad)
    assert st.llm == 0 and "<!-- MATH_SUSPECT -->" in text


def test_llm_waits_for_gpu_and_is_off_by_default(config):
    assert fallback_for(config) is None
    gate = GpuGate()
    calls: list = []
    fb = LlmFallback({"enabled": True}, gate, httpx.Client(transport=_transport("iksz", calls)))
    with gate.gpu_job():
        assert gate.gpu_busy
        assert fb("x ⊗ y") is None
    assert fb.skipped_gpu == 1 and calls == []
    assert not gate.gpu_busy
    with gate.gpu_job(active=False):
        assert not gate.gpu_busy
    assert fb("x ⊗ y") == "iksz" and len(calls) == 1


def test_llm_unreachable_server_degrades(config):
    def boom(request):
        raise httpx.ConnectError("nincs szerver")
    fb = LlmFallback({"enabled": True, "max_formulas": 5}, None, httpx.Client(transport=httpx.MockTransport(boom)))
    assert fb("x ⊗ y") is None
    assert fb("x ⊗ y") is None and fb.calls == 5  # az első hiba után nem próbálkozik tovább
