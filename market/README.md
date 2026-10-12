# 404 CULTURE: GPOE Streetwear Market booth promo (12s, Instagram ad)

`output/404_culture_market_9x16.mp4`: 1080x1920, 30 fps, H.264, no audio track.
`output/404_culture_market_4x5.mp4`: 1080x1350, same cut, text repositioned for Feed.
`output/404_culture_market_opening_frame.jpg`: first frame of the 9:16 cut, for Stories.

| Time | Beat |
|---|---|
| 0.0–2.0s | Hook: thermal product shot, punch-in. GREENSBORO / WED OCT 28 · 12–5 PM / ELM & BAIN, fully visible from frame 0 |
| 2.0–6.0s | THE THERMALS — 3 cuts (full, graphic detail, sleeve detail) |
| 6.0–10.0s | TIGER LEAGUE TEE — navy and baby-blue colorways, full + crest detail each |
| 10.0–12.0s | End card on concrete-gray: 404 CULTURE / GPOE STREETWEAR MARKET / date+time / address / follow CTA |

A persistent "OCT 28 · ELM & BAIN · 12–5 PM" strip runs 2.0–10.0s. Label/strip
backgrounds are solid concrete-gray cutouts (not just a dark overlay), so
the text never sits on top of a garment print regardless of the shot's crop.

## Known substitutions — confirm before posting

No clips of people wearing the gear, no official "404" logo file, and no
market-only piece photo exist in this environment (checked the whole repo
and the session's filesystem). This cut uses what's available instead:

- **Footage → flat-lay stills.** `../story/site/assets/img/culture-thermal.jpg`,
  `navy-tiger-tee.jpg`, `baby-blue-tiger-league.jpg` (flat lay on a plain
  background), treated with hard cuts and punch-in zooms instead of worn
  clips called for in the brief.
- **Logo → styled text.** No distressed "404" wordmark file exists; the end
  card sets "404 CULTURE" in Anton instead of the real logo.
- **Market-only piece → skipped**, per the brief's own fallback, since no
  photo of it exists. Its time went to THE THERMALS / TIGER LEAGUE TEE.
- **@handle → placeholder.** No real Instagram handle was found anywhere in
  this repo; the end card currently reads `@404CULTURE`. **Confirm or
  correct this before the ad runs.**

To redo this with the real assets (clips/photos/logo from a `gso-market-video`
folder), drop them in and point `SHOTS` / `PRODUCTS` in `render.py` at them.

## Rebuild

```
pip install pillow numpy
python3 render.py main    # 9x16 mp4
python3 render.py feed    # 4x5 mp4
python3 render.py still   # opening frame jpg
python3 render.py qa      # still frames at 0/1/2.5/6/9/11s, both aspects
```

Fonts: Anton + Bebas Neue (`fonts/`), both OFL-licensed, from
github.com/google/fonts.
