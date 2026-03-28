# ============================================================
#  app.py — The Silent Oath
#  Flask web server. Run: python app.py
#  Requires: pip install flask
# ============================================================
import json
import os
import subprocess

from flask import Flask, jsonify, render_template, request, session

from content.game_config import START_SCENE
from content.scenes import SCENES
from engine.combat import ENEMIES, get_player_actions, resolve_action, start_combat
from engine.scene_web import render_scene, apply_choice, _build_hud
from engine.state import PlayerState

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVES_DIR = os.path.join(BASE_DIR, "saves")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "the-silent-oath-dev-key")
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0  # disable static file caching in dev

# Always ensure saves dir exists regardless of how app is started
os.makedirs(SAVES_DIR, exist_ok=True)

# ── Session helpers ───────────────────────────────────────────


def _get_state() -> PlayerState:
    data = session.get("state")
    if data:
        return PlayerState.from_dict(data)
    return PlayerState()


def _save_state(state: PlayerState):
    session["state"] = state.to_dict()
    session.modified = True


def _get_combat() -> dict | None:
    raw = session.get("combat")
    if raw:
        return json.loads(raw)
    return None


def _save_combat(combat: dict | None):
    if combat is None:
        session.pop("combat", None)
    else:
        session["combat"] = json.dumps(combat)
    session.modified = True


# ═══════════════════════════════════════════════════════════
#  ROUTES
# ═══════════════════════════════════════════════════════════


def _git_rev() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return "0"

_STATIC_VER = _git_rev()


@app.route("/")
def index():
    return render_template("index.html", v=_STATIC_VER)


# ── New game ──────────────────────────────────────────────────
@app.route("/api/new", methods=["POST"])
def new_game():
    state = PlayerState()
    state.current_scene = START_SCENE
    _save_state(state)
    _save_combat(None)
    return jsonify({"ok": True})


# ── Load current scene ────────────────────────────────────────
@app.route("/api/scene", methods=["GET"])
def get_scene():
    state = _get_state()
    if not state.current_scene:
        state.current_scene = "name_entry"

    key = state.current_scene

    # Handle special keys
    if key in ("__save_quit__", "end", "__end__"):
        return jsonify({"game_over": True, "credits": True})

    if key == "__restart__":
        state = PlayerState()
        state.current_scene = "name_entry"
        _save_state(state)
        key = "name_entry"

    # Auto-advance through chain scenes that have NO prose to show
    # (pure side-effect scenes: only flag/stat/item beats, no prose/italic/memory)
    hops = 0
    while hops < 10:
        if key not in SCENES:
            break
        scene = SCENES[key]
        has_choices = bool(scene.get("choices"))
        has_next = bool(scene.get("next"))
        beats = scene.get("beats", [])
        has_combat = any(b.get("type") == "combat" for b in beats)
        has_input = any(b.get("type") == "input" for b in beats)
        has_prose = any(
            b.get("type") in ("prose", "italic", "memory", "conditional_prose")
            for b in beats
        )
        # Only auto-advance if: has next, no choices, no combat, no input, NO prose
        if (
            has_next
            and not has_choices
            and not has_combat
            and not has_input
            and not has_prose
        ):
            output = render_scene(key, state)
            _save_state(state)
            key = scene["next"]
            state.current_scene = key
            hops += 1
        else:
            break

    output = render_scene(key, state)
    _save_state(state)

    # If scene triggers combat, initialise it
    if output.get("combat"):
        enemy_key = output["combat"]["enemy_key"]
        _scene = SCENES.get(key, {})
        _cb_beat = next(
            (b for b in _scene.get("beats", []) if b.get("type") == "combat"), {}
        )
        combat_state = start_combat(enemy_key, state, variant=_cb_beat.get("variant"))
        # Store the scene-defined flag name so we can set it on victory
        combat_state["victory_flag"] = _cb_beat.get("flag", f"defeated_{enemy_key}")
        _save_combat(combat_state)
        _save_state(state)
        output["combat"]["actions"] = get_player_actions(combat_state, state)
        output["combat"]["enemy_name"] = ENEMIES[enemy_key]["name"]
        output["combat"]["enemy_hp_ratio"] = (
            combat_state["enemy"]["current_hp"] / combat_state["enemy"]["hp"]
        )
        output["combat"]["log"] = combat_state["log"]

    return jsonify(output)


