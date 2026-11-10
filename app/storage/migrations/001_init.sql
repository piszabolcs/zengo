CREATE TABLE IF NOT EXISTS projects (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    source_path TEXT,
    script_path TEXT NOT NULL,
    settings_json TEXT NOT NULL,
    warnings_json TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS voices (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    engine_id TEXT NOT NULL,
    ref_audio_path TEXT,
    ref_text TEXT,
    params_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS jobs (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    status TEXT NOT NULL,
    request_json TEXT NOT NULL,
    total_chunks INTEGER,
    done_chunks INTEGER DEFAULT 0,
    error TEXT,
    created_at TEXT,
    started_at TEXT,
    finished_at TEXT
);

CREATE TABLE IF NOT EXISTS chunks (
    job_id TEXT REFERENCES jobs(id) ON DELETE CASCADE,
    chunk_id TEXT,
    chapter_index INTEGER,
    seq INTEGER,
    status TEXT,
    attempts INTEGER DEFAULT 0,
    wer REAL,
    qa_warning INTEGER DEFAULT 0,
    duration_s REAL,
    rtf REAL,
    PRIMARY KEY (job_id, chapter_index, seq)
);

CREATE TABLE IF NOT EXISTS cache_entries (
    chunk_id TEXT PRIMARY KEY,
    path TEXT NOT NULL,
    bytes INTEGER,
    last_used_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS lexicon (
    written TEXT PRIMARY KEY,
    spoken TEXT NOT NULL,
    case_sensitive INTEGER DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
CREATE INDEX IF NOT EXISTS idx_chunks_job_status ON chunks(job_id, status);
CREATE INDEX IF NOT EXISTS idx_cache_last_used ON cache_entries(last_used_at);
