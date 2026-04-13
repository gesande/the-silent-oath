# ============================================================
#  engine/combat.py — Oath & Judgment
#  Combat is physical, mental, and spiritual simultaneously.
#
#  Enemy framework:
#    behavior  → aggressive | testing | passive | manipulative
#    special   → unique mechanic per enemy (id-driven hooks)
#    resolution → kill / free / understand
#    faith     → resistance to invoke_oath
# ============================================================
import random
from engine.state import PlayerState
from engine.dice import roll, roll_range, chance
from content.game_config import COMBAT_MODS, CONSUMABLES, EFFECTS, EQUIPMENT
from content.enemies import ENEMIES
from content.combat_prose import STRINGS, damage_word, strike_prose

S = STRINGS


# ── Combat state lives in Flask session ───────────────────────
# combat_state = {
#   "enemy":          {...},
#   "log":            [...],
#   "over":           bool,
#   "won":            bool,
#   "fled":           bool,
#   "released":       bool,
#   "items_gained":   [...],
#   "player_effects": {...},
#   "last_action":    str | None,   # for testing / trained_guard
#   "repeated_action":bool,         # same action used twice in a row
#   "player_has_struck": bool,      # for passive behavior
#   "enduring":       bool,         # player chose Endure last turn
# }


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
    if e.get("special", {}).get("id") == "relic_bound":
        e["relic_intact"] = True
    return {
        "enemy": e,
        "log": [f"You face {e['name']}."],
        "over": False,
        "won": False,
        "fled": False,
        "released": False,
        "items_gained": [],
        "player_effects": {},
        "last_action": None,
        "repeated_action": False,
        "player_has_struck": False,
        "enduring": False,
    }


