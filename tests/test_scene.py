"""Tests for engine/scene.py — scene rendering and choice application."""

import pytest
from unittest.mock import patch
from engine.state import PlayerState
from engine.scene import render_scene, apply_choice


# ── Minimal test scenes injected via patch ────────────────────

SIMPLE_SCENE = {
    "art": "test_art",
    "header": {"title": "Test Scene", "subtitle": "A subtitle"},
    "beats": [
        {"type": "prose", "text": "First paragraph."},
        {"type": "italic", "text": "An italicised line."},
    ],
    "choices": [
        {"label": "Go left", "next": "scene_left"},
        {"label": "Go right", "next": "scene_right"},
    ],
}

STAT_FLAG_SCENE = {
    "art": "test_art",
    "beats": [
        {"type": "stat", "changes": {"faith": 10, "doubt": -5}},
        {"type": "flag", "key": "test_flag"},
        {"type": "item", "item": "holy water", "action": "give"},
        {"type": "heal", "amount": 20},
    ],
    "choices": [],
    "next": "next_scene",
}

CONDITIONAL_PROSE_SCENE = {
    "art": "test_art",
    "beats": [
        {
            "type": "conditional_prose",
            "variants": [
                {"condition": {"flag": "special_flag"}, "text": "Variant A"},
                {"condition": None, "text": "Variant B (fallback)"},
            ],
        }
    ],
    "choices": [],
    "next": "next_scene",
}

GATED_BEAT_SCENE = {
    "art": "test_art",
    "beats": [
        {"type": "prose", "text": "Always visible."},
        {
            "type": "prose",
            "text": "Only if flag is set.",
            "condition": {"flag": "secret_flag"},
        },
    ],
    "choices": [],
    "next": "next_scene",
}

COMBAT_SCENE = {
    "art": "test_art",
    "beats": [
        {"type": "prose", "text": "Before combat."},
        {"type": "combat", "enemy": "royal_sergeant"},
        {"type": "prose", "text": "After combat — should not appear."},
    ],
    "next": "after_combat",
}

MEMORY_SCENE = {
    "art": "test_art",
    "beats": [
        {
            "type": "memory",
            "key": "test_memory",
            "label": "A Test Memory",
            "text": "You remember something.",
        }
    ],
    "choices": [],
    "next": "next_scene",
}

CHOICE_CONDITION_SCENE = {
    "art": "test_art",
    "beats": [],
    "choices": [
        {"label": "Always available", "next": "scene_a"},
        {
            "label": "Requires faith",
            "next": "scene_b",
            "condition": {"stat_gte": "faith", "value": 70},
        },
        {"label": "Also always available", "next": "scene_c"},
    ],
}

CHOICE_EFFECTS_SCENE = {
    "art": "test_art",
    "beats": [],
    "choices": [
        {
            "label": "Costly choice",
            "next": "scene_a",
            "effects": {"faith": -10, "doubt": 5},
            "flags": {"made_costly_choice": True},
            "item": "holy water",
            "heal": 15,
        }
    ],
}

AUTO_ADVANCE_SCENE = {
    "art": "test_art",
    "beats": [],  # no prose
    "choices": [],
    "next": "next_scene",
}

PROSE_NEXT_SCENE = {
    "art": "test_art",
    "beats": [{"type": "prose", "text": "Something to read."}],
    "choices": [],
    "next": "next_scene",
}

TEST_SCENES = {
    "simple": SIMPLE_SCENE,
    "stat_flag": STAT_FLAG_SCENE,
    "conditional_prose": CONDITIONAL_PROSE_SCENE,
    "gated_beat": GATED_BEAT_SCENE,
    "combat_scene": COMBAT_SCENE,
    "memory_scene": MEMORY_SCENE,
    "choice_condition": CHOICE_CONDITION_SCENE,
    "choice_effects": CHOICE_EFFECTS_SCENE,
    "auto_advance": AUTO_ADVANCE_SCENE,
    "prose_next": PROSE_NEXT_SCENE,
}


@pytest.fixture
def player():
    s = PlayerState()
    s.inventory = []
    s.equipped = {"weapon": "unarmed", "shield": "", "off_hand": ""}
    s.faith = 50
    s.doubt = 0
    return s


@pytest.fixture(autouse=True)
def patch_scenes():
    with patch("engine.scene.SCENES", TEST_SCENES):
        yield


# ── render_scene: basic output ────────────────────────────────


def test_unknown_scene_returns_error(player):
    out = render_scene("nonexistent", player)
    assert "error" in out


