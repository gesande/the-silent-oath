// ============================================================
//  audio.js — The Silent Oath
//  Named SoundEngine to avoid shadowing window.Audio.
// ============================================================

const SoundEngine = (() => {
  const SCENE_MUSIC = {
    title: "title",
    name_entry: "ambient_battlefield",
    battlefield: "ambient_battlefield",
    leif: "ambient_leif",
    longhouse: "ambient_forge",
    cairn: "ambient_cairn",
    mound: "ambient_mound",
    gunnar: "combat_gunnar",
    scavenge: "ambient_battlefield",
    combat_draugar: "combat_draugar",
    act_break: "ambient_void",
    // Act II — The Stirring Beneath
    forest: "forest",
    hermit_oak: "hermit_oak",
    fog_road: "ambient_fog",
    fog_sentinel: "combat_sentinel",
    gatehouse: "ambient_gatehouse",
    great_hall: "ambient_greathall",
    odrik_go_forward: "ambient_greathall",
  };

  const SFX_MAP = {
    choice: "sfx_choice",
    confirm: "sfx_confirm",
    memory: "sfx_memory",
    death: "sfx_death",
    shards: "sfx_shards",
    combat_hit: "sfx_hit",
    combat_miss: "sfx_miss",
    combat_parry: "sfx_parry",
  };

  let currentTrack = null;
  let currentTrackId = null;
  let musicVolume = 0.45;
  let sfxVolume = 0.7;
  let muted = false;

  const FADE_STEPS = 30;
  const FADE_DURATION = 2000;
  const MUSIC_BASE = "/static/audio/music/";
  const SFX_BASE = "/static/audio/sfx/"; // sfx in same folder for now

  // ── Crossfade ─────────────────────────────────────────────
  let _fadeTimer = null;
  let _outgoingTrack = null; // track currently fading out

  function _crossfade(incoming, outgoing) {
    if (_fadeTimer) {
      clearInterval(_fadeTimer);
      _fadeTimer = null;
    }
    // Stop any track that was still fading out from a previous transition
    if (_outgoingTrack) {
      _outgoingTrack.pause();
      _outgoingTrack.currentTime = 0;
    }
    _outgoingTrack = outgoing || null;

    const interval = FADE_DURATION / FADE_STEPS;
    let step = 0;
    _fadeTimer = setInterval(() => {
      step++;
      const r = step / FADE_STEPS;
      if (_outgoingTrack && !_outgoingTrack.paused)
        _outgoingTrack.volume = Math.max(0, musicVolume * (1 - r));
      if (incoming) incoming.volume = Math.min(musicVolume, musicVolume * r);
      if (step >= FADE_STEPS) {
        clearInterval(_fadeTimer);
        _fadeTimer = null;
        if (_outgoingTrack) {
          _outgoingTrack.pause();
          _outgoingTrack.currentTime = 0;
        }
        _outgoingTrack = null;
      }
    }, interval);
  }

  // ── Core switch — crossfades between tracks ───────────────
  function _switchTo(trackName) {
    if (trackName === currentTrackId) return;

    const outgoing = currentTrack;

    const track = new window.Audio();
    track.loop = true;
    track.volume = 0; // crossfade brings it up
    track.src = MUSIC_BASE + trackName + ".mp3";
    track.onerror = () => {
      track.src = MUSIC_BASE + trackName + ".ogg";
    };

    currentTrack = track;
    currentTrackId = trackName;

    if (muted) return;

    track
      .play()
      .then(() => _crossfade(track, outgoing))
      .catch((err) => console.warn("Audio blocked:", err.message));
  }

  // ── Public API ────────────────────────────────────────────
  function playTitle() {
    if (!muted) _switchTo("title");
  }

  function playScene(artKey) {
    if (muted) return;
    const t = SCENE_MUSIC[artKey] || "exploration";
    _switchTo(t);
  }

  function stopMusic(fade = true) {
    if (!currentTrack) return;
    if (_fadeTimer) {
      clearInterval(_fadeTimer);
      _fadeTimer = null;
    }
    if (fade) {
      _crossfade(null, currentTrack);
    } else {
      currentTrack.pause();
      currentTrack.currentTime = 0;
    }
    currentTrack = null;
    currentTrackId = null;
  }

  function playSfx(name) {
    if (muted) return;
    const sfxName = SFX_MAP[name];
    if (!sfxName) return;
    try {
      const a = new window.Audio(SFX_BASE + sfxName + ".wav");
      a.volume = sfxVolume;
      a.onerror = () => {
        a.src = SFX_BASE + sfxName + ".ogg";
        a.play().catch(() => {});
      };
      a.play().catch(() => {});
    } catch (e) {}
  }

  function toggleMute() {
    muted = !muted;
    if (currentTrack) currentTrack.volume = muted ? 0 : musicVolume;
    return muted;
  }

  function setMusicVolume(v) {
    musicVolume = Math.max(0, Math.min(1, v));
    if (currentTrack && !muted) currentTrack.volume = musicVolume;
  }

  function setSfxVolume(v) {
    sfxVolume = Math.max(0, Math.min(1, v));
  }
  function isMuted() {
    return muted;
  }

  return {
    playTitle,
    playScene,
    stopMusic,
    playSfx,
    toggleMute,
    isMuted,
    setMusicVolume,
    setSfxVolume,
  };
})();
