# ============================================================
#  content/game_config.py
#  Game-specific configuration consumed by the engine.
# ============================================================

# ── Stat definitions ──────────────────────────────────────────
# All stats the engine should know about (used for bounds in
# modify_stat). Stats not listed here default to 0–100 clamping.
STATS = {
    "body": {"default": 50, "min": 0, "max": 100, "threshold": 20},  # is_broken  <
    "faith": {"default": 50, "min": 0, "max": 100, "threshold": 70},  # is_faithful >=
    "resolve": {"default": 50, "min": 0, "max": 100, "threshold": 20},  # is_broken  <
    "doubt": {"default": 0, "min": 0, "max": 100, "threshold": 60},  # is_doubting >=
}

# ── Equipment registry ─────────────────────────────────────────
# All equippable items. "slot" determines which equipped[slot] they fill.
# Higher "tier" items auto-equip when picked up, replacing lower tier.
# Slot-specific properties:
#   weapon → "damage_bonus": flat added to every strike
#   shield → "defense":      flat damage absorbed per incoming hit
EQUIPMENT = {
    "unarmed": {"slot": "weapon", "tier": 0, "damage_bonus": 0},
}

# ── HUD layout ────────────────────────────────────────────────
# Maps frontend HUD keys to stat names on PlayerState.
# "max_stat" is optional; when present, also outputs max_{key}.
HUD_STATS = [
    {"key": "faith", "stat": "faith"},
    {"key": "doubt", "stat": "doubt"},
    {"key": "resolve", "stat": "resolve"},
]

# ── Starting scene ─────────────────────────────────────────────
START_SCENE = "name_entry"
