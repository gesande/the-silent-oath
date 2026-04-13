# TODO — The Silent Oath

## Story & Content

- [ ] **Act I** — 4 kohtausta olemassa (intro, name_entry, descent, commandery_night); tarina kesken
- [ ] **Act II** — tyhjä placeholder
- [ ] **Act III+** — ei aloitettu
- [ ] **Kaikki kohtaukset englanniksi** — kirjoittamatta

## Design

- [ ] **Oath & Judgment -taistelumekaniikka** — combat.py koodattu, muttei testattu oikealla sisällöllä
- [ ] **Faith / Doubt -dynamiikka** — statit olemassa, vaikutukset määritelty koodissa; tarvitsee tarinan joka testaa ne
- [ ] **Vihollisdesign** — 8 vihollista määritelty (`royal_sergeant` → `hollow_choir`); ei sidottu kohtauksiin
- [ ] **Resoluutiot** — kill / free / understand -system koodattu; tarvitsee kohtaukset

## Engine

- [x] **`combat_prose.py`** — STRINGS-dict + prose-funktiot eriytetty `engine/combat.py`:stä omaan tiedostoon
- [x] **`COMBAT_MODS`** — data-drivenina `game_config.py`:ssä; `_player_damage()` lukee sieltä
- [x] **`engine/dice.py`** — lisätty
- [x] **`engine/scene.py`** — nimetty uudelleen (oli scene_web.py)

## Assets

- [x] `title.png` — olemassa
- [x] `commandery_night.png` — olemassa
- [x] `descent.png` — olemassa
- [x] `title.mp3` — olemassa
- [ ] Lisää art: name_entry, combat-kuvitukset, muut kohtaukset
- [ ] Lisää musiikki: kohtauskohtaiset raidat

## Bugit & Rakenneongelmat

### HIGH — kaataa tai rikkoo pelin

- [x] **enemies.py loot — kirjoitusvirheet** — `"Templar Sword"` ja `"Kite Shield"` korjattu; `"spoiled holy water"` lisätty CONSUMABLES:iin
- [x] **apply_choice() palautustyyppi epäyhtenäinen** — OOB-tapaus korjattu palauttamaan `(scene_key, None)`
- [x] **Ei enemy_key-validointia app.py:ssä** — lisätty tarkistus ennen ENEMIES-lookuppia
- [x] **commandery_night hardkoodattu fallbackiksi 3 kertaa** — `FALLBACK_SCENE` game_config.py:ssä, käytetään app.py:ssä

### MEDIUM — toiminnallisuus rikki tai puuttuu

- [x] **broken_knight collapse-polku ilman on_death** — `collapsed` flag lisätty; `_resolve_enemy_death` ohittaa väkivaltapalkinnot ja death-fraasit; flag/memory/loot silti triggeröityvät
- [x] **Enemy phrases ilman fallbackia** — `_physical_turn` käyttää `.get()` + tyhjä lista windup/hit/miss; `_resolve_enemy_death` sama death-fraaseille
- [x] **`_advance_after_combat` pre_combat aina `{}`** — luetaan `death_return` combat-beatista; fallback = nykyinen kohtaus (pelaaja palaa taistelun alkuun)

### LOW — epäselvyys tai puuttuva logiikka

- [x] **faith_hesitation-logiikka epäselvä** — bugi löydetty: `player.resolve -= 8` `_resolve_enemy_turn`:ssa oli väärin kohdistettu (piti olla ritarin, ei pelaajan); rivi poistettu, ritari menettää resolvea jo `_apply_special`:ssa
- [ ] **commandery_night dead end** — molemmat valinnat silmukoivat takaisin itseensä; ei etene mihinkään (placeholder, mutta dokumentoimatta)

## Polish

- [ ] **HUD** — Body/Faith/Resolve/Doubt -statit; layout tarkistamatta
- [x] **Save/load UI** — favicon + "saved" välähdys lisätty
- [ ] **Mobiili** — testaamatta
