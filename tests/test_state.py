"""Tests for engine/state.py — PlayerState methods."""

import pytest
import os
import tempfile
from unittest.mock import patch
from engine.state import PlayerState


@pytest.fixture
def player():
    s = PlayerState()
    s.inventory = []
    s.equipped = {"weapon": "unarmed", "shield": "", "off_hand": ""}
    return s


# ── modify_stat ───────────────────────────────────────────────


def test_modify_stat_increases(player):
    player.faith = 50
    player.modify_stat("faith", 10)
    assert player.faith == 60


def test_modify_stat_decreases(player):
    player.faith = 50
    player.modify_stat("faith", -15)
    assert player.faith == 35


def test_modify_stat_clamps_at_max(player):
    player.faith = 95
    player.modify_stat("faith", 20)
    assert player.faith == 100


def test_modify_stat_clamps_at_min(player):
    player.faith = 5
    player.modify_stat("faith", -20)
    assert player.faith == 0


def test_modify_stat_doubt_clamps_at_max(player):
    player.doubt = 90
    player.modify_stat("doubt", 20)
    assert player.doubt == 100


def test_modify_stat_doubt_clamps_at_min(player):
    player.doubt = 5
    player.modify_stat("doubt", -20)
    assert player.doubt == 0


def test_modify_stat_unknown_stat_no_error(player):
    # Unknown stats are silently ignored (getattr returns None → early return)
    player.modify_stat("nonexistent_stat", 10)  # should not raise


# ── take_damage / heal ────────────────────────────────────────


def test_take_damage_reduces_health(player):
    player.health = 100
    actual = player.take_damage(30)
    assert player.health == 70
    assert actual == 30


def test_take_damage_cannot_go_below_zero(player):
    player.health = 10
    actual = player.take_damage(50)
    assert player.health == 0
    assert actual == 10  # only 10 actual damage dealt


def test_take_damage_returns_actual(player):
    player.health = 20
    actual = player.take_damage(100)
    assert actual == 20


def test_heal_increases_health(player):
    player.health = 60
    actual = player.heal(20)
    assert player.health == 80
    assert actual == 20


def test_heal_cannot_exceed_max_health(player):
    player.health = 90
    actual = player.heal(20)
    assert player.health == 100
    assert actual == 10  # only 10 healed


def test_heal_at_full_health_heals_nothing(player):
    player.health = 100
    actual = player.heal(20)
    assert player.health == 100
    assert actual == 0


def test_is_dead_false_when_alive(player):
    player.health = 1
    assert player.is_dead() is False


def test_is_dead_true_at_zero(player):
    player.health = 0
    assert player.is_dead() is True


# ── add_item / remove_item / has_item ─────────────────────────


def test_add_item_appears_in_inventory(player):
    player.add_item("holy water")
    assert "holy water" in player.inventory


def test_add_item_no_duplicates(player):
    player.add_item("holy water")
    player.add_item("holy water")
    assert player.inventory.count("holy water") == 1


def test_has_item_true(player):
    player.add_item("holy water")
    assert player.has_item("holy water") is True


def test_has_item_false(player):
    assert player.has_item("holy water") is False


def test_remove_item_removes(player):
    player.add_item("holy water")
    result = player.remove_item("holy water")
    assert result is True
    assert "holy water" not in player.inventory


def test_remove_item_not_present_returns_false(player):
    result = player.remove_item("holy water")
    assert result is False


# ── add_item auto-equip ───────────────────────────────────────


def test_add_item_equips_higher_tier_weapon(player):
    # unarmed is tier 0; dagger is tier 1
    player.equipped["weapon"] = "unarmed"
    player.add_item("dagger")
    assert player.equipped["weapon"] == "dagger"


def test_add_item_does_not_replace_higher_tier(player):
    # Templar Sword is tier 2; dagger is tier 1
    player.equipped["weapon"] = "Templar Sword"
    player.add_item("dagger")
    assert player.equipped["weapon"] == "Templar Sword"


def test_add_item_equips_shield(player):
    player.add_item("Kite Shield")
    assert player.equipped["shield"] == "Kite Shield"


def test_add_item_non_equipment_not_equipped(player):
    player.add_item("holy water")
    # holy water has no EQUIPMENT entry — equipped slots unchanged
    assert player.equipped["weapon"] == "unarmed"


# ── threshold derived properties ──────────────────────────────


def test_is_broken_body_below_threshold(player):
    player.body = 15
    player.resolve = 50
    assert player.is_broken() is True


def test_is_broken_resolve_below_threshold(player):
    player.body = 50
    player.resolve = 15
    assert player.is_broken() is True


def test_is_broken_false_when_both_above(player):
    player.body = 50
    player.resolve = 50
    assert player.is_broken() is False


def test_is_faithful_true_at_threshold(player):
    player.faith = 70
    assert player.is_faithful() is True


def test_is_faithful_false_below(player):
    player.faith = 69
    assert player.is_faithful() is False


def test_is_doubting_true_at_threshold(player):
    player.doubt = 60
    assert player.is_doubting() is True


def test_is_doubting_false_below(player):
    player.doubt = 59
    assert player.is_doubting() is False


# ── memory / flag helpers ─────────────────────────────────────


def test_add_memory_returns_true_first_time(player):
    assert player.add_memory("arnaud", "Brother Arnaud") is True


def test_add_memory_returns_false_if_already_present(player):
    player.add_memory("arnaud", "Brother Arnaud")
    assert player.add_memory("arnaud", "Brother Arnaud") is False


def test_has_memory_true(player):
    player.add_memory("arnaud", "Brother Arnaud")
    assert player.has_memory("arnaud") is True


def test_has_memory_false(player):
    assert player.has_memory("arnaud") is False


def test_set_flag_and_has_flag(player):
    player.set_flag("chapel_visited")
    assert player.has_flag("chapel_visited") is True


def test_has_flag_false_when_unset(player):
    assert player.has_flag("chapel_visited") is False


# ── save / load roundtrip ─────────────────────────────────────


def test_save_load_roundtrip(player):
    player.faith = 72
    player.doubt = 35
    player.add_memory("arnaud", "Brother Arnaud")
    player.set_flag("chapel_visited")
    player.add_item("holy water")

    with tempfile.TemporaryDirectory() as tmpdir:
        with patch(
            "engine.state.os.path.join", side_effect=lambda *a: os.path.join(*a)
        ), patch("engine.state.os.makedirs"), patch(
            "builtins.open",
            side_effect=lambda p, m="r", **kw: open(
                os.path.join(tmpdir, os.path.basename(p)), m, **kw
            ),
        ):
            pass  # skip patching approach — use direct to_dict/from_dict

    restored = PlayerState.from_dict(player.to_dict())
    assert restored.faith == 72
    assert restored.doubt == 35
    assert restored.has_memory("arnaud") is True
    assert restored.has_flag("chapel_visited") is True
    assert restored.has_item("holy water") is True


def test_to_dict_from_dict_preserves_inventory(player):
    player.add_item("holy water")
    player.add_item("false relic")
    restored = PlayerState.from_dict(player.to_dict())
    assert "holy water" in restored.inventory
    assert "false relic" in restored.inventory


def test_to_dict_from_dict_preserves_equipped(player):
    player.equipped["weapon"] = "Templar Sword"
    restored = PlayerState.from_dict(player.to_dict())
    assert restored.equipped["weapon"] == "Templar Sword"
