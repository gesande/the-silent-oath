# ============================================================
#  engine/combat.py — Oath & Judgment
#  Combat is physical, mental, and spiritual simultaneously.
#  Returns structured dicts instead of printing to terminal.
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
    return "something that would fell a lesser man"


# ── Combat state lives in Flask session ───────────────────────
# combat_state = { "enemy": {...}, "log": [...], "over": bool, "won": bool }


def start_combat(
    enemy_key: str, player: PlayerState, variant: str | None = None
) -> dict:
    e = dict(ENEMIES[enemy_key])
    if variant:
        e.update(ENEMIES[enemy_key].get("variants", {}).get(variant, {}))
    e["current_hp"] = e["hp"]
    e["key"] = enemy_key
    e["effects"] = {}
    if e.get("phases"):
        e["current_phase"] = 1
    return {
        "enemy": e,
        "log": [f"You face {e['name']}."],
        "over": False,
        "won": False,
        "fled": False,
        "items_gained": [],
        "player_effects": {},
    }


def get_player_actions(combat_state: dict, player: PlayerState) -> list:
    e = combat_state["enemy"]
    actions = [
        {"id": "strike", "label": "Strike — drive forward with your blade"},
        {"id": "endure", "label": "Endure — hold your ground and weather the blow"},
        {"id": "invoke_oath", "label": "Invoke your Oath — call on your faith"},
    ]
    if e.get("shield") and not e.get("flanked"):
        actions.append(
            {"id": "flank", "label": "Flank — circle wide past the shield"}
        )
    if player.doubt >= 40:
        actions.append(
            {
                "id": "doubt_surge",
                "label": "Yield to Doubt — let the darkness move through you",
            }
        )
    if not e.get("phases") and e["current_hp"] < e["hp"] * 0.30:
        actions.append({"id": "mercy", "label": "Show Mercy — lower your weapon"})
    actions.append({"id": "flee", "label": "Retreat — fall back while you still can"})
    return actions


def resolve_action(action_id: str, combat_state: dict, player: PlayerState) -> dict:
    """Process one player action + enemy counter. Returns updated combat_state."""
    e = combat_state["enemy"]
    log = combat_state["log"]

    # ── Player effects tick (at turn start) ───────────────────
    _tick_player_effects(combat_state, player, log)
    if player.is_dead():
        _handle_player_death(player, combat_state, log)
        return combat_state

    # ── Endure flag (set last turn) ────────────────────────────
    enduring = combat_state.pop("enduring", False)

    # ── Player action ─────────────────────────────────────────
    if action_id == "strike":
        base = roll_range(8, 18)
        dmg = _player_damage(base, player)
        _hit_enemy(dmg, e, player, log)
        log.append(_strike_prose(dmg, e))

    elif action_id == "endure":
        combat_state["enduring"] = True
        player.modify_stat("resolve", 5)
        log.append(
            "You set your feet and raise your guard. Whatever comes, you will meet it."
        )
        log.append("Your resolve steadies.")

    elif action_id == "invoke_oath":
        # Faith powers the invocation. Low faith risks failure.
        if player.faith >= 50 or not chance(0.35):
            base = roll_range(15, 30)
            if player.faith >= 70:
                base = roll_range(20, 35)
            dmg = _player_damage(base, player)
            _hit_enemy(dmg, e, player, log)
            player.modify_stat("doubt", -3)
            log.append(_invoke_prose(dmg, player, e))
        else:
            player.modify_stat("resolve", -5)
            log.append(
                "You reach for the oath — and find silence. The words do not come."
            )
            log.append("The doubt is louder than the prayer.")
        player.modify_stat("resolve", -3)  # cost of invocation regardless

    elif action_id == "doubt_surge":
        if player.doubt >= 60:
            dmg = roll_range(30, 55)
            player.modify_stat("resolve", -10)
            log.append(
                "The doubt does not resist. It opens like a wound and something pours through."
            )
        else:
            dmg = roll_range(20, 40)
            log.append(
                "The doubt rises in your chest. You stop fighting it and let it push your arm."
            )
        _hit_enemy(dmg, e, player, log)
        player.modify_stat("doubt", 8)
        log.append(f"The blow lands. {e['name_short']} reels.")

    elif action_id == "flank":
        e["flanked"] = True
        log.append("You circle wide. The shield is no longer between you.")

    elif action_id == "mercy":
        e["current_hp"] = 0
        player.modify_stat("faith", 10)
        player.modify_stat("doubt", -5)
        log.append(
            "You lower your blade. It is a choice. Perhaps the only holy one left to you."
        )

    elif action_id == "flee":
        dmg = roll_range(10, 20)
        player.take_damage(dmg)
        player.modify_stat("faith", -5)
        player.modify_stat("resolve", -5)
        log.append("You fall back. The shame of it follows faster than any soldier.")
        log.append(f"You escape — at the cost of {damage_word(dmg)}.")
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
        if e.get("current_phase") == 1 and ratio <= 0.65:
            e["current_phase"] = 2
            log.append(e["phrases"].get("phase2", ""))
        elif e.get("current_phase") == 2 and ratio <= 0.30:
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
        _resolve_enemy_turn(e, player, log, combat_state, enduring)

    # ── Taunt ─────────────────────────────────────────────────
    if "taunt" in e.get("phrases", {}) and chance(0.35):
        log.append(random.choice(e["phrases"]["taunt"]))

    # ── Check player death ────────────────────────────────────
    if player.is_dead():
        _handle_player_death(player, combat_state, log)

    return combat_state


