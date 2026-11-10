"""Projektek, hangprofilok, kiejtési szótár és feladatok adatbázis-műveletei."""

from __future__ import annotations

import json
import os
import re
import unicodedata
import uuid
from pathlib import Path
from typing import Any

from app.config import Config
from app.engines.protocol import DEFAULT_ENGINE_PARAMS
from app.normalize.hu import LexiconEntry
from app.storage.db import Database, now_iso


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8", newline="\n")
    os.replace(tmp, path)


def sanitize_filename(name: str, max_len: int = 80) -> str:
    """Fájlnévnek alkalmas alak: ékezetek maradnak, tiltott karakterek és `..` nem."""
    name = unicodedata.normalize("NFC", name)
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', " ", name)
    name = name.replace("..", " ")
    name = re.sub(r"\s+", " ", name).strip(" .")
    return (name[:max_len].rstrip(" .") or "nevtelen")


def slugify(name: str) -> str:
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "hang"


def default_project_settings(config: Config) -> dict[str, Any]:
    return {
        "voice_id": config["default_voice"],
        "read_footnotes": False,
        "read_figure_captions": False,
        "pauses": dict(config["pauses"]),
        "announce_chapters": bool(config["announce_chapters"]),
        "qa_enabled": bool(config["qa"]["enabled"]),
        "export_formats": list(config["export"]["formats"]),
        "export_speed": float(config["export"]["speed"]),
        "output_mode": "chapters",
        "seed": 0,
    }


