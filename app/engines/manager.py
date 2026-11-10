"""Worker folyamatok életciklusa: indítás, időkorlát, újraindítás, egy GPU worker szabály (L4-02)."""

from __future__ import annotations

import itertools
import json
import logging
import queue
import subprocess
import sys
import threading
from pathlib import Path
from typing import Any

from app.config import Config
from app.engines.protocol import (
    EngineCrashed,
    EngineError,
    EngineInfo,
    EngineTimeout,
    SynthesizeResult,
)

log = logging.getLogger(__name__)

DEFAULT_TIMEOUT_S = 120.0
STARTUP_TIMEOUT_S = 600.0  # modellbetöltés + első futás CUDA kernel fordítással


class WorkerProcess:
    """Egy futó worker. Egyszerre egy kérést szolgál ki (zár)."""

    def __init__(self, engine_id: str, cmd: list[str], cwd: Path, log_path: Path, env: dict | None = None):
        self.engine_id = engine_id
        self.cmd = cmd
        self.cwd = cwd
        self.log_path = log_path
        self.env = env
        self.lock = threading.RLock()
        self._ids = itertools.count(1)
        self._responses: queue.Queue = queue.Queue()
        self.proc: subprocess.Popen | None = None
        self.info: EngineInfo | None = None
        self.loaded_voices: dict[str, str] = {}  # voice_id -> profil ujjlenyomat

    def start(self) -> None:
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self._log_file = open(self.log_path, "ab")
        flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        self.proc = subprocess.Popen(
            self.cmd, cwd=self.cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=self._log_file, env=self.env, creationflags=flags,
        )
        self._responses = queue.Queue()
        t = threading.Thread(target=self._reader, args=(self.proc, self._responses), daemon=True)
        t.start()
        self.loaded_voices.clear()

    @staticmethod
    def _reader(proc: subprocess.Popen, out: queue.Queue) -> None:
        assert proc.stdout is not None
        for raw in proc.stdout:
            try:
                out.put(json.loads(raw.decode("utf-8")))
            except (json.JSONDecodeError, UnicodeDecodeError):
                log.warning("Érvénytelen worker kimenet: %r", raw[:200])
        out.put(None)  # EOF

    @property
    def alive(self) -> bool:
        return self.proc is not None and self.proc.poll() is None

    def call(self, method: str, params: dict | None = None, timeout: float = DEFAULT_TIMEOUT_S) -> Any:
        with self.lock:
            if not self.alive:
                raise EngineCrashed()
            rid = next(self._ids)
            msg = json.dumps({"jsonrpc": "2.0", "id": rid, "method": method, "params": params or {}},
                             ensure_ascii=False) + "\n"
            try:
                assert self.proc and self.proc.stdin
                self.proc.stdin.write(msg.encode("utf-8"))
                self.proc.stdin.flush()
            except OSError as e:
                raise EngineCrashed(f"Nem sikerült üzenetet küldeni a motornak: {e}") from e
            while True:
                try:
                    resp = self._responses.get(timeout=timeout)
                except queue.Empty:
                    self.kill()
                    raise EngineTimeout(f"A motor ({self.engine_id}) {timeout:.0f} s alatt nem válaszolt.") from None
                if resp is None:
                    raise EngineCrashed(f"A motor ({self.engine_id}) folyamata leállt.")
                if resp.get("id") != rid:
                    continue
                if "error" in resp:
                    err = resp["error"]
                    raise EngineError(int(err.get("code", -32603)), str(err.get("message", "")))
                return resp.get("result")

    def shutdown(self, timeout: float = 10.0) -> None:
        if not self.alive:
            self._close_log()
            return
        try:
            with self.lock:
                assert self.proc and self.proc.stdin
                self.proc.stdin.write(b'{"jsonrpc":"2.0","id":0,"method":"shutdown"}\n')
                self.proc.stdin.flush()
                self.proc.wait(timeout=timeout)
        except Exception:  # noqa: BLE001
            self.kill()
        self._close_log()

    def kill(self) -> None:
        if self.proc is not None and self.proc.poll() is None:
            self.proc.kill()
            try:
                self.proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                pass

    def _close_log(self) -> None:
        f = getattr(self, "_log_file", None)
        if f and not f.closed:
            f.close()


