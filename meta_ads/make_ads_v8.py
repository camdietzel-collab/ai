"""Round 8: five more feed-native ads carrying the BO15OFF offer.

Checkout screen (shows the real saving), lock-screen notifications,
photo dump, closet before/after meme and a tier list. The brand is the
only voice; no invented customers, reviews or counts.
"""
import os

from PIL import Image, ImageDraw, ImageFilter

from make_ads_v2 import BLACK, BLUE, H, NAVY, OUT, RED, W, WHITE, YELLOW, F, cover, garment, model, photo
from make_ads_v5 import red_tee_box, tight
from make_ads_v7 import (CODE, GREY_TXT, IN4, IN6, IN8, INK, avatar, emoji, rich, rich_len, rounded, save_as,
                         vgrad)

GREEN = (22, 150, 70)
TEE, THERMAL = 39.99, 52.99
DISCOUNT = round(TEE * 0.15, 2)          # 15% off the 2nd tee
TWO_TEES = round(TEE * 2 - DISCOUNT, 2)  # 73.98
EMOJI_EXTRA = "📸"


def red_tee_thumb(size, bg):
    rm = tight(model(2))
    x0, y0, x1, y1 = red_tee_box(rm)
    pad = int((x1 - x0) * 0.1)
    t = rm.crop((x0 - pad, y0 - pad * 2, x1 + pad, y1 + pad))
    return thumb_on(t, size, bg)


