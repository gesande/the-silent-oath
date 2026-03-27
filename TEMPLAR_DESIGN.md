# Templar Knights — Game Design Document

## Concept

Text-adventure game set in the world of the Knights Templar, ~1307 (historically charged — just before Philip IV's persecution of the order).

## Hook

You play an aging Templar knight called back to the heart of the order's secret guardianship. The brotherhood is fracturing from within — some brothers want to use the power, some want to destroy it. You are caught in the middle.

The Templars are not protecting the world. They are keeping something terrible locked away.

## The Secret

> "Voima ei ole voima — se on totuus, jota ei voi kantaa."

What the Templars guard is not an object or a place. It is **knowledge** — absolute, divine, unbearable.

It appears as a cosmic phenomenon. The player experiences it as supernatural. But what it truly is: a truth so complete that encountering it shatters faith or transforms the person beyond return.

The rituals in Jerusalem, the monasteries in Scotland, the fortresses in Cyprus — they do not keep the power contained. They keep **understanding** at a distance.

> Some brothers have seen it. They are not the same.

Its nature is never explicitly named — different brothers believe different things (the Ark, the Grail, something older). Ambiguity is intentional and mechanical: the player becomes the interpreter.

**Why this works with the stat system:**
- **Doubt** grows as you approach the truth — not because you doubt God, but because you begin to *understand*
- **Faith** protects — not because it is correct, but because it holds you together
- At the end, the player may choose to *understand* — and pay the price

## Core Stats

| Stat | Description |
|------|-------------|
| **Body** | Physical strength and endurance |
| **Faith** | Belief — drives abilities and powers |
| **Resolve** | Mental endurance — resists breaking |
| **Doubt** | Grows during play. Destabilizes Faith abilities but makes them unpredictable and powerful |

**Key tension:** High Faith = strong, stable abilities. High Doubt = unstable but potentially more powerful effects. Doubt is not purely negative — it is a different kind of strength.

## Combat System: Oath & Judgment

Combat is not traditional HP-grinding. Every encounter is simultaneously:

- A **physical** struggle
- A **mental** struggle
- A **religious/spiritual** struggle

Oaths made by the player carry mechanical weight in both combat and narrative. Breaking an oath has consequences. Keeping one under pressure has rewards.

*Details TBD.*

## Engine

Built on top of the forgotten-among-the-fallen engine (Flask/Python + vanilla JS).

**Reuse:**
- Scene/beat system
- Condition DSL
- Flask session state
- HUD + frontend

**Rewrite:**
- `engine/combat.py` — entirely new Oath & Judgment mechanics

## Open Questions

1. Where does Act I begin? (Specific location — fortress, ship, Paris dungeon?)
2. Oath & Judgment — exact turn structure and resolution
3. How does Doubt mechanically affect Faith abilities?
4. What triggers Doubt growth — choices, failures, witnessing the power?
