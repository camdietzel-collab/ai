"""Round 5: five objection-handling / retargeting Meta ads (1080x1350).

Each ad removes one purchase blocker: "what does it look like on?"
(native shop-the-look post), "is it good quality?" (detail loupes),
"how does it fit?" (fit guide), "is it worth it?" (price-led) and
"I was going to buy it" (cart retargeting). Claims are limited to what
is visible in the photos; no reviews, ratings, discounts or scarcity.
"""
import os

import numpy as np
from PIL import Image, ImageDraw

from make_ads_v2 import (ANTON, ARCHIVO, BLACK, BLUE, BODY, CREAM, F, H, NAVY, OUT, RED, W, WHITE, YELLOW,
                         cover, fit_h, fit_w, garment, grain, model, put, save)
from make_ads_v3 import radial
from make_ads_v4 import INK, MUTED, PAPER, check, cta, offer_bar


def tight(im, thresh=128):
    a = np.asarray(im.getchannel("A"))
    ys, xs = np.where(a > thresh)
    return im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))


def color_box(im, rule):
    a = np.asarray(im).astype(int)
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    ys, xs = np.where(rule(r, g, b) & (al > 200))
    return xs, ys


def red_tee_box(im):
    xs, ys = color_box(im, lambda r, g, b: (r > 150) & (g < 90) & (b < 90))
    return int(np.percentile(xs, 1)), int(np.percentile(ys, 1)), int(np.percentile(xs, 99)), int(np.percentile(ys, 99.5))


def red_model():
    return tight(model(2))


# ---------------------------------------------------------------- ad 21
def ad21_shop_the_look():
    """Feed-native post with shopping tags — looks like content, not an ad."""
    c = Image.new("RGBA", (W, H), WHITE + (255,))
    d = ImageDraw.Draw(c)
    d.ellipse((30, 26, 94, 90), fill=YELLOW)
    d.text((62, 58), "404", font=F(ANTON, 26), fill=BLACK, anchor="mm")
    d.text((112, 36), "404culture", font=F(ARCHIVO, 28), fill=INK)
    d.text((112, 70), "Shop the look", font=F(BODY, 22), fill=MUTED)
    for i in range(3):
        d.ellipse((W - 70 + i * 16, 54, W - 62 + i * 16, 62), fill=INK)

    ph_top, ph_h = 116, 1080
    src = Image.open(os.path.join(os.path.dirname(__file__), "source", "2.jpg")).convert("RGB")
    fy = 0.25
    s = max(W / src.width, ph_h / src.height)
    oy = (src.height * s - ph_h) * fy
    c.paste(cover(src, W, ph_h, fy), (0, ph_top))

    def tag(pt, lines, side="r"):
        x, y = pt
        d.ellipse((x - 14, y - 14, x + 14, y + 14), fill=(255, 255, 255, 230), outline=BLACK, width=3)
        f1, f2 = F(ARCHIVO, 26), F(BODY, 24)
        tw = max(f1.getlength(lines[0]), f2.getlength(lines[1])) + 40
        bx = x + 40 if side == "r" else x - 40 - tw
        box = (bx, y - 46, bx + tw, y + 46)
        tip = [(x + 18, y), (bx, y - 12), (bx, y + 12)] if side == "r" else [(x - 18, y), (bx + tw, y - 12), (bx + tw, y + 12)]
        d.polygon(tip, fill=(20, 20, 20))
        d.rounded_rectangle(box, radius=14, fill=(20, 20, 20))
        d.text((bx + 20, y - 30), lines[0], font=f1, fill=WHITE)
        d.text((bx + 20, y + 4), lines[1], font=f2, fill=YELLOW)

    # tee position in the source photo (fractions measured on 2.jpg)
    tx, ty = src.width * 0.49 * s, src.height * 0.47 * s - oy + ph_top
    tag((tx, ty), ["Tiger League Tee", "$39.99  ›"], side="l")
    # bag icon
    bx, by = 40, ph_top + ph_h - 90
    d.ellipse((bx, by, bx + 60, by + 60), fill=(20, 20, 20, 220))
    d.rounded_rectangle((bx + 18, by + 24, bx + 42, by + 44), radius=3, outline=WHITE, width=3)
    d.arc((bx + 22, by + 14, bx + 38, by + 32), 180, 360, fill=WHITE, width=3)

    # native shop bar
    y = ph_top + ph_h
    d.rectangle((0, y, W, H), fill=(242, 242, 242))
    d.text((40, y + 40), "Tiger League Tee — Red / Gold", font=F(ARCHIVO, 28), fill=INK)
    d.text((40, y + 84), "$39.99  •  also in Sky Blue", font=F(BODY, 26), fill=MUTED)
    d.rounded_rectangle((W - 260, y + 44, W - 40, y + 116), radius=12, fill=(210, 210, 210))
    d.text((W - 150, y + 80), "Shop now", font=F(ARCHIVO, 28), fill=INK, anchor="mm")
    save(c, "21_shop_the_look.jpg")


