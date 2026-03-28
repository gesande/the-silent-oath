// ============================================================
//  game.js — The Silent Oath
//  Frontend controller. Talks to Flask API, renders scenes.
// ============================================================

const ART_BASE = "/static/svg/";
const ART_FALLBACK = "title";

// Art key aliases — use a different image file but trigger different music
const ART_ALIASES = {};

// ── DOM refs ──────────────────────────────────────────────────
const $ = (id) => document.getElementById(id);

// ── DOM refs — resolved after DOMContentLoaded ───────────────
let screens = {};

// ── State ─────────────────────────────────────────────────────
let currentScene = null;
let inCombat = false;

// ── Paragraph pagination ───────────────────────────────────────
let _paraQueue = [];
let _paraIdx = 0;
let _paraReady = false;
let _paraOnDone = null;

const PAGE_SIZE = 3; // paragraphs shown per page before advance prompt

function _startParagraphs(paragraphs, onDone) {
  _paraQueue = (paragraphs || []).filter((p) => p.type !== "memory");
  _paraIdx = 0;
  _paraReady = false;
  _paraOnDone = onDone;
  $("prose-body").innerHTML = "";
  $("choices-wrap").innerHTML = "";
  if (_paraQueue.length === 0) { onDone(); return; }
  _showPage();
}

function _showPage() {
  const proseEl = $("prose-body");
  const pageParas = _paraQueue.slice(_paraIdx, _paraIdx + PAGE_SIZE);
  const PARA_GAP = 0.55; // seconds between paragraphs on same page

  pageParas.forEach((p, i) => {
    const div = document.createElement("div");
    div.className = "prose-block" + (p.type === "italic" ? " italic" : "");
    div.textContent = p.type === "italic" ? `"${p.text}"` : p.text;
    div.style.animationDelay = `${i * PARA_GAP}s`;
    proseEl.appendChild(div);
  });

  const lastDelay = (pageParas.length - 1) * PARA_GAP;
  setTimeout(
    () => proseEl.lastElementChild.scrollIntoView({ behavior: "smooth", block: "nearest" }),
    lastDelay * 1000 + 200,
  );

  const pageEnd = _paraIdx + pageParas.length - 1;
  const isLastPage = pageEnd >= _paraQueue.length - 1;

  setTimeout(() => {
    _paraReady = true;
    if (isLastPage) {
      setTimeout(() => _paraOnDone(), 300);
    } else {
      const ind = document.createElement("div");
      ind.id = "para-advance";
      ind.className = "para-advance";
      proseEl.appendChild(ind);
    }
  }, (lastDelay + 1.15) * 1000);
}

function _advanceParagraph() {
  if (!_paraReady) return;
  const pageEnd = _paraIdx + PAGE_SIZE - 1;
  if (pageEnd >= _paraQueue.length - 1) return;
  _paraReady = false;
  const ind = $("para-advance");
  if (ind) ind.remove();
  _paraIdx += PAGE_SIZE;
  _showPage();
}

// ── Central fetch helper — always sends session cookie ────────
async function api(path, body = null) {
  const opts = {
    credentials: "include",
    headers: {},
  };
  if (body !== null) {
    opts.method = "POST";
    opts.headers["Content-Type"] = "application/json";
    opts.body = JSON.stringify(body);
  } else {
    opts.method = "GET";
  }
  const res = await fetch(path, opts);
  return res.json();
}

// ═══════════════════════════════════════════════════════════
//  INIT
// ═══════════════════════════════════════════════════════════