def get_player_actions(combat_state: dict, player: PlayerState) -> list:
    e = combat_state["enemy"]
    resolution = e.get("resolution", {})
    hp_ratio = e["current_hp"] / e["hp"]
    special_id = e.get("special", {}).get("id")

    # ── Choir distortion: replace entire action list ───────────
    if special_id == "choir_distortion":
        actions = [
            {"id": "confess", "label": "Confess — speak a truth into the dark"},
            {"id": "kneel", "label": "Kneel — submit to the voices"},
            {"id": "silence", "label": "Silence — hold the oath against the noise"},
            {"id": "open", "label": "Open — let the voices through"},
        ]
        if combat_state.get("confessions_made", 0) >= 4:
            actions.append(
                {
                    "id": "dissolve_choir",
                    "label": "Name them — call each voice by its truth",
                }
            )
        actions.append({"id": "flee", "label": "Seal it — leave before it seals you"})
        return actions

    # ── Standard action list ───────────────────────────────────
    actions = [
        {"id": "strike", "label": "Strike — drive forward with your blade"},
        {"id": "endure", "label": "Endure — hold your ground and weather the blow"},
        {"id": "invoke_oath", "label": "Invoke your Oath — call on your faith"},
    ]
    if e.get("shield") and not e.get("flanked"):
        actions.append({"id": "flank", "label": "Flank — circle wide past the shield"})
    # Listen — available before attacking a passive enemy who can be understood
    if (
        resolution.get("listen")
        and not combat_state.get("player_has_struck")
        and not combat_state.get("heretic_transformed")
    ):
        actions.append({"id": "listen", "label": "Listen — hear what they have to say"})
    # Destroy relic — available while relic is intact
    if e.get("relic_intact"):
        actions.append(
            {
                "id": "destroy_relic",
                "label": "Destroy the Relic — shatter what binds it",
            }
        )
    # False saint bargain actions
    if special_id == "false_sanctity":
        actions.append(
            {"id": "accept_bargain", "label": "Accept — take what it offers"}
        )
        if player.faith >= 60:
            actions.append(
                {
                    "id": "expose_saint",
                    "label": "Expose it — call out the false sanctity",
                }
            )
    if player.doubt >= 40:
        actions.append(
            {
                "id": "doubt_surge",
                "label": "Yield to Doubt — let the darkness move through you",
            }
        )
    # Moral resolution options — appear at low enemy HP
    if hp_ratio < 0.30 and not e.get("phases"):
        if resolution.get("kill", True):
            actions.append({"id": "mercy", "label": "Show Mercy — lower your weapon"})
        if resolution.get("free"):
            actions.append({"id": "release", "label": "Release — let them go"})

    # Consumable items
    for item, cfg in CONSUMABLES.items():
        if player.has_item(item):
            actions.append({"id": f"use_{item}", "label": cfg["label"]})

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

    # ── Pull and reset turn flags ──────────────────────────────
    enduring = combat_state.pop("enduring", False)
    last_action = combat_state.get("last_action")
    repeated = action_id == last_action and action_id not in ("endure", "flee")
    combat_state["repeated_action"] = repeated
    combat_state["last_action"] = action_id

    # ── Player action ─────────────────────────────────────────
    dealt_damage = False

    if action_id == "strike":
        base = roll_range(8, 18)
        dmg = _player_damage(base, player, "strike")
        _hit_enemy(dmg, e, player, log)
        log.append(strike_prose(dmg, e["name_short"]))
        dealt_damage = True
        combat_state["player_has_struck"] = True

    elif action_id == "endure":
        combat_state["enduring"] = True
        player.modify_stat("resolve", 5)
        log.append(S["endure_set"])
        log.append(S["endure_steadies"])

    elif action_id == "invoke_oath":
        # Enemy faith provides resistance — high-faith enemies shrug off holy invocations
        faith_resist = 1.0 - (e.get("faith", 0) / 250.0)  # up to 40% reduction
        if player.faith >= 50 or not chance(0.35):
            base = roll_range(15, 30)
            if player.faith >= 70:
                base = roll_range(20, 35)
            dmg = int(_player_damage(base, player, "invoke_oath") * faith_resist)
            _hit_enemy(dmg, e, player, log, bypass_relic=True)
            player.modify_stat("doubt", -3)
            log.append(_invoke_prose(dmg, player, e, faith_resist))
            dealt_damage = True
        else:
            player.modify_stat("resolve", -5)
            log.append(S["oath_fail_silence"])
            log.append(S["oath_fail_doubt"])
        player.modify_stat("resolve", -3)  # cost of invocation regardless
        combat_state["player_has_struck"] = True

    elif action_id == "doubt_surge":
        if player.doubt >= 60:
            dmg = roll_range(30, 55)
            player.modify_stat("resolve", -10)
            log.append(S["doubt_surge_high"])
        else:
            dmg = roll_range(20, 40)
            log.append(S["doubt_surge_low"])
        _hit_enemy(dmg, e, player, log)
        player.modify_stat("doubt", 8)
        log.append(S["doubt_surge_lands"].format(name=e["name_short"]))
        dealt_damage = True
        combat_state["player_has_struck"] = True

    elif action_id == "flank":
        e["flanked"] = True
        log.append(S["flank"])

    elif action_id == "mercy":
        e["current_hp"] = 0
        player.modify_stat("faith", 10)
        player.modify_stat("doubt", -5)
        log.append(S["mercy"])

    elif action_id == "release":
        e["current_hp"] = 0
        player.modify_stat("faith", 15)
        player.modify_stat("doubt", -8)
        combat_state["released"] = True
        release_line = random.choice(e["phrases"].get("release", ["You let them go."]))
        log.append(release_line)

    elif action_id == "destroy_relic":
        e["relic_intact"] = False
        player.modify_stat("faith", -20)
        player.modify_stat("doubt", 10)
        log.append(e["phrases"].get("relic_destroyed", S["relic_destroyed_fallback"]))

    # ── Choir actions (choir_distortion special) ──────────────
    elif action_id == "confess":
        # Truth is offensive against voices in the dark
        dmg = roll_range(12, 22)
        _hit_enemy(dmg, e, player, log, bypass_relic=True)
        player.modify_stat("faith", 3)
        player.modify_stat("doubt", -5)
        player.modify_stat("resolve", -5)
        combat_state["confessions_made"] = combat_state.get("confessions_made", 0) + 1
        log.append(
            random.choice(
                e["phrases"].get("confess_recoil", ["The truth pushes them back."])
            )
        )
        dealt_damage = True

    elif action_id == "kneel":
        # Submit — choir pauses but doubt and resolve cost is heavy
        combat_state["choir_paused"] = True
        player.modify_stat("doubt", 10)
        player.modify_stat("resolve", -8)
        log.append(
            random.choice(e["phrases"].get("kneel_pleased", ["The choir stills."]))
        )

    elif action_id == "silence":
        # Hold the oath — faith attack, bypasses choir's faith resistance
        base = roll_range(15, 25)
        dmg = _player_damage(base, player, "silence")
        _hit_enemy(dmg, e, player, log, bypass_relic=True)
        player.modify_stat("doubt", -8)
        player.modify_stat("resolve", -5)
        log.append(
            random.choice(
                e["phrases"].get("silence_lands", ["The held oath cuts through."])
            )
        )
        dealt_damage = True

    elif action_id == "open":
        # Let them through — massive damage, massive self-cost
        dmg = roll_range(30, 50)
        _hit_enemy(dmg, e, player, log)
        player.modify_stat("resolve", -20)
        player.modify_stat("doubt", 20)
        log.append(
            random.choice(
                e["phrases"].get("open_consequence", ["The opening goes both ways."])
            )
        )
        dealt_damage = True

    elif action_id == "dissolve_choir":
        # Name each voice — understand resolution; choir dissolves
        e["current_hp"] = 0
        player.modify_stat("faith", 20)
        player.modify_stat("doubt", -15)
        player.modify_stat("resolve", 10)
        combat_state["listened"] = True  # reuse understood flag
        log.append(e["phrases"].get("dissolve", "You name them. They go quiet."))

    elif action_id == "accept_bargain":
        player.modify_stat("faith", 15)
        player.modify_stat("doubt", 20)
        player.heal(10)
        bargains = combat_state.get("bargains_taken", 0) + 1
        combat_state["bargains_taken"] = bargains
        log.append(
            random.choice(e["phrases"].get("bargain_accepted", ["You take it."]))
        )
        if bargains >= 3:
            # False blessing — saint departs, player is marked
            player.set_flag("false_blessed", True)
            combat_state["false_blessed"] = True
            combat_state["over"] = True
            combat_state["won"] = True
            log.append(
                e["phrases"].get("false_blessing", "It blesses you and departs.")
            )
            return combat_state

    elif action_id == "expose_saint":
        # Strip false faith — invoke_oath becomes fully effective afterward
        e["faith"] = 0
        dmg = roll_range(25, 40)
        _hit_enemy(dmg, e, player, log, bypass_relic=False)
        player.modify_stat("faith", -5)  # even true faith is shaken by this
        player.modify_stat("doubt", 5)
        log.append(
            random.choice(e["phrases"].get("exposed", ["The false light flickers."]))
        )

    elif action_id == "listen":
        # Understand resolution — ends combat peacefully; costs doubt, gains resolve
        e["current_hp"] = 0
        player.modify_stat("doubt", 15)  # what they say is unsettling
        player.modify_stat("faith", -5)  # shaken
        player.modify_stat("resolve", 10)  # you chose understanding
        combat_state["listened"] = True
        listen_line = random.choice(
            e["phrases"].get("listen", ["They speak. You listen."])
        )
        log.append(listen_line)
        on_listen = e.get("on_listen", {})
        if "memory" in on_listen:
            key, label = on_listen["memory"]
            player.add_memory(key, label)
        if "flag" in on_listen:
            player.set_flag(on_listen["flag"], True)

    elif action_id.startswith("use_"):
        item = action_id[4:]  # strip "use_"
        cfg = CONSUMABLES.get(item)
        if cfg and player.has_item(item):
            player.remove_item(item)
            if cfg.get("trap"):
                player.modify_stat("doubt", cfg.get("doubt", 0))
                player.modify_stat("faith", cfg.get("faith", 0))
                log.append(S["consumable_trap_1"])
                log.append(S["consumable_trap_2"])
            else:
                healed = player.heal(cfg.get("heal", 0))
                player.modify_stat("faith", cfg.get("faith", 0))
                log.append(S["consumable_holy_1"])
                if healed > 0:
                    log.append(S["consumable_holy_heal"].format(healed=healed))

    elif action_id == "flee":
        dmg = roll_range(10, 20)
        player.take_damage(dmg)
        player.modify_stat("faith", -5)
        player.modify_stat("resolve", -5)
        log.append(S["flee_1"])
        log.append(S["flee_2"].format(damage=damage_word(dmg)))
        combat_state["fled"] = True
        combat_state["over"] = True
        return combat_state

    # ── Special mechanic hook (post player action) ─────────────
    _apply_special(action_id, dealt_damage, e, player, combat_state, log)

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
    if "taunt" in e.get("phrases", {}) and chance(0.30):
        log.append(random.choice(e["phrases"]["taunt"]))

    # ── Check player death ────────────────────────────────────
    if player.is_dead():
        _handle_player_death(player, combat_state, log)

    return combat_state


