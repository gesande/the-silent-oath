"""Tests for engine/combat.py — action resolution."""

import pytest
from unittest.mock import patch
from engine.state import PlayerState
from engine.combat import start_combat, get_player_actions, resolve_action


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
