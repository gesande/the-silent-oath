# Forgotten Among the Fallen — Audio Generation Prompts

Music files go in `static/audio/music/` as `.mp3` (with `.ogg` fallback).
SFX files go in `static/audio/sfx/`.
Map new music tracks in `static/js/audio.js` → `SCENE_MUSIC` dict using the art key.

**Target duration:** 3–6 minutes, seamlessly loopable
**Format:** Instrumental, no lyrics, no vocals (except wordless/throat)

---

## Style reference (add to all music prompts)

Dark Norse ambient. Slow tempo, sparse arrangement.
Instruments: tagelharpa (bowed lyre), kravik lyre, frame drum, bone flute,
low drone strings, distant horn, breath texture.
Muted, desaturated sound — no reverb excess, no fantasy epic swells.
Think: death, fog, unfinished oaths. Not heroic. Not peaceful.

---

## Act I — existing tracks

| File | Art key | Mood |
|------|---------|------|
| `ambient_title.mp3` | `title` | Slow dark Norse ambient, builds slowly |
| `ambient_cairn.mp3` | `cairn`, `name_entry` | Ethereal, rune tones, sparse |
| `ambient_battlefield.mp3` | `battlefield`, `scavenge` | Wind, distant horn, no melody |
| `ambient_leif.mp3` | `leif` | Sorrowful strings, dying soldier |
| `ambient_forge.mp3` | `longhouse` | Dying embers, low drone, sacred |
| `ambient_mound.mp3` | `mound`, `gunnar` | Oppressive bass drone, ominous |
| `ambient_void.mp3` | `act_break` | Near silence, one distant horn note |
| `combat_draugar.mp3` | `combat_draugar` | Urgent percussion, no melody |
| `combat_boss.mp3` | `gunnar_combat` | War drums, heavy, relentless |

### Suno/Udio prompts — Act I

- **ambient_title**: "dark norse atmospheric intro, slow building tension, distant
  single horn note fading in, deep silence between sounds, title screen atmosphere,
  no melody, no percussion, 3 minutes loop"
- **ambient_leif**: "slow sorrowful norse ambient, single cello or low strings,
  sparse melody, dying soldier atmosphere, melancholic but not hopeless,
  quiet and intimate, no percussion, 3 minutes loop"
- **ambient_battlefield**: "dark norse ambient, wind howling, distant war horn,
  slow deep drums fading in and out, no melody, 3 minutes, loop"
- **ambient_forge**: "dark medieval blacksmith ambient, dying forge embers crackling,
  low resonant drone, occasional distant hammer strike on metal, warm but desolate,
  sacred atmosphere, no melody, 3 minutes loop"
- **ambient_cairn**: "ethereal norse ambient, singing bowls, rune tones,
  sparse, sacred feeling, very quiet, 3 minutes loop"
- **ambient_mound**: "oppressive dark norse drone, deep bass rumble, burial mound
  atmosphere, silence punctuated by distant wind, ominous, no melody, no percussion,
  unsettling, 3 minutes loop"
- **ambient_void**: "near silence dark ambient, single distant viking horn note,
  vast empty space, cold wind, between worlds liminal atmosphere, very minimal,
  90 seconds loop"
- **combat_draugar**: "viking battle percussion, urgent rhythmic drums, no
  melody, intense, dark, 90 seconds loop"
- **combat_boss**: "epic dark norse boss fight music, heavy war drums, chanting,
  ominous, relentless tempo, 2 minutes loop"

---

## Act II — tracks to generate

---

### Track 1 — `ambient_fog.mp3`
**Art key:** `fog_road`
**Used in:** fog_road, fog_the_held, fog_held_other, fog_held_release, fog_held_after, fog_sentinel_after

**Mood:** Something is alive in the fog. Not hostile — aware.
You cannot see the path ahead. You cannot see what is following you.
The air is wrong in a way you cannot name.

**Prompt:**
```
Dark Norse ambient drone. Tagelharpa bowed slowly, single note held and
released. Frame drum at 40 BPM, barely audible. Bone flute enters once
then disappears. Low vocal texture — not words, not song — breath shapes
in cold air. Field recording: wind over frozen ground, distant water.
No melody. No resolution. Fog. Seamlessly loopable.
Instrumental, no lyrics.
```

**Alternative (shorter Suno/Udio prompt):**
```
slow rhythmic breathing sound as ambient music, warm but deeply wrong
temperature, no instruments, fog atmosphere, purgatorial, something
inhuman exhaling slowly, liminal dread, 3 minutes loop
```