# ── Special mechanic hooks ────────────────────────────────────


def _apply_special(action_id, dealt_damage, e, player, combat_state, log):
    special_id = e.get("special", {}).get("id")
    if not special_id:
        return

    if special_id == "trained_guard":
        # Reads repeated actions — flags for accuracy penalty on enemy turn
        if combat_state["repeated_action"]:
            combat_state["guard_reads_pattern"] = True
            log.append(S["trained_guard_reads"].format(name=e["name_short"]))
        else:
            combat_state["guard_reads_pattern"] = False

    elif special_id == "interrogator":
        # Silence is losing: no damage dealt = Doubt grows
        if not dealt_damage:
            player.modify_stat("doubt", 4)
            log.append(
                random.choice(
                    e["phrases"].get(
                        "manipulate", ["He uses the pause. The doubt fills it."]
                    )
                )
            )

    elif special_id == "broken_mirror":
        # invoke_oath echoes back broken — adds Doubt even on success
        if action_id == "invoke_oath" and dealt_damage:
            player.modify_stat("doubt", 5)
            log.append(S["broken_mirror_echo"])

    elif special_id == "false_sanctity":
        # Striking what wears a saint's face costs faith
        if action_id == "strike":
            player.modify_stat("faith", -3)
            log.append(S["false_sanctity_strike"])

    elif special_id == "relic_bound":
        # Log immunity when physical attacks are used against intact relic
        if e.get("relic_intact") and action_id in ("strike", "doubt_surge"):
            log.append(
                random.choice(
                    e["phrases"].get(
                        "immune",
                        ["The blow connects. The relic holds the wound closed."],
                    )
                )
            )

    elif special_id == "doubt_watcher":
        # Physical strikes trigger transformation
        if action_id in ("strike", "doubt_surge") and not combat_state.get(
            "heretic_transformed"
        ):
            combat_state["heretic_transformed"] = True
            combat_state["player_has_struck"] = True
            e["behavior"] = "aggressive"
            e["hp"] += 70
            e["current_hp"] = min(e["hp"], e["current_hp"] + 70)
            e["damage"] = (15, 28)
            e["accuracy"] = 0.75
            log.append(e["phrases"].get("transform", "Something changes in them."))

    elif special_id == "oath_memory":
        # Direct strikes trigger counter (flagged for defensive turn)
        combat_state["player_struck_this_turn"] = action_id in ("strike", "doubt_surge")
        if action_id == "invoke_oath":
            # Faith ability causes hesitation — suppresses counter
            combat_state["faith_hesitation"] = True
            combat_state["player_struck_this_turn"] = False
            e["resolve"] = max(0, e.get("resolve", 80) - 8)
            # Understand resolution: at low HP, invoke_oath collapses him
            hp_ratio = e["current_hp"] / e["hp"]
            if hp_ratio < 0.30 and dealt_damage:
                e["current_hp"] = 0
                player.modify_stat("faith", 20)
                player.modify_stat("doubt", -10)
                combat_state["collapsed"] = True
                log.append(
                    random.choice(
                        e["phrases"].get(
                            "collapse",
                            ["The oath reaches him. He does not rise."],
                        )
                    )
                )


