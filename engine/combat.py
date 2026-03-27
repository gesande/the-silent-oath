# ============================================================
#  engine/combat.py
#  Combat engine.
#  Returns structured dicts instead of printing to terminal.
#  All prose, choices, and outcomes go through JSON to the UI.
# ============================================================
import random
from engine.state import PlayerState
from content.game_config import EQUIPMENT
from content.enemies import ENEMIES


# ── Dice ──────────────────────────────────────────────────────
def roll(sides):
    return random.randint(1, sides)


def roll_range(lo, hi):
    return random.randint(lo, hi)


def chance(p):
    return random.random() < p


def damage_word(dmg):
    if dmg <= 5:
        return "a graze"
    if dmg <= 12:
        return "a wound"
    if dmg <= 20:
        return "a serious wound"
    if dmg <= 30:
        return "a grievous blow"
    return "something that would kill a living man"


# ── Combat state lives in Flask session ───────────────────────
# combat_state = { "enemy": {...}, "log": [...], "over": bool, "won": bool }


def start_combat(
    enemy_key: str, player: PlayerState, variant: str | None = None
) -> dict:
    e = dict(ENEMIES[enemy_key])
    # Merge variant overrides (hp, damage, accuracy, weapon, etc.)
    if variant:
        e.update(ENEMIES[enemy_key].get("variants", {}).get(variant, {}))
    e["current_hp"] = e["hp"]
    e["key"] = enemy_key
    e["effects"] = {}
    # Apply curse scaling
    scale = 1.0 + player.curse_stacks * 0.06
    e["damage"] = (int(e["damage"][0] * scale), int(e["damage"][1] * scale))
    return {
        "enemy": e,
        "log": [f"You face {e['name']}."],
        "over": False,
        "won": False,
        "fled": False,
        "shards_gained": 0,
        "items_gained": [],
        "player_effects": {},
    }


def get_player_actions(combat_state: dict, player: PlayerState) -> list:
    e = combat_state["enemy"]
    actions = [
        {"id": "light", "label": "Strike — a fast, measured blow"},
        {"id": "heavy", "label": "Commit — a heavy, reckless strike"},
        {"id": "parry", "label": "Wait for the opening — attempt a parry"},
    ]
    if e.get("shield") and not e.get("flanked"):
        actions.append({"id": "flank", "label": "Circle wide — find the flank"})
    if player.echo_shards >= 100:
        actions.append({"id": "runic", "label": "Spend 100 shards — Runic Burst"})
    if not e.get("phases") and e["current_hp"] < e["hp"] * 0.30 and player.honour >= 40:
        actions.append({"id": "mercy", "label": "Lower your weapon"})
    actions.append({"id": "flee", "label": "Retreat into the fog"})
    return actions


