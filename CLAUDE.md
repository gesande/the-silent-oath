# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**The Silent Oath** is a dark historical text-adventure game set in the world of the Knights Templar (~1307). Flask/Python backend + vanilla JS frontend. Players navigate faith, doubt, oath-keeping, and a divine secret the order has guarded for centuries.

## Commands

**Run locally:**
```bash
pip install flask>=3.0.0
python app.py
# Available at http://localhost:5000
```

**Run with Docker:**
```bash
docker compose up --build
```

**Environment variables:** `PORT` (default 5000), `FLASK_ENV`, `SECRET_KEY`

There are no tests or build tools configured. Run after every code change:

```bash
python -m black engine/ content/ app.py
prettier --write static/js/
python -m ruff check engine/ content/ app.py
```

F8xx ruff errors are real bugs and must be fixed. E4xx/E7xx are style only.

## Architecture

**Backend (Python/Flask) — `app.py`**
- Stateless HTTP server; player state lives in Flask session (not database)
- State serialized/deserialized as `PlayerState` dataclass on every request
- API routes: `/api/new`, `/api/load`, `/api/scene`, `/api/choose`, `/api/combat/action`, `/api/advance`, `/api/status`

**Game Engine — `engine/`**
- `state.py`: `PlayerState` dataclass. Stats, inventory, flags, memory fragments, save/load. Derived threshold methods read thresholds from `STATS` config.
- `scene_web.py`: Processes scene beats and returns JSON. Side effects apply only on first visit. Auto-advances scenes with no prose/choices/combat.
- `combat.py`: Oath & Judgment combat engine (TBD — to be rewritten for this game).
- `conditions.py`: Data-driven condition evaluator used by scene and choice visibility logic.

**Game Config — `content/game_config.py`**
- `STATS`: per-stat bounds (`min`/`max`/`default`) and derived thresholds (`threshold`)
- `EQUIPMENT`: all equippable items with `slot`, `tier`, and slot-specific properties
- `HUD_STATS`: which stats appear in the HUD
- `START_SCENE`: entry point scene key

**Content — `content/`**
- `enemies.py`: Enemy definitions. No engine changes needed to add enemies.
- `act1.py`, `act2.py`: Scene dicts per act. Pure data, no logic.
- `scenes.py`: Thin aggregator — `SCENES = {**ACT1, **ACT2}`

**Frontend — `static/js/game.js` + `audio.js`**
- Vanilla JS, no frameworks
- `game.js`: Fetches scenes/choices/combat from API, updates DOM, manages HUD
- `audio.js`: Scene-based music via `art_key` → track mapping; crossfade (2s); independent music/SFX volume

## Core Stats

| Stat | Description | Threshold |
|------|-------------|-----------|
| `body` | Physical strength and endurance | < 20 = broken |
| `faith` | Belief — drives abilities | >= 70 = faithful |
| `resolve` | Mental endurance | < 20 = broken |
| `doubt` | Grows during play; destabilizes faith but adds power | >= 60 = doubting |

**Key tension:** High Faith = strong, stable abilities. High Doubt = unstable but potentially more powerful effects. Doubt is not purely negative.

## Key Game Systems

- **Oath & Judgment**: Combat is physical + mental + spiritual simultaneously. TBD.
- **Faith/Doubt tension**: Core stat interplay — doubt grows organically, affects faith-based abilities
- **Memory Fragments**: Narrative collectibles visible in HUD
- **Equipment slots**: `equipped` dict on PlayerState; `"weapon"` and `"shield"` slots

## The Secret

The Templars guard something divine beneath Jerusalem, Europe, and the northern wastes. Its nature is **never explicitly revealed** — different brothers believe different things. Ambiguity is intentional and mechanical: high Doubt reveals more interpretations, not the truth.

## Content Authoring

### Adding a scene
Add an entry to `content/act1.py` or `content/act2.py` and register it in the local `SCENES` dict at the bottom of the file. Scene keys must be unique.

```python
SCENE_MY_SCENE = {
    "art": "art_key",          # maps to static/svg/<art_key>.png and audio
    "header": {"title": "...", "subtitle": "..."},  # optional
    "beats": [...],
    "choices": [...],          # omit for auto-advance via "next"
    "next": "next_scene_key",
}
```

### Beat types
| Type | Effect |
|------|--------|
| `prose` | Paragraph of narrative text |
| `italic` | Italicised prose (speech, sensation) |
| `memory` | Adds memory fragment; `key`, `label`, `text` |
| `conditional_prose` | Shows first matching `variants[].condition` |
| `combat` | Triggers combat with `enemy` key; skipped if already defeated |
| `stat` | `{"changes": {"stat": delta}}` — first visit only |
| `flag` | Sets a story flag — first visit only |
| `item` | `action: "give"` or `action: "take"` — first visit only |
| `heal` | Restores HP — first visit only |
| `input` | Text input prompt |

### Condition DSL (used in `condition` fields on beats and choices)
```python
{"flag":     "name"}              # flag is set
{"memory":   "name"}              # player has memory
{"has_item": "name"}              # item in inventory
{"equipped": "weapon_name"}       # weapon slot matches
{"stat_gte": "stat", "value": N}  # stat >= N
{"not": <cond>}
{"and": [<cond>, ...]}
{"or":  [<cond>, ...]}
```

### Art and audio
- Images: `static/svg/<art_key>.png`
- Music: add `"art_key": "track_name"` to `SCENE_MUSIC` in `static/js/audio.js`, place `track_name.mp3` in `static/audio/music/`
- The `"art"` field in a scene drives both the image and the music track
- Unmapped art keys fall back to `exploration.mp3`
