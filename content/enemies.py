# ============================================================
#  content/enemies.py — Enemy Design Framework
#
#  Every enemy has five layers:
#
#  1. Identity   — who/what this is (not just a type, a person or force)
#  2. Stats      — threat (1–5), hp, damage, accuracy, faith, resolve
#  3. Behavior   — aggressive | testing | passive | manipulative
#  4. Special    — one mechanic that changes the rules of the fight
#  5. Resolution — kill / free / understand
#
#  Add new enemies here — no engine changes needed
#  unless a new special.id is introduced.
# ============================================================

ENEMIES = {
    # ── Royal sergeant ────────────────────────────────────────
    # Identity: sold soldier — obedient to the crown, not to conscience.
    # He is not evil. He is following orders from a king who needs him to be.
    "royal_sergeant": {
        "name": "a royal sergeant",
        "name_short": "the sergeant",
        "identity": "sold soldier — obedient to the crown, not to conscience",
        # Stats
        "threat": 2,
        "hp": 80,
        "damage": (10, 18),
        "accuracy": 0.65,
        "faith": 15,    # serves crown, not God — invoke_oath hits harder
        "resolve": 65,  # disciplined; hard to rattle
        # Behavior: presses forward, no hesitation, no mercy
        "behavior": "aggressive",
        # Special: reads repeated patterns — same action twice and he's ready
        "special": {
            "id": "trained_guard",
            "label": "Trained Guard",
            "desc": (
                "If the player uses the same action two turns in a row, "
                "the sergeant reads it. His next attack hits with +0.20 accuracy."
            ),
        },
        # Resolution
        "resolution": {
            "kill": True,
            "free": True,      # disarm and release — he'll leave
            "understand": True, # he's following orders; that's human
        },
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
            "release": [
                "He holds your gaze for a moment. Then he turns and walks.",
                "He sheathes nothing — he drops it. Then he goes.",
            ],
        },
    },

    # ── Inquisitor's agent ────────────────────────────────────
    # Identity: living doubt — weaponises uncertainty as effectively as steel.
    # He does not fight you. He interrogates you while you fight him.
    # The horror: he genuinely believes he serves God.
    "inquisitors_agent": {
        "name": "an agent of the Inquisition",
        "name_short": "the agent",
        "identity": "living doubt — he weaponises uncertainty as effectively as steel",
        # Stats
        "threat": 2,
        "hp": 55,
        "damage": (6, 14),
        "accuracy": 0.55,
        "faith": 70,    # genuinely believes — invoke_oath is weaker against him
        "resolve": 30,  # not a fighter; breaks under real pressure
        # Behavior: exploits hesitation; psychological before physical
        "behavior": "manipulative",
        "weapon": {"effect": "fear"},
        # Special: silence is losing — every turn the player doesn't attack, Doubt grows
        "special": {
            "id": "interrogator",
            "label": "Interrogator",
            "desc": (
                "Every turn the player defends or hesitates without dealing damage, "
                "Doubt increases by 4. Silence is not safety."
            ),
        },
        # Resolution
        "resolution": {
            "kill": True,
            "free": False,      # releasing him brings more
            "understand": True, # the horror is he might be right about God
        },
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
            "manipulate": [
                "\"What do you protect? Do you even know anymore?\"",
                "\"The order fell in a single night. What does that tell you about God's favour?\"",
                "\"You hesitate. That is already an answer.\"",
                "He says nothing. Just watches. The silence is deliberate.",
            ],
        },
    },

    # ── Fallen brother ────────────────────────────────────────
    # Identity: the broken oath made flesh — what the player could become.
    # He broke under interrogation. Now he serves the crown.
    # He is not a villain. He is a mirror.
    "fallen_brother": {
        "name": "Brother Arnaud — the broken oath",
        "name_short": "Arnaud",
        "identity": "the broken oath made flesh — what the player could become",
        # Stats
        "threat": 4,
        "hp": 140,
        "damage": (12, 22),
        "accuracy": 0.70,
        "faith": 35,    # broken but not gone; invoke_oath still costs something
        "resolve": 80,  # endures despite everything
        # Behavior: reads the player; adapts; has nothing left to hold back
        "behavior": "testing",
        "weapon": {"effect": "corruption"},
        "phases": True,
        # Special: broken mirror — when player invokes their oath, Arnaud echoes it broken
        "special": {
            "id": "broken_mirror",
            "label": "Broken Mirror",
            "desc": (
                "When the player invokes their Oath, Arnaud echoes it — broken. "
                "The invocation still works, but Doubt increases by 5 "
                "and the player hears their oath in his voice."
            ),
        },
        # Resolution
        "resolution": {
            "kill": True,
            "free": True,      # mercy; he accepts it, may even want it
            "understand": True, # his story is the player's possible future
        },
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
            "release": [
                "He does not thank you. He just goes. "
                "You think he was looking for permission.",
                "\"I didn't think you'd—\" He stops. He goes.",
            ],
            "taunt": [
                "\"They broke me in three days. How long do you think you'll last?\"",
                "\"I said the words they wanted. Just words. "
                "What did it cost? What did it change?\"",
                "\"You still believe. I can see it. It must be very heavy.\"",
            ],
            "testing": [
                "He adjusts. He saw that coming.",
                "\"Same move. You did that last time too.\"",
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