def resolve_action(action_id: str, combat_state: dict, player: PlayerState) -> dict:
    """Process one player action + enemy counter. Returns updated combat_state."""
    e = combat_state["enemy"]
    log = combat_state["log"]

    # ── Player effects tick (at turn start) ───────────────────
    _tick_player_effects(combat_state, player, log)
    if player.is_dead():
        log.append("You fall.")
        log.append("When you wake, it will be at the Bone Cairn.")
        player.deaths += 1
        player.curse_stacks = min(5, player.curse_stacks + 1)
        player.echo_shards = player.echo_shards // 4
        player.health = player.max_health
        combat_state["over"] = True
        combat_state["died"] = True
        return combat_state

    # ── Player action ─────────────────────────────────────────
    if action_id == "light":
        base = roll_range(8, 18)
        dmg = _apply_mods(base, player, "light")
        _hit_enemy(dmg, e, player, log)
        player.modify_stat("wrath", 10)
        combo = player.flags.get("combo", 0) + 1
        player.set_flag("combo", min(combo, 3))
        log.append(_light_prose(dmg, e))

    elif action_id == "heavy":
        if chance(0.25):
            log.append(
                "You overcommit. The blow goes wide and you nearly lose your footing."
            )
        else:
            base = roll_range(18, 30)
            dmg = _apply_mods(base, player, "heavy")
            _hit_enemy(dmg, e, player, log)
            player.modify_stat("wrath", 18)
            log.append(_heavy_prose(dmg, e))

    elif action_id == "parry":
        if chance(0.45 + player.honour * 0.003):
            dmg = roll_range(12, 22)
            _hit_enemy(dmg, e, player, log)
            player.modify_stat("honour", 2)
            player.modify_stat("wrath", 25)
            log.append(
                "You read the blow perfectly. Your parry opens a gap — you answer it."
            )
            log.append(f"{e['name_short']} staggers. Your strike finds bone.")
        else:
            dmg = roll_range(*e["damage"]) // 2
            actual = player.take_damage(dmg)
            log.append("The parry fails. You mistimed it.")
            log.append(f"It costs you — {damage_word(actual)}.")

    elif action_id == "flank":
        e["flanked"] = True
        log.append("You circle wide. The shield is useless now. Its side is open.")

    elif action_id == "runic":
        player.echo_shards -= 100
        dmg = roll_range(35, 50)
        _hit_enemy(dmg, e, player, log)
        player.modify_stat("brutality", 5)
        player.wrath = 0
        log.append(
            "The shards burn cold in your fist. The rune ᚠ blooms across your weapon."
        )
        log.append(f"The burst hits {e['name_short']} like a memory of fire.")

    elif action_id == "mercy":
        e["current_hp"] = 0
        player.modify_stat("mercy", 10)
        player.modify_stat("honour", 5)
        log.append("You lower your weapon. It sinks to the ground. It does not rise.")

    elif action_id == "flee":
        dmg = roll_range(10, 20)
        player.take_damage(dmg)
        player.modify_stat("honour", -5)
        log.append("You run. The thing behind you is slower — but not by much.")
        log.append("You reach the fog. It doesn't follow into the fog.")
        log.append(f"You are {damage_word(dmg)} from the retreat.")
        combat_state["fled"] = True
        combat_state["over"] = True
        return combat_state

    # ── Check enemy death ─────────────────────────────────────
    if e["current_hp"] <= 0:
        _resolve_enemy_death(e, player, combat_state, log)
        combat_state["over"] = True
        combat_state["won"] = True
        return combat_state

    # ── Phase transitions (boss) ──────────────────────────────
    if e.get("phases"):
        ratio = e["current_hp"] / e["hp"]
        if e["current_phase"] == 1 and ratio <= 0.65:
            e["current_phase"] = 2
            log.append(e["phrases"].get("phase2", ""))
        elif e["current_phase"] == 2 and ratio <= 0.30:
            e["current_phase"] = 3
            log.append(e["phrases"].get("phase3", ""))

    # ── Effects tick ──────────────────────────────────────────
    if not combat_state["over"]:
        _tick_effects(e, log)
        if e["current_hp"] <= 0:
            _resolve_enemy_death(e, player, combat_state, log)
            combat_state["over"] = True
            combat_state["won"] = True
            return combat_state

    # ── Enemy turn ────────────────────────────────────────────
    if not combat_state["over"]:
        _resolve_enemy_turn(e, player, log, combat_state)

    # Taunt
    if "taunt" in e.get("phrases", {}) and chance(0.35):
        log.append(random.choice(e["phrases"]["taunt"]))

    # Check player death
    if player.is_dead():
        log.append("You fall.")
        log.append("When you wake, it will be at the Bone Cairn.")
        player.deaths += 1
        player.curse_stacks = min(5, player.curse_stacks + 1)
        player.echo_shards = player.echo_shards // 4
        player.health = player.max_health
        combat_state["over"] = True
        combat_state["died"] = True

    return combat_state


def _tick_player_effects(combat_state, player, log):
    effects = combat_state.get("player_effects", {})
    if "bleeding" in effects:
        dmg = roll_range(4, 8)
        player.take_damage(dmg)
        log.append(f"Your wound bleeds — {dmg} damage.")
        effects["bleeding"] -= 1
        if effects["bleeding"] <= 0:
            del effects["bleeding"]
            log.append("The bleeding slows.")


