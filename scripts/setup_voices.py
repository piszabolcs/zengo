"""Alapértelmezett hangprofilok (12. fejezet, setup.ps1 (e) lépés).

A Piper hangokat az alkalmazás magától létrehozza. Referencia hang megadásakor egy minta F5 profil
(`f5-alap`) is készül, és ez lesz az alapértelmezett.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import soundfile as sf

from app.state import AppState


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--ref", default="")
    p.add_argument("--text", default="")
    args = p.parse_args()
    st = AppState()
    piper = [v["id"] for v in st.repo.list_voices() if v["engine_id"] == "piper_hu"]
    print("Piper hangok:", ", ".join(piper))
    if not args.ref:
        print('Minta F5 profilhoz add meg: -ReferenceWav <fajl.wav> -ReferenceText "<pontos atirat>"')
        return
    if not args.text.strip():
        sys.exit("A referencia hanghoz a pontos átirat is kell (-ReferenceText).")
    dur = sf.info(args.ref).duration
    if not 6 <= dur <= 30:
        sys.exit(f"A referencia {dur:.1f} s hosszú; 6 és 30 s között kell lennie (ajánlott 6-15 s).")
    dst = st.config.paths.voices_dir / "f5-alap.wav"
    shutil.copyfile(args.ref, dst)
    st.repo.upsert_voice("f5-alap", "F5 alap", "f5_hu", str(dst), args.text.strip(), {})
    st.config.update({"default_voice": "f5-alap"})
    print("Létrejött az f5-alap hangprofil, és ez lett az alapértelmezett.")


if __name__ == "__main__":
    main()
