"""F5-TTS worker magyar finomhangolt súlyokkal (sarpba/F5-TTS_V1_hun, F5TTS_v1_Base), CUDA (L4-04)."""

import hashlib
import os
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prosody import STRONG, split_segments
from worker_base import ERR_VOICE, ERR_WEIGHTS, RpcError, Worker, base_args, log, serve, write_wav_int16

CKPT_NAMES = ("model_965000_ema.pt", "model_965000.pt")
MODEL_CONFIG = "F5TTS_v1_Base"
HOP = 256
TARGET_RMS = 0.1
PEAK_LIMIT = 0.95
HIGHPASS_HZ = 70.0  # ez alatt nincs beszéd, csak búgás és dörej; a modell a referenciából ezt is lemásolná
# Az F5 a megadott hosszt tölti ki beszéddel; kis ráhagyás nélkül az utolsó szótag a puffer végén szakad el,
# túl sok ráhagyásnál viszont elnyújtja a végét.
DURATION_PAD_S = 0.15
# Egy generálás legfeljebb ennyi karakter (~10 s beszéd). A referenciával együtt a modell kb. 30 s-os hosszon
# tanult; a 300 karakteres chunk egyben generálva ennek a közelébe ér, és a vége felé zajossá, reszelőssé
# válik. Rövidebbre (minden mondatra külön) bontva viszont minden mondatvégnél hallható a varrat, ezért
# mondathatáron bontunk, de a rövid mondatokat egy generálásba fogjuk.
GEN_MAX_CHARS = 160
# Az F5 mindig a megadott hossz legvégéig beszél (több időnél csak lassabban), így a generálás utolsó hangja
# a puffer szélén elszakad ("pakk"). A mondat belsejében lévő pontnál viszont 120-340 ms lecsengő szünetet
# tart. Ezért minden generálás végére egy eldobható zárószót teszünk, a valódi vég mondatközi pontként szól,
# és a zárószót az előtte lévő szünetben levágjuk.
TAIL_FILLER = "... igen."  # 30 próbából 30-nál tiszta szünet előtte ("igen." magában: 28)


def check_gpu(torch) -> str:
    if not torch.cuda.is_available():
        log("FIGYELEM: CUDA nem érhető el, az F5 CPU-n fut (nagyon lassú).")
        return "cpu"
    cap = torch.cuda.get_device_capability(0)
    arch = f"sm_{cap[0]}{cap[1]}"
    if arch not in torch.cuda.get_arch_list():
        raise RpcError(ERR_WEIGHTS, f"A PyTorch build nem támogatja a GPU-t ({arch}); cu128 build kell.")
    return "cuda"


