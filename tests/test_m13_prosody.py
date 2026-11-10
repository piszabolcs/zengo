"""Prozódia: mondatonkénti szegmensek (F5 worker) és utólagos szünetek vesszőnél, zárójelnél, tört előtt."""

import sys

import numpy as np
import soundfile as sf

from app.audio.pauses import insert_pauses, pause_points
from app.config import REPO_ROOT

sys.path.insert(0, str(REPO_ROOT / "engines"))
from prosody import STRONG, split_segments


def test_strong_segments_split_sentences_and_colon_only():
    segs = split_segments("a tér csökken (kétszer messzebb), mert a vonalak szétoszlanak. potenciál: fi egyenlő.",
                          STRONG)
    assert [t for t, _ in segs] == ["a tér csökken (kétszer messzebb), mert a vonalak szétoszlanak.",
                                    "potenciál:", "fi egyenlő."]
    assert segs[0][1] > segs[1][1] > 0 and segs[-1][1] == 0.0


def test_short_strong_segment_is_merged():
    segs = split_segments("na. ez egy hosszabb mondat a végén.", STRONG)
    assert len(segs) == 1


def test_all_kinds_split_and_short_commas_merge():
    segs = split_segments("a, b, c és d: a kappa jel jelenti (mennyire polarizálható), mértékegysége nincs.")
    texts = [t for t, _ in segs]
    assert texts[0] == "a, b, c és d:"
    assert "mennyire polarizálható," in texts


def test_pause_points_kinds():
    words, points = pause_points("A tér egy per er négyzet szerint csökken (kétszer messzebb), mert így van, látod")
    by_word = {words[i]: (p, k) for i, p, k in points}
    assert by_word["tér"][1] == "fraction"
    assert by_word["csökken"][1] == "paren"
    assert by_word["messzebb"][1] in ("paren", "comma")
    assert by_word["van"][1] == "comma"


def _tone(sec: float, sr: int) -> np.ndarray:
    t = np.arange(int(sec * sr)) / sr
    return (0.3 * np.sin(2 * np.pi * 220 * t)).astype(np.float32)


def test_insert_pauses_at_quiet_comma(tmp_path):
    sr = 24000
    # "első szó, második szó": a vessző helyén 40 ms-os rés van, ezt 180 ms-ra kell nyújtani
    audio = np.concatenate([_tone(0.6, sr), np.zeros(int(0.04 * sr), np.float32), _tone(0.6, sr)])
    wav = tmp_path / "a.wav"
    sf.write(wav, audio, sr, subtype="PCM_16")
    words = [("első", 0.0, 0.3), ("szó", 0.3, 0.6), ("második", 0.64, 0.95), ("szó", 0.95, 1.24)]
    assert insert_pauses(wav, "első szó, második szó", words) == 1
    assert abs(sf.info(str(wav)).duration - (len(audio) / sr + 0.14)) < 0.02


def test_no_cut_without_quiet_gap_or_alignment(tmp_path):
    sr = 24000
    audio = _tone(1.2, sr)  # nincs csendes pont a vesszőnél
    wav = tmp_path / "b.wav"
    sf.write(wav, audio, sr, subtype="PCM_16")
    words = [("első", 0.0, 0.3), ("szó", 0.3, 0.6), ("második", 0.6, 0.9), ("szó", 0.9, 1.2)]
    assert insert_pauses(wav, "első szó, második szó", words) == 0
    # eltérő felismerés: nem vágunk
    assert insert_pauses(wav, "első szó, második szó", [("valami", 0.0, 1.2)]) == 0
