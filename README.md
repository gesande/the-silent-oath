# The Silent Oath

A dark historical text-adventure set in the world of the Knights Templar, 1307.

The Order has guarded a divine secret for centuries — beneath Jerusalem, beneath Europe, beneath the northern wastes.
Its nature is never revealed. High Doubt shows more interpretations, not the truth.

Players navigate faith, doubt, oath-keeping, and the weight of a secret that could shake Christendom.
The core tension is between Faith and Doubt: Faith grants stable, powerful abilities; Doubt is destabilising but
opens paths that certainty cannot reach. Neither is purely good or bad.

## Features

- Dark historical setting rooted in the fall of the Knights Templar
- Faith/Doubt tension as the primary mechanical and narrative dial
- Memory Fragments — narrative collectibles that accumulate across play
- Oath & Judgment combat: physical, mental, and spiritual simultaneously
- Ambiguity as a design principle — the secret is never explained

## Setup

```bash
pip install flask>=3.0.0
python app.py
```

Then open: http://localhost:5000

## Docker

```bash
docker compose up --build
```

## Structure

```
app.py                    ← Flask server + API routes
engine/
  state.py                ← PlayerState dataclass + save/load
  scene_web.py            ← Scene beat processor, returns JSON
  combat.py               ← Combat engine (TBD — Oath & Judgment)
  conditions.py           ← Data-driven condition evaluator
content/
  game_config.py          ← STATS, EQUIPMENT, HUD layout, start scene
  enemies.py              ← Enemy definitions
  act1.py                 ← Act I scenes
  act2.py                 ← Act II scenes
  scenes.py               ← Aggregator: {**ACT1, **ACT2}
static/
  css/game.css            ← Stylesheet
  js/game.js              ← Frontend controller
  js/audio.js             ← Music + SFX engine (art_key → track)
  svg/                    ← Scene illustrations
  audio/music/            ← Music tracks (.mp3)
templates/
  index.html              ← Single-page game shell
saves/                    ← Auto-created, JSON save files
IMAGE_PROMPTS.md          ← AI image generation prompts
AUDIO_PROMPTS.md          ← AI music generation prompts
```

## API

| Method | Route              | Description                         |
|--------|--------------------|-------------------------------------|
| POST   | /api/new           | Start a new game                    |
| POST   | /api/load          | Load save slot 0                    |
| GET    | /api/scene         | Get current scene                   |
| POST   | /api/choose        | Make a choice `{choice_id}`         |
| POST   | /api/combat/action | Execute combat action `{action_id}` |
| GET    | /api/status        | Save state summary                  |

## Content

**Act I — The Vow**
In progress.

**Act II — The Weight of Silence**
Planned.