class F5Worker(Worker):
    def __init__(self, weights: str, models_dir: str):
        from importlib.resources import files

        import torch
        from f5_tts.infer.utils_infer import load_model, load_vocoder
        from f5_tts.model import DiT
        from omegaconf import OmegaConf

        self.torch = torch
        wdir = Path(weights)
        ckpt = next((wdir / n for n in CKPT_NAMES if (wdir / n).exists()), None)
        vocab = wdir / "vocab.txt"
        if ckpt is None or not vocab.exists():
            raise RpcError(ERR_WEIGHTS, f"Hiányzó F5 súlyok itt: {wdir}. "
                                        "Futtasd: uv run python scripts/download_models.py --only f5")
        vocos_dir = Path(models_dir) / "vocos"
        if not (vocos_dir / "pytorch_model.bin").exists():
            raise RpcError(ERR_WEIGHTS, f"Hiányzó vocos vokóder: {vocos_dir}")
        self.device = check_gpu(torch)
        cfg = OmegaConf.load(str(files("f5_tts").joinpath(f"configs/{MODEL_CONFIG}.yaml")))
        self.vocoder = load_vocoder(vocoder_name="vocos", is_local=True, local_path=str(vocos_dir),
                                    device=self.device)
        self.model = load_model(DiT, cfg.model.arch, str(ckpt), mel_spec_type="vocos", vocab_file=str(vocab),
                                device=self.device)
        self.sample_rate = int(cfg.model.mel_spec.target_sample_rate)
        self.voices: dict[str, tuple] = {}
        try:
            from importlib.metadata import version

            self.version = version("f5-tts")
        except Exception:
            self.version = "1.1"
        log(f"F5 betöltve: {ckpt.name}, eszköz: {self.device}")

    def info(self) -> dict:
        return {"engine_id": "f5_hu", "version": self.version, "sample_rate": self.sample_rate, "max_chars": 300,
                "device": self.device, "supports_reference_audio": True}

    def load_voice(self, voice_id, ref_audio_path, ref_text, params):
        from f5_tts.infer.utils_infer import preprocess_ref_audio_text

        if not ref_audio_path or not Path(ref_audio_path).exists():
            raise RpcError(ERR_VOICE, "Az F5 hangprofilhoz referencia hangminta kell.")
        if not (ref_text or "").strip():
            raise RpcError(ERR_VOICE, "Az F5 hangprofilhoz a referencia átirata is kell.")
        import torchaudio

        audio_path, text = preprocess_ref_audio_text(ref_audio_path, ref_text.lower(), show_info=log)
        audio, sr = torchaudio.load(audio_path)
        if audio.shape[0] > 1:
            audio = audio.mean(dim=0, keepdim=True)
        audio = _highpass(audio, sr)
        rms = float(audio.square().mean().sqrt())
        # mindkét irányba normálunk: a túl hangos (túlvezérelt) referenciát a modell hangerővel és
        # recsegéssel együtt másolja, ezért azt is a célszintre vesszük le
        audio = audio * TARGET_RMS / max(rms, 1e-6)
        if sr != self.sample_rate:
            audio = torchaudio.transforms.Resample(sr, self.sample_rate)(audio)
        if len(text[-1].encode("utf-8")) == 1:
            text += " "
        self.voices[voice_id] = (audio.to(self.device), text, rms)
        return {"ok": True}

    def _seed(self, seed: int) -> None:
        import numpy as np

        random.seed(seed)
        np.random.seed(seed % (2**32))
        self.torch.manual_seed(seed)
        if self.device == "cuda":
            self.torch.cuda.manual_seed_all(seed)

    def _generate(self, voice_id: str, texts: list[str], params: dict) -> list:
        """Szegmensek generálása egyenként ugyanazzal a referenciával.

        Kötegelni nem érdemes: a GPU egy szegmensnél is telítve van, és a torch-os figyelem a kitöltést
        nem maszkolja, így kötegben a rövidebb szegmensek hangja eltorzul.
        """
        from f5_tts.infer.utils_infer import convert_char_to_pinyin

        torch = self.torch
        audio, ref_text, rms = self.voices[voice_id]
        ref_len = audio.shape[-1] // HOP
        ref_bytes = len(ref_text.encode("utf-8"))
        speed = float(params.get("speed", 1.0))
        pad = int(float(params.get("duration_pad_s", DURATION_PAD_S)) * self.sample_rate / HOP)
        out = []
        for text in texts:
            duration = ref_len + int(ref_len / ref_bytes * len(text.encode("utf-8")) / speed) + pad
            with torch.inference_mode():
                mel, _ = self.model.sample(
                    cond=audio, text=convert_char_to_pinyin([ref_text + text]), duration=duration,
                    steps=int(params.get("nfe_step", 32)), cfg_strength=float(params.get("cfg_strength", 2.0)),
                    sway_sampling_coef=-1,
                )
                wave = self.vocoder.decode(mel.to(torch.float32)[:, ref_len:, :].permute(0, 2, 1))
                wave = _highpass(wave, self.sample_rate)
                if rms < TARGET_RMS:
                    wave = wave * rms / TARGET_RMS
                out.append(wave.squeeze().cpu().numpy())
        return out

    def synthesize(self, chunk_id, text, voice_id, params, out_path):
        import numpy as np

        if voice_id not in self.voices:
            raise RpcError(ERR_VOICE, f"A hang nincs betöltve: {voice_id}")
        # A magyar finomhangolás kisbetűs szövegen tanult: a nagybetűs szókezdet (mondat eleje, "É", "J",
        # "A") félreejtett első hangot ad ("Értéke" -> "Örtéke"), az "Ő" / "Ű" pedig hiányzik a szótárból.
        text = text.lower()
        segments = _groups(text, int(params.get("gen_max_chars", GEN_MAX_CHARS)))
        seed = int(params.get("seed", 0))
        # chunkonként determinisztikus, de chunkonként eltérő seed
        self._seed(seed + int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:8], 16))
        filler = str(params.get("tail_filler", TAIL_FILLER))
        sr = self.sample_rate
        if filler:
            audio_ref, ref_text, _ = self.voices[voice_id]
            sec_per_byte = audio_ref.shape[-1] / sr / len(ref_text.encode("utf-8")) / float(params.get("speed", 1.0))
            filler_s = sec_per_byte * len((" " + filler).encode("utf-8"))
            waves = self._generate(voice_id, [_with_filler(t, filler) for t, _ in segments], params)
            waves = [_cut_filler(w, sr, filler_s) for w in waves]
        else:
            waves = self._generate(voice_id, [t for t, _ in segments], params)
        parts = []
        for (_, pause), wave in zip(segments, waves):
            parts.append(_trim(wave, sr))
            if pause > 0:
                parts.append(np.zeros(int(sr * pause), dtype=np.float32))
        audio = np.concatenate(parts)
        peak = float(np.abs(audio).max()) if audio.size else 0.0
        if peak > PEAK_LIMIT:  # int16-ba írva a csúcs levágódna (recsegés)
            audio = audio * (PEAK_LIMIT / peak)
        dur = write_wav_int16(out_path, audio, sr)
        return {"ok": True, "out_path": out_path, "duration_s": dur}