async function init() {
  // Resolve all DOM refs now that the document is ready
  screens.title = $("title-screen");
  screens.game = $("game-screen");
  screens.credits = $("credits-screen");

  // Check for existing save
  try {
    const data = await api("/api/status");
    // load button intentionally hidden — save/load not yet in use
    void data.has_save;
  } catch (e) {}

  $("btn-new").addEventListener("click", () => {
    dismissOverlay();
    startNewGame();
  });
  $("btn-load").addEventListener("click", () => {
    dismissOverlay();
    loadGame();
  });
  $("btn-quit").addEventListener("click", () => {
    if (!window.close()) {
      window.location.href = "about:blank";
    }
  });
  $("btn-rise").addEventListener("click", riseAgain);
  $("btn-credits-back").addEventListener("click", () => {
    show("title");
    hide("credits-screen");
    SoundEngine.playTitle();
  });
  $("name-submit").addEventListener("click", submitName);
  $("name-input").addEventListener("keydown", (e) => {
    if (e.key === "Enter") submitName();
  });

  // Advance paragraph on click (narrative area) or Space / ArrowRight
  $("narrative-panel").addEventListener("click", (e) => {
    if (e.target.closest("button, input")) return;
    _advanceParagraph();
  });
  document.addEventListener("keydown", (e) => {
    if (e.code === "Space" || e.code === "ArrowRight") {
      if (document.activeElement.tagName === "INPUT") return;
      e.preventDefault();
      _advanceParagraph();
    }
  });

  // ── Audio controls ─────────────────────────────────────────

  // Helper: sync in-game audio UI to current engine state
  function syncAudioUI(musicPct, sfxPct, muted) {
    const muteEl = $("mute-btn");
    if (muteEl) {
      muteEl.textContent = muted ? "♪ muted" : "♪ sound on";
      muteEl.classList.toggle("muted", muted);
    }
    const mv = $("music-vol");
    if (mv) mv.value = musicPct;
    const mv2 = $("music-val");
    if (mv2) mv2.textContent = musicPct;
    const sv = $("sfx-vol");
    if (sv) sv.value = sfxPct;
    const sv2 = $("sfx-val");
    if (sv2) sv2.textContent = sfxPct;
  }

  let musicPct = 45,
    sfxPct = 70,
    isMuted = false;

  // Mute button — in-game only
  const muteBtn = $("mute-btn");
  if (muteBtn) {
    muteBtn.addEventListener("click", () => {
      isMuted = SoundEngine.toggleMute();
      syncAudioUI(musicPct, sfxPct, isMuted);
    });
  }

  // In-game audio panel toggle
  const audioPanel = $("audio-panel");
  if (muteBtn && audioPanel) {
    muteBtn.addEventListener("click", () => {
      audioPanel.classList.toggle("hidden");
    });
  }

  // Music volume slider — in-game only
  const musicVolEl = $("music-vol");
  if (musicVolEl) {
    musicVolEl.addEventListener("input", () => {
      musicPct = parseInt(musicVolEl.value);
      SoundEngine.setMusicVolume(musicPct / 100);
      syncAudioUI(musicPct, sfxPct, isMuted);
    });
  }

  // SFX volume slider — in-game only
  const sfxVolEl = $("sfx-vol");
  if (sfxVolEl) {
    sfxVolEl.addEventListener("input", () => {
      sfxPct = parseInt(sfxVolEl.value);
      SoundEngine.setSfxVolume(sfxPct / 100);
      syncAudioUI(musicPct, sfxPct, isMuted);
    });
  }

  // Initial UI state
  syncAudioUI(musicPct, sfxPct, false);
}

// ── Enter overlay — at module level for clean gesture call stack ──────
// Browsers require play() to be in the direct call stack of a user event.
// Keeping this outside init() / DOMContentLoaded avoids async chain breaks.
function dismissOverlay() {
  const overlay = document.getElementById("enter-overlay");
  if (!overlay || overlay.classList.contains("fade-out")) return;
  overlay.classList.add("fade-out");
  SoundEngine.playTitle();
  setTimeout(() => overlay.remove(), 900);
}

(function () {
  function attachOverlay() {
    const overlay = document.getElementById("enter-overlay");
    if (!overlay) return;
    overlay.addEventListener("click", dismissOverlay);
    document.addEventListener("keydown", dismissOverlay, { once: true });
    document.addEventListener("touchstart", dismissOverlay, { once: true });
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", attachOverlay);
  } else {
    attachOverlay();
  }
})();

// ═══════════════════════════════════════════════════════════
//  NAVIGATION
// ═══════════════════════════════════════════════════════════

function show(screenId) {
  Object.values(screens).forEach((s) => s && s.classList.add("hidden"));
  if (screens[screenId]) screens[screenId].classList.remove("hidden");
}

function hide(id) {
  $(id).classList.add("hidden");
}
function unhide(id) {
  $(id).classList.remove("hidden");
}

// ═══════════════════════════════════════════════════════════
//  NEW GAME / LOAD
// ═══════════════════════════════════════════════════════════

async function startNewGame() {
  await api("/api/new", {});
  show("game");
  loadScene();
}

async function loadGame() {
  const data = await api("/api/load", {});
  if (!data.ok) {
    alert("No save found.");
    return;
  }
  SoundEngine.stopMusic(true);
  show("game");
  loadScene();
}

// ═══════════════════════════════════════════════════════════
//  SCENE LOADING
// ═══════════════════════════════════════════════════════════

