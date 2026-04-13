# ============================================================
#  content/combat_prose.py
#  All combat narrative strings and prose helpers.
#  engine/combat.py contains only logic; text lives here.
# ============================================================

STRINGS = {
    # ── Endure ────────────────────────────────────────────────
    "endure_set": (
        "You set your feet and raise your guard. " "Whatever comes, you will meet it."
    ),
    "endure_steadies": "Your resolve steadies.",
    # ── Invoke oath ───────────────────────────────────────────
    "oath_fail_silence": (
        "You reach for the oath — and find silence. The words do not come."
    ),
    "oath_fail_doubt": "The doubt is louder than the prayer.",
    # ── Doubt surge ───────────────────────────────────────────
    "doubt_surge_high": (
        "The doubt does not resist. "
        "It opens like a wound and something pours through."
    ),
    "doubt_surge_low": (
        "The doubt rises in your chest. "
        "You stop fighting it and let it push your arm."
    ),
    "doubt_surge_lands": "The blow lands. {name} reels.",
    # ── Flank ─────────────────────────────────────────────────
    "flank": "You circle wide. The shield is no longer between you.",
    # ── Mercy ─────────────────────────────────────────────────
    "mercy": (
        "You lower your blade. It is a choice. "
        "Perhaps the only holy one left to you."
    ),
    # ── Flee ──────────────────────────────────────────────────
    "flee_1": "You fall back. The shame of it follows faster than any soldier.",
    "flee_2": "You escape — at the cost of {damage}.",
    # ── Consumables ───────────────────────────────────────────
    "consumable_trap_1": (
        "The warmth of it is wrong — too immediate, too easy. "
        "You feel it move through you and take something as it goes."
    ),
    "consumable_trap_2": "The relic was false. The doubt it left is not.",
    "consumable_holy_1": (
        "You uncork the vial. The water is cold and clear. "
        "Whatever it passed through to get here, it carried something through."
    ),
    "consumable_holy_heal": "You recover {healed} health.",
    # ── Player death ──────────────────────────────────────────
    "player_death_1": "You fall.",
    "player_death_2": ("Darkness. Then cold stone. You are not finished — not yet."),
    # ── Bleeding ──────────────────────────────────────────────
    "bleeding_player_tick": "Your wound bleeds — {dmg} damage.",
    "bleeding_slows": "The bleeding slows.",
    "bleeding_enemy_tick": "The wound bleeds. {name} loses {dmg}.",
    "bleeding_open_enemy": "The wound opens. Dark blood begins to run.",
    "bleeding_open_player": "The wound opens. You are bleeding.",
    # ── Weapon effects ────────────────────────────────────────
    "effect_fear": "Something in you shrinks back.",
    "effect_corruption": "The doubt is louder after that blow.",
    # ── Enemy turn ────────────────────────────────────────────
    "damage_taken": "— {damage} taken.",
    "manipulative_turn_end": "The doubt is louder. The resolve costs more.",
    # ── Special mechanic strings ──────────────────────────────
    "trained_guard_reads": "{name} adjusts. He's seen that move already.",
    "broken_mirror_echo": (
        "Arnaud mutters something — the same words, broken. "
        "Your oath sounds different coming back from his mouth."
    ),
    "false_sanctity_strike": "Striking what wears a saint's face costs something.",
    "relic_destroyed_fallback": "The relic shatters.",
}


def damage_word(dmg: int) -> str:
    if dmg <= 5:
        return "a graze"
    if dmg <= 12:
        return "a wound"
    if dmg <= 20:
        return "a serious wound"
    if dmg <= 30:
        return "a grievous blow"
    return "something that would fell a lesser man"


def strike_prose(dmg: int, name_short: str) -> str:
    if dmg < 10:
        return f"Your blow glances off {name_short}. You leave a mark, nothing more."
    if dmg < 20:
        return f"The strike lands clean. {name_short} staggers."
    return f"You drive the blow home. {name_short} reels."
