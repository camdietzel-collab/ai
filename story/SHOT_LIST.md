# Shot list: "Order to outfit" (15s, 9:16)

Twelve short phone clips. Everything else (the website close-ups, your phone lighting up with the order, the product close-up, the end card, music and sound) is already built. Once the clips are in `story/footage/`, `python3 assemble.py` cuts the finished ad.

## Before you shoot

- **One product, start to finish:** the tee you pick (**Baby blue tiger league** or **Navy tiger tee**; the edit renders either). Use that exact colourway in every shot, website to walk, and keep 3–6 units on hand for the stock shot.
- **Camera:** any recent phone, **vertical**, 4K or 1080p at **60 fps**. The edit slows some moves down. Turn off filters, beauty and "vivid" modes. Tap-and-hold to lock focus and exposure before each take.
- **Light:** daylight from a big window for the indoor shots, the same window for all of them, and no overhead bulbs mixed in. That keeps the tee's true colour and the print colours the same across every shot.
- **Takes:** start recording about 1s before the action and keep rolling about 1s after. Do 2–3 takes of each. The edit uses 0.5–1.5s of each clip.
- **Privacy:** use only the printed staged label (`props/staged_shipping_label_4x6.pdf`, 4×6 in). Don't show real labels, names, house numbers, street signs or licence plates.
- **Props:** a clean matte table, mailers (one colour), the staged label, a doorstep, and a helper to hold the camera for the door and walking shots.
- **The customer:** one person for D1–W1. Neutral bottoms and shoes with no other logos. Natural and relaxed, nothing acted.

## Shots

| Code | In the ad | Record | Framing | Action |
|---|---|---|---|---|
| **A1** | 0.00–0.90 | 4s | Close, from the side / over the shoulder; phone screen visible and bright | Thumb scrolls 404cultureclothing.com with natural flicks |
| S1–S4 | 0.90–4.00 | — | *rendered* | Website close-ups: tap product, pick size L, add to cart, tap Check out |
| N1 | 4.00–5.00 | — | *rendered* | Your phone lights up: "New order · (tee) · Size L · $39.99" |
| **F1** | 5.00–5.75 | 4s | Medium close on a stack or rail of the same tee (3+ visible) | A hand pulls one off the stack |
| **F2** | 5.75–6.50 | 5s | **Top-down**, phone locked in place above the table | Lay it flat graphic-up, fold the sleeves in |
| **F3** | 6.50–7.00 | 4s | **Identical** top-down position to F2 (don't move the phone) | Fold it in half, graphic side up |
| **F4** | 7.00–7.50 | 4s | Close, about 45° from above | Slide the folded tee into the mailer |
| **F5** | 7.50–8.25 | 4s | Tight on the flap | Peel the adhesive strip, press it shut, run fingers along the seal |
| **F6** | 8.25–9.00 | 4s | Top-down, label roughly filling the frame | Slap the staged label on, pat it, slide the package out of frame |
| **D1** | 9.00–9.75 | 5s | Low, doorstep level | Package on the mat, door opens, hand picks it up |
| **D2** | 9.75–10.50 | 4s | Close on hands | Tear the mailer open |
| **D3** | 10.50–11.25 | 5s | Close; **end with the chest graphic filling the frame, centred** | Pull the tee out and lift it straight toward the lens |
| **D4** | 11.25–12.00 | 5s | **Start on the same framing as D3's last frame**, now worn | Camera eases back to reveal the customer wearing it (waist up) |
| **W1** | 12.00–13.50 | 8s × 3 takes | Outside in daylight, full body, camera walking backwards ahead of them | Walk, glance or turn to camera, relaxed thumbs-up, keep walking |
| C1 | 13.50–14.00 | — | *rendered* | Clean close-up of the tee (product photo) |
| END | 14.00–15.00 | — | *rendered* | 404 CULTURE / PREMADE. READY TO SHIP. / 404cultureclothing.com |

### The two match cuts

- **F2 → F3:** keep the phone in exactly the same spot. The cut lands mid-fold, so the garment appears to fold itself.
- **D3 → D4:** D3 ends with the graphic filling the frame. D4 starts on that same framing at the same distance and height, with the tee now worn, then pulls back. Check D3's last frame on your screen before shooting D4.

## Delivering the clips

Name each file by its code (`A1.mov`, `F2.mp4` …) and put them in `story/footage/`, or share a Google Drive folder with me. Any missing clip keeps its storyboard card, so partial deliveries still render.

Per-clip trims go in `story/footage/edit.json`. I'll set these when the clips arrive:

```json
{
  "F2": {"in": 1.2, "speed": 0.8},
  "D3": {"in": 0.6, "speed": 0.5, "zoom": 1.1, "center": [0.5, 0.45]},
  "W1": {"in": 2.0, "speed": 0.7}
}
```

`in` = start time in the clip (s) · `speed` < 1 = slow motion (needs 60 fps) · `zoom` / `center` = reframe inside the 9:16 crop · `flip` = mirror.