async function loadScene() {
  showLoading(true);
  try {
    const data = await api("/api/scene");

    if (data.game_over) {
      if (data.credits) {
        show("credits");
        hide("credits-screen");
        unhide("credits-screen");
      }
      return;
    }

    currentScene = data;
    renderScene(data);

    if (data.combat) {
      startCombat(data);
    } else if (data.combat_resolved) {
      // Combat scene already won — advance immediately
      await api("/api/advance", {
        next_scene: "__scene_next__",
        scene_key: data.scene_key,
      });
      loadScene();
    }
  } catch (e) {
    console.error("Scene load error:", e);
  } finally {
    showLoading(false);
  }
}

// ═══════════════════════════════════════════════════════════
//  SCENE RENDERING
// ═══════════════════════════════════════════════════════════

function renderScene(data) {
  // ── Illustration — try .png first, fall back to .svg ────────
  const artKey = data.art_key || ART_FALLBACK;
  const imgKey = ART_ALIASES[artKey] || artKey;
  const artEl = $("scene-art");
  artEl.style.opacity = "0";
  artEl.src = ""; // clear first to force reload even if same src

  function tryLoad(exts, idx) {
    if (idx >= exts.length) {
      // All formats failed — show fallback
      artEl.src = `${ART_BASE}${ART_FALLBACK}.svg`;
      artEl.style.opacity = "1";
      return;
    }
    const url = `${ART_BASE}${imgKey}.${exts[idx]}`;
    artEl.onload = () => {
      artEl.style.opacity = "1";
    };
    artEl.onerror = () => tryLoad(exts, idx + 1);
    artEl.src = url;
  }
  tryLoad(["png", "jpg", "svg"], 0);

  // ── Scene music ───────────────────────────────────────────
  SoundEngine.playScene(artKey);

  // ── HUD ───────────────────────────────────────────────────
  if (data.hud) renderHUD(data.hud);

  // ── Header ────────────────────────────────────────────────
  const hdr = $("scene-header");
  if (data.header) {
    $("scene-title").textContent = data.header.title || "";
    $("scene-subtitle").textContent = data.header.subtitle || "";
    // Reset animation by cloning element
    hdr.classList.remove("hidden");
    hdr.style.animation = "none";
    hdr.offsetHeight; // force reflow
    hdr.style.animation = "";
  } else {
    hdr.classList.add("hidden");
  }

  // ── Notifications (items / shards) ────────────────────────
  const notif = $("notification");
  const notifParts = [];
  if (data.shards > 0) notifParts.push(`+ ${data.shards} echo shards`);
  if (data.items?.length) notifParts.push(...data.items.map((i) => `+ ${i}`));
  if (notifParts.length) {
    notif.innerHTML = notifParts.join("<br>");
    notif.classList.remove("hidden");
  } else {
    notif.classList.add("hidden");
  }

  // ── Memory flash ──────────────────────────────────────────
  const memFlash = $("memory-flash");
  if (data.memories?.length) {
    $("memory-text").textContent = data.memories[0];
    memFlash.classList.remove("hidden");
    SoundEngine.playSfx("memory");
  } else {
    memFlash.classList.add("hidden");
  }

  // ── Name input — reset ────────────────────────────────────
  $("name-input").value = "";
  $("name-input-wrap").classList.add("hidden");

  // ── Prose — paginated, one paragraph at a time ────────────
  _startParagraphs(data.paragraphs, () => {
    if (data.auto_advance && data.next) {
      advanceScene(data.next);
      return;
    }
    if (data.name_prompt) {
      const nameWrap = $("name-input-wrap");
      nameWrap.classList.remove("hidden");
      setTimeout(() => $("name-input").focus(), 100);
      return;
    }
    renderChoices(data.choices || [], data.next);
  });
}

function renderChoices(choices, autoNext) {
  const wrap = $("choices-wrap");
  wrap.innerHTML = "";

  if (autoNext && !choices.length) {
    const btn = document.createElement("button");
    btn.className = "choice-btn";
    btn.dataset.num = "·";
    btn.textContent = "Continue";
    btn.addEventListener("click", () => advanceScene(autoNext));
    wrap.appendChild(btn);
    return;
  }

  choices.forEach((choice, i) => {
    const btn = document.createElement("button");
    btn.className = "choice-btn";
    btn.dataset.num = i + 1;
    btn.textContent = choice.label;
    btn.addEventListener("mouseenter", () => SoundEngine.playSfx("choice"));
    btn.addEventListener("click", () => {
      SoundEngine.playSfx("confirm");
      makeChoice(choice.id);
    });
    wrap.appendChild(btn);
  });
}