def test_render_returns_art_key(player):
    out = render_scene("simple", player)
    assert out["art_key"] == "test_art"


def test_render_returns_header(player):
    out = render_scene("simple", player)
    assert out["header"]["title"] == "Test Scene"


def test_render_prose_beats(player):
    out = render_scene("simple", player)
    texts = [p["text"] for p in out["paragraphs"]]
    assert "First paragraph." in texts


def test_render_italic_beats(player):
    out = render_scene("simple", player)
    italic = [p for p in out["paragraphs"] if p["type"] == "italic"]
    assert any(p["text"] == "An italicised line." for p in italic)


def test_render_choices(player):
    out = render_scene("simple", player)
    labels = [c["label"] for c in out["choices"]]
    assert "Go left" in labels
    assert "Go right" in labels


def test_render_hud_present(player):
    out = render_scene("simple", player)
    assert "hud" in out
    assert "hp" in out["hud"]


# ── render_scene: first visit side-effects ────────────────────


def test_stat_beat_applies_on_first_visit(player):
    player.faith = 50
    player.doubt = 10
    render_scene("stat_flag", player)
    assert player.faith == 60
    assert player.doubt == 5


def test_flag_beat_applies_on_first_visit(player):
    render_scene("stat_flag", player)
    assert player.has_flag("test_flag")


def test_item_beat_gives_item_on_first_visit(player):
    render_scene("stat_flag", player)
    assert player.has_item("holy water")


def test_heal_beat_applies_on_first_visit(player):
    player.health = 60
    render_scene("stat_flag", player)
    assert player.health == 80


# ── render_scene: repeat visit — no side-effects ─────────────


def test_stat_beat_skipped_on_repeat_visit(player):
    render_scene("stat_flag", player)
    faith_after_first = player.faith
    render_scene("stat_flag", player)
    assert player.faith == faith_after_first


def test_flag_beat_skipped_on_repeat_visit(player):
    render_scene("stat_flag", player)
    player.set_flag("test_flag", False)  # manually unset
    render_scene("stat_flag", player)
    # Flag was NOT re-applied on second visit
    assert not player.has_flag("test_flag")


def test_item_beat_skipped_on_repeat_visit(player):
    render_scene("stat_flag", player)
    player.remove_item("holy water")
    render_scene("stat_flag", player)
    assert not player.has_item("holy water")


def test_heal_beat_skipped_on_repeat_visit(player):
    player.health = 60
    render_scene("stat_flag", player)
    player.health = 60  # reduce again
    render_scene("stat_flag", player)
    assert player.health == 60  # no heal on second visit


# ── render_scene: conditional_prose ──────────────────────────


def test_conditional_prose_shows_matching_variant(player):
    player.set_flag("special_flag")
    out = render_scene("conditional_prose", player)
    texts = [p["text"] for p in out["paragraphs"]]
    assert "Variant A" in texts
    assert "Variant B (fallback)" not in texts


def test_conditional_prose_fallback_when_no_match(player):
    out = render_scene("conditional_prose", player)
    texts = [p["text"] for p in out["paragraphs"]]
    assert "Variant B (fallback)" in texts
    assert "Variant A" not in texts


# ── render_scene: gated beats ─────────────────────────────────


def test_gated_beat_hidden_when_condition_false(player):
    out = render_scene("gated_beat", player)
    texts = [p["text"] for p in out["paragraphs"]]
    assert "Always visible." in texts
    assert "Only if flag is set." not in texts


def test_gated_beat_shown_when_condition_true(player):
    player.set_flag("secret_flag")
    out = render_scene("gated_beat", player)
    texts = [p["text"] for p in out["paragraphs"]]
    assert "Only if flag is set." in texts


# ── render_scene: combat beat ─────────────────────────────────


def test_combat_beat_sets_combat(player):
    out = render_scene("combat_scene", player)
    assert out["combat"] is not None
    assert out["combat"]["enemy_key"] == "royal_sergeant"


def test_combat_beat_stops_further_beats(player):
    out = render_scene("combat_scene", player)
    texts = [p["text"] for p in out["paragraphs"]]
    assert "After combat — should not appear." not in texts


def test_combat_beat_skipped_if_already_defeated(player):
    player.set_flag("defeated_royal_sergeant")
    out = render_scene("combat_scene", player)
    assert out["combat"] is None


# ── render_scene: memory beat ─────────────────────────────────


def test_memory_beat_adds_memory(player):
    render_scene("memory_scene", player)
    assert player.has_memory("test_memory")


