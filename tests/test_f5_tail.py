"""F5 worker: eldobható zárószó és levágása (a generálás végi "pakk" ellen)."""

import importlib.util
import sys
from pathlib import Path

import numpy as np

ENGINES = Path(__file__).resolve().parents[1] / "engines"
sys.path.insert(0, str(ENGINES))
_spec = importlib.util.spec_from_file_location("f5_worker_under_test", ENGINES / "f5" / "worker.py")
W = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(W)

SR = 24000


def tone(seconds: float, amp: float = 0.2) -> np.ndarray:
    t = np.arange(int(SR * seconds)) / SR
    return (amp * np.sin(2 * np.pi * 180 * t)).astype(np.float32)


def test_with_filler_closes_with_period():
    assert W._with_filler("ezért:", "... igen.") == "ezért. ... igen."
    assert W._with_filler("a teret, ", "... igen.") == "a teret. ... igen."
    assert W._with_filler("miért?", "... igen.") == "miért? ... igen."
    assert W._with_filler("nabla e", "... igen.") == "nabla e. ... igen."
    assert W._with_filler(" ", "... igen.") == " "


def test_cut_filler_cuts_in_the_pause_and_fades():
    speech, pause, filler = tone(2.0), np.zeros(int(SR * 0.25), np.float32), tone(0.45)
    out = W._cut_filler(np.concatenate([speech, pause, filler]), SR, filler_s=0.45)
    # a beszéd megmarad, a zárószó nem; a vágás a szünetben van
    assert len(speech) <= out.size <= len(speech) + len(pause)
    assert abs(out[-1]) < 1e-4


def test_cut_filler_without_pause_still_drops_filler():
    x = np.concatenate([tone(2.0), tone(0.1, 0.002), tone(0.45)])  # csak egy rövid halk pont
    out = W._cut_filler(x, SR, filler_s=0.45)
    assert out.size < x.size - int(SR * 0.3)
    assert abs(out[-1]) < 1e-4


def test_cut_filler_leaves_short_audio_alone():
    x = tone(0.1)
    assert W._cut_filler(x, SR, filler_s=0.45).size == x.size