# ---------------------------------------------------------------- ad 22
def loupe(c, src, center, r, zoom, at, ring=NAVY):
    """Circular magnified crop of `src` around `center`, drawn at `at`."""
    rr = r / zoom
    crop = src.crop((center[0] - rr, center[1] - rr, center[0] + rr, center[1] + rr)).resize((2 * r, 2 * r), Image.LANCZOS)
    bg = Image.new("RGBA", crop.size, (214, 236, 250, 255))
    bg.alpha_composite(crop)
    m = Image.new("L", crop.size, 0)
    ImageDraw.Draw(m).ellipse((0, 0, 2 * r - 1, 2 * r - 1), fill=255)
    shadow = Image.new("RGBA", crop.size, (0, 0, 0, 0))
    shadow.putalpha(m)
    put(c, shadow, (at[0] - r, at[1] - r), drop=True, off=(0, 18), blur=22, alpha=90)
    c.paste(bg, (at[0] - r, at[1] - r), m)
    ImageDraw.Draw(c).ellipse((at[0] - r, at[1] - r, at[0] + r, at[1] + r), outline=ring, width=10)


def ad22_look_closer():
    c = radial((W, H), (400, 600), 900, (236, 246, 252), (196, 224, 242))
    d = ImageDraw.Draw(c)
    top = offer_bar(d)
    d.text((60, top + 40), "LOOK CLOSER.", font=F(ANTON, 118), fill=NAVY)
    d.text((W - 60, top + 62), "$39.99", font=F(ANTON, 84), fill=NAVY, anchor="ra")
    d.text((60, top + 200), "The details a basic tee doesn't have.", font=F(BODY, 32), fill=NAVY)

    g = garment(4)
    gw = 620
    s = gw / g.width
    gx, gy = 30, 420
    put(c, fit_w(g, gw), (gx, gy), off=(0, 18), blur=22, alpha=80)
    d = ImageDraw.Draw(c)

    spots = [((586, 420), (840, 520), 170, "Distressed tiger print"),
             ((300, 875), (330, 1010), 130, "Layered contrast hem")]
    for (px, py), at, r, lab in spots:
        cx, cy = gx + px * s, gy + py * s
        d.line([(cx, cy), at], fill=NAVY, width=4)
        d.ellipse((cx - 16, cy - 16, cx + 16, cy + 16), outline=NAVY, width=5)
        loupe(c, g, (px, py), r, 1.05, at)
        d = ImageDraw.Draw(c)
        f = F(ARCHIVO, 26)
        tw = f.getlength(lab) + 40
        d.rounded_rectangle((at[0] - tw / 2, at[1] + r + 12, at[0] + tw / 2, at[1] + r + 62), radius=25, fill=NAVY)
        d.text((at[0], at[1] + r + 37), lab, font=f, fill=WHITE, anchor="mm")
    cta(d, 1224, "SHOP THE TIGER TEE  →", bg=NAVY, fg=WHITE)
    save(grain(c, 3, 22), "22_look_closer.jpg")