def test_memory_beat_appears_in_paragraphs(player):
    out = render_scene("memory_scene", player)
    memory_paras = [p for p in out["paragraphs"] if p["type"] == "memory"]
    assert any(p["text"] == "You remember something." for p in memory_paras)


def test_memory_beat_not_duplicated_on_repeat(player):
    render_scene("memory_scene", player)
    out = render_scene("memory_scene", player)
    memory_paras = [p for p in out["paragraphs"] if p["type"] == "memory"]
    assert len(memory_paras) == 0  # already in memories; not re-added


# ── render_scene: choice filtering ───────────────────────────


def test_choices_filtered_by_condition(player):
    player.faith = 50  # below 70 threshold
    out = render_scene("choice_condition", player)
    labels = [c["label"] for c in out["choices"]]
    assert "Always available" in labels
    assert "Also always available" in labels
    assert "Requires faith" not in labels


def test_choices_include_gated_when_condition_met(player):
    player.faith = 70
    out = render_scene("choice_condition", player)
    labels = [c["label"] for c in out["choices"]]
    assert "Requires faith" in labels


def test_choice_ids_are_sequential_after_filtering(player):
    player.faith = 50  # faith choice filtered out
    out = render_scene("choice_condition", player)
    ids = [c["id"] for c in out["choices"]]
    assert ids == ["0", "1"]


# ── render_scene: auto-advance / Continue button ──────────────


def test_no_prose_with_next_auto_advances(player):
    out = render_scene("auto_advance", player)
    assert out["next"] == "next_scene"
    assert out["choices"] == []


def test_prose_with_next_shows_continue_button(player):
    out = render_scene("prose_next", player)
    assert any(c["id"] == "__next__" for c in out["choices"])
    assert out["next"] is None


# ── apply_choice ──────────────────────────────────────────────


def test_apply_choice_returns_next_scene(player):
    next_key, _ = apply_choice("simple", "0", player)
    assert next_key == "scene_left"


def test_apply_choice_second_option(player):
    next_key, _ = apply_choice("simple", "1", player)
    assert next_key == "scene_right"


def test_apply_choice_applies_stat_effects(player):
    player.faith = 50
    player.doubt = 0
    apply_choice("choice_effects", "0", player)
    assert player.faith == 40
    assert player.doubt == 5


def test_apply_choice_sets_flags(player):
    apply_choice("choice_effects", "0", player)
    assert player.has_flag("made_costly_choice")


def test_apply_choice_gives_item(player):
    apply_choice("choice_effects", "0", player)
    assert player.has_item("holy water")


def test_apply_choice_heals_player(player):
    player.health = 70
    apply_choice("choice_effects", "0", player)
    assert player.health == 85


def test_apply_choice_respects_condition_filtering(player):
    player.faith = 50  # faith choice (index 1) filtered out
    next_key, _ = apply_choice("choice_condition", "1", player)
    # Index 1 after filtering is "Also always available" → scene_c
    assert next_key == "scene_c"


def test_apply_choice_out_of_bounds_returns_scene_key(player):
    # Out-of-bounds returns just the scene_key string (no narration tuple)
    result = apply_choice("simple", "99", player)
    assert result == "simple"


# ── _build_hud: hp_desc thresholds ───────────────────────────


def test_hud_hp_desc_unbroken(player):
    player.health = 100
    player.max_health = 100
    out = render_scene("simple", player)
    assert out["hud"]["hp_desc"] == "Unbroken"


def test_hud_hp_desc_wounded(player):
    player.health = 60
    player.max_health = 100
    out = render_scene("simple", player)
    assert out["hud"]["hp_desc"] == "Wounded"


def test_hud_hp_desc_bleeding(player):
    player.health = 30
    player.max_health = 100
    out = render_scene("simple", player)
    assert out["hud"]["hp_desc"] == "Bleeding"


def test_hud_hp_desc_near_death(player):
    player.health = 5
    player.max_health = 100
    out = render_scene("simple", player)
    assert out["hud"]["hp_desc"] == "Near Death"


def test_hud_includes_faith_and_doubt(player):
    player.faith = 65
    player.doubt = 30
    out = render_scene("simple", player)
    assert out["hud"]["faith"] == 65
    assert out["hud"]["doubt"] == 30


def test_hud_reflects_stat_changes_after_beat(player):
    player.faith = 50
    out = render_scene("stat_flag", player)
    assert out["hud"]["faith"] == 60
