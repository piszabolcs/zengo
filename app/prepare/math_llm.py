"""Opcionális tartalék: helyi nyelvi modell (Ollama vagy llama.cpp szerver) egyetlen képlethez.

Csak a szabályalapú olvasó által nem értett képletet kapja meg, néhány példával a
`math-reading-hu.md` szabályaiból. A választ csak akkor fogadjuk el, ha a validátor szerint tiszta
(nincs számjegy, matematikai jel, LaTeX); különben a képlet `MATH_SUSPECT` marad. GPU-s TTS feladat
közben nem fut, és amíg fut, a TTS a két chunk között vár (`GpuGate`).
"""

from __future__ import annotations

import logging
import re
from pathlib import Path

import httpx

from app.config import REPO_ROOT
from app.normalize.hu import Normalizer
from app.ttsmd.validator import validate_text

log = logging.getLogger(__name__)

RULES_FILE = REPO_ROOT / "claude-skill" / "felolvaso-elokeszito" / "references" / "math-reading-hu.md"
FALLBACK_EXAMPLES = [
    ("R = ρ·l/A", "er egyenlő ró szorozva el per á"),
    ("P = U²/R", "pé egyenlő ú négyzet per er"),
    ("f = 1/(2π√(LC))", "ef egyenlő egy per, zárójelben kettő pí szorozva négyzetgyök el cé"),
    ("Σ_{k=1}^{n} I_k = 0", "szumma ká egyenlő egytől en-ig í ká egyenlő nulla"),
]
ALLOWED_RE = re.compile(r"^[a-záéíóöőúüűA-ZÁÉÍÓÖŐÚÜŰ ,\-]{3,400}$")


def examples(path: Path = RULES_FILE) -> list[tuple[str, str]]:
    """A szabályfájl "Példák" táblázata (képlet, felolvasás) párokként."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return FALLBACK_EXAMPLES
    part = text.split("## Példák", 1)[-1]
    out = []
    for m in re.finditer(r"^\|\s*`([^`]+)`\s*\|\s*([^|]+?)\s*\|\s*$", part, re.MULTILINE):
        out.append((m.group(1), m.group(2)))
    return out or FALLBACK_EXAMPLES


def build_prompt(formula: str, shots: list[tuple[str, str]]) -> str:
    lines = [
        "Írd át a képletet egyetlen magyar felolvasható kifejezéssé, ahogy egy tanár hangosan mondaná.",
        "Szabályok: számok betűvel, betűk betűnévvel (á, bé, cé, ef, ká, kú, er, iksz), görög betűk névvel",
        "(alfa, epszilon, ró), = egyenlő, + plusz, − mínusz, · szorozva, / per, x² x négyzet,",
        "összetett tört: egy tört, a számláló …, a nevező …. Ne használj számjegyet, jelet, LaTeX-et.",
        "Csak a felolvasást írd, magyarázat nélkül.",
        "",
    ]
    for f, s in shots:
        lines += [f"Képlet: {f}", f"Felolvasás: {s}", ""]
    lines += [f"Képlet: {formula}", "Felolvasás:"]
    return "\n".join(lines)


def clean_answer(text: str) -> str:
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    text = text.strip().splitlines()[0] if text.strip() else ""
    text = re.sub(r"^(Felolvasás|Válasz)\s*:\s*", "", text).strip().strip('"„”').rstrip(".")
    return text


def acceptable(text: str) -> bool:
    """Csak a validátor szerint figyelmeztetés nélküli, tisztán szöveges választ fogadjuk el."""
    if not ALLOWED_RE.match(text):
        return False
    script = f"---\nformat: ttsmd/1\ntitle: x\nlanguage: hu\n---\n\n# x\n\n{text}.\n"
    _, report = validate_text(script, Normalizer().normalize)
    return not report.errors and not report.warnings


class LlmFallback:
    """Hívható: képlet -> kimondott alak vagy None."""

    def __init__(self, cfg: dict, gate=None, client: httpx.Client | None = None):
        self.cfg = cfg
        self.gate = gate
        self.client = client
        self.shots = examples()
        self.calls = 0
        self.skipped_gpu = 0

    def __call__(self, formula: str) -> str | None:
        if self.calls >= int(self.cfg.get("max_formulas", 40)):
            return None
        if self.gate is not None and self.gate.gpu_busy:
            self.skipped_gpu += 1
            return None
        self.calls += 1
        prompt = build_prompt(formula, self.shots)
        try:
            if self.gate is not None:
                with self.gate.priority():  # a futó TTS a két chunk között vár
                    answer = self._ask(prompt)
            else:
                answer = self._ask(prompt)
        except (httpx.HTTPError, ValueError, KeyError) as e:
            log.warning("Helyi nyelvi modell nem érhető el: %s", e)
            self.calls = int(self.cfg.get("max_formulas", 40))  # többet nem próbálunk ebben az importban
            return None
        text = clean_answer(answer)
        if acceptable(text):
            return text
        log.info("Elvetett modellválasz (%s): %r", formula, text)
        return None

    def _ask(self, prompt: str) -> str:
        url = str(self.cfg.get("url", "http://127.0.0.1:11434")).rstrip("/")
        timeout = float(self.cfg.get("timeout_s", 60))
        client = self.client or httpx.Client(timeout=timeout)
        try:
            if self.cfg.get("provider", "ollama") == "ollama":
                r = client.post(f"{url}/api/generate", json={
                    "model": self.cfg.get("model", "qwen3:8b"), "prompt": prompt + " /no_think", "stream": False,
                    "options": {"temperature": 0, "num_predict": 200}})
                r.raise_for_status()
                return r.json()["response"]
            # llama.cpp szerver (OpenAI-kompatibilis végpont)
            r = client.post(f"{url}/v1/chat/completions", json={
                "model": self.cfg.get("model", ""), "temperature": 0, "max_tokens": 200,
                "messages": [{"role": "user", "content": prompt}]})
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
        finally:
            if self.client is None:
                client.close()


def fallback_for(config, gate=None) -> LlmFallback | None:
    cfg = config.get("math_llm") or {}
    if not cfg.get("enabled"):
        return None
    return LlmFallback(cfg, gate)