# ── Enemy turn — routed by behavior ──────────────────────────


def _resolve_enemy_turn(e, player, log, combat_state, enduring=False):
    # Choir has its own turn logic entirely
    if e.get("special", {}).get("id") == "choir_distortion":
        _choir_turn(e, player, log, combat_state)
        return

    behavior = e.get("behavior", "aggressive")

    if behavior == "passive":
        if not combat_state.get("player_has_struck"):
            # doubt_watcher grows doubt even while standing still
            if e.get("special", {}).get("id") == "doubt_watcher":
                player.modify_stat("doubt", 3)
                log.append(random.choice(e["phrases"].get("watch", ["He watches."])))
            else:
                log.append(
                    random.choice(
                        e["phrases"].get("passive", ["It watches. It does not move."])
                    )
                )
            return

    if behavior == "defensive":
        # Does not initiate — only counters direct strikes
        # Counter is suppressed this turn if oath_memory triggered (faith hesitation)
        if combat_state.pop("faith_hesitation", False):
            line = random.choice(e["phrases"].get("faith_hesitation", []))
            if line:
                log.append(line)
            player.modify_stat("resolve", -8)  # the knight loses resolve too
            return
        if not combat_state.get("player_struck_this_turn"):
            # Holds position — no attack
            log.append(
                random.choice(e["phrases"].get("passive", ["He holds his ground."]))
            )
            return
        # Counter on direct strike
        log.append(random.choice(e["phrases"].get("counter", ["He answers."])))
        _physical_turn(e, player, log, combat_state, enduring, acc_bonus=0.20)
        return

    if behavior == "manipulative":
        # Enemies with no damage capability are always psychological
        no_damage = e.get("damage", (1, 1))[1] == 0
        if no_damage or chance(0.60):
            _manipulative_turn(e, player, log)
            return

    # Accuracy modifier by behavior and special state
    acc_bonus = 0.0
    if behavior == "aggressive":
        acc_bonus = 0.08
    if behavior == "testing":
        if combat_state.get("repeated_action"):
            line = random.choice(e["phrases"].get("testing", []))
            if line:
                log.append(line)
            acc_bonus = 0.20  # read the pattern
    if combat_state.get("guard_reads_pattern"):
        acc_bonus = max(acc_bonus, 0.20)

    _physical_turn(e, player, log, combat_state, enduring, acc_bonus)