class EngineManager:
    """Workerek kezelése. Legfeljebb egy GPU-s worker van betöltve egyszerre."""

    def __init__(self, config: Config):
        self.config = config
        self.workers: dict[str, WorkerProcess] = {}
        self.lock = threading.RLock()
        self.timeout_s = DEFAULT_TIMEOUT_S

    def _command(self, engine_id: str) -> tuple[list[str], Path]:
        engine_dir = self.config.engine_dir(engine_id)
        py = self.config.engine_python(engine_id)
        if not py.exists():
            if engine_id == "dummy":
                py = Path(sys.executable)
            else:
                raise EngineError(-32002, f"A(z) {engine_id} motor nincs telepítve (hiányzik: {py}). "
                                          "Futtasd a setup.ps1-et.")
        weights = self.config.engine_weights(engine_id)
        cmd = [str(py), "-u", str(engine_dir / "worker.py"), "--weights", str(weights),
               "--models-dir", str(self.config.paths.models_dir)]
        return cmd, engine_dir

    def get(self, engine_id: str) -> WorkerProcess:
        with self.lock:
            w = self.workers.get(engine_id)
            if w is not None and w.alive:
                return w
            if self.config.engine_is_gpu(engine_id):
                for other_id, other in list(self.workers.items()):
                    if other_id != engine_id and self.config.engine_is_gpu(other_id):
                        log.info("GPU motor váltás: %s leállítása", other_id)
                        other.shutdown()
                        del self.workers[other_id]
            cmd, cwd = self._command(engine_id)
            w = WorkerProcess(engine_id, cmd, cwd, self.config.paths.logs_dir / f"engine-{engine_id}.log")
            log.info("Worker indítása: %s", " ".join(cmd))
            w.start()
            try:
                w.info = EngineInfo.model_validate(w.call("info", timeout=STARTUP_TIMEOUT_S))
            except EngineError:
                w.kill()
                raise
            self.workers[engine_id] = w
            return w

    def info(self, engine_id: str) -> EngineInfo:
        w = self.get(engine_id)
        assert w.info is not None
        return w.info

    def restart(self, engine_id: str) -> WorkerProcess:
        with self.lock:
            w = self.workers.pop(engine_id, None)
            if w is not None:
                w.kill()
                w._close_log()
            return self.get(engine_id)

    def ensure_voice(self, w: WorkerProcess, voice: dict) -> None:
        fingerprint = json.dumps([voice.get("ref_audio_path"), voice.get("ref_text"), voice.get("params")],
                                 sort_keys=True, ensure_ascii=False)
        if w.loaded_voices.get(voice["id"]) == fingerprint:
            return
        w.call("load_voice", {"voice_id": voice["id"], "ref_audio_path": voice.get("ref_audio_path"),
                              "ref_text": voice.get("ref_text"), "params": voice.get("params") or {}},
               timeout=STARTUP_TIMEOUT_S)
        w.loaded_voices[voice["id"]] = fingerprint

    def synthesize(self, engine_id: str, voice: dict, chunk_id: str, text: str, params: dict,
                   out_path: Path, timeout: float | None = None) -> SynthesizeResult:
        """Egy chunk generálása. Hiba esetén a worker állapota rendbe kerül, a kivétel továbbmegy."""
        w = self.get(engine_id)
        try:
            self.ensure_voice(w, voice)
            res = w.call("synthesize", {"chunk_id": chunk_id, "text": text, "voice_id": voice["id"],
                                        "params": params, "out_path": str(out_path)},
                         timeout=timeout or self.timeout_s)
            return SynthesizeResult.model_validate(res)
        except EngineError as e:
            if isinstance(e, (EngineTimeout, EngineCrashed)) or e.is_oom:
                log.warning("Motor hiba (%s), újraindítás: %s", engine_id, e)
                with self.lock:
                    self.workers.pop(engine_id, None)
                w.kill()
                w._close_log()
            raise

    def shutdown_all(self) -> None:
        with self.lock:
            for w in self.workers.values():
                w.shutdown()
            self.workers.clear()
