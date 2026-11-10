"""Modellsúlyok letöltése a `<data_dir>/models` alá (12. fejezet, setup.ps1 (c) lépés).

Használat:  uv run python scripts/download_models.py [--only f5,piper,xtts,whisper] [--accept-cpml]

Az XTTS-v2 súlyai a Coqui Public Model License (CPML, nem kereskedelmi) alatt állnak;
a letöltéshez a `--accept-cpml` kapcsoló kell.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from huggingface_hub import hf_hub_download

from app.config import Config

F5_REPO = "sarpba/F5-TTS_V1_hun"
F5_CKPT = "model_965000.pt"
F5_EMA = "model_965000_ema.pt"
VOCOS_REPO = "charactr/vocos-mel-24khz"
PIPER_REPO = "rhasspy/piper-voices"
PIPER_VOICES = ["anna", "berta", "imre"]
XTTS_REPO = "coqui/XTTS-v2"
XTTS_FILES = ["config.json", "model.pth", "vocab.json", "speakers_xtts.pth"]
WHISPER_MODEL = "large-v3-turbo"

STRIP_EMA = """
import sys, torch
src, dst = sys.argv[1], sys.argv[2]
ck = torch.load(src, map_location="cpu", weights_only=False)
ema = ck.get("ema_model_state_dict") or ck
torch.save({"ema_model_state_dict": ema}, dst)
"""


def log(msg: str) -> None:
    print(msg, flush=True)


def download_f5(cfg: Config) -> None:
    out = cfg.engine_weights("f5_hu")
    out.mkdir(parents=True, exist_ok=True)
    hf_hub_download(F5_REPO, "vocab.txt", local_dir=out)
    if not (out / F5_EMA).exists():
        log(f"F5: {F5_REPO}/{F5_CKPT} letöltése (5,4 GB)...")
        full = Path(hf_hub_download(F5_REPO, F5_CKPT, local_dir=out))
        py = cfg.engine_python("f5_hu")
        if not py.exists():
            raise SystemExit("Az F5 worker környezete hiányzik (engines/f5/.venv). Futtasd előbb a setup.ps1-et.")
        log("F5: optimizer-állapot eltávolítása, csak az EMA súlyok maradnak...")
        subprocess.run([str(py), "-c", STRIP_EMA, str(full), str(out / F5_EMA)], check=True)
        full.unlink()
        shutil.rmtree(out / ".cache", ignore_errors=True)
    vocos = cfg.paths.models_dir / "vocos"
    for f in ("config.yaml", "pytorch_model.bin"):
        hf_hub_download(VOCOS_REPO, f, local_dir=vocos)
    log(f"F5: kész ({out})")


def download_piper(cfg: Config) -> None:
    out = cfg.engine_weights("piper_hu")
    out.mkdir(parents=True, exist_ok=True)
    for name in PIPER_VOICES:
        base = f"hu/hu_HU/{name}/medium/hu_HU-{name}-medium"
        for ext in (".onnx", ".onnx.json"):
            path = Path(hf_hub_download(PIPER_REPO, base + ext, local_dir=out / ".dl"))
            shutil.copyfile(path, out / f"hu_HU-{name}-medium{ext}")
    shutil.rmtree(out / ".dl", ignore_errors=True)
    log(f"Piper: kész ({out})")


def download_xtts(cfg: Config, accept: bool) -> None:
    if not accept:
        log("XTTS: kihagyva. A letöltéshez fogadd el a CPML licencet: --accept-cpml "
            "(https://coqui.ai/cpml.txt)")
        return
    out = cfg.engine_weights("xtts")
    out.mkdir(parents=True, exist_ok=True)
    for f in XTTS_FILES:
        hf_hub_download(XTTS_REPO, f, local_dir=out)
    (out / "CPML_ACCEPTED").write_text("A felhasználó elfogadta a Coqui Public Model License-et.\n",
                                       encoding="utf-8")
    shutil.rmtree(out / ".cache", ignore_errors=True)
    log(f"XTTS: kész ({out})")


def download_whisper(cfg: Config) -> None:
    from faster_whisper import download_model

    out = cfg.paths.models_dir / f"whisper-{WHISPER_MODEL}"
    download_model(WHISPER_MODEL, output_dir=str(out))
    log(f"Whisper: kész ({out})")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--only", default="piper,f5,xtts,whisper")
    p.add_argument("--accept-cpml", action="store_true")
    args = p.parse_args()
    cfg = Config.load()
    wanted = {x.strip() for x in args.only.split(",") if x.strip()}
    if "piper" in wanted:
        download_piper(cfg)
    if "f5" in wanted:
        download_f5(cfg)
    if "xtts" in wanted:
        download_xtts(cfg, args.accept_cpml)
    if "whisper" in wanted:
        download_whisper(cfg)


if __name__ == "__main__":
    main()
