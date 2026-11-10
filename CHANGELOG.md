# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), versioning: [SemVer](https://semver.org/).

## [2.0.0] - 2026-11-10

### Added
- Desktop app: the UI runs in its own window (pywebview, WebView2); the internal server starts and stops with it.
- Portable build (`scripts/build_portable.ps1`): one folder with a `Zengo.exe` launcher, bundled Python runtimes, engine environments, models and ffmpeg.
- One-time migration of projects, voices, cache and finished audiobooks from the previous install.
- New name and icon (Zengő).

### Changed
- F5-TTS endings: a throwaway closing word makes the last syllable fade out instead of being cut at the buffer edge.
- Generation is grouped into sentence groups of at most 160 characters.

### Removed
- XTTS-v2 from the default install and the portable build.

## [1.0.0] - 2026-11-08

### Added
- First release as Felolvasó: import, Hungarian normalizer, F5-TTS / Piper / XTTS workers, job queue, Whisper QA, MP3 / M4B export, reader view, MCP server.
