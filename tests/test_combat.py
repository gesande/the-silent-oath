"""Tests for engine/combat.py — action resolution."""

import pytest
from unittest.mock import patch
from engine.state import PlayerState
from engine.combat import (
    _player_damage,
    start_combat,
    get_player_actions,
    resolve_action,
)


@pytest.fixture
def player():
    s = PlayerState()
    s.health = 100
    s.faith = 50
    s.doubt = 0
    s.resolve = 50
    s.inventory = []
    s.equipped = {"weapon": "unarmed", "shield": "", "off_hand": ""}
    return s


@pytest.fixture
def sergeant_combat(player):
    return start_combat("royal_sergeant", player)


@pytest.fixture
def agent_combat(player):
    return start_combat("inquisitors_agent", player)


@pytest.fixture
def saint_combat(player):
    return start_combat("false_saint", player)


@pytest.fixture
def beast_combat(player):
    return start_combat("reliquary_beast", player)


@pytest.fixture
def choir_combat(player):
    return start_combat("hollow_choir", player)


# ── start_combat ──────────────────────────────────────────────


def test_start_combat_initialises_enemy(player):
    cs = start_combat("royal_sergeant", player)
    e = cs["enemy"]
    assert e["current_hp"] == e["hp"]
    assert cs["over"] is False
    assert cs["won"] is False
    assert cs["fled"] is False


def test_start_combat_relic_bound_sets_flag(player):
    cs = start_combat("reliquary_beast", player)
    assert cs["enemy"]["relic_intact"] is True


def test_start_combat_phases_sets_phase(player):
    cs = start_combat("fallen_brother", player)
    assert cs["enemy"]["current_phase"] == 1


# ── get_player_actions ────────────────────────────────────────


def test_actions_standard_always_present(player, sergeant_combat):
    ids = [a["id"] for a in get_player_actions(sergeant_combat, player)]
    assert "strike" in ids
    assert "endure" in ids
    assert "invoke_oath" in ids
    assert "flee" in ids


def test_actions_choir_replaces_standard(player, choir_combat):
    ids = [a["id"] for a in get_player_actions(choir_combat, player)]
    assert "confess" in ids
    assert "kneel" in ids
    assert "silence" in ids
    assert "open" in ids
    assert "strike" not in ids


def test_actions_dissolve_requires_four_confessions(player, choir_combat):
    ids = [a["id"] for a in get_player_actions(choir_combat, player)]
    assert "dissolve_choir" not in ids

    choir_combat["confessions_made"] = 4
    ids = [a["id"] for a in get_player_actions(choir_combat, player)]
    assert "dissolve_choir" in ids


def test_actions_destroy_relic_when_intact(player, beast_combat):
    ids = [a["id"] for a in get_player_actions(beast_combat, player)]
    assert "destroy_relic" in ids


def test_actions_destroy_relic_gone_after_shattered(player, beast_combat):
    beast_combat["enemy"]["relic_intact"] = False
    ids = [a["id"] for a in get_player_actions(beast_combat, player)]
    assert "destroy_relic" not in ids


def test_actions_expose_saint_requires_faith(player, saint_combat):
    player.faith = 50
    ids = [a["id"] for a in get_player_actions(saint_combat, player)]
    assert "expose_saint" not in ids

    player.faith = 60
    ids = [a["id"] for a in get_player_actions(saint_combat, player)]
    assert "expose_saint" in ids


def test_actions_doubt_surge_requires_doubt(player, sergeant_combat):
    player.doubt = 30
    ids = [a["id"] for a in get_player_actions(sergeant_combat, player)]
    assert "doubt_surge" not in ids

    player.doubt = 40
    ids = [a["id"] for a in get_player_actions(sergeant_combat, player)]
    assert "doubt_surge" in ids


def test_actions_consumable_holy_water_appears(player, sergeant_combat):
    player.add_item("holy water")
    ids = [a["id"] for a in get_player_actions(sergeant_combat, player)]
    assert "use_holy water" in ids