def _choir_turn(e, player, log, combat_state):
    """The Hollow Choir's turn — psychological, scales with player Doubt."""
    if combat_state.pop("choir_paused", False):
        log.append(
            random.choice(e["phrases"].get("paused", ["The choir is briefly still."]))
        )
        return
    base_dmg = roll_range(5, 12)
    doubt_bonus = player.doubt // 8
    dmg = base_dmg + doubt_bonus
    player.take_damage(dmg)
    player.modify_stat("resolve", -roll_range(3, 6))
    log.append(
        random.choice(e["phrases"].get("choir_attack", ["The voices press in."]))
    )
    log.append(S["damage_taken"].format(damage=damage_word(dmg)))
    # Near dissolution — choir is more desperate
    if e["current_hp"] < e["hp"] * 0.40:
        log.append(
            random.choice(
                e["phrases"].get(
                    "near_dissolution", ["The remaining voices are louder."]
                )
            )
        )


def _manipulative_turn(e, player, log):
    """Psychological attack — no physical damage; targets resolve and doubt."""
    line = random.choice(e["phrases"].get("manipulate", ["He watches."]))
    log.append(line)
    player.modify_stat("doubt", roll_range(3, 6))
    player.modify_stat("resolve", -roll_range(2, 5))
    log.append(S["manipulative_turn_end"])


def _physical_turn(e, player, log, combat_state, enduring, acc_bonus):
    windup_opts = e.get("phrases", {}).get("windup", [])
    if windup_opts:
        log.append(random.choice(windup_opts))

    dmg_range = e["damage"]
    if e.get("shield") and not e.get("flanked"):
        dmg_range = (dmg_range[0] + 5, dmg_range[1] + 8)

    if chance(e["accuracy"] + acc_bonus):
        dmg = roll_range(*dmg_range)
        shield_def = EQUIPMENT.get(player.equipped.get("shield", ""), {}).get(
            "defense", 0
        )
        dmg = max(1, dmg - shield_def)
        if enduring:
            dmg = dmg // 2
        actual = player.take_damage(dmg)
        hit_opts = e.get("phrases", {}).get("hit", [])
        if hit_opts:
            log.append(random.choice(hit_opts))
        log.append(S["damage_taken"].format(damage=damage_word(actual)))

        # Weapon effects on hit
        effect = e.get("weapon", {}).get("effect")
        if effect == "bleeding" and combat_state is not None:
            peff = combat_state.setdefault("player_effects", {})
            _apply_effect("bleeding", peff, log, target="player")
        if effect == "fear":
            player.modify_stat("resolve", -8)
            log.append(S["effect_fear"])
        if effect == "corruption":
            player.modify_stat("doubt", 6)
            log.append(S["effect_corruption"])
    else:
        miss_opts = e.get("phrases", {}).get("miss", [])
        if miss_opts:
            log.append(random.choice(miss_opts))


# ── Shared helpers ────────────────────────────────────────────


def _apply_effect(effect_name, effects_dict, log=None, target="enemy"):
    """Apply a status effect from the EFFECTS registry. Does not stack."""
    cfg = EFFECTS.get(effect_name)
    if not cfg or effects_dict.get(effect_name):
        return
    duration = cfg["duration"]
    if isinstance(duration, tuple):
        duration = roll_range(*duration)
    effects_dict[effect_name] = duration
    if log is not None:
        open_key = f"{effect_name}_open_{target}"
        if open_key in S:
            log.append(S[open_key])