---

### Track 2 — `combat_sentinel.mp3`
**Art key:** `fog_sentinel`
**Used in:** combat_fog_sentinel, fog_sentinel_wait

**Mood:** Fighting something that grows stronger the harder you strike.
Not a battle to win with force — the music should feel like it is
absorbing the player's effort. Draining, not escalating.

**Prompt:**
```
Dark Norse percussive ambient. Dissonant bowed strings that swell when
struck and slowly deflate. Frame drum pulse, irregular — 60 BPM but
slightly unsteady, as if breathing. Low drone bass that builds when
drums accelerate, then releases. No triumphant crescendo. The tension
never fully resolves — it absorbs. Cold, oppressive, relentless.
Seamlessly loopable. Instrumental, no lyrics.
```

**Alternative (shorter Suno/Udio prompt):**
```
single sustained low bell tone pulsing slowly, no percussion no melody,
the bell never fully decays, something absorbing sound, combat
atmosphere without urgency, 90 seconds loop
```

---

### Track 3 — `ambient_gatehouse.mp3`
**Art key:** `gatehouse`
**Used in:** gatehouse_approach, gatehouse_guards and all gatehouse variants, gatehouse_courtyard, gatehouse_wall, gatehouse_inside

**Mood:** Forty warriors frozen mid-step. A moment suspended for decades.
Not death — something more precise than death. Waiting, without knowing
they are waiting. The silence of interrupted time.

**Prompt:**
```
Norse ambient, stillness. Single tagelharpa note held for eight counts,
released, silence for four, repeated. Sparse frame drum — one strike
every twelve beats. Wind ambience through stone. Distant horn, heard
once, fading. The feeling of a held breath that has lasted forty years.
No rhythm, no forward motion. Time has stopped here.
Seamlessly loopable. Instrumental, no lyrics.
```

**Alternative (shorter Suno/Udio prompt):**
```
complete interior silence ambient, single drop of water echoing in stone
chamber, occasional distant creak of heavy wood, held breath atmosphere,
warmth without comfort, 3 minutes loop
```

---

### Track 4 — `ambient_great_hall.mp3`
**Art key:** `great_hall`, `odrik_go_forward`
**Used in:** great_hall_entrance, great_hall_rune_door, all odrik_* scenes, act2_end

**Mood:** An old man and an unfinished rune.
Forty frozen warriors still seated at the feast tables.
Something in the walls that has been holding for a long time
and is beginning, very slowly, to shift.

**Prompt:**
```
Dark Norse chamber ambient. Solo kravik lyre, fingerpicked slowly —
a pattern that almost resolves but doesn't. Low cello drone beneath.
Fire ambience, very quiet. Occasional creak of old timber.
The music should feel inhabited — not empty, not peaceful.
Someone has been in this room for a very long time.
Sparse, intimate, heavy with unspoken weight.
Seamlessly loopable. Instrumental, no lyrics.
```

---

## SFX — all acts

| File | Trigger |
|------|---------|
| `sfx_choice.ogg` | Hover over choice button |
| `sfx_confirm.ogg` | Click a choice |
| `sfx_memory.ogg` | Memory fragment recovered |
| `sfx_death.ogg` | Player falls in combat |
| `sfx_shards.ogg` | Echo shards gained |
| `sfx_hit.ogg` | Combat hit lands |
| `sfx_miss.ogg` | Combat attack misses |
| `sfx_parry.ogg` | Parry succeeds |

### Suno/Udio prompts — SFX

- **sfx_choice**: "soft parchment rustling, quiet, subtle, ui hover sound"
- **sfx_confirm**: "heavy iron click, satisfying, medieval, selection confirm sound"
- **sfx_memory**: "ethereal frost bell chime, single note, reverb, memory recovered"
- **sfx_death**: "deep resonant iron toll, single heavy bell, slow decay, death knell"
- **sfx_shards**: "crystalline ice shards clinking, bright, magical, short"
- **sfx_hit**: "iron on iron impact, heavy, combat hit, short sharp"
- **sfx_miss**: "weapon swoosh through air, short, combat miss"
- **sfx_parry**: "ringing metal clash, iron parry, short bright tone, success sound"

---

## Adding a new track — checklist

1. Generate audio, save as `static/audio/music/<trackname>.mp3`
2. Add `.ogg` version for browser fallback
3. In `audio.js`, add to `SCENE_MUSIC`:
   ```js
   "art_key": "trackname",
   ```
4. Test: the track should crossfade (2s) when entering the first scene that uses the art key