def test_actions_consumable_false_relic_appears(player, sergeant_combat):
    player.add_item("false relic")
    ids = [a["id"] for a in get_player_actions(sergeant_combat, player)]
    assert "use_false relic" in ids


def test_actions_no_consumable_without_item(player, sergeant_combat):
    ids = [a["id"] for a in get_player_actions(sergeant_combat, player)]
    assert "use_holy water" not in ids
    assert "use_false relic" not in ids


# ── resolve_action: consumables ───────────────────────────────


def test_holy_water_heals_player(player, sergeant_combat):
    player.health = 50
    player.add_item("holy water")
    with patch("engine.combat.roll_range", return_value=5), patch(
        "engine.combat.chance", return_value=False
    ):
        resolve_action("use_holy water", sergeant_combat, player)
    assert player.health > 50


def test_holy_water_raises_faith(player, sergeant_combat):
    player.faith = 50
    player.add_item("holy water")
    with patch("engine.combat.roll_range", return_value=5), patch(
        "engine.combat.chance", return_value=False
    ):
        resolve_action("use_holy water", sergeant_combat, player)
    assert player.faith == 55


def test_holy_water_removed_after_use(player, sergeant_combat):
    player.add_item("holy water")
    with patch("engine.combat.roll_range", return_value=5), patch(
        "engine.combat.chance", return_value=False
    ):
        resolve_action("use_holy water", sergeant_combat, player)
    assert not player.has_item("holy water")


def test_false_relic_raises_doubt(player, sergeant_combat):
    player.doubt = 0
    player.add_item("false relic")
    with patch("engine.combat.roll_range", return_value=5), patch(
        "engine.combat.chance", return_value=False
    ):
        resolve_action("use_false relic", sergeant_combat, player)
    assert player.doubt == 15


def test_false_relic_lowers_faith(player, sergeant_combat):
    player.faith = 50
    player.add_item("false relic")
    with patch("engine.combat.roll_range", return_value=5), patch(
        "engine.combat.chance", return_value=False
    ):
        resolve_action("use_false relic", sergeant_combat, player)
    assert player.faith == 45


def test_false_relic_removed_after_use(player, sergeant_combat):
    player.add_item("false relic")
    with patch("engine.combat.roll_range", return_value=5), patch(
        "engine.combat.chance", return_value=False
    ):
        resolve_action("use_false relic", sergeant_combat, player)
    assert not player.has_item("false relic")


def test_false_relic_does_not_heal(player, sergeant_combat):
    player.health = 50
    player.add_item("false relic")
    with patch("engine.combat.roll_range", return_value=5), patch(
        "engine.combat.chance", return_value=False
    ):
        resolve_action("use_false relic", sergeant_combat, player)
    assert player.health == 50


# ── resolve_action: relic_bound ───────────────────────────────


def test_strike_deals_one_damage_while_relic_intact(player, beast_combat):
    hp_before = beast_combat["enemy"]["current_hp"]
    with patch("engine.combat.roll_range", return_value=50), patch(
        "engine.combat.chance", return_value=False
    ):
        resolve_action("strike", beast_combat, player)
    assert beast_combat["enemy"]["current_hp"] == hp_before - 1


def test_invoke_oath_bypasses_relic(player, beast_combat):
    hp_before = beast_combat["enemy"]["current_hp"]
    with patch("engine.combat.roll_range", return_value=30), patch(
        "engine.combat.chance", return_value=True  # oath succeeds
    ):
        resolve_action("invoke_oath", beast_combat, player)
    assert beast_combat["enemy"]["current_hp"] < hp_before - 1


def test_destroy_relic_removes_immunity(player, beast_combat):
    assert beast_combat["enemy"]["relic_intact"] is True
    with patch("engine.combat.roll_range", return_value=5), patch(
        "engine.combat.chance", return_value=False
    ):
        resolve_action("destroy_relic", beast_combat, player)
    assert beast_combat["enemy"].get("relic_intact") is False


