# The Silent Oath — Audio Generation Prompts

Music files go in `static/audio/music/` as `.mp3` (with `.ogg` fallback).
SFX files go in `static/audio/sfx/`.
Map new music tracks in `static/js/audio.js` → `SCENE_MUSIC` dict using the art key.

**Target duration:** 3–6 minutes, seamlessly loopable
**Format:** Instrumental, no lyrics, no vocals (except wordless/throat)

---

## Style reference (add to all music prompts)

Dark medieval Templar ambient. Slow tempo, sparse arrangement.
Instruments: solo lute or oud, bowed psaltery, low drone strings, church bell
(distant, sparse), plainchant breath texture (no words), stone resonance.
Muted, desaturated sound — no reverb excess, no epic orchestral swells.
Think: vaulted stone, candlelight, an oath that cannot be unspoken.
Not heroic. Not peaceful. Sacred and heavy.

---

## Act I — The Vow

| File | Art key | Mood |
|------|---------|------|
| `title.mp3` | `title` | Slow dark medieval ambient, builds slowly — **exists** |

### Tracks to generate — Act I

#### `commandery.mp3`
**Art key:** `commandery`, `commandery_night`
**Mood:** A commandery that knows what is coming. Too quiet for the hour.
The torches burn low. Something beneath has been disturbed.

**Prompt:**
```
Dark medieval ambient. Single bowed psaltery note held and released.
Distant church bell, heard once, fading into stone walls.
Low cello drone beneath. Wind through a courtyard at night.
Candle-flame texture — present but fragile. The silence of people
who are not sleeping. No melody. No resolution.
Seamlessly loopable. Instrumental, no lyrics.
```

**Short prompt (Suno/Udio):**
```
dark medieval ambient, stone courtyard at night, single distant church bell,
bowed strings sustain, candle atmosphere, dread without violence,
Templar commandery, quiet before arrest, 3 minutes loop
```

---

#### `chapter_house.mp3`
**Art key:** `chapter_house`
**Mood:** The inner circle. Something has been opened that should remain sealed.
The Grand Master knows. He has not fled.

**Prompt:**
```
Medieval sacred ambient, descending. Solo oud or lute, fingerpicked
very slowly — a phrase that does not resolve. Low drone strings.
Plainchant breath texture — exhale only, no pitch. Stone resonance.
The feeling of a decision already made. Sparse, interior, final.
Seamlessly loopable. Instrumental, no lyrics.
```

**Short prompt (Suno/Udio):**
```
sacred medieval ambient, single lute phrase repeating without resolution,
Templar inner sanctum, low bass drone, plainchant breath, no percussion,
weight of unspoken knowledge, 3 minutes loop
```

---

#### `crypta.mp3`
**Art key:** `crypta`
**Mood:** Beneath the commandery. What the Order has guarded for centuries.
Not a tomb — something alive. Different interpretations are all true.

**Prompt:**
```
Dark sacred ambient. Deep stone resonance — the sound of a very large
enclosed space breathing. Single bowed string, barely audible, one note
held for the entire piece. Water drip, very distant. No percussion.
No melody. The sound of something that has been here longer than the Order.
Unsettling, not violent. Liminal. Sacred.
Seamlessly loopable. Instrumental, no lyrics.
```

**Short prompt (Suno/Udio):**
```
underground sacred chamber ambient, deep stone resonance, single drone,
water echo, something ancient and alive, Templar secret, no melody,
liminal dread, 4 minutes loop
```

---

#### `combat_templar.mp3`
**Art key:** `combat` (general combat fallback)
**Mood:** Oath & Judgment — physical and spiritual simultaneously.
Not a triumph. A test.

**Prompt:**
```
Medieval combat ambient. Irregular frame drum, 70 BPM, occasionally
silent. Dissonant bowed strings. Heavy breath texture. No triumphant
crescendo — the tension does not release, it shifts. Cold, interior,
relentless. The sound of violence committed in a place of God.
Seamlessly loopable. Instrumental, no lyrics.
```

**Short prompt (Suno/Udio):**
```
dark medieval combat music, frame drum irregular rhythm, dissonant
bowed strings, no heroism, Templar violence sacred space atmosphere,
heavy physical presence, 90 seconds loop
```

---

## SFX — all acts

| File | Trigger |
|------|---------|
| `sfx_choice.ogg` | Hover over choice button |
| `sfx_confirm.ogg` | Click a choice |
| `sfx_memory.ogg` | Memory fragment recovered |
| `sfx_death.ogg` | Player falls in combat |
| `sfx_hit.ogg` | Combat hit lands |
| `sfx_miss.ogg` | Combat attack misses |
| `sfx_parry.ogg` | Parry succeeds |

### Suno/Udio prompts — SFX

- **sfx_choice**: "parchment unfolding, soft, quiet, medieval, ui hover sound"
- **sfx_confirm**: "heavy iron latch clicking shut, satisfying, medieval stone, selection confirm"
- **sfx_memory**: "single resonant church bell, very quiet, reverb decay, sacred, memory recovered"
- **sfx_death**: "deep iron toll, single heavy bell, slow long decay, death knell, solemn"
- **sfx_hit**: "iron on iron impact, heavy, combat hit, short sharp"
- **sfx_miss**: "weapon swoosh through air, short, combat miss"
- **sfx_parry**: "ringing metal clash, iron parry, short bright tone, success"

---

## Adding a new track — checklist

1. Generate audio, save as `static/audio/music/<trackname>.mp3`
2. Add `.ogg` version for browser fallback
3. In `audio.js`, add to `SCENE_MUSIC`:
   ```js
   "art_key": "trackname",
   ```
4. Test: the track should crossfade (2s) when entering the first scene that uses the art key