class Repo:
    def __init__(self, db: Database, config: Config):
        self.db = db
        self.config = config

    # --- projektek ---
    def project_dir(self, project_id: str) -> Path:
        return self.config.paths.projects_dir / project_id

    def create_project(self, name: str, script_text: str, source_path: str | None, warnings: list[str],
                       settings: dict | None = None) -> dict:
        pid = str(uuid.uuid4())
        pdir = self.project_dir(pid)
        pdir.mkdir(parents=True, exist_ok=True)
        script_path = pdir / "script.tts.md"
        atomic_write_text(script_path, script_text)
        s = default_project_settings(self.config)
        if settings:
            s.update({k: v for k, v in settings.items() if v is not None})
        ts = now_iso()
        self.db.execute(
            "INSERT INTO projects (id, name, source_path, script_path, settings_json, warnings_json, created_at, "
            "updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (pid, name, source_path, str(script_path), json.dumps(s, ensure_ascii=False),
             json.dumps(warnings, ensure_ascii=False), ts, ts),
        )
        return self.get_project(pid)

    def _project_row(self, row) -> dict:
        d = dict(row)
        d["settings"] = {**default_project_settings(self.config), **json.loads(d.pop("settings_json") or "{}")}
        d["warnings"] = json.loads(d.pop("warnings_json") or "[]")
        return d

    def get_project(self, project_id: str) -> dict | None:
        row = self.db.one("SELECT * FROM projects WHERE id = ?", (project_id,))
        return self._project_row(row) if row else None

    def list_projects(self) -> list[dict]:
        return [self._project_row(r) for r in self.db.query("SELECT * FROM projects ORDER BY updated_at DESC")]

    def read_script(self, project: dict) -> str:
        return Path(project["script_path"]).read_text(encoding="utf-8")

    def save_script(self, project_id: str, text: str, warnings: list[str] | None = None) -> None:
        p = self.get_project(project_id)
        assert p is not None
        atomic_write_text(Path(p["script_path"]), text)
        if warnings is None:
            self.db.execute("UPDATE projects SET updated_at = ? WHERE id = ?", (now_iso(), project_id))
        else:
            self.db.execute("UPDATE projects SET updated_at = ?, warnings_json = ? WHERE id = ?",
                            (now_iso(), json.dumps(warnings, ensure_ascii=False), project_id))

    def update_settings(self, project_id: str, changes: dict) -> dict:
        p = self.get_project(project_id)
        assert p is not None
        s = {**p["settings"], **changes}
        self.db.execute("UPDATE projects SET settings_json = ?, updated_at = ? WHERE id = ?",
                        (json.dumps(s, ensure_ascii=False), now_iso(), project_id))
        return s

    def delete_project(self, project_id: str) -> None:
        self.db.execute("DELETE FROM projects WHERE id = ?", (project_id,))

    # --- hangprofilok ---
    def _voice_row(self, row) -> dict:
        d = dict(row)
        params = json.loads(d.pop("params_json") or "{}")
        d["params"] = {**DEFAULT_ENGINE_PARAMS.get(d["engine_id"], {}), **params}
        return d

    def list_voices(self) -> list[dict]:
        return [self._voice_row(r) for r in self.db.query("SELECT * FROM voices ORDER BY name")]

    def get_voice(self, voice_id: str) -> dict | None:
        row = self.db.one("SELECT * FROM voices WHERE id = ?", (voice_id,))
        return self._voice_row(row) if row else None

    def upsert_voice(self, voice_id: str, name: str, engine_id: str, ref_audio_path: str | None,
                     ref_text: str | None, params: dict) -> dict:
        self.db.execute(
            "INSERT INTO voices (id, name, engine_id, ref_audio_path, ref_text, params_json, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?) ON CONFLICT(id) DO UPDATE SET name = excluded.name, "
            "engine_id = excluded.engine_id, ref_audio_path = excluded.ref_audio_path, "
            "ref_text = excluded.ref_text, params_json = excluded.params_json",
            (voice_id, name, engine_id, ref_audio_path, ref_text, json.dumps(params, ensure_ascii=False),
             now_iso()),
        )
        v = self.get_voice(voice_id)
        assert v is not None
        return v

    def delete_voice(self, voice_id: str) -> None:
        self.db.execute("DELETE FROM voices WHERE id = ?", (voice_id,))

    def unique_voice_id(self, name: str) -> str:
        base = slugify(name)
        vid, i = base, 2
        while self.get_voice(vid):
            vid = f"{base}-{i}"
            i += 1
        return vid

    # --- kiejtési szótár ---
    def lexicon(self) -> list[dict]:
        return [dict(r) for r in self.db.query("SELECT * FROM lexicon ORDER BY written COLLATE NOCASE")]

    def lexicon_entries(self) -> list[LexiconEntry]:
        return [LexiconEntry(r["written"], r["spoken"], bool(r["case_sensitive"])) for r in self.lexicon()]

    def set_lexicon(self, entries: list[dict]) -> None:
        with self.db.write_lock:
            c = self.db.conn()
            c.execute("DELETE FROM lexicon")
            c.executemany("INSERT OR REPLACE INTO lexicon (written, spoken, case_sensitive) VALUES (?, ?, ?)",
                          [(e["written"], e["spoken"], int(bool(e.get("case_sensitive")))) for e in entries
                           if e.get("written") and e.get("spoken")])
            c.commit()

    def add_lexicon_entry(self, written: str, spoken: str, case_sensitive: bool = False) -> None:
        self.db.execute("INSERT OR REPLACE INTO lexicon (written, spoken, case_sensitive) VALUES (?, ?, ?)",
                        (written, spoken, int(case_sensitive)))

    def delete_lexicon_entry(self, written: str) -> None:
        self.db.execute("DELETE FROM lexicon WHERE written = ?", (written,))

    # --- feladatok ---
    def create_job(self, project_id: str, request: dict) -> dict:
        jid = str(uuid.uuid4())
        self.db.execute(
            "INSERT INTO jobs (id, project_id, status, request_json, total_chunks, done_chunks, created_at) "
            "VALUES (?, ?, 'queued', ?, NULL, 0, ?)",
            (jid, project_id, json.dumps(request, ensure_ascii=False), now_iso()),
        )
        job = self.get_job(jid)
        assert job is not None
        return job

    def _job_row(self, row) -> dict:
        d = dict(row)
        d["request"] = json.loads(d.pop("request_json") or "{}")
        return d

    def get_job(self, job_id: str) -> dict | None:
        row = self.db.one("SELECT * FROM jobs WHERE id = ?", (job_id,))
        return self._job_row(row) if row else None

    def list_jobs(self, project_id: str | None = None) -> list[dict]:
        if project_id:
            rows = self.db.query("SELECT * FROM jobs WHERE project_id = ? ORDER BY created_at DESC", (project_id,))
        else:
            rows = self.db.query("SELECT * FROM jobs ORDER BY created_at DESC")
        return [self._job_row(r) for r in rows]

    def set_job(self, job_id: str, **fields: Any) -> None:
        if not fields:
            return
        cols = ", ".join(f"{k} = ?" for k in fields)
        self.db.execute(f"UPDATE jobs SET {cols} WHERE id = ?", (*fields.values(), job_id))

    def job_request(self, job_id: str) -> dict:
        job = self.get_job(job_id)
        return job["request"] if job else {}

    def update_job_request(self, job_id: str, changes: dict) -> None:
        req = {**self.job_request(job_id), **changes}
        self.set_job(job_id, request_json=json.dumps(req, ensure_ascii=False))

    def job_chunks(self, job_id: str) -> list[dict]:
        return [dict(r) for r in self.db.query(
            "SELECT * FROM chunks WHERE job_id = ? ORDER BY chapter_index, seq", (job_id,))]