def test_destroy_relic_costs_faith_and_raises_doubt(player, beast_combat):
    player.faith = 60
    player.doubt = 10
    with patch("engine.combat.roll_range", return_value=5), patch(
        "engine.combat.chance", return_value=False
    ):
        resolve_action("destroy_relic", beast_combat, player)
    assert player.faith == 40
    assert player.doubt == 20


def test_strike_full_damage_after_relic_destroyed(player, beast_combat):
    beast_combat["enemy"]["relic_intact"] = False
    hp_before = beast_combat["enemy"]["current_hp"]
    with patch("engine.combat.roll_range", return_value=30), patch(
        "engine.combat.chance", return_value=False
    ):
        resolve_action("strike", beast_combat, player)
    assert beast_combat["enemy"]["current_hp"] < hp_before - 1


# ── resolve_action: false_sanctity ───────────────────────────


def test_accept_bargain_grants_faith_and_doubt(player, saint_combat):
    player.faith = 50
    player.doubt = 10
    with patch("engine.combat.roll_range", return_value=5), patch(
        "engine.combat.chance", return_value=False
    ):
        resolve_action("accept_bargain", saint_combat, player)
    assert player.faith == 65
    # bargain adds +20; manipulative enemy turn adds roll_range(3,6)=5
    assert player.doubt == 35


def test_three_bargains_trigger_false_blessing(player, saint_combat):
    saint_combat["bargains_taken"] = 2
    with patch("engine.combat.roll_range", return_value=5), patch(
        "engine.combat.chance", return_value=False
    ):
        cs = resolve_action("accept_bargain", saint_combat, player)
    assert cs["over"] is True
    assert cs["won"] is True
    assert cs.get("false_blessed") is True
    assert player.has_flag("false_blessed")


def test_two_bargains_do_not_trigger_false_blessing(player, saint_combat):
    saint_combat["bargains_taken"] = 1
    with patch("engine.combat.roll_range", return_value=5), patch(
        "engine.combat.chance", return_value=False
    ):
        cs = resolve_action("accept_bargain", saint_combat, player)
    assert cs["over"] is False


def test_expose_saint_zeroes_enemy_faith(player, saint_combat):
    player.faith = 70
    with patch("engine.combat.roll_range", return_value=30), patch(
        "engine.combat.chance", return_value=False
    ):
        resolve_action("expose_saint", saint_combat, player)
    assert saint_combat["enemy"]["faith"] == 0


def test_strike_costs_faith_against_saint(player, saint_combat):
    player.faith = 50
    with patch("engine.combat.roll_range", return_value=10), patch(
        "engine.combat.chance", return_value=False
    ):
        resolve_action("strike", saint_combat, player)
    assert player.faith == 47  # -3 from false_sanctity special


# ── resolve_action: choir_distortion ─────────────────────────


def test_confess_damages_choir(player, choir_combat):
    hp_before = choir_combat["enemy"]["current_hp"]
    with patch("engine.combat.roll_range", return_value=15), patch(
        "engine.combat.chance", return_value=False
    ):
        resolve_action("confess", choir_combat, player)
    assert choir_combat["enemy"]["current_hp"] < hp_before


def test_confess_increments_counter(player, choir_combat):
    with patch("engine.combat.roll_range", return_value=5), patch(
        "engine.combat.chance", return_value=False
    ):
        resolve_action("confess", choir_combat, player)
    assert choir_combat["confessions_made"] == 1


def test_confess_raises_faith_lowers_doubt(player, choir_combat):
    player.faith = 50
    player.doubt = 20
    with patch("engine.combat.roll_range", return_value=5), patch(
        "engine.combat.chance", return_value=False
    ):
        resolve_action("confess", choir_combat, player)
    assert player.faith == 53
    assert player.doubt == 15


def test_dissolve_choir_ends_combat(player, choir_combat):
    choir_combat["confessions_made"] = 4
    choir_combat["enemy"]["current_hp"] = 50
    with patch("engine.combat.roll_range", return_value=5), patch(
        "engine.combat.chance", return_value=False
    ):
        cs = resolve_action("dissolve_choir", choir_combat, player)
    assert cs["over"] is True
    assert cs["won"] is True


