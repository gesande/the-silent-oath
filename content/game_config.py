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
#            "effect":       on-hit effect ("bleeding")
#   shield → "defense":      flat damage absorbed per incoming hit
EQUIPMENT = {
    "unarmed": {"slot": "weapon", "tier": 0, "damage_bonus": 0},
    "dagger": {"slot": "weapon", "tier": 1, "damage_bonus": 3},
    "Templar Sword": {"slot": "weapon", "tier": 2, "damage_bonus": 8},
    "Greatsword": {"slot": "weapon", "tier": 3, "damage_bonus": 14, "two_handed": True},
    "Kite Shield": {"slot": "shield", "tier": 1, "defense": 8},
    "Templar Shield": {"slot": "shield", "tier": 2, "defense": 12},
    "Lantern": {"slot": "off_hand", "tier": 1, "light": True},
}

# ── HUD layout ────────────────────────────────────────────────
# Maps frontend HUD keys to stat names on PlayerState.
# "max_stat" is optional; when present, also outputs max_{key}.
HUD_STATS = [
    {"key": "faith", "stat": "faith"},
    {"key": "doubt", "stat": "doubt"},
    {"key": "resolve", "stat": "resolve"},
]

# ── Combat config ─────────────────────────────────────────────
COMBAT_CONFIG = {
    # HP description thresholds — checked high-to-low, last entry is fallback
    "hp_desc": [
        (0.75, "Unbroken"),
        (0.50, "Wounded"),
        (0.25, "Bleeding"),
        (0.00, "Near Death"),
    ],
}

# ── Consumable items ──────────────────────────────────────────
# Items in player inventory that can be used during combat.
# "trap": True — item appears to offer help but delivers the opposite.
CONSUMABLES = {
    "holy water": {
        "label": "Use Holy Water — drink deep",
        "heal": 30,
        "faith": 5,
    },
    "false relic": {
        "label": "Invoke the Relic — call on its blessing",
        "trap": True,
        "doubt": 15,
        "faith": -5,
    },
}

# ── Starting scene ─────────────────────────────────────────────
START_SCENE = "name_entry"