def _groups(text: str, max_chars: int) -> list[tuple[str, float]]:
    """(szöveg, utána tartandó szünet) párok: mondathatáron bontva, a rövid mondatok `max_chars`-ig egyben.

    A csoporton belüli írásjeleknél a modell maga tart szünetet. Csak a `max_chars`-nál hosszabb mondatot
    bontjuk tovább vesszőnél / zárójelnél / gondolatjelnél.
    """
    if len(text) <= max_chars:
        return [(text, 0.0)]
    parts: list[tuple[str, float]] = []
    for seg, pause in split_segments(text, STRONG):
        if len(seg) > max_chars:
            sub = split_segments(seg, frozenset({"comma", "paren", "dash"}))
            parts += sub[:-1] + [(sub[-1][0], pause)]  # a mondat végi szünet az utolsó darab után jön
        else:
            parts.append((seg, pause))
    out: list[list] = []
    for seg, pause in parts:
        if out and len(out[-1][0]) + 1 + len(seg) <= max_chars:
            out[-1][0] += " " + seg
            out[-1][1] = pause
        else:
            out.append([seg, pause])
    out[-1][1] = 0.0
    return [(t, p) for t, p in out]


def _with_filler(text: str, filler: str) -> str:
    """A szöveg ponttal lezárva (a kettőspont, vessző után nem tart szünetet a modell), utána a zárószó."""
    body = re.sub(r"[\s:;,\-–]+$", "", text)
    if not body:
        return text
    if body[-1] not in ".!?":
        body += "."
    return f"{body} {filler}"