def _tick_effect(effect_name, effects_dict, hp_target, log, name_short=None):
    """Tick one effect entry. hp_target is a mutable dict with 'current_hp' key,
    or None (for player, where damage is applied externally)."""
    if effect_name not in effects_dict:
        return 0
    cfg = EFFECTS.get(effect_name, {})
    lo, hi = cfg.get("dmg", (4, 8))
    dmg = roll_range(lo, hi)
    if hp_target is not None:
        hp_target["current_hp"] = max(0, hp_target["current_hp"] - dmg)
        tick_key = f"{effect_name}_enemy_tick"
        log.append(S[tick_key].format(name=name_short, dmg=dmg))
    else:
        tick_key = f"{effect_name}_player_tick"
        log.append(S[tick_key].format(dmg=dmg))
    effects_dict[effect_name] -= 1
    if effects_dict[effect_name] <= 0:
        del effects_dict[effect_name]
        slow_key = f"{effect_name}_slow"
        if slow_key in S:
            log.append(S[slow_key])
    return dmg


def _handle_player_death(player, combat_state, log):
    log.append(S["player_death_1"])
    log.append(S["player_death_2"])
    player.deaths += 1
    player.modify_stat("faith", -5)
    player.modify_stat("resolve", -5)
    player.health = player.max_health
    combat_state["over"] = True
    combat_state["died"] = True


def _tick_player_effects(combat_state, player, log):
    effects = combat_state.get("player_effects", {})
    for effect_name in list(effects.keys()):
        dmg = _tick_effect(effect_name, effects, None, log)
        if dmg:
            player.take_damage(dmg)


def _resolve_enemy_death(e, player, combat_state, log):
    # Non-violent endings (listen, release, collapse) skip death prose and violence rewards
    violent_end = not any(
        combat_state.get(k) for k in ("listened", "released", "collapsed")
    )
    if violent_end:
        death_phrases = e.get("phrases", {}).get("death", [])
        if death_phrases:
            log.append(random.choice(death_phrases))
        # Winning through violence: faith up slightly, doubt up slightly
        player.modify_stat("faith", 3)
        player.modify_stat("doubt", 2)

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
    for effect_name in list(effects.keys()):
        _tick_effect(effect_name, effects, e, log, name_short=e["name_short"])


def _hit_enemy(dmg, e, player=None, log=None, bypass_relic=False):
    if e.get("relic_intact") and not bypass_relic:
        dmg = 1
    e["current_hp"] = max(0, e["current_hp"] - dmg)
    if player is not None and e["current_hp"] > 0:
        weapon = player.equipped.get("weapon", "unarmed")
        effect = EQUIPMENT.get(weapon, {}).get("effect")
        if effect == "bleeding":
            _apply_effect("bleeding", e.setdefault("effects", {}), log, target="enemy")


def _player_damage(base, player, action="strike"):
    mod = base
    mod += EQUIPMENT.get(player.equipped.get("weapon", "unarmed"), {}).get(
        "damage_bonus", 0
    )
    for m in COMBAT_MODS:
        if "fn" in m:
            applies = getattr(player, m["fn"])()
        else:
            applies = getattr(player, m["stat"], 0) > m["gt"]
        if "action" in m and m["action"] != action:
            applies = False
        if applies:
            if "bonus_die" in m:
                mod += roll(m["bonus_die"])
            if "penalty_die" in m:
                mod -= roll(m["penalty_die"])
    return max(1, mod)


def _invoke_prose(dmg, player, e, faith_resist):
    name = e["name_short"]
    resisted = faith_resist < 0.85  # enemy had meaningful faith resistance
    if resisted:
        if player.faith >= 70:
            return (
                f"The oath holds. The blow carries weight — but {name} has faith of his own. "
                f"It costs him something. Not everything."
            )
        return f"The invocation lands, diminished. {name}'s belief blunts it."
    if player.faith >= 70:
        return (
            f"The oath holds. The blow falls with the weight of something older than the order. "
            f"{name} is driven back."
        )
    if dmg >= 25:
        return f"The words of the oath are rough in your throat — but they land. {name} recoils."
    return "The invocation is uncertain. But the blow finds its mark."