async function advanceScene(nextKey) {
  showLoading(true);
  try {
    const payload = nextKey
      ? { next_scene: nextKey }
      : {
          next_scene: "__scene_next__",
          scene_key: currentScene ? currentScene.scene_key : "",
        };
    const data = await api("/api/advance", payload);
    if (data.game_over) {
      unhide("credits-screen");
      return;
    }
    loadScene();
  } catch (e) {
    console.error("Advance error:", e);
    showLoading(false);
  }
}

// ═══════════════════════════════════════════════════════════
//  CHOICES
// ═══════════════════════════════════════════════════════════

async function makeChoice(choiceId) {
  showLoading(true);
  $("choices-wrap").innerHTML = "";
  try {
    // __next__ is a synthetic Continue for prose-only auto-next scenes
    if (choiceId === "__next__") {
      await advanceScene(null);
      return;
    }
    const data = await api("/api/choose", { choice_id: choiceId });
    if (data.game_over) {
      show("credits");
      unhide("credits-screen");
      return;
    }
    if (data.narration) {
      const proseEl = $("prose-body");
      proseEl.innerHTML = "";
      const div = document.createElement("div");
      div.className = "prose-block";
      div.textContent = data.narration;
      proseEl.appendChild(div);
      $("choices-wrap").innerHTML = "";
      $("notification").classList.add("hidden");
      showLoading(false);
      await sleep(1800);
    }
    loadScene();
  } catch (e) {
    console.error("Choice error:", e);
    showLoading(false);
    disableChoices(false);
  }
}

async function submitName() {
  const name = $("name-input").value.trim();
  if (!name) return;
  showLoading(true);
  try {
    await api("/api/choose", { name });
    loadScene();
  } catch (e) {
    showLoading(false);
  }
}

// ═══════════════════════════════════════════════════════════
//  HUD
// ═══════════════════════════════════════════════════════════

function renderHUD(hud) {
$("hp-bar").style.width = hud.hp_ratio * 100 + "%";
  $("wrath-bar").style.width = (hud.faith || 0) + "%";
  $("doubt-bar").style.width = (hud.doubt || 0) + "%";
  $("hud-hp-desc").textContent = hud.hp_desc || "";

  // Doubting state indicator
  const curseEl = $("hud-curse");
  curseEl.innerHTML = "";
  if (hud.is_doubting) {
    curseEl.textContent = "Doubting";
  }

  // Memories
  const memEl = $("hud-memories");
  if (hud.memories > 0) {
    memEl.textContent = `${hud.memories} ${hud.memories === 1 ? "memory" : "memories"} recovered`;
  }

  // Equipped items
  const eq = hud.equipped || {};
  const weaponEl = $("hud-weapon");
  if (weaponEl) weaponEl.textContent = eq.weapon && eq.weapon !== "unarmed" ? eq.weapon : "";
  const shieldEl = $("hud-shield");
  if (shieldEl) shieldEl.textContent = eq.shield || "";
  const offHandEl = $("hud-off-hand");
  if (offHandEl) offHandEl.textContent = eq.off_hand || "";

  // Inventory — unequipped items only
  const invEl = $("hud-inventory");
  if (invEl) {
    invEl.innerHTML = "";
    const equippedSet = new Set(Object.values(eq));
    (hud.inventory || []).filter((item) => !equippedSet.has(item)).forEach((item) => {
      const span = document.createElement("span");
      span.className = "hud-item";
      span.textContent = item;
      invEl.appendChild(span);
    });
  }
}

// ═══════════════════════════════════════════════════════════
//  COMBAT
// ═══════════════════════════════════════════════════════════

