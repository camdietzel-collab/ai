# 404 CULTURE: premade tee designs (10)

Two new takes on each of the five reference pieces, rebranded to 404 CULTURE.
Every graphic is drawn from code. No reference pixels, logos or likenesses are reused.

| # | File | Garment | Based on |
|---|---|---|---|
| 01 | `out/01_eagle_lost_signal_tee.png` | washed black boxy tee | Americana eagle + flag |
| 02 | `out/02_eagle_home_of_the_lost_tee.png` | faded smoke boxy tee | Americana eagle + flag |
| 03 | `out/03_thermal_404_crt_longsleeve.png` | bone waffle thermal L/S | halftone photo thermal |
| 04 | `out/04_missed_calls_rotary_longsleeve.png` | charcoal waffle thermal L/S | halftone photo thermal |
| 05 | `out/05_heat_signature_orbit_tee.png` | washed black tee | thermal heat-map graphic |
| 06 | `out/06_err404_thermal_heart_tee.png` | faded black tee | thermal heat-map graphic |
| 07 | `out/07_memories_dont_load_longsleeve.png` | black L/S | faded gothic bats + script |
| 08 | `out/08_lost_never_found_longsleeve.png` | black L/S | faded gothic bats + script |
| 09 | `out/09_molten_cross_tee.png` | washed black crop tee | burning cross + outline tag |
| 10 | `out/10_burning_404_tee.png` | washed brown-black crop tee | burning cross + outline tag |

## Rebuild

```
NODE_PATH=$(npm root -g) node render.js          # all -> out/*.png (1800x2250)
NODE_PATH=$(npm root -g) node render.js 07       # just one
```

`lib.js` handles tee silhouettes, wash, fading, holes and raw edges. `eagle.js` covers the eagle, flag and arched type.
`fx.js` covers halftone, thermal, gothic line art and lava. `designs.js` holds the ten layouts. Fonts are from Google Fonts (OFL).
