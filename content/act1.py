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
            "text": ("Paris. October 1307."),
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
        {"type": "prose", "text": "Paris. October, 1307."},
        {
            "type": "prose",
            "text": (
                "For years, King Philip IV has watched the Order in silence — "
                "measuring its wealth, its influence, its reach across kingdoms "
                "that answer to no crown. "
                "What cannot be owned, he has chosen to break."
            ),
        },
        {"type": "prose", "text": "Tonight, that decision moves."},
        {
            "type": "prose",
            "text": (
                "Sealed letters rest in the hands of every royal sheriff in France. "
                "Wax unbroken. Commands unseen. "
                "They are not to be opened until dawn."
            ),
        },
        {"type": "prose", "text": "By noon, the arrests will begin."},
        {"type": "prose", "text": "The Order does not yet fall."},
        {
            "type": "prose",
            "text": (
                "Its banners still hang in chapels. "
                "Its knights still keep their vigils. "
                "Its coffers remain sealed, its rites unbroken."
            ),
        },
        {"type": "prose", "text": "But something has shifted."},
        {
            "type": "italic",
            "text": (
                "Not in the courts of kings, nor in the whispers of Rome — "
                "but beneath stone, where no crown has ever held authority."
            ),
        },
        {"type": "prose", "text": "The Grand Master knows."},
        {"type": "prose", "text": "He has known for three days."},
        {
            "type": "prose",
            "text": (
                "He has not fled. He has not called the banners. "
                "He has not warned those who would run if given the chance."
            ),
        },
        {"type": "prose", "text": "Instead, he has waited."},
        {
            "type": "italic",
            "text": "And in that waiting, something older than fear has begun to stir.",
        },
        {
            "type": "prose",
            "text": (
                "Beneath the Paris commandery, far below the vaults and prayer halls, "
                "there are chambers that do not appear on any record of the Order."
            ),
        },
        {
            "type": "prose",
            "text": "They were not built by the brothers who serve above.",
        },
        {"type": "prose", "text": "They were not meant to be found."},
        {
            "type": "prose",
            "text": (
                "For generations, they have remained sealed — "
                "not by lock, but by oath."
            ),
        },
        {"type": "prose", "text": "Three nights ago, something changed."},
        {
            "type": "italic",
            "text": "No door was broken. No seal was lifted.",
        },
        {"type": "prose", "text": "And yet, the silence below was disturbed."},
        {
            "type": "prose",
            "text": (
                "The Grand Master summoned the inner circle. "
                "No record was made of the gathering. "
                "No servant was permitted near. "
                "Those called did not speak of it afterward."
            ),
        },
        {"type": "italic", "text": "Some did not emerge at all."},
        {"type": "prose", "text": "Now, more are being called."},
        {
            "type": "italic",
            "text": "Not the oldest. Not the highest.",
        },
        {
            "type": "prose",
            "text": "But those who have not yet chosen what they believe.",
        },
        {
            "type": "prose",
            "text": "By dawn, the King will move against the Order.",
        },
        {"type": "prose", "text": "By dusk, the Order may already be broken."},
        {
            "type": "prose",
            "text": (
                "But what waits below the commandery does not answer to kings. "
                "It does not fear chains."
            ),
        },
        {"type": "italic", "text": "And it has already begun to wake."},
        {
            "type": "input",
            "prompt": "What is your name, brother?",
            "store_as": "name",
        },
    ],
    "next": "descent",
}

# ── Scene: The Descent ───────────────────────────────────────
SCENE_DESCENT = {
    "art": "commandery_night",
    "header": {"title": "The Silent Oath", "subtitle": "Act I — The Vow"},
    "beats": [
        {
            "type": "prose",
            "text": "The commandery gates are open.",
        },
        {
            "type": "italic",
            "text": "That is the first thing that seems wrong.",
        },
        {
            "type": "prose",
            "text": (
                "A brother you do not recognise meets you in the outer courtyard. "
                "He does not give his name. He does not look at you long. "
                "He says only: below. And he turns."
            ),
        },
        {
            "type": "prose",
            "text": (
                "You follow him through the chapel, past the prayer halls, "
                "down a staircase that does not appear on any plan you have seen. "
                "The torches burn lower here than they should. "
                "The walls are older than the building above."
            ),
        },
        {
            "type": "italic",
            "text": "The air is different. Not cold. Something else.",
        },
        {
            "type": "prose",
            "text": (
                "At the base of the stairs, a passage opens into a chamber. "
                "No torch burns here. "
                "The only light comes from the door at the far end."
            ),
        },
        {
            "type": "italic",
            "text": "It is open.",
        },
        {
            "type": "prose",
            "text": (
                "Not forced. Not broken. "
                "Opened from the other side."
            ),
        },
        {
            "type": "prose",
            "text": "The brother who led you here has stopped walking.",
        },
        {
            "type": "italic",
            "text": "He will not say why.",
        },
        {
            "type": "prose",
            "text": "You take one step through the door.",
        },
        {
            "type": "italic",
            "text": "And then the light goes out.",
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
                "Cold air fills your lungs as you draw breath. " "It tastes of smoke."
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
        {"type": "italic", "text": "They do not cry out."},
        {"type": "italic", "text": "They do not move."},
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
            "text": "And for a moment, you feel that something is looking back.",
        },
        {"type": "italic", "text": "Not an enemy."},
        {"type": "italic", "text": "Not a person."},
        {"type": "italic", "text": "Something that knows your name."},
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
            "text": ("But now, in this silence, none of them feel whole."),
        },
        {"type": "prose", "text": "The fire crackles."},
        {"type": "prose", "text": "Through the smoke, something else drifts."},
        {"type": "prose", "text": "You are not alone."},
        {"type": "italic", "text": "You have not been for some time."},
    ],
    "choices": [
        {
            "label": "Move forward into the ruins.",
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
    "descent": SCENE_DESCENT,
    "commandery_night": SCENE_COMMANDERY_NIGHT,
}
