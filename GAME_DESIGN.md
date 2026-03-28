# The Silent Oath — Game Design Document

## Concept

Text-adventure set in the world of the Knights Templar, ~1307.
Historically charged — the year Philip IV of France moves against the Order.

## Hook

You play a Templar knight called back to the heart of the order's secret guardianship.
The brotherhood is fracturing from within — some brothers want to use the power,
some want to destroy it. You are caught in the middle.

The Templars are not protecting the world. They are keeping something terrible locked away.

## Lore

*They did not find God.*

*They found the answer.*

*And the answer was not meant for human minds.*

*So the door was sealed.*
*So the oath was given.*

*Not to protect the world —*

*but to keep it ignorant.*

---

## The Secret

> "The power is not power — it is a truth no one can carry."

What the Templars guard is not an object or a place. It is **knowledge** — absolute, divine, unbearable.

It appears as a cosmic phenomenon. The player experiences it as supernatural.
But what it truly is: a truth so complete that encountering it shatters faith
or transforms the person beyond return.

The rituals in Jerusalem, the monasteries in Scotland, the fortresses in Cyprus —
they do not keep the power contained. They keep **understanding** at a distance.

> Some brothers have seen it. They are not the same.

Its nature is never explicitly named — different brothers believe different things
(the Ark, the Grail, something older). Ambiguity is intentional and mechanical:
the player becomes the interpreter.

**The final definition:**

It is the original revelation — before the Church, before doctrine.

The Templars do not guard an artifact. They guard a truth that:

- Overturns organised faith
- Reveals that mankind is not chosen
- Reveals that prayers go nowhere
- Reveals that the "divine voice" is something else entirely

The Church did not build its doctrine on this truth. It built its doctrine *against* it.

**Why this works with the stat system:**
- **Doubt** grows as you approach the truth — not because you doubt God, but because you begin to *understand*
- **Faith** protects — not because it is correct, but because it holds you together
- At the end, the player may choose to *understand* — and pay the price

---

## Core Stats

| Stat | Range | Description | Threshold |
|------|-------|-------------|-----------|
| **Body** | 0–100 | Physical strength and endurance | < 20 = broken |
| **Faith** | 0–100 | Belief — drives abilities and powers | ≥ 70 = faithful |
| **Resolve** | 0–100 | Mental endurance — resists breaking | < 20 = broken |
| **Doubt** | 0–100 | Grows during play. Destabilizes Faith but adds power | ≥ 60 = doubting |

**Key tension:** High Faith = strong, stable abilities.
High Doubt = unstable but potentially more powerful effects. Doubt is not purely negative.

---

## Combat System: Oath & Judgment

Combat is not traditional HP-grinding. Every encounter is simultaneously physical,
mental, and spiritual. Stats shift during combat. Winning through violence has a cost.

### Player Actions

| Action | Available When | Effect |
|--------|---------------|--------|
| **Strike** | Always | Physical damage. Body > 60 = bonus. Costs faith -3 vs saints. |
| **Endure** | Always | Halves incoming damage. Resolve +5. |
| **Invoke Oath** | Always | Faith attack. Unreliable if faith < 50. Costs resolve -3. Doubt -3 on success. |
| **Yield to Doubt** | Doubt ≥ 40 | High damage. Doubt +8. Resolve -10 if doubt ≥ 60. |
| **Flank** | Enemy has shield | Removes shield advantage. |
| **Show Mercy** | Enemy HP < 30% | Ends combat. Faith +10, Doubt -5. |
| **Release** | Enemy HP < 30%, resolution.free | Lets them go. Faith +15, Doubt -8. |
| **Listen** | Passive enemy, resolution.listen | Peaceful end. Doubt +15, Faith -5, Resolve +10. |
| **Flee** | Always | Escape. Take damage. Faith -5, Resolve -5. |

### Enemy Faith Resistance

Enemies have a `faith` stat (0–100). High enemy faith resists `invoke_oath`
(up to 40% damage reduction at faith 100). Faith 0 = no resistance at all.

### Death

On player death: deaths counter increases, health restores, faith -5, resolve -5.
Combat ends with `died: True`. Scene system handles what comes next.

### Victory

Killing through combat: faith +3, doubt +2.
Mercy/release/listen: no death log, cleaner stat costs.

---

## Enemy Design Framework

Every enemy has five layers:

### 1. Identity
Not a type — a person, a force, a consequence.
The identity is one line that tells the writer what the enemy *means*, not what it does.

### 2. Stats

| Stat | Engine field | What it drives |
|------|-------------|----------------|
| Threat (1–5) | `threat` | Overall difficulty scale |
| Body (1–5) | `hp`, `damage` | Physical capability |
| Faith (0–5) | `faith` (0–100) | Resistance to invoke_oath |
| Resolve (1–5) | `resolve` (0–100) | Mental fortitude |

### 3. Behavior