def _resolve_enemy_turn(e, player, log, combat_state=None):
    windup = random.choice(e["phrases"]["windup"])
    log.append(windup)
    dmg_range = e["damage"]
    if e.get("shield") and not e.get("flanked"):
        dmg_range = (dmg_range[0] + 5, dmg_range[1] + 8)
    if chance(e["accuracy"]):
        dmg = roll_range(*dmg_range)
        shield_def = EQUIPMENT.get(player.equipped.get("shield", ""), {}).get(
            "defense", 0
        )
        dmg = max(1, dmg - shield_def)
        actual = player.take_damage(dmg)
        player.modify_stat("wrath", 8)
        log.append(random.choice(e["phrases"]["hit"]))
        log.append(f"— {damage_word(actual)} taken.")
        # Enemy weapon effect
        effect = e.get("weapon", {}).get("effect")
        if effect == "bleeding" and combat_state is not None:
            peff = combat_state.setdefault("player_effects", {})
            if not peff.get("bleeding"):
                peff["bleeding"] = 3
                log.append("The wound opens. You are bleeding.")
    else:
        log.append(random.choice(e["phrases"]["miss"]))


def _resolve_enemy_death(e, player, combat_state, log):
    log.append(random.choice(e["phrases"]["death"]))
    lo, hi = e["shards"]
    shards = roll_range(lo, hi)
    player.echo_shards += shards
    combat_state["shards_gained"] = shards
    for item, prob in e.get("loot", []):
        if chance(prob):
            player.add_item(item)
            combat_state["items_gained"].append(item)
    on_death = e.get("on_death", {})
    if "flag" in on_death:
        player.set_flag(on_death["flag"], True)
    if "memory" in on_death:
        key, label = on_death["memory"]
        player.add_memory(key, label)
    player.set_flag(f"defeated_{e['key']}", True)


def _tick_effects(e, log):
    effects = e.get("effects", {})
    if "bleeding" in effects:
        dmg = roll_range(4, 8)
        e["current_hp"] = max(0, e["current_hp"] - dmg)
        log.append(f"The wound bleeds. {e['name_short']} loses {dmg}.")
        effects["bleeding"] -= 1
        if effects["bleeding"] <= 0:
            del effects["bleeding"]
            log.append("The bleeding slows.")


def _hit_enemy(dmg, e, player=None, log=None):
    e["current_hp"] = max(0, e["current_hp"] - dmg)
    # Weapon effect — apply on hit if weapon carries one
    if player is not None and e["current_hp"] > 0:
        weapon = player.equipped.get("weapon", "bare hands")
        effect = EQUIPMENT.get(weapon, {}).get("effect")
        if effect == "bleeding" and not e.get("effects", {}).get("bleeding"):
            e.setdefault("effects", {})["bleeding"] = 3
            if log is not None:
                log.append("The wound opens. Dark blood begins to run.")
    # Drain mechanic — sentinel heals from player wrath
    if e.get("drain") and player is not None:
        drain = min(e["drain_amount"], getattr(player, "wrath", 0))
        if drain > 0:
            player.wrath = max(0, player.wrath - drain)
            heal = min(drain, e["hp"] - e["current_hp"])
            e["current_hp"] = min(e["hp"], e["current_hp"] + heal)
            if log is not None:
                log.append(random.choice(e["phrases"]["drain_trigger"]))


def _apply_mods(base, player, kind):
    mod = base
    mod += EQUIPMENT.get(player.equipped.get("weapon", "bare hands"), {}).get(
        "damage_bonus", 0
    )
    if player.brutality > 50:
        mod += roll(6)
    if player.honour > 70 and kind == "light":
        mod += roll(4)
    if player.is_cursed():
        mod -= roll(4)
    return max(1, mod)


def _light_prose(dmg, e):
    name = e["name_short"]
    if dmg < 10:
        return f"Your blow glances off {name}. It slows, but does not stop."
    if dmg < 20:
        return f"The strike lands clean. {name} staggers."
    return f"You drive the blow deep. {name} reels."


def _heavy_prose(dmg, e):
    name = e["name_short"]
    if dmg < 15:
        return "A solid hit — the weight tells, even if the precision does not."
    if dmg < 25:
        return (
            f"{name} is staggered by the force. You feel the impact in your shoulders."
        )
    return (
        f"The heavy strike connects. {name} is driven back — something in it is broken."
    )
