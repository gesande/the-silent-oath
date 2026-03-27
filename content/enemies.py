# ============================================================
#  content/enemies.py
#  Enemy definitions consumed by the combat engine.
#  Add new enemies here — no engine changes needed.
#
#  Required fields:
#    name, name_short, hp, damage (tuple), accuracy, phrases
#  Optional:
#    shield, loot, on_death, weapon (effect), variants, phases
# ============================================================

ENEMIES = {
    # ── Royal sergeant ────────────────────────────────────────
    # A soldier of the French crown. Disciplined, armoured.
    # Sent to enforce Philip IV's arrest of the Templars.
    "royal_sergeant": {
        "name": "a royal sergeant",
        "name_short": "the sergeant",
        "hp": 80,
        "damage": (10, 18),
        "accuracy": 0.65,
        "shield": False,
        "loot": [],
        "phrases": {
            "windup": [
                "The sergeant advances, sword levelled.",
                "He moves with the economy of a man who has done this before.",
                "He reads the gap and presses forward.",
            ],
            "hit": [
                "The blow gets through.",
                "You take it on the shoulder — he knows what he's doing.",
                "He finds the gap in your guard.",
            ],
            "miss": [
                "You turn the blow aside.",
                "He overcorrects and the strike falls wide.",
                "The edge glances off your arm without purchase.",
            ],
            "death": [
                "He goes down slowly, like he still doesn't believe it.",
                "The sergeant falls. His king sent him here. His king does not come.",
                "He stops moving. The silence after is loud.",
            ],
            "taunt": [
                "\"Surrender and the Inquisition will hear your confession.\"",
                "\"Your order is finished, Templar. This is mercy.\"",
                "\"There are more of us outside.\"",
            ],
        },
    },

    # ── Inquisitor's agent ────────────────────────────────────
    # Not a warrior but dangerous in a different way.
    # His presence erodes resolve and feeds doubt.
    "inquisitors_agent": {
        "name": "an agent of the Inquisition",
        "name_short": "the agent",
        "hp": 55,
        "damage": (6, 14),
        "accuracy": 0.55,
        "shield": False,
        "weapon": {"effect": "fear"},
        "loot": [],
        "phrases": {
            "windup": [
                "He speaks as he moves — questions dressed as accusations.",
                "The agent circles, watching for the flinch.",
                "He does not hurry. He has learned that waiting does more work.",
            ],
            "hit": [
                "The blade is almost an afterthought. The words cut deeper.",
                "He wounds you — and while you bleed, asks what you believe.",
                "A shallow cut. He seems more interested in your face than the wound.",
            ],
            "miss": [
                "You step back. He lets you.",
                "The strike misses — he files it away and continues watching.",
                "He doesn't press. He is patient.",
            ],
            "death": [
                "He falls without ceremony. His questions die with him.",
                "The agent goes down. Whatever he was building toward, it ends here.",
                "He is quiet at last.",
            ],
            "taunt": [
                "\"Did you know what the order guarded? Did they tell you?\"",
                "\"Confession is not weakness. Silence is.\"",
                "\"Every brother we've questioned has said the same: they didn't know. "
                "Are you different?\"",
            ],
        },
    },

    # ── Fallen brother ────────────────────────────────────────
    # A Templar who broke under interrogation and now serves the crown.
    # Boss. Has phases. His corruption bleeds into the player.
    "fallen_brother": {
        "name": "Brother Arnaud — the broken oath",
        "name_short": "Arnaud",
        "hp": 140,
        "damage": (12, 22),
        "accuracy": 0.70,
        "shield": False,
        "weapon": {"effect": "corruption"},
        "phases": True,
        "loot": [("templar_sword", 1.0)],
        "on_death": {
            "flag": "arnaud_defeated",
            "memory": ("arnaud", "Brother Arnaud"),
        },
        "phrases": {
            "windup": [
                "Arnaud moves like he's still running drills in the commandery yard.",
                "He advances without flourish. The form is perfect. The man inside it is not.",
                "He presses. He has nothing left to hold back.",
            ],
            "hit": [
                "The blow is textbook Templar — you taught each other this.",
                "He finds the opening. He always was the better swordsman.",
                "You knew this form. You practised against it. That doesn't help.",
            ],
            "miss": [
                "You read him — the old pattern. You slip it.",
                "He lunges. You were already moving.",
                "The edge passes close. You remember his tells.",
            ],
            "death": [
                "Arnaud falls to one knee. Stays there. "
                "\"I thought it would feel like something,\" he says. Then nothing.",
                "He goes down without a word. The sword drops from his hand. "
                "It was a good sword. It deserved better.",
                "He looks at you at the end with something like relief. "
                "You don't know what to do with that.",
            ],
            "taunt": [
                "\"They broke me in three days. How long do you think you'll last?\"",
                "\"I said the words they wanted. Just words. "
                "What did it cost? What did it change?\"",
                "\"You still believe. I can see it. It must be very heavy.\"",
            ],
            "phase2": (
                "Arnaud stops. He looks at you — really looks. "
                "\"You haven't run,\" he says. Then he comes at you harder."
            ),
            "phase3": (
                "He is bleeding badly now. It doesn't slow him. "
                "\"Finish it,\" he says, between strikes. \"One of us should.\""
            ),
        },
    },
}
