"""Generálási ciklus: ChunkPlan -> motor -> QA -> gyorsítótár -> export (L7-04, 6.4, 6.5, 6.6)."""

from __future__ import annotations

import contextlib
import logging
import shutil
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

import numpy as np
import soundfile as sf

from app.audio.assemble import ChunkAudio, build_chapter, loudnorm
from app.audio.export_m4b import export_m4b, m4b_name
from app.audio.export_mp3 import book_mp3_name, export_mp3, export_mp3_book, mp3_name
from app.audio.ffmpeg import Ffmpeg
from app.audio.pauses import insert_pauses
from app.engines.protocol import DEFAULT_MAX_CHARS, EngineCrashed, EngineError, EngineTimeout
from app.normalize.chunker import Chunker, ChunkSettings, _split_long, split_sentences
from app.reader.timing import save_chapter_timing
from app.reader.view import chapter_block_sig
from app.storage.repo import sanitize_filename
from app.ttsmd.models import Chunk, ChunkPlan, Script
from app.ttsmd.validator import validate_text

if TYPE_CHECKING:
    from app.state import AppState

log = logging.getLogger(__name__)

QA_MAX_RETRIES = 2
SOFT_PAUSE_CUTS = False  # utólagos szünetbeszúrás vesszőnél / zárójelnél (lásd generate_chunk)


class JobStopped(Exception):
    def __init__(self, status: str, message: str | None = None):
        super().__init__(message or status)
        self.status = status
        self.message = message


class ChunkFailed(Exception):
    pass


@dataclass
class Control:
    stop: str | None = None  # "pause" | "cancel"


@dataclass
class Progress:
    phase: str = "queued"
    total_chars: int = 0
    done_chars: int = 0
    audio_s: float = 0.0
    synth_s: float = 0.0
    started: float = field(default_factory=time.time)
    eta_s: float | None = None
    wall_s: float = 0.0
    current_text: str = ""


class GpuGate:
    """Az előhallgatás a futó feladat két chunkja között kap sort (NFR-04)."""

    def __init__(self) -> None:
        self.cond = threading.Condition()
        self.pending = 0
        self.gpu_jobs = 0  # futó GPU-s TTS feladatok: közben a helyi nyelvi modell nem indulhat

    @contextlib.contextmanager
    def gpu_job(self, active: bool = True):
        if not active:
            yield
            return
        with self.cond:
            self.gpu_jobs += 1
        try:
            yield
        finally:
            with self.cond:
                self.gpu_jobs -= 1
                self.cond.notify_all()

    @property
    def gpu_busy(self) -> bool:
        return self.gpu_jobs > 0

    @contextlib.contextmanager
    def priority(self):
        with self.cond:
            self.pending += 1
        try:
            yield
        finally:
            with self.cond:
                self.pending -= 1
                self.cond.notify_all()

    def wait_turn(self) -> None:
        with self.cond:
            while self.pending > 0:
                self.cond.wait(timeout=1.0)


def project_cover(project_dir: Path, script: Script | None = None) -> Path | None:
    if script is not None and script.front_matter.get("cover"):
        p = (project_dir / str(script.front_matter["cover"])).resolve()
        if p.is_relative_to(project_dir.resolve()) and p.exists():
            return p
    for ext in ("jpg", "jpeg", "png"):
        p = project_dir / f"cover.{ext}"
        if p.exists():
            return p
    return None


