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

- [ ] **broken_knight collapse-polku ilman on_death** — invoke_oath matalalla HP:lla triggeröi erityisen lopun, mutta ei aseta flagia/muistia; ei rekisteröidy pelitilaan
- [ ] **Enemy phrases ilman fallbackia** — `e["phrases"]["windup"]` / `"hit"` / `"miss"]` kaataa jos avain puuttuu; pitäisi käyttää `.get()` + tyhjä lista
- [ ] **`_advance_after_combat` pre_combat aina `{}`** — `combat.py`: pre_combat-dict rakennetaan muttei täytetä koskaan; scene-konteksti häviää taistelun jälkeen

### LOW — epäselvyys tai puuttuva logiikka

- [ ] **faith_hesitation-logiikka epäselvä** — `_resolve_enemy_turn()`: faith_hesitation-ehto lasketaan mutta ei käytetä systemaattisesti kaikkialla; kannattaa tarkistaa tarkoitus
- [ ] **commandery_night dead end** — molemmat valinnat silmukoivat takaisin itseensä; ei etene mihinkään (placeholder, mutta dokumentoimatta)

## Polish

- [ ] **HUD** — Body/Faith/Resolve/Doubt -statit; layout tarkistamatta
- [x] **Save/load UI** — favicon + "saved" välähdys lisätty
- [ ] **Mobiili** — testaamatta