def _cut_filler(wave, sr: int, filler_s: float, fade_s: float = 0.06):
    """A zárószó levágása: a várt helye előtti leghosszabb csendes szakaszban vágunk, a lecsengést megtartva.

    Csendes az a 10 ms-os ablak, amely 30 dB-lel a beszédszint alatt van. Ha ilyen nincs (a modell nem tartott
    szünetet), a keresőablak leghalkabb pontján vágunk.
    """
    import numpy as np

    wave = np.asarray(wave, dtype=np.float32)
    win = max(1, int(sr * 0.01))
    n = wave.size // win
    if n < 20:
        return wave
    env = np.sqrt(np.mean(wave[: n * win].reshape(n, win) ** 2, axis=1))
    voiced = env > env.max() * 0.1
    if not voiced.any():
        return wave
    speech = float(np.median(env[voiced]))
    filler_f = int(filler_s * 100)
    first = int(np.argmax(voiced))
    lo = max(first + 20, n - filler_f - 80)
    hi = n - max(3, int(filler_f * 0.3))
    if hi - lo < 4:
        return wave
    quiet = env < speech * 10 ** (-30 / 20)
    best, j = None, lo
    while j < hi:
        if quiet[j]:
            k = j
            while k < hi and quiet[k]:
                k += 1
            if k - j >= 4 and (best is None or k - j >= best[1] - best[0]):
                best = (j, k)
            j = k
        else:
            j += 1
    if best:
        cut = (best[0] + min(8, (best[1] - best[0]) // 2)) * win
    else:  # nincs szünet: a leghalkabb ponton, hosszabb elhalkulással
        smooth = np.convolve(env, np.ones(3) / 3, mode="same")
        cut = (lo + int(np.argmin(smooth[lo:hi]))) * win
        fade_s = max(fade_s, 0.15)
    out = wave[:cut].copy()
    f = min(int(sr * fade_s), out.size // 2)
    if f > 0:
        out[-f:] *= (0.5 + 0.5 * np.cos(np.linspace(0.0, np.pi, f))).astype(np.float32)
    return out


def _highpass(audio, sr: int):
    """Másodfokú felüláteresztő kétszer egymás után (24 dB/oktáv) a hálózati búgás és a dörej ellen."""
    from torchaudio.functional import highpass_biquad

    return highpass_biquad(highpass_biquad(audio, sr, HIGHPASS_HZ), sr, HIGHPASS_HZ)


def _trim(wave, sr: int, head_s: float = 0.03, tail_s: float = 0.15, fade_in_s: float = 0.008,
          fade_out_s: float = 0.1):
    """Eleji/végi csend levágása (a szünetet mi tesszük be).

    A szó vége halkan cseng le (zöngétlen mássalhangzó, kifújás); ha ezt éles határon vágjuk és digitális
    csend jön utána, a hang "elvágottnak" hat. Ezért a végén -40 dB-ig a beszédhez számítjuk, utána még
    `tail_s` lecsengést hagyunk, és azon koszinuszos elhalkulással érünk el a csendig.
    """
    import numpy as np

    wave = np.asarray(wave, dtype=np.float32)
    if wave.size == 0:
        return wave
    win = max(1, int(sr * 0.01))
    n = wave.size // win
    if n == 0:
        return wave
    env = np.sqrt(np.mean(wave[: n * win].reshape(n, win) ** 2, axis=1))
    loud = np.nonzero(env > max(env.max() * 0.01, 1e-4))[0]  # ~ -40 dB a csúcshoz
    if loud.size:
        wave = wave[max(0, loud[0] * win - int(sr * head_s)):
                    min(wave.size, (loud[-1] + 1) * win + int(sr * tail_s))].copy()
    f = min(int(sr * fade_in_s), wave.size // 2)
    if f > 0:
        wave[:f] *= np.linspace(0.0, 1.0, f, dtype=np.float32)
    f = min(int(sr * fade_out_s), wave.size // 2)
    if f > 0:
        wave[-f:] *= (0.5 + 0.5 * np.cos(np.linspace(0.0, np.pi, f))).astype(np.float32)
    return wave


if __name__ == "__main__":
    args = base_args()
    serve(lambda: F5Worker(args.weights, args.models_dir))
