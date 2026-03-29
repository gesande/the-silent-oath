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

- [ ] **`combat_prose.py`** — tekstit kovakoodattu `combat.py`:hin; faith/doubt-dynamiikka vaikeuttaa erottelua; tehdään kun tarina on selkeämpi
- [ ] **`COMBAT_MODS`** — puuttuu `game_config.py`:stä (forgotten-among-the-fallenissa on esimerkki)
- [x] **`engine/dice.py`** — lisätty
- [x] **`engine/scene.py`** — nimetty uudelleen (oli scene_web.py)

## Assets

- [x] `title.png` — olemassa
- [x] `commandery_night.png` — olemassa
- [x] `descent.png` — olemassa
- [x] `title.mp3` — olemassa
- [ ] Lisää art: name_entry, combat-kuvitukset, muut kohtaukset
- [ ] Lisää musiikki: kohtauskohtaiset raidat

## Polish

- [ ] **HUD** — Body/Faith/Resolve/Doubt -statit; layout tarkistamatta
- [x] **Save/load UI** — favicon + "saved" välähdys lisätty
- [ ] **Mobiili** — testaamatta