def test_dissolve_choir_raises_faith_and_resolve(player, choir_combat):
    choir_combat["confessions_made"] = 4
    choir_combat["enemy"]["current_hp"] = 50
    player.faith = 50
    player.resolve = 50
    player.doubt = 30
    with patch("engine.combat.roll_range", return_value=5), patch(
        "engine.combat.chance", return_value=False
    ):
        resolve_action("dissolve_choir", choir_combat, player)
    assert player.faith == 70
    assert player.resolve == 60
    assert player.doubt == 15


def test_kneel_pauses_choir_this_turn(player, choir_combat):
    # choir_paused is consumed within the same resolve_action call by _choir_turn.
    # Verify the effect: choir did not attack this turn, so player health is unchanged.
    with patch("engine.combat.roll_range", return_value=5), patch(
        "engine.combat.chance", return_value=False
    ):
        resolve_action("kneel", choir_combat, player)
    assert player.health == 100


def test_kneel_costs_resolve_and_raises_doubt(player, choir_combat):
    player.resolve = 50
    player.doubt = 10
    with patch("engine.combat.roll_range", return_value=5), patch(
        "engine.combat.chance", return_value=False
    ):
        resolve_action("kneel", choir_combat, player)
    assert player.resolve == 42
    assert player.doubt == 20


# ── resolve_action: interrogator ──────────────────────────────


def test_interrogator_no_damage_raises_doubt(player, agent_combat):
    # endure deals no damage → interrogator special adds Doubt +4
    player.doubt = 0
    agent_combat["enemy"]["current_hp"] = 9999
    with patch("engine.combat.roll_range", return_value=5), patch(
        "engine.combat.chance", return_value=False
    ):
        resolve_action("endure", agent_combat, player)
    assert player.doubt == 4


def test_interrogator_damage_no_doubt_penalty(player, agent_combat):
    # strike deals damage → interrogator special does not fire
    player.doubt = 0
    agent_combat["enemy"]["current_hp"] = 9999
    with patch("engine.combat.roll_range", return_value=10), patch(
        "engine.combat.chance", return_value=False
    ):
        resolve_action("strike", agent_combat, player)
    assert player.doubt == 0


# ── resolve_action: broken_mirror ────────────────────────────


def test_broken_mirror_invoke_oath_raises_doubt(player):
    cs = start_combat("fallen_brother", player)
    cs["enemy"]["current_hp"] = 9999
    player.faith = 50  # ensures invoke_oath always deals damage
    player.doubt = 0
    with patch("engine.combat.roll_range", return_value=20), patch(
        "engine.combat.chance", return_value=False
    ):
        resolve_action("invoke_oath", cs, player)
    # broken_mirror adds Doubt +5 on successful invoke_oath
    assert player.doubt >= 5


def test_broken_mirror_only_on_hit(player):
    # With faith=0 and chance=True, invoke_oath fails (dealt_damage=False).
    # broken_mirror should not add its +5 Doubt penalty.
    # Enemy hits with corruption (+6 Doubt) — so doubt without broken_mirror = 6.
    cs = start_combat("fallen_brother", player)
    cs["enemy"]["current_hp"] = 9999
    player.faith = 0
    player.doubt = 0
    with patch("engine.combat.roll_range", return_value=20), patch(
        "engine.combat.chance", return_value=True
    ):
        resolve_action("invoke_oath", cs, player)
    # broken_mirror did not fire: doubt is from enemy hit only, not +5 extra
    assert player.doubt == 6


# ── resolve_action: oath_memory ───────────────────────────────


def test_oath_memory_strike_triggers_counter(player):
    cs = start_combat("broken_knight", player)
    cs["enemy"]["current_hp"] = 9999
    player.health = 100
    # chance=True: counter hits player
    with patch("engine.combat.roll_range", return_value=10), patch(
        "engine.combat.chance", return_value=True
    ):
        resolve_action("strike", cs, player)
    assert player.health < 100


