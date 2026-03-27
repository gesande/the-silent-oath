# Templar Knights — Game Design Document

## Concept

Text-adventure game set in the world of the Knights Templar, ~1307 (historically charged — just before Philip IV's persecution of the order).

## Hook

You play an aging Templar knight called back to the heart of the order's secret guardianship. The brotherhood is fracturing from within — some brothers want to use the power, some want to destroy it. You are caught in the middle.

The Templars are not protecting the world. They are keeping something terrible locked away.

## The Secret

An ancient, divine power beneath Jerusalem, Europe, and the northern wastes. Its nature is never explicitly revealed — different brothers believe different things (the Ark, the Holy Grail, something else). Ambiguity is intentional. The player becomes the interpreter.

> High Doubt does not reveal the truth — it reveals more possibilities.

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
