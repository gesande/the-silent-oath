"""Tests for engine/conditions.py — condition evaluator."""

import pytest
from engine.state import PlayerState
from engine.conditions import eval_condition


@pytest.fixture
def player():
    s = PlayerState()
    s.inventory = []
    s.equipped = {"weapon": "Templar Sword", "shield": "", "off_hand": ""}
    s.faith = 50
    s.doubt = 0
    return s


# ── None / callable ───────────────────────────────────────────


def test_none_always_true(player):
    assert eval_condition(None, player) is True


def test_callable_true(player):
    assert eval_condition(lambda s: True, player) is True


def test_callable_false(player):
    assert eval_condition(lambda s: False, player) is False


def test_callable_receives_state(player):
    player.faith = 75
    assert eval_condition(lambda s: s.faith >= 70, player) is True


# ── flag ──────────────────────────────────────────────────────


def test_flag_true_when_set(player):
    player.set_flag("chapel_visited")
    assert eval_condition({"flag": "chapel_visited"}, player) is True


def test_flag_false_when_unset(player):
    assert eval_condition({"flag": "chapel_visited"}, player) is False


def test_flag_false_when_explicitly_false(player):
    player.set_flag("chapel_visited", False)
    assert eval_condition({"flag": "chapel_visited"}, player) is False


# ── memory ────────────────────────────────────────────────────


def test_memory_true_when_present(player):
    player.add_memory("arnaud", "Brother Arnaud")
    assert eval_condition({"memory": "arnaud"}, player) is True


def test_memory_false_when_absent(player):
    assert eval_condition({"memory": "arnaud"}, player) is False


# ── has_item ──────────────────────────────────────────────────


def test_has_item_true(player):
    player.inventory.append("holy water")
    assert eval_condition({"has_item": "holy water"}, player) is True


def test_has_item_false(player):
    assert eval_condition({"has_item": "holy water"}, player) is False


# ── equipped ──────────────────────────────────────────────────


def test_equipped_true(player):
    assert eval_condition({"equipped": "Templar Sword"}, player) is True


def test_equipped_false_wrong_weapon(player):
    assert eval_condition({"equipped": "dagger"}, player) is False


def test_equipped_false_no_weapon(player):
    player.equipped["weapon"] = ""
    assert eval_condition({"equipped": "Templar Sword"}, player) is False


# ── stat_gte ──────────────────────────────────────────────────


def test_stat_gte_true_equal(player):
    player.faith = 60
    assert eval_condition({"stat_gte": "faith", "value": 60}, player) is True


def test_stat_gte_true_above(player):
    player.faith = 80
    assert eval_condition({"stat_gte": "faith", "value": 60}, player) is True


def test_stat_gte_false_below(player):
    player.faith = 40
    assert eval_condition({"stat_gte": "faith", "value": 60}, player) is False


def test_stat_gte_doubt(player):
    player.doubt = 55
    assert eval_condition({"stat_gte": "doubt", "value": 60}, player) is False
    player.doubt = 60
    assert eval_condition({"stat_gte": "doubt", "value": 60}, player) is True


# ── not ───────────────────────────────────────────────────────


def test_not_inverts_true(player):
    player.set_flag("gate_open")
    assert eval_condition({"not": {"flag": "gate_open"}}, player) is False


def test_not_inverts_false(player):
    assert eval_condition({"not": {"flag": "gate_open"}}, player) is True


def test_not_nested(player):
    player.set_flag("gate_open")
    assert eval_condition({"not": {"not": {"flag": "gate_open"}}}, player) is True


# ── and ───────────────────────────────────────────────────────


def test_and_all_true(player):
    player.set_flag("flag_a")
    player.set_flag("flag_b")
    cond = {"and": [{"flag": "flag_a"}, {"flag": "flag_b"}]}
    assert eval_condition(cond, player) is True


def test_and_one_false(player):
    player.set_flag("flag_a")
    cond = {"and": [{"flag": "flag_a"}, {"flag": "flag_b"}]}
    assert eval_condition(cond, player) is False


def test_and_all_false(player):
    cond = {"and": [{"flag": "flag_a"}, {"flag": "flag_b"}]}
    assert eval_condition(cond, player) is False


def test_and_empty_true(player):
    assert eval_condition({"and": []}, player) is True


# ── or ────────────────────────────────────────────────────────


def test_or_all_true(player):
    player.set_flag("flag_a")
    player.set_flag("flag_b")
    cond = {"or": [{"flag": "flag_a"}, {"flag": "flag_b"}]}
    assert eval_condition(cond, player) is True


def test_or_one_true(player):
    player.set_flag("flag_a")
    cond = {"or": [{"flag": "flag_a"}, {"flag": "flag_b"}]}
    assert eval_condition(cond, player) is True


def test_or_all_false(player):
    cond = {"or": [{"flag": "flag_a"}, {"flag": "flag_b"}]}
    assert eval_condition(cond, player) is False


def test_or_empty_false(player):
    assert eval_condition({"or": []}, player) is False


# ── nested combinators ────────────────────────────────────────


def test_and_with_or(player):
    player.set_flag("key")
    player.faith = 70
    # (has key) AND (faith >= 70 OR has holy water)
    cond = {
        "and": [
            {"flag": "key"},
            {"or": [{"stat_gte": "faith", "value": 70}, {"has_item": "holy water"}]},
        ]
    }
    assert eval_condition(cond, player) is True


def test_and_with_or_inner_false(player):
    player.set_flag("key")
    player.faith = 40
    cond = {
        "and": [
            {"flag": "key"},
            {"or": [{"stat_gte": "faith", "value": 70}, {"has_item": "holy water"}]},
        ]
    }
    assert eval_condition(cond, player) is False


def test_not_and(player):
    player.set_flag("flag_a")
    # NOT (flag_a AND flag_b) → True because flag_b is not set
    cond = {"not": {"and": [{"flag": "flag_a"}, {"flag": "flag_b"}]}}
    assert eval_condition(cond, player) is True


# ── unknown condition ─────────────────────────────────────────


def test_unknown_condition_raises(player):
    with pytest.raises(ValueError, match="Unknown condition"):
        eval_condition({"unknown_key": "value"}, player)