| Behavior | Description |
|----------|-------------|
| `aggressive` | Presses forward. Accuracy +8%. Reads patterns (trained_guard). |
| `testing` | Adapts. Reads last player action. Repeated moves give +20% accuracy. |
| `passive` | Holds position. Does not attack unless provoked. |
| `defensive` | Waits and counters. Only attacks when player strikes first. |
| `manipulative` | 60% psychological (doubt/resolve), 40% physical. No damage = 100% psychological. |

### 4. Special Mechanic

Every enemy changes one rule of combat. New `special.id` values require engine support in `combat.py`.

### 5. Moral Resolution

| Resolution | Effect |
|------------|--------|
| `kill: True` | Standard combat victory available |
| `free: True` | **Release** action appears at low HP |
| `understand: True` | Thematic — unlocks post-combat content via scene flags |
| `listen: True` | **Listen** action appears (passive enemies only) |
| `expose: True` | Metadata — **Expose** action added via special hook |

---

## Enemies

### Royal Sergeant
**Identity:** Sold soldier — obedient to the crown, not to conscience.

| Stat | Value |
|------|-------|
| Threat | 2 |
| HP | 80 |
| Faith | 15 |
| Resolve | 65 |
| Behavior | Aggressive |

**Special — Trained Guard:**
If the player uses the same action two turns in a row, the sergeant reads it.
His next attack hits with +20% accuracy.