def test_oath_memory_invoke_oath_suppresses_counter(player):
    cs = start_combat("broken_knight", player)
    cs["enemy"]["current_hp"] = 9999
    player.health = 100
    player.faith = 50  # ensures oath fires
    # chance=True but faith_hesitation suppresses counter
    with patch("engine.combat.roll_range", return_value=20), patch(
        "engine.combat.chance", return_value=True
    ):
        resolve_action("invoke_oath", cs, player)
    # Knight hesitates — no counter, health unchanged from enemy
    assert player.health == 100


def test_oath_memory_collapse_at_low_hp(player):
    cs = start_combat("broken_knight", player)
    cs["enemy"]["current_hp"] = 30  # < 30% of 110
    player.faith = 50  # ensures oath always deals damage
    with patch("engine.combat.roll_range", return_value=20), patch(
        "engine.combat.chance", return_value=False
    ):
        result = resolve_action("invoke_oath", cs, player)
    assert result["won"] is True
    assert result["enemy"]["current_hp"] == 0


def test_oath_memory_collapse_raises_faith(player):
    cs = start_combat("broken_knight", player)
    cs["enemy"]["current_hp"] = 30
    player.faith = 50
    player.doubt = 20
    with patch("engine.combat.roll_range", return_value=20), patch(
        "engine.combat.chance", return_value=False
    ):
        resolve_action("invoke_oath", cs, player)
    # collapse: +20 faith, -10 doubt; invoke_oath: -3 doubt
    # _resolve_enemy_death skips violence rewards (collapsed=True)
    assert player.faith == 70
    assert player.doubt == 7


def test_oath_memory_collapse_sets_on_death_flag(player):
    cs = start_combat("broken_knight", player)
    cs["enemy"]["current_hp"] = 30
    player.faith = 50
    with patch("engine.combat.roll_range", return_value=20), patch(
        "engine.combat.chance", return_value=False
    ):
        resolve_action("invoke_oath", cs, player)
    # on_death flag and memory must fire even on non-violent collapse ending
    assert player.flags.get("broken_knight_defeated") is True
    assert "broken_knight" in player.memories


# ── resolve_action: doubt_watcher ────────────────────────────


def test_doubt_watcher_strike_transforms(player):
    cs = start_combat("watching_heretic", player)
    hp_before = cs["enemy"]["current_hp"]
    with patch("engine.combat.roll_range", return_value=10), patch(
        "engine.combat.chance", return_value=False
    ):
        resolve_action("strike", cs, player)
    assert cs.get("heretic_transformed") is True
    assert cs["enemy"]["behavior"] == "aggressive"
    assert cs["enemy"]["current_hp"] > hp_before  # HP surged on transform


def test_doubt_watcher_passive_raises_doubt(player):
    cs = start_combat("watching_heretic", player)
    player.doubt = 0
    with patch("engine.combat.roll_range", return_value=5), patch(
        "engine.combat.chance", return_value=False
    ):
        resolve_action("endure", cs, player)
    assert player.doubt == 3


def test_doubt_watcher_listen_available_before_transform(player):
    cs = start_combat("watching_heretic", player)
    ids = [a["id"] for a in get_player_actions(cs, player)]
    assert "listen" in ids


def test_doubt_watcher_listen_unavailable_after_transform(player):
    cs = start_combat("watching_heretic", player)
    cs["heretic_transformed"] = True
    cs["player_has_struck"] = True
    ids = [a["id"] for a in get_player_actions(cs, player)]
    assert "listen" not in ids


# ── resolve_action: resolution paths ─────────────────────────


def test_mercy_ends_combat(player, sergeant_combat):
    sergeant_combat["enemy"]["current_hp"] = 20
    with patch("engine.combat.roll_range", return_value=5), patch(
        "engine.combat.chance", return_value=False
    ):
        cs = resolve_action("mercy", sergeant_combat, player)
    assert cs["over"] is True
    assert cs["won"] is True


