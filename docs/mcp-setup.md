# MCP beállítás: Claude Desktop és Claude Code

A `felolvaso-mcp` egy stdio MCP szerver, ami a futó Felolvasó szolgáltatás REST API-ját hívja.
Előfeltétel: a szolgáltatás fusson (`start.bat`), különben az eszközök ezt a hibát adják:
„A Felolvasó szolgáltatás nem fut. Indítsd el a start.bat-tal.”

Az alábbi példákban a repó útvonala `F:\AI\Project\TTes dolog\felolvaso`; ha máshol van, cseréld le.

## Claude Desktop

Nyisd meg a `%APPDATA%\Claude\claude_desktop_config.json` fájlt (Claude Desktop: Beállítások →
Fejlesztő → Konfiguráció szerkesztése), és vedd fel a szervert:

```json
{
  "mcpServers": {
    "felolvaso": {
      "command": "uv",
      "args": ["run", "--project", "F:\\AI\\Project\\TTes dolog\\felolvaso", "felolvaso-mcp"]
    }
  }
}
```

Mentés után indítsd újra a Claude Desktopot. Az eszközök listájában megjelenik a `felolvaso`.

## Claude Code

```bash
claude mcp add felolvaso --scope user -- uv run --project "F:\AI\Project\TTes dolog\felolvaso" felolvaso-mcp
```

Ellenőrzés: `claude mcp list` → `felolvaso: ... ✓ Connected`.

## Ha nem a 8765-ös porton fut a szolgáltatás

A szolgáltatás `--port` kapcsolóval más porton is indítható (`uv run felolvaso --port 8767`). Ilyenkor az
MCP szervernek is meg kell adni a címet a `FELOLVASO_URL` környezeti változóval:

```json
"felolvaso": {
  "command": "uv",
  "args": ["run", "--project", "F:\\AI\\Project\\TTes dolog\\felolvaso", "felolvaso-mcp"],
  "env": { "FELOLVASO_URL": "http://127.0.0.1:8767" }
}
```

## Eszközök

| Eszköz | Mire jó |
|---|---|
| `get_script_format` | a `.tts.md` formátum leírása |
| `list_voices` | hangprofilok (`id`, név, motor) |
| `validate_script` | forgatókönyv ellenőrzése projekt létrehozása nélkül |
| `submit_script` | projekt létrehozása és a generálás indítása; hibás forgatókönyvnél nem hoz létre projektet |
| `get_job_status` | állapot, haladás, hátralévő idő, kész állapotban a kimeneti fájlok útvonala |
| `list_projects` | projektlista |
| `add_lexicon_entry` | bejegyzés a kiejtési szótárba |

Tipikus menet Claude-dal: a `felolvaso-elokeszito` skill elkészíti a forgatókönyvet →
`validate_script` → `submit_script` → `get_job_status` a végéig.