# ── Make a choice ─────────────────────────────────────────────
@app.route("/api/choose", methods=["POST"])
def choose():
    data = request.get_json()
    choice_id = data.get("choice_id", "0")
    state = _get_state()
    scene_key = state.current_scene

    # Handle name input specially
    if data.get("name"):
        state.name = data["name"].strip() or "the brother"
        # Use the choice the player actually selected before typing their name
        pending_id = str(data.get("pending_choice_id", "0"))
        scene = SCENES.get(scene_key, {})
        choices = scene.get("choices", [])
        if choices:
            next_key, _ = apply_choice(scene_key, pending_id, state)
        else:
            next_key = scene.get("next", "commandery_night")
        state.current_scene = next_key
        _save_state(state)
        return jsonify({"next_scene": next_key, "ok": True})

    next_key, narration = apply_choice(scene_key, choice_id, state)

    # Handle special destinations
    if next_key == "__save_quit__":
        state.save(0)
        _save_state(state)
        return jsonify({"game_over": True})

    state.current_scene = next_key
    state.visited.append(scene_key)
    state.save(0)
    _save_state(state)
    return jsonify({"next_scene": next_key, "ok": True, "narration": narration})


# ── Combat action ─────────────────────────────────────────────
@app.route("/api/combat/action", methods=["POST"])
def combat_action():
    data = request.get_json()
    action_id = data.get("action_id")
    state = _get_state()
    combat = _get_combat()

    if not combat:
        return jsonify({"error": "No active combat"}), 400

    combat = resolve_action(action_id, combat, state)
    _save_state(state)

    response = {
        "log": combat["log"][-6:],  # last 6 entries
        "over": combat["over"],
        "won": combat.get("won", False),
        "fled": combat.get("fled", False),
        "died": combat.get("died", False),
        "false_blessed": combat.get("false_blessed", False),
        "listened": combat.get("listened", False),
        "released": combat.get("released", False),
        "hud": _build_hud(state),
        "enemy_hp_ratio": (
            combat["enemy"]["current_hp"] / combat["enemy"]["hp"]
            if combat["enemy"]["hp"] > 0
            else 0
        ),
        "items_gained": combat.get("items_gained", []),
    }

    if not combat["over"]:
        response["actions"] = get_player_actions(combat, state)
        _save_combat(combat)
    else:
        # Set the scene-defined victory flag on the player state
        if combat.get("won") and combat.get("victory_flag"):
            state.set_flag(combat["victory_flag"], True)
        _save_combat(None)
        state.current_scene = _advance_after_combat(state.current_scene, combat)
        state.save(0)
        _save_state(state)
        response["next_scene"] = state.current_scene

    return jsonify(response)


# ── Status ────────────────────────────────────────────────────
@app.route("/api/status", methods=["GET"])
def status():
    state = _get_state()
    return jsonify(
        {
            "has_save": os.path.exists(os.path.join(SAVES_DIR, "save_0.json")),
            "scene": state.current_scene,
            "memories": state.memories,
            "inventory": state.inventory,
            "deaths": state.deaths,
        }
    )


@app.route("/api/advance", methods=["POST"])
def advance():
    """Advance to a known next scene (used by auto-next scenes with no choices)."""
    data = request.get_json()
    next_key = data.get("next_scene", "")
    state = _get_state()

    # __scene_next__ means: look up the current scene's next key
    if next_key == "__scene_next__":
        scene_key = data.get("scene_key") or state.current_scene
        next_key = SCENES.get(scene_key, {}).get("next", "commandery_night")

    if next_key in ("__save_quit__", "end", "__end__"):
        state.save(0)
        _save_state(state)
        return jsonify({"game_over": True})

    if next_key == "__restart__":
        state = PlayerState()
        next_key = "name_entry"

    state.current_scene = next_key
    state.save(0)
    _save_state(state)
    return jsonify({"ok": True, "next_scene": next_key})


@app.route("/api/load", methods=["POST"])
def load_game():
    state = PlayerState.load(0)
    if state is None:
        return jsonify({"ok": False, "error": "No save found"})
    _save_state(state)
    _save_combat(None)
    return jsonify({"ok": True, "scene": state.current_scene})


# ── Helpers ───────────────────────────────────────────────────


def _advance_after_combat(scene_key: str, combat: dict) -> str:
    """After combat ends, move to the right next scene."""
    # On death: go to the scene BEFORE the combat so player
    # sees the approach again rather than re-entering combat immediately
    # Populate these as combat scenes are added to the acts.
    # Key: combat scene key → scene to return to on death/flee.
    pre_combat: dict[str, str] = {}
    if combat.get("died") or combat.get("fled"):
        return pre_combat.get(scene_key, "commandery_night")
    # Victory: advance to scene defined in scene data
    return SCENES[scene_key].get("next", scene_key)


# ═══════════════════════════════════════════════════════════
#  ENTRY
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    os.makedirs(SAVES_DIR, exist_ok=True)
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV") != "production"
    print("\n  The Silent Oath")
    print(f"  Open: http://localhost:{port}\n")
    app.run(host="0.0.0.0", port=port, debug=debug)
