# ============================================================
#  content/act1.py
#  Act I — The Vow
#  Pure data. No logic. The engine in scene_web.py runs these.
# ============================================================

# ── Scene: Intro ──────────────────────────────────────────────
SCENE_INTRO = {
    "art": "title",
    "beats": [
        {
            "type": "prose",
            "text": (
                "Paris. October 1307."
            ),
        },
        {
            "type": "prose",
            "text": (
                "King Philip IV has been watching the Order for years. "
                "Tonight, sealed letters are in the hands of every sheriff in France. "
                "At dawn they will be opened. "
                "By noon, the arrests will begin."
            ),
        },
        {
            "type": "prose",
            "text": (
                "The Grand Master knows. He has known for three days. "
                "He has not fled."
            ),
        },
        {
            "type": "italic",
            "text": (
                "Something beneath the commandery has been disturbed. "
                "He summoned the inner circle. "
                "You were called."
            ),
        },
    ],
    "next": "name_entry",
}

# ── Scene: Name entry ─────────────────────────────────────────
SCENE_NAME_ENTRY = {
    "art": "title",
    "beats": [
        {
            "type": "prose",
            "text": "Paris. October, 1307.",
        },
        {
            "type": "prose",
            "text": (
                "For years, King Philip IV has watched the Order in silence — "
                "weighing its wealth, its influence, its independence. "
                "Tonight, that silence breaks."
            ),
        },
        {
            "type": "prose",
            "text": (
                "Sealed letters now rest in the hands of every royal sheriff in France. "
                "Wax unbroken. Orders unseen. "
                "They are not to be opened until dawn."
            ),
        },
        {
            "type": "prose",
            "text": "By noon, the arrests will begin.",
        },
        {
            "type": "prose",
            "text": (
                "Within the walls of the Temple in Paris, the night feels wrong."
            ),
        },
        {
            "type": "prose",
            "text": (
                "The brothers speak in lowered voices, if they speak at all. "
                "Servants move quickly, avoiding eye contact. "
                "Even the horses in the lower stables are restless, "
                "stamping against stone as if sensing a storm that has not yet arrived."
            ),
        },
        {
            "type": "italic",
            "text": (
                "No alarm has been sounded. "
                "No command to prepare, no call to arms."
            ),
        },
        {
            "type": "prose",
            "text": "Only waiting.",
        },
        {
            "type": "input",
            "prompt": "What is your name, brother?",
            "store_as": "name",
        },
    ],
    "next": "commandery_night",
}

# ── Scene: Commandery at night ────────────────────────────────
SCENE_COMMANDERY_NIGHT = {
    "art": "commandery_night",
    "header": {"title": "The Silent Oath", "subtitle": "Act I — The Vow"},
    "beats": [
        {
            "type": "prose",
            "text": (
                "Cold air fills your lungs as you draw breath. "
                "It tastes of smoke."
            ),
        },
        {
            "type": "prose",
            "text": (
                "You cannot remember when it was last this quiet. "
                "No wind, no voices — only fire, slowly consuming "
                "what was, moments ago, your brothers."
            ),
        },
        {
            "type": "prose",
            "text": (
                "You stand in the shadow of a stone bridge. "
                "The view beneath the arch is distorted through smoke and grey light, "
                "as if the world were withdrawing from this place. "
                "The lantern in your hand trembles slightly, though your hand does not. "
                "Its light does not carry far. It does not want to."
            ),
        },
        {
            "type": "prose",
            "text": "Two bodies burn before you.",
        },
        {
            "type": "italic",
            "text": (
                "They do not cry out. "
                "They do not move."
            ),
        },
        {
            "type": "prose",
            "text": "Their armor bears the same mark as yours.",
        },
        {
            "type": "italic",
            "text": "The red cross, now blackened.",
        },
        {
            "type": "prose",
            "text": (
                "Your sword feels heavier than it should. "
                "The blade is dirty, and the blood is no longer fresh. "
                "You do not remember the strike that left it there. "
                "You do not remember the moment when everything broke."
            ),
        },
        {
            "type": "italic",
            "text": "But something in this place does.",
        },
        {
            "type": "prose",
            "text": (
                "The bridge continues forward into the ruins, arch after arch, "
                "as if it leads somewhere not meant to be traveled. "
                "Further on, behind the smoke, something moves — "
                "or perhaps it is only the light, refusing to stay still."
            ),
        },
        {
            "type": "prose",
            "text": "Your lantern flickers again.",
        },
        {
            "type": "italic",
            "text": (
                "And for a moment, you feel that something is looking back. "
                "Not an enemy. Not a person. "
                "Something that knows your name."
            ),
        },
        {
            "type": "prose",
            "text": "Your oath was clear.",
        },
        {
            "type": "italic",
            "text": "Protect. Hold fast. Do not doubt.",
        },
        {
            "type": "prose",
            "text": (
                "But now, in this silence, none of them feel whole."
            ),
        },
        {
            "type": "prose",
            "text": (
                "The fire crackles. "
                "Through the smoke, something else drifts."
            ),
        },
        {
            "type": "prose",
            "text": "You are not alone.",
        },
        {
            "type": "italic",
            "text": "You have not been for some time.",
        },
    ],
    "choices": [
        {
            "label": "Cross the bridge.",
            "next": "commandery_night",  # placeholder
        },
        {
            "label": "Kneel beside your brothers.",
            "next": "commandery_night",  # placeholder
        },
    ],
}

SCENES = {
    "intro": SCENE_INTRO,
    "name_entry": SCENE_NAME_ENTRY,
    "commandery_night": SCENE_COMMANDERY_NIGHT,
}