# ── Internal helpers ──────────────────────────────────────────


def _handle_player_death(player, combat_state, log):
    log.append("You fall.")
    log.append("Darkness. Then cold stone. You are not finished — not yet.")
    player.deaths += 1
    player.modify_stat("faith", -5)
    player.modify_stat("resolve", -5)
    player.health = player.max_health
    combat_state["over"] = True
    combat_state["died"] = True


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


def _resolve_enemy_turn(e, player, log, combat_state, enduring=False):
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
        if enduring:
            dmg = dmg // 2
        actual = player.take_damage(dmg)
        log.append(random.choice(e["phrases"]["hit"]))
        log.append(f"— {damage_word(actual)} taken.")
        # Special enemy weapon effects
        effect = e.get("weapon", {}).get("effect")
        if effect == "bleeding" and combat_state is not None:
            peff = combat_state.setdefault("player_effects", {})
            if not peff.get("bleeding"):
                peff["bleeding"] = 3
                log.append("The wound opens. You are bleeding.")
        if effect == "fear":
            player.modify_stat("resolve", -8)
            log.append("Something in you shrinks back. The resolve costs more here.")
        if effect == "corruption":
            player.modify_stat("doubt", 6)
            log.append(
                "The doubt is louder after that. The blow carries something with it."
            )
    else:
        log.append(random.choice(e["phrases"]["miss"]))


def _resolve_enemy_death(e, player, combat_state, log):
    log.append(random.choice(e["phrases"]["death"]))
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
    # Holding the oath through violence costs something too
    player.modify_stat("faith", 3)
    player.modify_stat("doubt", 2)


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
    if player is not None and e["current_hp"] > 0:
        weapon = player.equipped.get("weapon", "unarmed")
        effect = EQUIPMENT.get(weapon, {}).get("effect")
        if effect == "bleeding" and not e.get("effects", {}).get("bleeding"):
            e.setdefault("effects", {})["bleeding"] = 3
            if log is not None:
                log.append("The wound opens. Dark blood begins to run.")


def _player_damage(base, player):
    mod = base
    mod += EQUIPMENT.get(player.equipped.get("weapon", "unarmed"), {}).get(
        "damage_bonus", 0
    )
    if player.body > 60:
        mod += roll(4)
    if player.body < 20:
        mod -= roll(4)
    return max(1, mod)


def _strike_prose(dmg, e):
    name = e["name_short"]
    if dmg < 10:
        return f"Your blow glances off {name}. You leave a mark, nothing more."
    if dmg < 20:
        return f"The strike lands clean. {name} staggers."
    return f"You drive the blow home. {name} reels."


def _invoke_prose(dmg, player, e):
    name = e["name_short"]
    if player.faith >= 70:
        return (
            f"The oath holds. The blow falls with the weight of something older than the order. "
            f"{name} is driven back."
        )
    if dmg >= 25:
        return f"The words of the oath are rough in your throat — but they land. {name} recoils."
    return "The invocation is uncertain. But the blow finds its mark."
