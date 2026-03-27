# ============================================================
#  content/act1.py
#  Act I — The Commandery
#  Pure data. No logic. The engine in scene_web.py runs these.
# ============================================================

# ── Scene: Name entry ─────────────────────────────────────────
SCENE_NAME_ENTRY = {
    "art": "name_entry",
    "beats": [
        {
            "type": "prose",
            "text": "You are a Knight of the Temple. You have kept your oath through fire and doubt.",
        },
        {
            "type": "prose",
            "text": "But tonight, something stirs beneath the stones of the commandery.",
        },
        {"type": "input", "prompt": "What is your name, brother?", "stat": "name"},
    ],
    "next": "commandery_night",
}

# ── Scene: Act I opening ──────────────────────────────────────
SCENE_COMMANDERY_NIGHT = {
    "art": "commandery",
    "header": {"title": "The Silent Oath", "subtitle": "Act I — The Commandery"},
    "beats": [
        {
            "type": "prose",
            "text": "The commandery is quiet. Too quiet for a night when the Grand Master has called the inner circle.",
        },
        {
            "type": "prose",
            "text": "You stand in the courtyard. The torches burn low. Somewhere beneath the chapter house, a door has been opened that should remain sealed.",
        },
    ],
    "choices": [
        {"text": "Go to the chapter house.", "next": "commandery_night"},
    ],
}

SCENES = {
    "name_entry": SCENE_NAME_ENTRY,
    "commandery_night": SCENE_COMMANDERY_NIGHT,
}