class JobRunner:
    def __init__(self, state: AppState):
        self.state = state
        self.progress: dict[str, Progress] = {}

    # --- terv ---
    def resolve_voice(self, project: dict) -> dict:
        repo = self.state.repo
        voice = repo.get_voice(project["settings"].get("voice_id") or "") or repo.get_voice(
            self.state.config["default_voice"])
        if voice is None:
            raise JobStopped("failed", "Nincs érvényes hangprofil a projekthez.")
        return voice

    def engine_params(self, voice: dict, project: dict) -> dict:
        return {**voice["params"], "seed": int(project["settings"].get("seed", 0))}

    def max_chars(self, engine_id: str) -> int:
        try:
            return self.state.manager.info(engine_id).max_chars
        except EngineError:
            return DEFAULT_MAX_CHARS.get(engine_id, 200)

    def make_chunker(self, project: dict, voice: dict) -> Chunker:
        s = project["settings"]
        settings = ChunkSettings(
            engine_id=voice["engine_id"], voice_id=voice["id"], engine_params=self.engine_params(voice, project),
            max_chars=self.max_chars(voice["engine_id"]), pauses=s.get("pauses") or {},
            announce_chapters=bool(s.get("announce_chapters", True)),
        )
        return Chunker(settings, self.state.repo.lexicon_entries())

    def plan_for(self, project: dict, chapters) -> tuple[Script, ChunkPlan, dict, Chunker]:
        text = self.state.repo.read_script(project)
        script, report = validate_text(text)
        if report.errors:
            msg = "; ".join(f"{e.line}. sor: {e.message}" for e in report.errors[:5])
            raise JobStopped("failed", f"A forgatókönyv hibás: {msg}")
        voice = self.resolve_voice(project)
        chunker = self.make_chunker(project, voice)
        wanted = None if chapters in (None, "all") else [int(c) for c in chapters]
        return script, chunker.plan(script, wanted), voice, chunker

    # --- egy chunk generálása ---
    def _synth_raw(self, voice: dict, chunk_id: str, text: str, params: dict, out: Path, depth: int = 0) -> float:
        """Motor hívás időkorlát- és OOM-kezeléssel. Visszaadja a generálás idejét."""
        mgr = self.state.manager
        engine_id = voice["engine_id"]
        t0 = time.perf_counter()
        for attempt in range(2):
            try:
                mgr.synthesize(engine_id, voice, chunk_id, text, params, out)
                return time.perf_counter() - t0
            except EngineTimeout as e:
                log.warning("Időtúllépés (%s), %d. próba: %s", chunk_id[:10], attempt + 1, e)
                if attempt == 1:
                    raise ChunkFailed(str(e)) from e
            except EngineCrashed as e:
                raise JobStopped("paused", f"A motor összeomlott: {e.message}") from e
            except EngineError as e:
                if e.is_oom and depth < 3:
                    return self._synth_split(voice, chunk_id, text, params, out, depth)
                raise ChunkFailed(e.message) from e
        raise ChunkFailed("ismeretlen hiba")

    def _synth_split(self, voice: dict, chunk_id: str, text: str, params: dict, out: Path, depth: int) -> float:
        """CUDA OOM: a chunk mondathatár mentén ketté vágva, a két fél hangja egy fájlba fűzve."""
        sentences = split_sentences(text)
        if len(sentences) >= 2:
            mid = len(sentences) // 2
            halves = [" ".join(sentences[:mid]), " ".join(sentences[mid:])]
        else:
            pieces = _split_long(text, max(10, len(text) // 2 + 1))
            if len(pieces) < 2:
                raise ChunkFailed("CUDA memóriahiány, a chunk nem bontható tovább.")
            mid = len(pieces) // 2
            halves = [" ".join(pieces[:mid]), " ".join(pieces[mid:])]
        log.info("OOM: chunk kettévágva (%s)", chunk_id[:10])
        elapsed = 0.0
        arrays = []
        sr = 24000
        for i, half in enumerate(halves):
            part = out.with_name(f"{out.stem}.h{depth}{i}.wav")
            elapsed += self._synth_raw(voice, f"{chunk_id}-{depth}{i}", half, params, part, depth + 1)
            data, sr = sf.read(str(part), dtype="float32")
            arrays.append(data)
            part.unlink(missing_ok=True)
        gap = np.zeros(int(sr * 0.25), dtype=np.float32)
        sf.write(str(out), np.concatenate([arrays[0], gap, arrays[1]]), sr, subtype="PCM_16")
        return elapsed

    def generate_chunk(self, voice: dict, chunk: Chunk, base_params: dict, qa_enabled: bool,
                       work_dir: Path) -> dict:
        """Generálás + QA ciklus. Visszaadja a chunk rekord mezőit."""
        qa = self.state.qa if qa_enabled else None
        candidates: list[tuple[float, Path, float, float, list]] = []  # (wer, path, duration, synth_s, szavak)
        attempts = 0
        qa_ok = False
        for attempt in range(QA_MAX_RETRIES + 1):
            attempts += 1
            params = dict(base_params)
            if attempt:
                params["seed"] = int(base_params.get("seed", 0)) + 7919 * attempt
            out = work_dir / f"{chunk.chunk_id}.a{attempt}.wav"
            synth_s = self._synth_raw(voice, chunk.chunk_id, chunk.text, params, out)
            duration = sf.info(str(out)).duration
            if qa is None:
                candidates.append((0.0, out, duration, synth_s, []))
                break
            result = qa.check(out, chunk.text, duration)
            candidates.append((result.wer, out, duration, synth_s, result.words))
            if result.ok:
                qa_ok = True
                break
        # siker esetén az utolsó (jó) változat marad, különben a legkisebb WER-ű
        best = candidates[-1] if qa is None or qa_ok else min(candidates, key=lambda c: c[0])
        qa_warning = qa is not None and not qa_ok
        # Vesszőnél, zárójelnél és tört előtt korábban utólag csendet vágtunk a hangba; a vágás a szóvég
        # lecsengésébe is belekapott, és minden ilyen helyen elvágottnak hatott a beszéd. Az egyben generált
        # szöveg szünetei elég természetesek, ezért ez ki van kapcsolva.
        if SOFT_PAUSE_CUTS and best[4] and insert_pauses(best[1], chunk.text, best[4]):
            best = (best[0], best[1], sf.info(str(best[1])).duration, best[3], best[4])
        self.state.cache.put(chunk.chunk_id, best[1])
        for c in candidates:
            c[1].unlink(missing_ok=True)
        total_synth = sum(c[3] for c in candidates)
        return {"attempts": attempts, "wer": best[0] if qa is not None else None,
                "qa_warning": int(bool(qa_warning)), "duration_s": best[2],
                "rtf": total_synth / best[2] if best[2] > 0 else None, "synth_s": total_synth}

    # --- feladat ---
    def run(self, job_id: str, control: Control) -> None:
        st = self.state
        repo = st.repo
        job = repo.get_job(job_id)
        assert job is not None
        project = repo.get_project(job["project_id"])
        if project is None:
            raise JobStopped("failed", "A projekt nem létezik.")
        req = job["request"]
        prog = self.progress.setdefault(job_id, Progress())
        prog.phase = "planning"
        script, plan, voice, _ = self.plan_for(project, req.get("chapters", "all"))
        chunks = plan.all_chunks()
        if not chunks:
            raise JobStopped("failed", "A kiválasztott fejezetekben nincs felolvasható szöveg.")
        base_params = self.engine_params(voice, project)
        qa_enabled = bool(project["settings"].get("qa_enabled", True)) and st.qa is not None

        # chunk rekordok újraépítése: a kész állapot forrása a gyorsítótár (folytatás, módosított forgatókönyv)
        old = {(r["chapter_index"], r["seq"], r["chunk_id"]): r for r in repo.job_chunks(job_id)}
        rows = []
        for c in chunks:
            prev = old.get((c.chapter_index, c.seq, c.chunk_id))
            done = st.cache.has(c.chunk_id)
            rows.append((job_id, c.chunk_id, c.chapter_index, c.seq, "done" if done else "pending",
                         prev["attempts"] if prev else 0, prev["wer"] if prev else None,
                         prev["qa_warning"] if prev else 0, prev["duration_s"] if prev else None,
                         prev["rtf"] if prev else None))
        with st.db.write_lock:
            c_ = st.db.conn()
            c_.execute("DELETE FROM chunks WHERE job_id = ?", (job_id,))
            c_.executemany("INSERT INTO chunks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", rows)
            c_.commit()
        done_count = sum(1 for r in rows if r[4] == "done")
        repo.set_job(job_id, total_chunks=len(chunks), done_chunks=done_count, error=None)

        prog.total_chars = sum(len(c.text) for c in chunks)
        prog.done_chars = sum(len(c.text) for c, r in zip(chunks, rows) if r[4] == "done")
        prog.phase = "generating"
        work_dir = st.config.paths.tmp_dir / job_id
        work_dir.mkdir(parents=True, exist_ok=True)
        failed: list[Chunk] = []
        gpu_job = st.gate.gpu_job(st.config.engine_is_gpu(voice["engine_id"]))
        gpu_job.__enter__()
        try:
            for c, r in zip(chunks, rows):
                if r[4] == "done":
                    continue
                if control.stop:
                    raise JobStopped("paused" if control.stop == "pause" else "cancelled")
                st.gate.wait_turn()
                prog.current_text = c.text
                if st.cache.has(c.chunk_id):  # ugyanaz a szöveg korábban már elkészült
                    rec = None
                else:
                    t_chunk = time.perf_counter()
                    try:
                        rec = self.generate_chunk(voice, c, base_params, qa_enabled, work_dir)
                    except ChunkFailed as e:
                        log.error("Chunk hiba (%s): %s", c.chunk_id[:10], e)
                        repo.db.execute(
                            "UPDATE chunks SET status = 'failed', attempts = attempts + 1 "
                            "WHERE job_id = ? AND chapter_index = ? AND seq = ?", (job_id, c.chapter_index, c.seq))
                        failed.append(c)
                        continue
                if rec:
                    repo.db.execute(
                        "UPDATE chunks SET status = 'done', attempts = ?, wer = ?, qa_warning = ?, duration_s = ?, "
                        "rtf = ? WHERE job_id = ? AND chapter_index = ? AND seq = ?",
                        (rec["attempts"], rec["wer"], rec["qa_warning"], rec["duration_s"], rec["rtf"],
                         job_id, c.chapter_index, c.seq))
                    prog.audio_s += rec["duration_s"]
                    prog.synth_s += rec["synth_s"]
                    prog.wall_s += time.perf_counter() - t_chunk
                else:
                    repo.db.execute("UPDATE chunks SET status = 'done' WHERE job_id = ? AND chapter_index = ? "
                                    "AND seq = ?", (job_id, c.chapter_index, c.seq))
                done_count += 1
                prog.done_chars += len(c.text)
                repo.set_job(job_id, done_chunks=done_count)
                self._update_eta(prog)
        finally:
            gpu_job.__exit__(None, None, None)
            prog.current_text = ""
            shutil.rmtree(work_dir, ignore_errors=True)

        if control.stop == "cancel":
            raise JobStopped("cancelled")
        prog.phase = "exporting"
        prog.eta_s = None
        outputs, export_errors = self.export(project, script, plan, req.get("formats") or
                                             project["settings"].get("export_formats") or ["mp3", "m4b"])
        repo.update_job_request(job_id, {"outputs": [str(p) for p in outputs]})
        problems = []
        if failed:
            problems.append(f"{len(failed)} chunk generálása nem sikerült.")
        problems.extend(export_errors)
        if problems:
            raise JobStopped("failed", " ".join(problems))
        prog.phase = "done"

    def _update_eta(self, prog: Progress) -> None:
        """Átlagos rtf × a hátralévő karakterekből becsült hanghossz.

        Az rtf a feladat falióra-ideje (motor + QA + újrapróbák) a kész hang hosszához mérve,
        így a becslés a minőségellenőrzés idejét is tartalmazza.
        """
        if prog.audio_s <= 0 or prog.done_chars <= 0:
            return
        rtf = max(prog.synth_s, prog.wall_s) / prog.audio_s
        sec_per_char = prog.audio_s / max(1, prog.done_chars)
        prog.eta_s = rtf * sec_per_char * max(0, prog.total_chars - prog.done_chars)

    # --- export ---
    def output_dir(self, project: dict) -> Path:
        return self.state.config.output_root / sanitize_filename(project["name"])

    def export(self, project: dict, script: Script, plan: ChunkPlan, formats: list[str]) -> tuple[list[Path], list[str]]:
        st = self.state
        ff = Ffmpeg(st.config["ffmpeg_path"])
        pdir = st.repo.project_dir(project["id"])
        build = pdir / "build"
        build.mkdir(parents=True, exist_ok=True)
        out_dir = self.output_dir(project)
        cover = project_cover(pdir, script)
        album = script.title or project["name"]
        artist = str(script.front_matter.get("author") or "Ismeretlen")
        speed = float(project["settings"].get("export_speed", 1.0))
        total_chapters = len(script.chapters())
        # egyfájlos kimenetnél a fejezetenkénti MP3 csak az olvasónak kell: a projekt mappájába kerül
        single = project["settings"].get("output_mode") == "single"
        chapter_dir = pdir / "audio" if single else out_dir
        outputs: list[Path] = []
        errors: list[str] = []
        ready: list[tuple[str, Path]] = []
        for ch in plan.chapters:
            missing = [c for c in ch.chunks if not st.cache.has(c.chunk_id)]
            if missing:
                errors.append(f"A(z) {ch.index + 1}. fejezetből {len(missing)} chunk hiányzik, az exportja kimaradt.")
                continue
            raw = build / f"ch{ch.index:03d}.wav"
            norm = build / f"ch{ch.index:03d}.norm.wav"
            durations = build_chapter(
                ff, [ChunkAudio(st.cache.path_for(c.chunk_id), c.pause_after_ms) for c in ch.chunks],
                raw, build / "parts")
            loudnorm(ff, raw, norm, speed)
            raw.unlink(missing_ok=True)
            ready.append((ch.title, norm))
            mp3 = None
            if "mp3" in formats or single:
                mp3 = export_mp3(ff, norm, chapter_dir / mp3_name(ch.index + 1, ch.title), title=ch.title,
                                 album=album, artist=artist, track=ch.index + 1,
                                 total_tracks=total_chapters, cover=cover)
                if not single:
                    outputs.append(mp3)
            mp3_ref = (f"audio/{mp3.name}" if single else mp3.name) if mp3 else None
            save_chapter_timing(pdir, ch, durations, speed, mp3_ref, chapter_block_sig(script, ch.index), single)
        complete = len(ready) == len(plan.chapters) and bool(ready)
        if single and "mp3" in formats:
            if complete:
                outputs.append(export_mp3_book(ff, ready, out_dir / book_mp3_name(album), title=album,
                                               artist=artist, work_dir=build, cover=cover))
            elif ready:
                errors.append("Az egyfájlos MP3 nem készült el, mert nem minden fejezet teljes.")
        if "m4b" in formats:
            if complete:
                outputs.append(export_m4b(ff, ready, out_dir / m4b_name(album), title=album, artist=artist,
                                          work_dir=build, cover=cover))
            elif ready:
                errors.append("Az M4B nem készült el, mert nem minden fejezet teljes.")
        return outputs, errors