function startCombat(data) {
  inCombat = true;
  const c = data.combat;

  // Switch to combat music and set art — one declaration
  const artKey = data.art_key || "combat_draugar";
  const imgKeyC = ART_ALIASES[artKey] || artKey; // alias for image file
  SoundEngine.playScene(artKey);

  // Set combat art — try png/jpg before svg
  const combatArtEl = $("combat-art");
  combatArtEl.style.opacity = "0";
  combatArtEl.src = "";
  function tryCombatLoad(exts, idx) {
    if (idx >= exts.length) {
      combatArtEl.src = `${ART_BASE}${ART_FALLBACK}.svg`;
      combatArtEl.style.opacity = "1";
      return;
    }
    const url = `${ART_BASE}${imgKeyC}.${exts[idx]}`;
    combatArtEl.onload = () => {
      combatArtEl.style.opacity = "1";
    };
    combatArtEl.onerror = () => tryCombatLoad(exts, idx + 1);
    combatArtEl.src = url;
  }
  tryCombatLoad(["png", "jpg", "svg"], 0);

  // Enemy name & HP bar
  $("combat-enemy-name").textContent = c.enemy_name || "Enemy";
  $("enemy-hp-bar").style.width = c.enemy_hp_ratio * 100 + "%";

  // Initial log
  const logEl = $("combat-log");
  logEl.innerHTML = "";
  (c.log || []).forEach((msg) => appendCombatLog(msg));

  // Actions
  renderCombatActions(c.actions || []);

  // Show combat panel
  unhide("combat-panel");
}

function renderCombatActions(actions) {
  const wrap = $("combat-actions");
  wrap.innerHTML = "";
  actions.forEach((a) => {
    const btn = document.createElement("button");
    btn.className = "combat-btn";
    btn.textContent = a.label;
    btn.dataset.id = a.id;
    btn.addEventListener("click", () => doCombatAction(a.id));
    wrap.appendChild(btn);
  });
}

async function doCombatAction(actionId) {
  disableCombatBtns(true);
  try {
    const data = await api("/api/combat/action", { action_id: actionId });

    // Update enemy HP bar
    $("enemy-hp-bar").style.width = data.enemy_hp_ratio * 100 + "%";
    if (data.hud) renderHUD(data.hud);

    // Append log entries
    (data.log || []).forEach((msg) => appendCombatLog(msg));

    if (data.over) {
      await handleCombatEnd(data);
    } else {
      renderCombatActions(data.actions || []);
    }
  } catch (e) {
    console.error("Combat error:", e);
    disableCombatBtns(false);
  }
}

async function handleCombatEnd(data) {
  if (data.died) {
    // Show death overlay
    SoundEngine.playSfx("death");
    SoundEngine.stopMusic(true);
    hide("combat-panel");
    inCombat = false;
    const curseStacks = data.hud?.curse || 0;
    $("death-curse").textContent =
      curseStacks > 0
        ? `Curse: ${"●".repeat(curseStacks)}${"○".repeat(5 - curseStacks)}`
        : "";
    unhide("death-overlay");
    return;
  }

  // Won or fled — show rewards briefly then advance
  if (data.shards_gained > 0) {
    SoundEngine.playSfx("shards");
    appendCombatLog(`+ ${data.shards_gained} echo shards`, "system");
  }
  (data.items_gained || []).forEach((item) =>
    appendCombatLog(`+ ${item}`, "system"),
  );

  await sleep(1800);
  hide("combat-panel");
  inCombat = false;
  loadScene();
}

function appendCombatLog(msg, type = "") {
  const logEl = $("combat-log");
  const div = document.createElement("div");
  div.className = "log-entry" + (type ? ` ${type}` : "");
  // Auto-classify messages and play sfx
  if (!type) {
    if (
      msg.includes("taken") ||
      msg.includes("wound") ||
      msg.includes("fall")
    ) {
      div.classList.add("damage");
      SoundEngine.playSfx("combat_hit");
    } else if (
      msg.includes("miss") ||
      msg.includes("wide") ||
      msg.includes("step aside")
    ) {
      div.classList.add("miss");
      SoundEngine.playSfx("combat_miss");
    } else if (msg.includes("parry") || msg.includes("PARRY")) {
      div.classList.add("parry");
      SoundEngine.playSfx("combat_parry");
    }
  }
  div.textContent = msg;
  logEl.appendChild(div);
  // Scroll the wrapper (which has overflow-y: auto), not the log div itself
  const wrapEl = $("combat-log-wrap");
  if (wrapEl) wrapEl.scrollTop = wrapEl.scrollHeight;
}

async function riseAgain() {
  hide("death-overlay");
  loadScene();
}

// ═══════════════════════════════════════════════════════════
//  HELPERS
// ═══════════════════════════════════════════════════════════

function showLoading(on) {
  const el = $("loading");
  if (on) el.classList.remove("hidden");
  else el.classList.add("hidden");
}

function disableChoices(on) {
  document.querySelectorAll(".choice-btn").forEach((b) => (b.disabled = on));
}

function disableCombatBtns(on) {
  document.querySelectorAll(".combat-btn").forEach((b) => (b.disabled = on));
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

// ── Boot ──────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", init);
