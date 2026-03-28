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
            "text": "Paris. October 1307.",
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
                "The commandery is quiet. "
                "Too quiet for a night when the Grand Master has called the inner circle."
            ),
        },
        {
            "type": "prose",
            "text": (
                "You stand in the courtyard. The torches burn low. "
                "Somewhere beneath the chapter house, a door has been opened "
                "that should remain sealed."
            ),
        },
        {
            "type": "italic",
            "text": "You feel it before you understand it. Something has changed down there.",
        },
    ],
    "choices": [
        {
            "label": "Go to the chapter house.",
            "next": "commandery_night",  # placeholder — replace when next scene exists
        },
    ],
}

SCENES = {
    "intro": SCENE_INTRO,
    "name_entry": SCENE_NAME_ENTRY,
    "commandery_night": SCENE_COMMANDERY_NIGHT,
}