def thumb_on(img, size, bg, r=18):
    t = img.copy()
    t.thumbnail((int(size * 0.86), int(size * 0.86)), Image.LANCZOS)
    tile = Image.new("RGBA", (size, size), bg + (255,))
    tile.alpha_composite(t, ((size - t.width) // 2, (size - t.height) // 2))
    return rounded(tile, r)


def money(v):
    return f"${v:,.2f}"


# ---------------------------------------------------------------- ad 36
def ad36_checkout():
    c = Image.new("RGBA", (W, H), (245, 245, 247, 255))
    d = ImageDraw.Draw(c)
    rich(c, (50, 44), f"2 tiger tees = {money(TWO_TEES)} 🐯", F(IN8, 64), INK)
    d = ImageDraw.Draw(c)
    d.text((52, 130), f"with code {CODE}  •  2nd tee 15% off", font=F(IN6, 32), fill=GREY_TXT)

    card = (40, 210, W - 40, H - 40)
    d.rounded_rectangle(card, radius=34, fill=WHITE)
    # lock + title
    d.rounded_rectangle((80, 262, 104, 284), radius=4, fill=INK)
    d.arc((84, 246, 100, 270), 180, 360, fill=INK, width=4)
    d.text((120, 254), "Checkout", font=F(IN8, 36), fill=INK)
    d.text((card[2] - 40, 258), "404 CULTURE", font=F(IN6, 26), fill=GREY_TXT, anchor="ra")
    d.line([(80, 320), (card[2] - 40, 320)], fill=(234, 234, 234), width=2)

    rows = [(red_tee_thumb(130, (252, 232, 226)), "Tiger League Tee", "Red / Gold"),
            (thumb_on(garment(4), 130, (226, 240, 250)), "Tiger League Tee", "Sky Blue")]
    y = 344
    for th, name, var in rows:
        c.alpha_composite(th, (80, y))
        d = ImageDraw.Draw(c)
        d.ellipse((190, y - 10, 226, y + 26), fill=(110, 110, 110))
        d.text((208, y + 8), "1", font=F(IN6, 22), fill=WHITE, anchor="mm")
        d.text((240, y + 30), name, font=F(IN6, 34), fill=INK)
        d.text((240, y + 76), var, font=F(IN4, 28), fill=GREY_TXT)
        d.text((card[2] - 40, y + 30), money(TEE), font=F(IN6, 34), fill=INK, anchor="ra")
        y += 160

    # discount field, applied
    d.rounded_rectangle((80, y + 6, card[2] - 230, y + 96), radius=16, outline=(210, 210, 210), width=3)
    d.text((110, y + 51), CODE, font=F(IN8, 36), fill=INK, anchor="lm")
    d.rounded_rectangle((card[2] - 210, y + 6, card[2] - 40, y + 96), radius=16, fill=INK)
    d.text((card[2] - 125, y + 51), "Apply", font=F(IN6, 32), fill=WHITE, anchor="mm")
    y += 116
    chip = f"{CODE}  •  15% off 2nd item"
    cw = F(IN6, 26).getlength(chip) + 80
    d.rounded_rectangle((80, y, 80 + cw, y + 52), radius=26, fill=(226, 244, 232))
    c.alpha_composite(emoji("✅", 28), (96, y + 12))
    d = ImageDraw.Draw(c)
    d.text((136, y + 26), chip, font=F(IN6, 26), fill=GREEN, anchor="lm")
    y += 84
    d.line([(80, y), (card[2] - 40, y)], fill=(234, 234, 234), width=2)
    y += 22
    for k, v, col in [("Subtotal", money(TEE * 2), INK), (f"Discount ({CODE})", f"−{money(DISCOUNT)}", GREEN),
                      ("Shipping", "Calculated next step", GREY_TXT)]:
        d.text((80, y), k, font=F(IN4, 32), fill=INK if col != GREEN else GREEN)
        d.text((card[2] - 40, y), v, font=F(IN6 if col != GREY_TXT else IN4, 32), fill=col, anchor="ra")
        y += 54
    y += 8
    d.text((80, y), "Total", font=F(IN8, 44), fill=INK)
    d.text((card[2] - 40, y - 4), money(TWO_TEES), font=F(IN8, 54), fill=INK, anchor="ra")
    by = card[3] - 130
    d.rounded_rectangle((80, by, card[2] - 40, by + 100), radius=20, fill=RED)
    d.text(((80 + card[2] - 40) // 2, by + 50), "Pay now  →", font=F(IN8, 40), fill=WHITE, anchor="mm")
    save_as(c, "36_checkout_bo15off.jpg")


# ---------------------------------------------------------------- ad 37
def glass(c, box, r=36, tint=(255, 255, 255, 150)):
    x0, y0, x1, y1 = [int(v) for v in box]
    region = c.crop((x0, y0, x1, y1)).filter(ImageFilter.GaussianBlur(24))
    region.alpha_composite(Image.new("RGBA", region.size, tint))
    m = Image.new("L", region.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, region.width - 1, region.height - 1), radius=r, fill=255)
    c.paste(region, (x0, y0), m)


def ad37_lockscreen():
    c = cover(photo(4), W, H, 0.05).convert("RGBA")
    vgrad(c, 0, 520, 90, 20)
    vgrad(c, 700, H, 20, 120)
    d = ImageDraw.Draw(c)
    d.text((W // 2, 110), "Wednesday, September 30", font=F(IN6, 40), fill=WHITE, anchor="ma")
    d.text((W // 2, 150), "9:41", font=F(IN8, 250), fill=(255, 255, 255, 240), anchor="ma")
    notes = [("now", "Buy 1, get 1 15% off 🐯", f"use code {CODE} at checkout"),
             ("5m ago", "the tiger tees come in red + blue", "$39.99 each. get both."),
             ("12m ago", "the culture thermal is $52.99", "pair it with a tiger tee")]
    y = 610
    for when, title, body in notes:
        box = (40, y, W - 40, y + 176)
        glass(c, box)
        d = ImageDraw.Draw(c)
        tile = Image.new("RGBA", (88, 88), (0, 0, 0, 0))
        avatar(ImageDraw.Draw(tile), (0, 0), 44)
        c.alpha_composite(rounded(tile, 20), (70, y + 44))
        d = ImageDraw.Draw(c)
        d.text((182, y + 30), "404 CULTURE", font=F(IN8, 30), fill=INK)
        d.text((W - 76, y + 32), when, font=F(IN4, 26), fill=(70, 70, 70), anchor="ra")
        rich(c, (182, y + 72), title, F(IN6, 32), INK)
        d = ImageDraw.Draw(c)
        d.text((182, y + 116), body, font=F(IN4, 30), fill=(50, 50, 50))
        y += 196
    # lockscreen buttons + home bar
    for cx in (130, W - 130):
        glass(c, (cx - 50, H - 170, cx + 50, H - 70), r=50, tint=(40, 40, 40, 120))
    d = ImageDraw.Draw(c)
    d.rounded_rectangle((W // 2 - 140, H - 30, W // 2 + 140, H - 20), radius=5, fill=WHITE)
    # flashlight / camera glyphs
    d.rounded_rectangle((120, H - 140, 140, H - 100), radius=4, outline=WHITE, width=4)
    d.rounded_rectangle((W - 160, H - 138, W - 100, H - 100), radius=8, outline=WHITE, width=4)
    d.ellipse((W - 142, H - 130, W - 118, H - 106), outline=WHITE, width=4)
    save_as(c, "37_lockscreen_notifications.jpg")


# ---------------------------------------------------------------- ad 38
def ad38_photo_dump():
    c = Image.new("RGBA", (W, H), WHITE + (255,))
    d = ImageDraw.Draw(c)
    avatar(d, (40, 32), 36)
    d.text((126, 40), "404culture", font=F(IN8, 32), fill=INK)
    d.text((126, 80), "fit dump", font=F(IN4, 26), fill=GREY_TXT)
    g, x0, top = 10, 0, 140
    big_w, big_h = 640, 820
    sw = W - big_w - g
    c.paste(cover(photo(2), big_w, big_h, 0.3), (0, top))
    c.paste(cover(photo(4), sw, (big_h - g) // 2, 0.12), (big_w + g, top))
    c.paste(cover(photo(3), sw, (big_h - g) // 2, 0.3), (big_w + g, top + (big_h + g) // 2))
    bh = 280
    bw = (W - g) // 2
    c.paste(cover(photo(5), bw, bh, 0.2), (0, top + big_h + g))
    c.paste(cover(photo(1), W - bw - g, bh, 0.3), (bw + g, top + big_h + g))
    d = ImageDraw.Draw(c)
    # a couple of native-feeling stickers
    def pill(xy, text, bg, fg, f):
        tw = rich_len(text, f)
        x, y = xy
        d.rounded_rectangle((x, y, x + tw + 44, y + 64), radius=32, fill=bg)
        rich(c, (x + 22, y + 12), text, f, fg)
    pill((24, top + 24), "fit dump 📸", WHITE, INK, F(IN8, 34))
    d = ImageDraw.Draw(c)
    # footer offer
    fy = top + big_h + g + bh
    d.rectangle((0, fy, W, H), fill=BLACK)
    d.text((40, fy + (H - fy) // 2), "Buy 1, get 1 15% off", font=F(IN8, 40), fill=WHITE, anchor="lm")
    cw = F(IN8, 36).getlength(CODE) + 60
    d.rounded_rectangle((W - 40 - cw, fy + 22, W - 40, H - 22), radius=18, fill=YELLOW)
    d.text((W - 40 - cw / 2, fy + (H - fy) // 2), CODE, font=F(IN8, 36), fill=BLACK, anchor="mm")
    save_as(c, "38_fit_dump.jpg")


# ---------------------------------------------------------------- ad 39
def hanger(d, cx, y, w=150, color=(60, 60, 60)):
    d.arc((cx - 16, y - 34, cx + 16, y - 2), 180, 90, fill=color, width=5)
    d.line([(cx, y), (cx - w / 2, y + 44)], fill=color, width=5)
    d.line([(cx, y), (cx + w / 2, y + 44)], fill=color, width=5)
    d.line([(cx - w / 2, y + 44), (cx + w / 2, y + 44)], fill=color, width=5)


def plain_tee(w, color):
    im = Image.new("RGBA", (w, int(w * .95)), (0, 0, 0, 0))
    k = w / 100
    pts = [(35, 4), (42, 9), (58, 9), (65, 4), (88, 14), (100, 36), (84, 44), (80, 36), (80, 94),
           (20, 94), (20, 36), (16, 44), (0, 36), (12, 14)]
    ImageDraw.Draw(im).polygon([(x * k, y * k) for x, y in pts], fill=color)
    return im


def ad39_closet_meme():
    c = Image.new("RGBA", (W, H), WHITE + (255,))
    d = ImageDraw.Draw(c)
    f = F(IN6, 50)
    d.text((44, 40), "my closet before vs. after", font=f, fill=INK)
    d.text((44, 104), "finding 404 CULTURE", font=f, fill=INK)
    pw, ph, py = (W - 30) // 2, 900, 200
    panels = [(10, (228, 226, 222), "before"), (20 + pw, (40, 40, 44), "after")]
    for x, bg, lab in panels:
        d.rectangle((x, py, x + pw, py + ph), fill=bg)
        d.line([(x + 20, py + 90), (x + pw - 20, py + 90)], fill=(150, 150, 150), width=8)
    # before: sad plain tees
    for i, col in enumerate([(160, 160, 160), (120, 120, 120), (200, 200, 200), (90, 90, 90)]):
        cx = 10 + 70 + i * 110
        hanger(d, cx, py + 96, 120, (110, 110, 110))
        t = plain_tee(150, col)
        c.alpha_composite(t, (int(cx - 75), py + 130 + (i % 2) * 14))
    d = ImageDraw.Draw(c)
    d.text((10 + pw // 2, py + ph - 150), "basic.", font=F(IN8, 64), fill=(140, 140, 140), anchor="mm")
    # after: the drop
    ax = 20 + pw
    items = [(red_tee_thumb(240, (40, 40, 44)), ax + 130, py + 140),
             (thumb_on(garment(4), 240, (40, 40, 44)), ax + pw - 130, py + 140)]
    for img, cx, yy in items:
        hanger(d, cx, py + 96, 150, (200, 200, 200))
        c.alpha_composite(img, (cx - 120, yy))
    th = thumb_on(garment(3), 330, (40, 40, 44))
    c.alpha_composite(th, (ax + (pw - 330) // 2, py + 400))
    d = ImageDraw.Draw(c)
    for cx in (ax + 130, ax + pw - 130):
        hanger(d, cx, py + 96, 150, (200, 200, 200))
    d.text((ax + pw // 2, py + ph - 110), "the league.", font=F(IN8, 56), fill=YELLOW, anchor="mm")
    for x, _, lab in panels:
        d.rounded_rectangle((x + 16, py + ph - 66, x + 150, py + ph - 16), radius=25, fill=(0, 0, 0, 160))
        d.text((x + 83, py + ph - 41), lab, font=F(IN6, 28), fill=WHITE, anchor="mm")
    # offer
    d.rounded_rectangle((40, H - 136, W - 40, H - 36), radius=22, fill=BLACK)
    d.text((W // 2, H - 86), f"BUY 1, GET 1 15% OFF  •  CODE {CODE}", font=F(IN8, 36), fill=YELLOW, anchor="mm")
    save_as(c, "39_closet_before_after.jpg")


# ---------------------------------------------------------------- ad 40
def ad40_tier_list():
    c = Image.new("RGBA", (W, H), (26, 26, 28, 255))
    d = ImageDraw.Draw(c)
    rich(c, (40, 40), "ranking the 404 drop 🐯", F(IN8, 60), WHITE)
    d = ImageDraw.Draw(c)
    tiers = [("S", (255, 127, 127)), ("A", (255, 191, 127)), ("B", (255, 223, 127)), ("C", (255, 255, 127)),
             ("D", (191, 255, 127))]
    rh, top, lw = 176, 150, 150
    tile = 160
    items = [red_tee_thumb(tile, (58, 58, 62)), thumb_on(garment(4), tile, (58, 58, 62)),
             thumb_on(garment(3), tile, (58, 58, 62))]
    for i, (t, col) in enumerate(tiers):
        y = top + i * (rh + 4)
        d.rectangle((0, y, lw, y + rh), fill=col)
        d.text((lw // 2, y + rh // 2), t, font=F(IN8, 70), fill=BLACK, anchor="mm")
        d.rectangle((lw + 4, y, W, y + rh), fill=(44, 44, 48))
    for k, im in enumerate(items):
        c.alpha_composite(im, (lw + 16 + k * (tile + 12), top + (rh - tile) // 2))
    d = ImageDraw.Draw(c)
    d.text((lw + 40, top + (rh + 4) + rh // 2), "(nothing else made the list)", font=F(IN4, 30), fill=(120, 120, 124), anchor="lm")
    y = top + 5 * (rh + 4) + 20
    d.text((40, y), "no notes. get 2 and the 2nd one is 15% off.", font=F(IN6, 36), fill=WHITE)
    d.rounded_rectangle((40, H - 150, W - 40, H - 40), radius=22, fill=YELLOW)
    d.text((W // 2, H - 95), f"SHOP THE DROP  •  CODE {CODE}", font=F(IN8, 38), fill=BLACK, anchor="mm")
    save_as(c, "40_tier_list.jpg")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn in (ad36_checkout, ad37_lockscreen, ad38_photo_dump, ad39_closet_meme, ad40_tier_list):
        fn()
