# 404 CULTURE: "Order to outfit" (15s, 9:16)

The buying journey in 15 seconds: a customer finds the **Culture thermal** on 404cultureclothing.com, picks size L and checks out. The order lands on the owner's phone, and the piece is pulled from stock, packed and labelled. It arrives, gets unboxed, and is worn outside. Close-up, then end card.

`404_culture_order_to_outfit_animatic_15s.mp4` is the current cut: 1080×1920, 30 fps, sound mixed to -14 LUFS.

| Time | Shot | Status |
|---|---|---|
| 0.00–0.90 | A1 hand scrolling the site | **to film** (storyboard card) |
| 0.90–4.00 | S1–S4 phone close-ups: tap product → size L → add to cart → tap Check out | rendered from a site capture (stand-in, see below) |
| 4.00–5.00 | N1 owner's phone lights up: *New order · Culture thermal · Size L · $52.99*, on the drop | rendered, staged (no name, address or order number) |
| 5.00–9.00 | F1–F6 pull from stock, fold, mailer, seal, label | **to film** |
| 9.00–12.00 | D1–D4 doorstep, open, pull it out, match cut to wearing it | **to film** |
| 12.00–13.50 | W1 walking outside, thumbs-up | **to film** |
| 13.50–14.00 | C1 clean close-up from the real product photo | rendered |
| 14.00–15.00 | 404 CULTURE / PREMADE. READY TO SHIP. / 404cultureclothing.com | rendered |

The shoot plan is in [SHOT_LIST.md](SHOT_LIST.md). A printable 4×6 staged label for shot F6 is in `props/`.

## Product data

Pulled from the connected Shopify store: **Culture thermal**, $52.99, sizes Small / M / L / XL / 2XL, "Premade / 100% cotton / 3-5 day shipping". It's the listing with real stock (122 units), which is why it's the hero. `config.py` assumes it's the black "Culture Never Dies" thermal (`campaign/source/1.webp`). If it's the cream one, change `PRODUCT["photo"]` and `PRODUCT["cutout"]`.

## The website section

The build machine can't reach `404cultureclothing.com` or `cdn.shopify.com`: the environment's network policy blocks them. So `site/` is a **stand-in** store page built from the real listing data and product photos, using standard Shopify mobile-theme layout. Once both domains are allowed in the environment's network settings:

```
python3 capture_site.py --live   # real pages: collection, product, size L, add to cart
python3 assemble.py
```

Live capture only browses, picks a size and adds one item to a throwaway browser cart. It never presses Check out; the pressed look is a style change.

## Build

```
pip install pillow numpy scipy imageio-ffmpeg playwright==1.56.0
python3 capture_site.py   # build/screens/ (stand-in by default)
python3 props.py          # props/staged_shipping_label_4x6.{png,pdf}
python3 audio.py          # build/audio.wav
python3 assemble.py       # conform footage, render, mux
```

`assemble.py` conforms any clips in `footage/` (in-point, speed, 9:16 reframe from `footage/edit.json`) and falls back to storyboard cards for missing ones. It writes `404_culture_order_to_outfit_15s.mp4` once every filmed shot is present, and the `_animatic_` name until then. Music and sound design are synthesised in `audio.py` (original, no licensing), cued to the same timeline in `config.py`.