def test_mercy_raises_faith_lowers_doubt(player, sergeant_combat):
    player.faith = 50
    player.doubt = 20
    sergeant_combat["enemy"]["current_hp"] = 20
    with patch("engine.combat.roll_range", return_value=5), patch(
        "engine.combat.chance", return_value=False
    ):
        resolve_action("mercy", sergeant_combat, player)
    # mercy: +10 faith, -5 doubt; _resolve_enemy_death: +3 faith, +2 doubt
    assert player.faith == 63
    assert player.doubt == 17


def test_release_ends_combat_with_flag(player, sergeant_combat):
    sergeant_combat["enemy"]["current_hp"] = 20
    with patch("engine.combat.roll_range", return_value=5), patch(
        "engine.combat.chance", return_value=False
    ):
        cs = resolve_action("release", sergeant_combat, player)
    assert cs["over"] is True
    assert cs["won"] is True
    assert cs["released"] is True


def test_listen_ends_combat_peacefully(player):
    cs = start_combat("watching_heretic", player)
    with patch("engine.combat.roll_range", return_value=5), patch(
        "engine.combat.chance", return_value=False
    ):
        result = resolve_action("listen", cs, player)
    assert result["over"] is True
    assert result["won"] is True
    assert result.get("listened") is True


# ── resolve_action: flee ──────────────────────────────────────


def test_flee_ends_combat(player, sergeant_combat):
    with patch("engine.combat.roll_range", return_value=10), patch(
        "engine.combat.chance", return_value=False
    ):
        cs = resolve_action("flee", sergeant_combat, player)
    assert cs["fled"] is True
    assert cs["over"] is True
    assert cs["won"] is False


def test_flee_costs_health_faith_resolve(player, sergeant_combat):
    player.faith = 50
    player.resolve = 50
    with patch("engine.combat.roll_range", return_value=10), patch(
        "engine.combat.chance", return_value=False
    ):
        resolve_action("flee", sergeant_combat, player)
    assert player.health < 100
    assert player.faith == 45
    assert player.resolve == 45


# ── player death ──────────────────────────────────────────────


def test_player_death_ends_combat(player, sergeant_combat):
    player.health = 1
    sergeant_combat["enemy"]["current_hp"] = 9999
    # chance=True → enemy hits; roll_range for dmg returns 15
    with patch("engine.combat.roll_range", return_value=15), patch(
        "engine.combat.chance", return_value=True
    ):
        cs = resolve_action("endure", sergeant_combat, player)
    assert cs["over"] is True
    assert cs.get("died") is True


def test_player_death_increments_deaths(player, sergeant_combat):
    player.health = 1
    sergeant_combat["enemy"]["current_hp"] = 9999
    with patch("engine.combat.roll_range", return_value=15), patch(
        "engine.combat.chance", return_value=True
    ):
        resolve_action("endure", sergeant_combat, player)
    assert player.deaths == 1


def test_player_death_restores_health(player, sergeant_combat):
    player.health = 1
    sergeant_combat["enemy"]["current_hp"] = 9999
    with patch("engine.combat.roll_range", return_value=15), patch(
        "engine.combat.chance", return_value=True
    ):
        resolve_action("endure", sergeant_combat, player)
    assert player.health == player.max_health


# ── bleeding tick ─────────────────────────────────────────────


def test_bleeding_damages_player_each_turn(player, sergeant_combat):
    sergeant_combat["player_effects"]["bleeding"] = 2
    sergeant_combat["enemy"]["current_hp"] = 9999
    with patch("engine.combat.roll_range", return_value=5), patch(
        "engine.combat.chance", return_value=False
    ):
        resolve_action("endure", sergeant_combat, player)
    assert player.health < 100


