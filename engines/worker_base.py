"""Közös JSON-RPC 2.0 ciklus a motor workereknek (6.4).

Minden worker a saját venv-jében fut, és ezt a fájlt `sys.path`-ra véve importálja.
A protokoll stdout-ja egy duplikált fájlleíró; az eredeti stdout a stderr-re irányul,
így a könyvtárak kiírásai nem rontják el a protokollt.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import traceback
import wave
from typing import Any

ERR_PARSE = -32700
ERR_METHOD = -32601
ERR_PARAMS = -32602
ERR_INTERNAL = -32603
ERR_OOM = -32001
ERR_WEIGHTS = -32002
ERR_VOICE = -32003


class RpcError(Exception):
    def __init__(self, code: int, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def log(*args: Any) -> None:
    print(*args, file=sys.stderr, flush=True)


def write_wav_int16(path: str, samples, sample_rate: int) -> float:
    """float [-1, 1] mintákból 16 bites mono WAV, atomikusan. Visszaadja a hosszt másodpercben."""
    import numpy as np

    arr = np.asarray(samples, dtype=np.float32).reshape(-1)
    arr = np.clip(arr, -1.0, 1.0)
    pcm = (arr * 32767.0).astype("<i2")
    tmp = path + ".tmp"
    with wave.open(tmp, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sample_rate)
        w.writeframes(pcm.tobytes())
    os.replace(tmp, path)
    return len(pcm) / float(sample_rate)


def base_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--weights", default="")
    p.add_argument("--models-dir", default="")
    p.add_argument("--device", default="")
    return p.parse_args()


def is_oom(exc: BaseException) -> bool:
    name = type(exc).__name__
    return "OutOfMemory" in name or "out of memory" in str(exc).lower()


class Worker:
    """Leszármazottak felülírják: info(), load_voice(), synthesize()."""

    def info(self) -> dict:
        raise NotImplementedError

    def load_voice(self, voice_id: str, ref_audio_path: str | None, ref_text: str | None,
                   params: dict) -> dict:
        return {"ok": True}

    def synthesize(self, chunk_id: str, text: str, voice_id: str, params: dict, out_path: str) -> dict:
        raise NotImplementedError


def serve(factory) -> None:
    proto_out = os.fdopen(os.dup(1), "w", encoding="utf-8", newline="\n")
    os.dup2(2, 1)
    sys.stdout = sys.stderr

    def send(obj: dict) -> None:
        proto_out.write(json.dumps(obj, ensure_ascii=False) + "\n")
        proto_out.flush()

    worker = None
    init_error: RpcError | None = None
    try:
        worker = factory()
    except RpcError as e:
        init_error = e
        log(f"Worker init hiba: {e.message}")
    except Exception as e:  # noqa: BLE001
        init_error = RpcError(ERR_WEIGHTS if isinstance(e, FileNotFoundError) else ERR_INTERNAL, str(e))
        log(traceback.format_exc())

    stdin = sys.stdin.buffer
    for raw in stdin:
        line = raw.decode("utf-8").strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except json.JSONDecodeError as e:
            send({"jsonrpc": "2.0", "id": None, "error": {"code": ERR_PARSE, "message": str(e)}})
            continue
        rid = req.get("id")
        method = req.get("method")
        params = req.get("params") or {}
        if method == "shutdown":
            send({"jsonrpc": "2.0", "id": rid, "result": {"ok": True}})
            break
        try:
            if init_error is not None:
                raise init_error
            if method == "info":
                result = worker.info()
            elif method == "load_voice":
                result = worker.load_voice(params["voice_id"], params.get("ref_audio_path"),
                                           params.get("ref_text"), params.get("params") or {})
            elif method == "synthesize":
                t0 = time.perf_counter()
                result = worker.synthesize(params["chunk_id"], params["text"], params.get("voice_id", ""),
                                           params.get("params") or {}, params["out_path"])
                elapsed = time.perf_counter() - t0
                dur = result.get("duration_s") or 0.0
                result.setdefault("rtf", elapsed / dur if dur > 0 else 0.0)
                result.setdefault("ok", True)
                result.setdefault("out_path", params["out_path"])
            else:
                raise RpcError(ERR_METHOD, f"Ismeretlen metódus: {method}")
            send({"jsonrpc": "2.0", "id": rid, "result": result})
        except RpcError as e:
            send({"jsonrpc": "2.0", "id": rid, "error": {"code": e.code, "message": e.message}})
        except KeyError as e:
            send({"jsonrpc": "2.0", "id": rid, "error": {"code": ERR_PARAMS, "message": f"Hiányzó paraméter: {e}"}})
        except Exception as e:  # noqa: BLE001
            log(traceback.format_exc())
            code = ERR_OOM if is_oom(e) else ERR_INTERNAL
            send({"jsonrpc": "2.0", "id": rid, "error": {"code": code, "message": str(e)}})
            if code == ERR_OOM:
                # OOM után a CUDA állapota bizonytalan: a manager újraindít
                break
    proto_out.flush()