# ---------------------------------------------------------------- ad 23
def ad23_how_it_fits():
    c = radial((W, H), (360, 700), 900, (246, 242, 234), (220, 212, 198))
    d = ImageDraw.Draw(c)
    top = offer_bar(d)
    m = red_model()
    mh = 1240
    s = mh / m.height
    mm = fit_h(m, mh)
    mx, my = 40, H - mh + 30
    put(c, mm, (mx, my), off=(24, 10), blur=26, alpha=70)
    d = ImageDraw.Draw(c)
    x0, y0, x1, y1 = red_tee_box(m)
    X = lambda x: mx + x * s
    Y = lambda y: my + y * s
    tw_ = x1 - x0
    th_ = y1 - y0

    d.text((W - 60, top + 40), "HOW IT", font=F(ANTON, 110), fill=INK, anchor="ra")
    d.text((W - 60, top + 160), "FITS.", font=F(ANTON, 110), fill=RED, anchor="ra")

    notes = [((x0 + tw_ * 0.80, y0 + th_ * 0.06), 420, "Relaxed shoulders"),
             ((x1 - tw_ * 0.06, y0 + th_ * 0.25), 560, "Layered sleeve trim"),
             ((x0 + tw_ * 0.72, y0 + th_ * 0.55), 700, "Boxy through the body"),
             ((x0 + tw_ * 0.55, y1 - th_ * 0.02), 840, "Cropped at the waist")]
    lx = 660
    for (px, py), ly, text in notes:
        px, py = X(px), Y(py)
        d.line([(px, py), (lx - 20, ly)], fill=INK, width=3)
        d.ellipse((px - 11, py - 11, px + 11, py + 11), fill=YELLOW, outline=INK, width=4)
        check(d, (lx - 16, ly - 20), 40, RED)
        d.text((lx + 36, ly), text, font=F(ARCHIVO, 26), fill=INK, anchor="lm")

    d.text((W - 60, 990), "Tiger League Tee", font=F(BODY, 32), fill=INK, anchor="ra")
    d.text((W - 60, 1030), "$39.99", font=F(ANTON, 100), fill=RED, anchor="ra")
    d.rounded_rectangle((640, 1200, W - 40, 1300), radius=22, fill=INK)
    d.text(((640 + W - 40) // 2, 1250), "FIND MY SIZE  →", font=F(ARCHIVO, 34), fill=WHITE, anchor="mm")
    save(grain(c, 3, 23), "23_how_it_fits.jpg")


# ---------------------------------------------------------------- ad 24
def ad24_under_40():
    c = Image.new("RGBA", (W, H), YELLOW + (255,))
    d = ImageDraw.Draw(c)
    top = offer_bar(d, BLACK, YELLOW)
    d.text((W // 2, top + 30), "UNDER $40.", font=F(ANTON, 200), fill=BLACK, anchor="ma")
    d.text((W // 2, top + 300), "The easiest fit upgrade you'll buy this year.", font=F(BODY, 32), fill=BLACK, anchor="ma")

    panels = [(red_model(), RED, "RED / GOLD", YELLOW), (tight(model(4)), BLUE, "SKY BLUE", NAVY)]
    pw, ph, py = 470, 700, 400
    for i, (m, col, name, fg) in enumerate(panels):
        px = 60 + i * (pw + 20)
        d.rounded_rectangle((px, py, px + pw, py + ph), radius=28, fill=col)
        mm = fit_w(m, round(pw * 1.05)) if m.width / m.height > pw / (ph * 1.3) else fit_h(m, round(ph * 1.3))
        mm = mm.crop((0, 0, mm.width, min(mm.height, ph + 40)))
        layer = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
        layer.alpha_composite(mm, ((pw - mm.width) // 2, 40 if i == 0 else 10))
        mask = Image.new("L", (pw, ph), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, pw, ph), radius=28, fill=255)
        la = np.minimum(np.asarray(layer.getchannel("A")), np.asarray(mask))
        layer.putalpha(Image.fromarray(la))
        c.alpha_composite(layer, (px, py))
        d = ImageDraw.Draw(c)
        d.rounded_rectangle((px + 20, py + ph - 110, px + pw - 20, py + ph - 20), radius=20, fill=WHITE)
        d.text((px + 44, py + ph - 65), name, font=F(ARCHIVO, 26), fill=INK, anchor="lm")
        d.text((px + pw - 44, py + ph - 65), "$39.99", font=F(ANTON, 56), fill=RED if i == 0 else NAVY, anchor="rm")
    cta(d, 1180, "SHOP BOTH COLORWAYS  →", bg=BLACK, fg=YELLOW)
    d.text((W // 2, 1310), "+ The Culture Thermal, $52.99", font=F(BODY, 26), fill=BLACK, anchor="mm")
    save(grain(c, 4, 24), "24_under_40.jpg")


# ---------------------------------------------------------------- ad 25
def ad25_cart():
    """Retargeting: a cart drawer with the full fit and one big checkout button."""
    c = radial((W, H), (W / 2, 300), 1100, (40, 40, 48), (10, 10, 14))
    d = ImageDraw.Draw(c)
    top = offer_bar(d)
    d.text((W // 2, top + 40), "STILL THINKING", font=F(ANTON, 116), fill=WHITE, anchor="ma")
    d.text((W // 2, top + 166), "ABOUT IT?", font=F(ANTON, 116), fill=YELLOW, anchor="ma")

    card = (60, 360, W - 60, 1270)
    d.rounded_rectangle((card[0], card[1] + 14, card[2], card[3] + 14), radius=34, fill=(0, 0, 0))
    d.rounded_rectangle(card, radius=34, fill=WHITE)
    d.text((100, card[1] + 40), "YOUR CART (3)", font=F(ARCHIVO, 32), fill=INK)
    xx, xy = card[2] - 70, card[1] + 50
    d.line([(xx, xy), (xx + 24, xy + 24)], fill=MUTED, width=4)
    d.line([(xx + 24, xy), (xx, xy + 24)], fill=MUTED, width=4)
    d.line([(100, card[1] + 104), (card[2] - 40, card[1] + 104)], fill=(230, 230, 230), width=2)

    rm = red_model()
    x0, y0, x1, y1 = red_tee_box(rm)
    pad = int((x1 - x0) * 0.12)
    red_thumb = rm.crop((x0 - pad, y0 - pad * 2, x1 + pad, y1 + pad))
    items = [(red_thumb, (252, 232, 226), "Tiger League Tee", "Red / Gold  •  L", "$39.99"),
             (garment(4), (226, 240, 250), "Tiger League Tee", "Sky Blue  •  L", "$39.99"),
             (garment(3), (246, 242, 230), "Culture Thermal", "Cream  •  L", "$52.99")]
    y = card[1] + 130
    for thumb, bg, name, var, price in items:
        d.rounded_rectangle((100, y, 260, y + 160), radius=18, fill=bg)
        t = thumb.copy()
        t.thumbnail((140, 140), Image.LANCZOS)
        c.alpha_composite(t, (180 - t.width // 2, y + 80 - t.height // 2))
        d = ImageDraw.Draw(c)
        d.text((290, y + 30), name, font=F(ARCHIVO, 30), fill=INK)
        d.text((290, y + 76), var, font=F(BODY, 24), fill=MUTED)
        d.rounded_rectangle((290, y + 112, 400, y + 150), radius=19, outline=(210, 210, 210), width=2)
        d.text((345, y + 131), "–   1   +", font=F(BODY, 20), fill=INK, anchor="mm")
        d.text((card[2] - 40, y + 32), price, font=F(ARCHIVO, 30), fill=INK, anchor="ra")
        y += 186
    d.line([(100, y), (card[2] - 40, y)], fill=(230, 230, 230), width=2)
    d.text((100, y + 26), "Subtotal", font=F(BODY, 30), fill=INK)
    d.text((card[2] - 40, y + 22), "$132.97", font=F(ARCHIVO, 36), fill=INK, anchor="ra")
    d.rounded_rectangle((100, y + 90, card[2] - 40, y + 190), radius=50, fill=RED)
    d.text(((100 + card[2] - 40) // 2, y + 140), "CHECKOUT  →", font=F(ARCHIVO, 40), fill=WHITE, anchor="mm")
    d.text((W // 2, 1310), "Tees from $39.99  •  Thermal $52.99", font=F(BODY, 26), fill=CREAM, anchor="mm")
    save(grain(c, 3, 25), "25_still_thinking.jpg")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn in (ad21_shop_the_look, ad22_look_closer, ad23_how_it_fits, ad24_under_40, ad25_cart):
        fn()