def test_bleeding_decrements_counter(player, sergeant_combat):
    sergeant_combat["player_effects"]["bleeding"] = 2
    sergeant_combat["enemy"]["current_hp"] = 9999
    with patch("engine.combat.roll_range", return_value=5), patch(
        "engine.combat.chance", return_value=False
    ):
        resolve_action("endure", sergeant_combat, player)
    assert sergeant_combat["player_effects"]["bleeding"] == 1


def test_bleeding_removed_when_expired(player, sergeant_combat):
    sergeant_combat["player_effects"]["bleeding"] = 1
    sergeant_combat["enemy"]["current_hp"] = 9999
    with patch("engine.combat.roll_range", return_value=5), patch(
        "engine.combat.chance", return_value=False
    ):
        resolve_action("endure", sergeant_combat, player)
    assert "bleeding" not in sergeant_combat["player_effects"]


# ── trained_guard ─────────────────────────────────────────────


def test_trained_guard_same_action_reads_pattern(player, sergeant_combat):
    sergeant_combat["enemy"]["current_hp"] = 9999
    with patch("engine.combat.roll_range", return_value=10), patch(
        "engine.combat.chance", return_value=False
    ):
        resolve_action("strike", sergeant_combat, player)
        resolve_action("strike", sergeant_combat, player)
    assert sergeant_combat.get("guard_reads_pattern") is True


def test_trained_guard_different_action_clears_pattern(player, sergeant_combat):
    sergeant_combat["enemy"]["current_hp"] = 9999
    with patch("engine.combat.roll_range", return_value=10), patch(
        "engine.combat.chance", return_value=False
    ):
        resolve_action("strike", sergeant_combat, player)
        resolve_action("endure", sergeant_combat, player)
    assert sergeant_combat.get("guard_reads_pattern") is False


# ── COMBAT_MODS ───────────────────────────────────────────────


def test_high_body_adds_bonus(player):
    player.body = 70  # > 60 threshold
    with patch("engine.combat.roll", return_value=3):
        dmg = _player_damage(10, player, "strike")
    # base 10 + roll(4)=3 bonus
    assert dmg == 13


def test_normal_body_no_bonus(player):
    player.body = 50  # not > 60, not < 20
    player.resolve = 50
    with patch("engine.combat.roll", return_value=3):
        dmg = _player_damage(10, player, "strike")
    assert dmg == 10


def test_is_broken_adds_penalty(player):
    player.body = 15  # < 20 → is_broken
    player.resolve = 50
    with patch("engine.combat.roll", return_value=3):
        dmg = _player_damage(10, player, "strike")
    # base 10 - roll(4)=3 penalty
    assert dmg == 7


def test_is_faithful_bonus_on_invoke_oath(player):
    player.faith = 70  # is_faithful
    player.body = 50
    player.resolve = 50
    with patch("engine.combat.roll", return_value=4):
        dmg = _player_damage(20, player, "invoke_oath")
    # base 20 + roll(6)=4
    assert dmg == 24


def test_is_faithful_bonus_not_on_strike(player):
    player.faith = 70  # is_faithful — but action is strike, not invoke_oath
    player.body = 50
    player.resolve = 50
    with patch("engine.combat.roll", return_value=4):
        dmg = _player_damage(20, player, "strike")
    assert dmg == 20


def test_is_doubting_bonus_on_doubt_surge(player):
    player.doubt = 60  # is_doubting
    player.body = 50
    player.resolve = 50
    with patch("engine.combat.roll", return_value=5):
        dmg = _player_damage(15, player, "doubt_surge")
    # base 15 + roll(6)=5
    assert dmg == 20


def test_is_doubting_bonus_not_on_strike(player):
    player.doubt = 60  # is_doubting — but action is strike
    player.body = 50
    player.resolve = 50
    with patch("engine.combat.roll", return_value=5):
        dmg = _player_damage(15, player, "strike")
    assert dmg == 15


def test_damage_never_below_one(player):
    player.body = 15  # is_broken → penalty
    player.resolve = 50
    with patch("engine.combat.roll", return_value=6):
        dmg = _player_damage(1, player, "strike")
    assert dmg >= 1
