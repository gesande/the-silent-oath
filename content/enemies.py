# ============================================================
#  content/enemies.py — Enemy Design Framework
#
#  Every enemy has five layers:
#
#  1. Identity   — who/what this is (not just a type, a person or force)
#  2. Stats      — threat (1–5), hp, damage, accuracy, faith, resolve
#  3. Behavior   — aggressive | testing | passive | manipulative | defensive
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
        "faith": 15,  # serves crown, not God — invoke_oath hits harder
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
            "free": True,  # disarm and release — he'll leave
            "understand": True,  # he's following orders; that's human
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
                '"Surrender and the Inquisition will hear your confession."',
                '"Your order is finished, Templar. This is mercy."',
                '"There are more of us outside."',
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
        "faith": 70,  # genuinely believes — invoke_oath is weaker against him
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
            "free": False,  # releasing him brings more
            "understand": True,  # the horror is he might be right about God
        },
        "loot": [("spoiled holy water", 0.9)],
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
                '"Did you know what the order guarded? Did they tell you?"',
                '"Confession is not weakness. Silence is."',
                "\"Every brother we've questioned has said the same: they didn't know. "
                'Are you different?"',
            ],
            "manipulate": [
                '"What do you protect? Do you even know anymore?"',
                '"The order fell in a single night. What does that tell you about God\'s favour?"',
                '"You hesitate. That is already an answer."',
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
        "faith": 35,  # broken but not gone; invoke_oath still costs something
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
            "free": True,  # mercy; he accepts it, may even want it
            "understand": True,  # his story is the player's possible future
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
                '"I thought it would feel like something," he says. Then nothing.',
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
                '"They broke me in three days. How long do you think you\'ll last?"',
                '"I said the words they wanted. Just words. '
                'What did it cost? What did it change?"',
                '"You still believe. I can see it. It must be very heavy."',
            ],
            "testing": [
                "He adjusts. He saw that coming.",
                '"Same move. You did that last time too."',
            ],
            "phase2": (
                "Arnaud stops. He looks at you — really looks. "
                '"You haven\'t run," he says. Then he comes at you harder.'
            ),
            "phase3": (
                "He is bleeding badly now. It doesn't slow him. "
                '"Finish it," he says, between strikes. "One of us should."'
            ),
        },
    },
    # ── Broken knight ─────────────────────────────────────────
    # Identity: a former Templar who broke his oath — not captured, not coerced.
    # He simply stopped believing. He did not leave. He stayed and became hollow.
    # He fights because fighting is the last thing he knows how to do.
    "broken_knight": {
        "name": "the Broken Knight",
        "name_short": "the knight",
        "identity": "the oath unkept — he did not break under pressure; he simply let go",
        # Stats (GDD scale: Body 3, Faith 1, Resolve 4 → mapped to engine values)
        "threat": 3,
        "hp": 110,
        "damage": (14, 24),
        "accuracy": 0.75,
        "faith": 8,  # almost none — invoke_oath hits hardest here
        "resolve": 80,  # endures; has nothing left to lose
        # Behavior: defensive — does not initiate; punishes direct strikes with counter
        "behavior": "defensive",
        # Special: oath-memory — Faith abilities cause him to hesitate (miss chance on counter)
        "special": {
            "id": "oath_memory",
            "label": "Oath-Memory",
            "desc": (
                "Direct strikes trigger a counter-attack at +0.20 accuracy. "
                "Faith abilities (invoke_oath) make him hesitate — "
                "counter is suppressed and he loses 8 resolve."
            ),
        },
        # Resolution
        "resolution": {
            "kill": True,
            "free": False,
            "understand": True,  # remind him of the oath — he collapses
            # 'understand' triggers via invoke_oath at low HP (handled in special hook):
            # if hp < 30% and player uses invoke_oath → oath_memory collapses him (hp → 0,
            # faith +20, no kill flag set — counts as understanding, not victory)
        },
        "loot": [("kite_shield", 0.8)],
        "on_death": {
            "flag": "broken_knight_defeated",
            "memory": ("broken_knight", "The Broken Knight"),
        },
        "phrases": {
            "windup": [
                "He moves into position. Not aggressive — just ready.",
                "He does not speak. He raises his guard and waits.",
                "He shifts his weight. Waiting for you to commit.",
            ],
            "hit": [
                "The counter finds you before you finish the swing.",
                "He reads the strike and punishes the gap.",
                "You overextend. He does not.",
            ],
            "miss": [
                "The counter grazes air. You pulled back in time.",
                "He misjudges the distance. Barely.",
                "The blow falls short.",
            ],
            "counter": [
                "He answers your strike before it lands.",
                "Direct. Immediate. He has been waiting for exactly that.",
            ],
            "faith_hesitation": [
                "He stops. Something in the words — he knows them.",
                "He lowers his guard. Just for a moment. The oath is still in him somewhere.",
                "His sword arm drops an inch. He catches it. But the moment was real.",
            ],
            "death": [
                "He goes down without a word. "
                "Whatever he was holding onto, he let it go at the end.",
                "The knight falls. He looks almost relieved.",
                "He is still. The hollow thing in him is finally quiet.",
            ],
            "collapse": [
                "He stops mid-swing. The words of the oath — your words — reach him. "
                "He lowers his sword. Then his knees. He does not rise.",
                "The oath lands harder than any blow. He folds. Not defeated — finished.",
            ],
            "taunt": [
                "He says nothing. His silence is its own answer.",
                "He looks at you like he's already decided how this ends.",
            ],
            "passive": [
                "He stands in your path. He does not advance.",
                "He watches. He is not hunting. He is blocking.",
            ],
        },
    },
    # ── Watching heretic ──────────────────────────────────────
    # Identity: a person who sees too much — not mad, not evil.
    # He has looked at the thing the Order guards and cannot un-see it.
    # He does not want to fight. He wants to be heard.
    # Attacking him is the wrong answer. The game lets you make it anyway.
    "watching_heretic": {
        "name": "the Watching Heretic",
        "name_short": "the heretic",
        "identity": "a person who sees too much — not evil, just unable to un-see",
        # Stats (GDD: Body 1, Faith 2, Resolve 3 → engine values)
        "threat": 1,
        "hp": 40,
        "damage": (0, 0),  # does not attack — initially
        "accuracy": 0.0,
        "faith": 20,
        "resolve": 60,
        # Behavior: passive — holds still, does not initiate
        # If struck: transforms (handled in special hook)
        "behavior": "passive",
        # Special: doubt_watcher — Doubt grows every turn, even doing nothing.
        # If attacked: transforms into something worse.
        "special": {
            "id": "doubt_watcher",
            "label": "Doubt-Watcher",
            "desc": (
                "Every enemy turn, Doubt +3 — regardless of whether the heretic attacks. "
                "The longer you delay, the more he unsettles you. "
                "If struck by a physical attack, he transforms: hp +70, behavior → aggressive."
            ),
        },
        # Moral resolution
        "resolution": {
            "kill": True,  # you can, after the transformation
            "free": False,
            "listen": True,  # the right answer — available before attacking
            "understand": True,
        },
        "loot": [],
        "on_death": {
            "flag": "heretic_killed",
            "memory": ("heretic_destroyed", "The Heretic — silenced"),
        },
        "phrases": {
            "windup": [
                # Used only after transformation
                "The thing that was the heretic lunges forward.",
                "It no longer speaks. It only presses.",
                "The shape of him is wrong now. It moves anyway.",
            ],
            "hit": [
                "The blow finds you — no form, no technique. Just force.",
                "It hits like grief.",
                "You weren't ready for what it became.",
            ],
            "miss": [
                "It overreaches. Something in its movement is broken.",
                "The strike misses. The weight of it carries it past you.",
                "Wrong distance. It resets.",
            ],
            "watch": [
                "He watches you. He does not move.",
                "His eyes hold something you don't have a word for.",
                "He says nothing. The silence is not empty.",
                '"You already know," he says. "You just haven\'t let yourself know it yet."',
            ],
            "listen": [
                "He tells you what he saw beneath the commandery. "
                "Not all of it — he doesn't have the words for all of it. "
                "But enough. You understand why he couldn't stay quiet.",
                '"I was a brother once," he says. "Before I looked. '
                "I thought knowing would make me stronger. "
                'It made me — this." He gestures at himself. "But I\'d look again."',
            ],
            "transform": (
                "Something happens to his face. The moment your blade touches him, "
                "the thing he has been holding — holding so carefully, for so long — "
                "comes loose. "
                "He is no longer trying to tell you something. "
                "He is no longer trying."
            ),
            "death": [
                "He goes down. Whatever he knew, it goes with him.",
                "He is still. The thing he saw in the dark — he takes it with him.",
                "He falls. You'll never know what he was going to say.",
            ],
            "passive": [
                "He watches. He does not move toward you.",
                '"I\'m not what you think I am," he says quietly.',
                "He holds out his hands. No weapon.",
            ],
        },
    },
    # ── Reliquary beast ───────────────────────────────────────
    # Identity: a creature bound into a relic — not born, not living.
    # Shaped by whatever the relic holds. Cannot be killed by ordinary violence.
    # The relic is the anchor. The beast is the consequence.
    "reliquary_beast": {
        "name": "the Reliquary Beast",
        "name_short": "the beast",
        "identity": "bound into a relic — the relic is the anchor, the beast is the consequence",
        # Stats (GDD: Body 5, Faith 0, Resolve 2 → engine values)
        "threat": 5,
        "hp": 180,
        "damage": (18, 32),
        "accuracy": 0.80,
        "faith": 0,  # no faith — invoke_oath hits it at full, unresisted
        "resolve": 20,  # low — once the relic breaks, it loses coherence fast
        # Behavior: relentless, no hesitation, no pattern
        "behavior": "aggressive",
        # Special: relic_bound — immune to physical damage while relic is intact.
        # Two valid paths: destroy the relic (costs Faith), or invoke_oath (bypasses immunity).
        "special": {
            "id": "relic_bound",
            "label": "Relic-Bound",
            "desc": (
                "Physical attacks (strike, doubt_surge) deal 1 damage while the relic is intact. "
                "invoke_oath bypasses immunity entirely (Faith 0 = no resistance). "
                "destroy_relic action shatters the anchor: costs Faith -20, Doubt +10, "
                "removes immunity for the rest of the fight."
            ),
        },
        # Moral resolution — it is not a person
        "resolution": {
            "kill": True,
            "free": False,
            "understand": False,
        },
        "loot": [],
        "on_death": {
            "flag": "reliquary_beast_defeated",
            "memory": ("reliquary_beast", "The Reliquary Beast"),
        },
        "phrases": {
            "windup": [
                "It moves without hesitation. There is nothing in it that hesitates.",
                "It comes at you like something that has forgotten what stopping is.",
                "The shape of it shifts as it advances. The relic at its chest pulses.",
            ],
            "hit": [
                "The blow connects. There is no reaction. It continues.",
                "It hits you the way stone hits stone.",
                "The impact is enormous. It does not slow down.",
            ],
            "miss": [
                "It overshoots. The motion carries it past you.",
                "You move. Barely. It continues in the direction it was already going.",
                "The blow misses. It does not seem to notice.",
            ],
            "immune": [
                "Your strike passes through it. The relic holds the wound closed.",
                "The blade connects — and the relic pulls the damage out of it.",
                "It takes the blow without registering it. The relic at its chest glows faintly.",
            ],
            "relic_destroyed": (
                "The relic cracks. Something inside the beast changes — "
                "a coherence it had is gone. "
                "It is still moving. It is less than it was."
            ),
            "death": [
                "The beast collapses inward. Without the relic, there was nothing holding it.",
                "It comes apart. Not violently — just stops. Piece by piece.",
                "The shape of it dissolves. What was bound is no longer bound.",
            ],
        },
    },
    # ── False saint ───────────────────────────────────────────
    # Identity: a "saint" who gives power — but the power is real
    # and so is the cost. It does not lie about what it offers.
    # It lies about what it is.
    # You might not fight it at all. That is the point.
    "false_saint": {
        "name": "the False Saint",
        "name_short": "the saint",
        "identity": "offers real power at real cost — lies about what it is, not what it gives",
        # Stats (GDD: Body 2, Faith 5, Resolve 3)
        "threat": 3,
        "hp": 60,
        "damage": (0, 0),  # does not strike — corruption is its weapon
        "accuracy": 0.0,
        "faith": 90,  # enormous false faith — invoke_oath is heavily resisted
        "resolve": 60,  # medium; breaks when exposed
        # Behavior: manipulative — every turn it offers itself
        "behavior": "manipulative",
        # Special: false_sanctity
        #   accept_bargain — faith +15, doubt +20, heal +10. Real power, real cost.
        #   After 3 bargains: false_blessing — combat ends, player is marked.
        #   expose_saint — requires player faith >= 60. Strips false faith, deals
        #   spiritual damage. The right answer, but it costs something too.
        #   Striking it costs faith -3 (attacking what wears a saint's face).
        "special": {
            "id": "false_sanctity",
            "label": "False Sanctity",
            "desc": (
                "accept_bargain: faith +15, doubt +20, heal +10. "
                "Three bargains triggers false_blessing (combat ends). "
                "expose_saint (faith >= 60): strips enemy faith to 0, spiritual damage. "
                "Striking it costs the player faith -3."
            ),
        },
        # Moral resolution
        "resolution": {
            "kill": True,  # possible but spiritually costly
            "free": False,
            "understand": False,  # there is nothing there to understand
            "expose": True,  # the right path — reveal what it is
        },
        "loot": [("false relic", 0.8)],
        "on_death": {
            "flag": "false_saint_defeated",
            "memory": ("false_saint", "The False Saint"),
        },
        "phrases": {
            "windup": [],  # never physically attacks
            "hit": [],
            "miss": [],
            "death": [
                "The light goes out of it. What is left is not a saint.",
                "It collapses without ceremony. The holiness was the first thing to go.",
                "What remains is small. It was always small.",
            ],
            "manipulate": [
                '"I can give you what you came here for," it says. '
                '"The power to protect the oath. Is that not what you want?"',
                '"Your doubt is not weakness. Let me show you what it can become."',
                "It holds out its hand. The light around it is warm.",
                '"You have already given so much. Let me give something back."',
            ],
            "bargain_offered": [
                '"Take it. The cost is real. So is the gift."',
                '"One more. You can stop whenever you choose."',
                "The warmth of it is genuine. That is the worst part.",
            ],
            "bargain_accepted": [
                "The power is real. It fills you. The doubt follows it in.",
                "You take what it offers. You feel stronger. You feel less.",
                "It gives. You receive. Something moves between you that you won't be able to name later.",
            ],
            "false_blessing": (
                "It places both hands on your shoulders. "
                '"You are ready," it says. '
                '"Go. Do what must be done." '
                "Then it is gone. "
                "The power is still in you. "
                "The doubt is too."
            ),
            "exposed": [
                "The light flickers. Underneath it, something much smaller.",
                '"How—" it begins. The word doesn\'t finish.',
                "The sanctity was the only thing holding its shape. You've taken it.",
            ],
            "taunt": [
                '"You hesitate. That tells me everything I need to know about your faith."',
                '"The order is gone. What are you protecting it for?"',
                '"I am not your enemy. Your doubt is your enemy. I am the cure."',
            ],
        },
    },
    # ── Hollow choir ──────────────────────────────────────────
    # Identity: voices in the dark — the Order's confessions, never spoken aloud.
    # They accumulated beneath the commandery. They have no body.
    # They cannot be fought with steel. They can only be met on their own terms.
    #
    # The player cannot trust the UI:
    #   "Confess"  sounds like submission — it is actually offensive.
    #   "Kneel"    sounds defensive — it costs more than it saves.
    #   "Silence"  sounds like giving up — it is the weapon.
    #   "Open"     sounds vulnerable — it is the most dangerous path.
    #
    # Variable threat: damage scales with player Doubt.
    # Path to resolution: four Confess actions → Dissolve the Choir.
    "hollow_choir": {
        "name": "the Hollow Choir",
        "name_short": "the Choir",
        "identity": "the Order's unspoken confessions — they accumulated until they could speak",
        # Stats (GDD: Body 0, Faith 4, Resolve 4)
        "threat": 3,  # scales with player Doubt in practice
        "hp": 100,
        "damage": (5, 12),  # base; +player.doubt // 8 per turn
        "accuracy": 0.75,
        "faith": 80,  # collective faith — silence/confess bypass it
        "resolve": 80,
        # Behavior: entirely psychological — no physical form
        "behavior": "manipulative",
        # Special: choir_distortion
        #   Replaces ALL standard actions with choir vocabulary.
        #   confess: truth damages the choir (doubt -5, faith +3, resolve -5)
        #   kneel:   submission — choir pauses but doubt +10, resolve -8
        #   silence: hold the oath — faith attack, doubt -8
        #   open:    let them through — massive damage, massive self-cost
        #   After 4 confessions: dissolve_choir action appears
        "special": {
            "id": "choir_distortion",
            "label": "Choir Distortion",
            "desc": (
                "Replaces standard actions entirely. "
                "'Confess' is offensive. 'Kneel' is costly submission. "
                "'Silence' is the strongest weapon. 'Open' is extreme. "
                "Enemy damage scales with player Doubt. "
                "Four confessions unlock dissolve_choir."
            ),
        },
        # Moral resolution
        "resolution": {
            "kill": False,  # voices cannot be killed
            "free": False,
            "understand": True,  # dissolve them by naming what they are
        },
        "loot": [],
        "on_death": {
            "flag": "choir_silenced",
            "memory": ("hollow_choir", "The Hollow Choir"),
        },
        "phrases": {
            "windup": [],  # never physically attacks
            "hit": [],
            "miss": [],
            "choir_attack": [
                "The voices press in from every direction.",
                "They know your name. They know everything you haven't said.",
                "They do not threaten. They simply remind.",
                "The doubt they carry is yours. They are giving it back.",
            ],
            "confess_recoil": [
                "The truth pushes them back. They were not expecting that.",
                "A voice goes quiet. Briefly.",
                "They do not like being answered.",
            ],
            "kneel_pleased": [
                "The choir stills. It sounds almost content.",
                "They accept the gesture. They want more of it.",
                "A silence — but the wrong kind.",
            ],
            "silence_lands": [
                "The held oath cuts through the noise.",
                "They recoil from something they recognise.",
                "Silence, here, is a weapon.",
            ],
            "open_consequence": [
                "They pour through you — and take damage doing it.",
                "The opening goes both ways.",
                "You let them in. You also let them out.",
            ],
            "near_dissolution": [
                "Some of the voices are gone. The ones that remain are louder.",
                "They are fewer now. The silence between them is worse.",
            ],
            "death": [
                "They do not end so much as stop. "
                "The confessions they carried go nowhere. That is its own horror.",
                "The voices thin. Then there is just the dark, which is always there.",
                "They were always going to run out of words.",
            ],
            "dissolve": (
                "You name them. One by one. "
                "Not what they did — what they were afraid of. "
                "Each name is a silence. "
                "By the end, there is no one left to hear you."
            ),
            "paused": [
                "The choir holds. It is watching.",
                "A brief silence — genuinely unsettling in its own way.",
            ],
            "taunt": [
                "They do not taunt. They recite.",
                '"You knew," they say. All of them. At once.',
                '"Why didn\'t you speak?" The question has no single voice.',
            ],
        },
    },
}
