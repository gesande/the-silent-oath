# ============================================================
#  engine/state.py
#  Game state — player stats, inventory, flags, memory.
#  Stats are hidden from the player; they shape the prose.
# ============================================================
from dataclasses import dataclass, field
from typing import Optional
import json
import os
from content.game_config import STATS, EQUIPMENT, START_SCENE


@dataclass
class PlayerState:
    # ── Identity (recovered through play) ────────────────────
    name: str = "the drengr"
    clan: str = "unknown"
    oath: str = "unknown"  # What oath was broken

    # ── Visible resources ─────────────────────────────────────
    echo_shards: int = 0
    curse_stacks: int = 0  # 0–5; world darkens as it rises

    # ── Hidden moral stats (0–100) ────────────────────────────
    # These shape which choices appear and how prose reads
    honour: int = 50  # affects how others treat you
    resolve: int = 50  # mental fortitude; low = hallucinations
    brutality: int = 0  # rises with violent choices
    mercy: int = 0  # rises with sparing / aiding others

    # ── Combat stats ──────────────────────────────────────────
    health: int = 100
    max_health: int = 100
    stamina: int = 100
    wrath: int = 0
    max_wrath: int = 100

    # ── Inventory ─────────────────────────────────────────────
    inventory: list = field(default_factory=list)
    equipped: dict = field(
        default_factory=lambda: {"weapon": "bare hands", "shield": ""}
    )

    # ── Story flags ───────────────────────────────────────────
    flags: dict = field(default_factory=dict)

    # ── Memory fragments recovered ────────────────────────────
    memories: list = field(default_factory=list)

    # ── World state ───────────────────────────────────────────
    current_scene: str = START_SCENE
    visited: list = field(default_factory=list)
    deaths: int = 0

    # ── Derived properties ────────────────────────────────────
    def is_cursed(self) -> bool:
        return self.curse_stacks >= STATS["curse_stacks"]["threshold"]

    def is_broken(self) -> bool:
        return self.resolve < STATS["resolve"]["threshold"]

    def is_honoured(self) -> bool:
        return self.honour >= STATS["honour"]["threshold"]

    def is_brutal(self) -> bool:
        return self.brutality >= STATS["brutality"]["threshold"]

    def has_memory(self, key: str) -> bool:
        return key in self.memories

    def has_flag(self, key: str) -> bool:
        return self.flags.get(key, False)

    def set_flag(self, key: str, value=True):
        self.flags[key] = value

    def add_memory(self, key: str, label: str):
        if key not in self.memories:
            self.memories.append(key)
            return True
        return False

    def modify_stat(self, stat: str, delta: int):
        val = getattr(self, stat, None)
        if val is None:
            return
        cfg = STATS.get(stat, {"min": 0, "max": 100})
        lo = cfg.get("min", 0)
        hi = cfg.get("max", 100)
        new_val = max(lo, val + delta)
        if hi is not None:
            new_val = min(hi, new_val)
        setattr(self, stat, new_val)

    def take_damage(self, amount: int) -> int:
        actual = min(self.health, amount)
        self.health -= actual
        return actual

    def heal(self, amount: int) -> int:
        actual = min(self.max_health - self.health, amount)
        self.health += actual
        return actual

    def is_dead(self) -> bool:
        return self.health <= 0

    def add_item(self, item: str):
        if item not in self.inventory:
            self.inventory.append(item)
        eq = EQUIPMENT.get(item)
        if eq:
            slot = eq["slot"]
            current_tier = EQUIPMENT.get(self.equipped.get(slot, ""), {}).get("tier", 0)
            if eq["tier"] > current_tier:
                self.equipped[slot] = item

    def has_item(self, item: str) -> bool:
        return item in self.inventory

    def remove_item(self, item: str) -> bool:
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False

    # ── Save / Load ───────────────────────────────────────────
    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}

    @classmethod
    def from_dict(cls, data: dict) -> "PlayerState":
        obj = cls()
        for k, v in data.items():
            if hasattr(obj, k):
                setattr(obj, k, v)
        return obj

    def save(self, slot: int = 0):
        saves_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "saves"
        )
        saves_dir = os.path.normpath(saves_dir)
        os.makedirs(saves_dir, exist_ok=True)
        path = os.path.join(saves_dir, f"save_{slot}.json")
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, slot: int = 0) -> Optional["PlayerState"]:
        saves_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "saves"
        )
        saves_dir = os.path.normpath(saves_dir)
        path = os.path.join(saves_dir, f"save_{slot}.json")
        if not os.path.exists(path):
            return None
        with open(path) as f:
            return cls.from_dict(json.load(f))