**Resolution:** Kill, Free (disarm and release), Understand (he's following orders).

---

### Inquisitor's Agent
**Identity:** Living doubt — weaponises uncertainty as effectively as steel.
He genuinely believes he serves God. The horror is he might be right.

| Stat | Value |
|------|-------|
| Threat | 2 |
| HP | 55 |
| Faith | 70 |
| Resolve | 30 |
| Behavior | Manipulative |

**Special — Interrogator:**
Every turn the player does not deal damage, Doubt +4.
Silence is not safety. His high faith (70) also heavily resists `invoke_oath`.

**Weapon effect:** Fear — resolve -8 on hit.

**Resolution:** Kill, Understand (there is nothing to save, but understanding what he is matters).

---

### Fallen Brother (Arnaud)
**Identity:** The broken oath made flesh — what the player could become.
He broke under interrogation. He is not a villain. He is a mirror.

| Stat | Value |
|------|-------|
| Threat | 4 |
| HP | 140 |
| Faith | 35 |
| Resolve | 80 |
| Behavior | Testing |
| Phases | 3 |

**Special — Broken Mirror:**
When the player uses `invoke_oath` successfully, Arnaud echoes the words — broken.
The invocation still lands, but Doubt +5. The player hears their oath in his voice.

**Weapon effect:** Corruption — doubt +6 on hit.

**Resolution:** Kill, Free (mercy — he accepts it, may want it), Understand.

**Loot:** Templar sword (100%).

---

### Broken Knight
**Identity:** The oath unkept — did not break under pressure; simply let go.
He stayed. He became hollow. He fights because it is the last thing he knows.

| Stat | Value |
|------|-------|
| Threat | 3 |
| HP | 110 |
| Faith | 8 |
| Resolve | 80 |
| Behavior | Defensive |

**Special — Oath-Memory:**
- Physical strikes (`strike`, `doubt_surge`) trigger a counter at +20% accuracy.
- `invoke_oath` suppresses the counter — he hesitates. His resolve -8.
- At HP < 30%: `invoke_oath` collapses him entirely (oath-memory resolution).
  Faith +20, Doubt -10. Counts as understanding, not killing.

**Resolution:** Kill, Understand (invoke_oath at low HP).

**Loot:** Kite shield (80%).

---

### Watching Heretic
**Identity:** A person who sees too much — not evil, just unable to un-see.
He does not want to fight. He wants to be heard. Attacking him is the wrong answer.

| Stat | Value |
|------|-------|
| Threat | 1 |
| HP | 40 (→ 110 after transformation) |
| Faith | 20 |
| Resolve | 60 |
| Behavior | Passive |

**Special — Doubt-Watcher:**
Every enemy turn, Doubt +3 — regardless of whether he attacks.
The longer the player waits, the more he unsettles them.
Physical strike triggers transformation: HP +70, behavior → aggressive.

**Resolution:**
- **Listen** (before attacking) — Doubt +15, Faith -5, Resolve +10. He speaks. Memory gained.
- **Kill** (after transformation) — standard. What he knew goes with him.

---

### Reliquary Beast
**Identity:** Bound into a relic — the relic is the anchor, the beast is the consequence.
Cannot be killed by ordinary violence. Has no faith. Has no hesitation.

| Stat | Value |
|------|-------|
| Threat | 5 |
| HP | 180 |
| Faith | 0 |
| Resolve | 20 |
| Behavior | Aggressive |

**Special — Relic-Bound:**
Physical attacks (`strike`, `doubt_surge`) deal 1 damage while the relic is intact.
Two valid paths:

| Path | Action | Cost | Effect |
|------|--------|------|--------|
| Faith | `invoke_oath` | Resolve -3 | Bypasses immunity entirely. Faith 0 = full damage. |
| Destroy | `destroy_relic` | Faith -20, Doubt +10 | Removes immunity. Normal combat resumes. |

`invoke_oath` is cheaper but requires sustained faith. `destroy_relic` is a one-time cost
that opens up physical attacks — better if faith is low.

**Resolution:** Kill only (it is not a person).

---

### False Saint
**Identity:** Offers real power at real cost. Lies about what it *is*, not what it gives.
You might not fight it at all. That is the point.

| Stat | Value |
|------|-------|
| Threat | 3 |
| HP | 60 |
| Faith | 90 |
| Resolve | 60 |
| Behavior | Manipulative (100% psychological — no physical attacks) |

**Special — False Sanctity:**
Three encounter paths:

| Path | Action | Cost | Outcome |
|------|--------|------|---------|
| Bargain | `accept_bargain` × 3 | Doubt +60 total | `false_blessed` flag. Saint departs. |
| Expose | `expose_saint` (faith ≥ 60) | Faith -5, Doubt +5 | Strips enemy faith to 0. Full damage resumes. |
| Violence | `strike` | Faith -3 per strike | Works. Spiritually costly. |

Accept bargain once: Faith +15, Doubt +20, HP +10. The power is real.
After three bargains the saint blesses the player and leaves without a fight.
`false_blessed` flag is set — scene content can respond to this.

**Resolution:** Kill, Expose (the right answer, but it costs something too).

---

### Hollow Choir
**Identity:** The Order's unspoken confessions — accumulated until they could speak.
No physical form. Cannot be fought with steel.
The player cannot trust the UI.

| Stat | Value |
|------|-------|
| Threat | 3 (scales with Doubt) |
| HP | 100 |
| Faith | 80 |
| Resolve | 80 |
| Behavior | Manipulative |

**Special — Choir Distortion:**
Replaces ALL standard actions with choir vocabulary. Labels are counterintuitive by design.

| Label | Action ID | What it actually does |
|-------|-----------|----------------------|
| *Confess* | `confess` | **Offensive.** Truth damages the choir. Faith +3, Doubt -5, Resolve -5. |
| *Kneel* | `kneel` | Choir pauses its turn. But: Doubt +10, Resolve -8. |
| *Silence* | `silence` | **Strongest weapon.** Faith attack, bypasses resistance. Doubt -8. |
| *Open* | `open` | 30–50 damage + Resolve -20, Doubt +20. High risk. |
| *Name them* | `dissolve_choir` | Appears after 4 confessions. Understand resolution: Faith +20, Doubt -15. |
| *Seal it* | `flee` | Standard flee. |

**Enemy turn damage** = base (5–12) + player.Doubt ÷ 8. The more doubt, the worse it gets.

**Resolution:** Dissolve (name them — 4 confessions required). Cannot be killed conventionally.

---

## Experience Arc

**Act I — The Sacred:**
- Feels holy. Warm light at the edges of perception.
- Faith abilities work cleanly — prayers answered, resolve holds.

**Act II — The Fracture:**
- Contradictions surface. Something is off in the silence after prayer.
- Faith abilities become unstable: sometimes stronger, sometimes wrong.
- Doubt rises not from weakness but from paying attention.

**Act III — The Choice:**
- No monster. No boss. Only a door, and a question:

> Do you want to know?

The player chooses. Both paths are valid. Neither is safe.

---

## Faith vs Doubt Builds

**Faith build:**
- Abilities are stable and powerful
- Can resist the truth — prayers hold, resolve does not crack
- Pays a price: never fully understands what is happening
- Ending: walks away intact, but blind

**Doubt build:**
- Sees more — hidden dialogue, deeper scene variants, things Faith-built players never encounter
- Begins to fracture — abilities destabilize, some fail at critical moments
- Pays a price: the closer you get, the less you can hold together
- Ending: understands — and must decide what to do with that

Neither build is wrong. Both are complete experiences.

---

## Engine

Flask/Python backend + vanilla JS frontend. Stateless HTTP; player state in Flask session.

**Key files:**
- `engine/state.py` — PlayerState dataclass (body, faith, resolve, doubt)
- `engine/combat.py` — Oath & Judgment engine; enemy behavior/special/resolution hooks
- `engine/scene_web.py` — Scene beat processor
- `engine/conditions.py` — Condition DSL
- `content/game_config.py` — Stat bounds, equipment, HUD, start scene
- `content/enemies.py` — All enemy definitions (data only, no engine changes to add enemies)
- `content/act1.py`, `content/act2.py` — Scene content

**Adding a new enemy special mechanic:**
1. Add `special.id` to enemy in `enemies.py`
2. Add hook in `_apply_special()` in `combat.py`
3. If behavior is new: add branch in `_resolve_enemy_turn()`
4. If action is new: add to `get_player_actions()` and `resolve_action()`

---

## Open Questions

1. Act I opens at the commandery, night of the arrests (`commandery_night`). First combat encounter TBD.
2. How does the Doubt threshold (≥ 60) mechanically affect scene content beyond combat?
3. What triggers `false_blessed` consequences in scene content?
4. Act III structure — how does the player reach the door?
