# Forgotten Among the Fallen

A dark fantasy Viking experience set in a desolate world between life and death.

Beneath a silent, star-filled sky, fallen warriors lie forgotten — but not at rest.
Ancient runes still burn in the earth, and something stirs beneath the fog.

Explore a cursed battlefield where time has no meaning, uncover remnants of a lost world,
and face forces that should not exist.

The core hook is the tension between your Viking identity (die gloriously, reach Valhalla) and your actual state (
forgotten, neither alive nor dead). Every system reinforces this — you can't truly die, but that's a curse, not a power
fantasy. The gameplay loop is built around the Curse Accumulation system as the primary tension dial. Instead of a
simple death penalty, deaths literally darken your world and empower enemies, which makes every encounter feel
meaningful without being frustrating. The Death Echo mechanic (your ghost staying in the world) turns failure into a
risk/reward decision. Level 1 design philosophy: the Battlefield of Silence is intentionally sparse and atmospheric
early on, teaching through environment rather than text — the layout of fallen soldiers is the tutorial. The boss,
Gunnar, isn't just a difficulty gate; he's the emotional climax of act 1, because the Memory Shards scattered across the
zone have been building toward that reveal. The progression system avoids number-chasing by framing upgrades as
narrative events — spending a Memory Fragment to grow stronger means giving up a piece of who you were. That's a real
choice with story weight

## Features

- Atmospheric dark fantasy setting inspired by Norse myth and liminal spaces
- Desolate environments shaped by war, ruin, and silence
- Runic elements and subtle supernatural presence
- Cinematic visual tone with painterly aesthetics

## Vision

A slow, immersive experience focused on mood, isolation, and the boundary between life and death.

---

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
  combat.py               ← Combat engine, returns JSON
  conditions.py           ← Data-driven condition evaluator
content/
  game_config.py          ← STATS, EQUIPMENT, HUD layout, start scene
  enemies.py              ← Enemy definitions (stats, phrases, loot)
  act1.py                 ← Act I scenes
  act2.py                 ← Act II scenes
  scenes.py               ← Aggregator: {**ACT1, **ACT2}
static/
  css/game.css            ← Dark fantasy stylesheet
  js/game.js              ← Frontend controller
  js/audio.js             ← Music + SFX engine (art_key → track)
  svg/                    ← Scene illustrations
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

**Act I — The Battlefield of Silence**
Complete. A warrior wakes on a battlefield, denied Valhalla, denied death.
Leif. Gunnar. The Mound of Oathbreakers. A broken oath.

**Act II — The Stirring Beneath**
Complete. A fortified keep frozen in time. Odrik the Bound.
A runic structure that holds the moment in place. The rune is not alone.

**Act III — The Silence Beneath**
Planned.

**Act IV — The Keeper of the Unfinished**
Planned.
