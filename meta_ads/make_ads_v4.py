"""Round 4: five conversion-focused Meta ads (1080x1350) for 404 CULTURE.

Direct-response formats: feature callouts, us-vs-basic comparison, styling
proof, product-page mock with upsell, and a colorway picker. Every ad keeps
the product large, the price obvious and a single tappable CTA.

Only claims visible in the product photos are used (layered trim, distressed
print, boxy cropped cut). No reviews, ratings, discounts or scarcity are
invented. If there is a real offer, set OFFER and it is added to every ad.
"""
import os

from PIL import Image, ImageDraw, ImageFilter

from make_ads_v2 import (ANTON, ARCHIVO, BLACK, BLUE, BODY, CREAM, DRED, F, H, NAVY, OUT, RED, W, WHITE, YELLOW,
                         cover, fit_font, fit_h, fit_w, garment, grain, model, photo, pill, put, save)
from make_ads_v3 import radial

OFFER = ""   # e.g. "FREE SHIPPING OVER $75" or "10% OFF WITH CODE LEAGUE" — only if it is real
INK = (22, 22, 22)
MUTED = (110, 110, 110)
PAPER = (247, 245, 240)
GREEN = (30, 170, 90)


def cta(d, y, text, bg=BLACK, fg=WHITE, size=40):
    """Full-width, button-shaped CTA — reads as tappable."""
    d.rounded_rectangle((60, y, W - 60, y + 104), radius=22, fill=bg)
    d.text((W // 2, y + 52), text, font=F(ARCHIVO, size), fill=fg, anchor="mm")


def offer_bar(d, bg=YELLOW, fg=BLACK):
    if OFFER:
        d.rectangle((0, 0, W, 56), fill=bg)
        d.text((W // 2, 28), OFFER, font=F(ARCHIVO, 26), fill=fg, anchor="mm")
        return 56
    return 0


def check(d, xy, s=30, color=GREEN):
    x, y = xy
    d.ellipse((x, y, x + s, y + s), fill=color)
    d.line([(x + s * .25, y + s * .52), (x + s * .43, y + s * .7), (x + s * .76, y + s * .32)], fill=WHITE, width=max(3, s // 8))


def cross(d, xy, s=30, color=(200, 200, 200)):
    x, y = xy
    d.ellipse((x, y, x + s, y + s), fill=color)
    p = s * .3
    d.line([(x + p, y + p), (x + s - p, y + s - p)], fill=WHITE, width=max(3, s // 8))
    d.line([(x + s - p, y + p), (x + p, y + s - p)], fill=WHITE, width=max(3, s // 8))


# ---------------------------------------------------------------- ad 16
def ad16_feature_callouts():
    c = radial((W, H), (W / 2, 640), 760, (214, 236, 250), (170, 210, 236))
    d = ImageDraw.Draw(c)
    top = offer_bar(d)
    d.text((W // 2, top + 44), "NOT YOUR BASIC TEE.", font=F(ANTON, 104), fill=NAVY, anchor="ma")
    d.text((W // 2, top + 196), "Tiger League Tee  •  Sky Blue", font=F(BODY, 32), fill=NAVY, anchor="ma")

    g = garment(4)
    pw = 700
    s = pw / g.width
    tee = fit_w(g, pw)
    ox, oy = (W - pw) // 2, 360
    put(c, tee, (ox, oy), off=(0, 22), blur=26, alpha=80)
    d = ImageDraw.Draw(c)

    def P(x, y):  # garment-pixel -> canvas
        return ox + x * s, oy + y * s

    callouts = [  # (point on garment, label anchor, label, side)
        (P(586, 470), (60, 300), "Distressed tiger crest", "l"),
        (P(1125, 360), (W - 60, 330), "Layered sleeve trim", "r"),
        (P(300, 880), (60, 1010), "Contrast double hem", "l"),
        (P(950, 800), (W - 60, 1000), "Boxy, cropped cut", "r"),
    ]
    f = F(ARCHIVO, 28)
    for i, (pt, (lx, ly), text, side) in enumerate(callouts, 1):
        tw = f.getlength(text)
        bw, bh = tw + 90, 64
        x0 = lx if side == "l" else lx - bw
        box = (x0, ly - bh / 2, x0 + bw, ly + bh / 2)
        ex = box[2] - 20 if side == "l" else box[0] + 20
        d.line([pt, (ex, ly)], fill=NAVY, width=4)
        d.ellipse((pt[0] - 12, pt[1] - 12, pt[0] + 12, pt[1] + 12), fill=WHITE, outline=NAVY, width=5)
        d.rounded_rectangle(box, radius=32, fill=NAVY)
        d.ellipse((x0 + 12, ly - 22, x0 + 56, ly + 22), fill=YELLOW)
        d.text((x0 + 34, ly), str(i), font=F(ARCHIVO, 24), fill=NAVY, anchor="mm")
        d.text((x0 + 70, ly), text, font=f, fill=WHITE, anchor="lm")

    d.text((W // 2, 1150), "$39.99", font=F(ANTON, 90), fill=NAVY, anchor="mm")
    cta(d, 1224, "SHOP THE TIGER TEE  →", bg=NAVY, fg=WHITE)
    save(grain(c, 3, 16), "16_feature_callouts.jpg")


# ---------------------------------------------------------------- ad 17
def basic_tee(w, color):
    """Plain generic tee silhouette."""
    im = Image.new("RGBA", (w, int(w * .95)), (0, 0, 0, 0))
    k = w / 100
    pts = [(35, 4), (42, 9), (58, 9), (65, 4), (88, 14), (100, 36), (84, 44), (80, 36), (80, 94),
           (20, 94), (20, 36), (16, 44), (0, 36), (12, 14)]
    ImageDraw.Draw(im).polygon([(x * k, y * k) for x, y in pts], fill=color)
    ImageDraw.Draw(im).arc((40 * k, 0, 60 * k, 16 * k), 0, 180, fill=tuple(v - 25 for v in color), width=int(2 * k))
    return im


def ad17_vs_basic():
    c = Image.new("RGBA", (W, H), PAPER + (255,))
    d = ImageDraw.Draw(c)
    top = offer_bar(d)
    d.rectangle((W // 2, top, W, H), fill=RED)
    d.text((W // 4, top + 44), "BASIC TEE", font=F(ANTON, 64), fill=MUTED, anchor="ma")
    d.text((W * 3 // 4, top + 44), "TIGER LEAGUE", font=F(ANTON, 64), fill=YELLOW, anchor="ma")

    bt = basic_tee(380, (200, 200, 198))
    put(c, bt, (W // 4 - bt.width // 2, 240), off=(0, 16), blur=18, alpha=60)
    m = fit_h(model(2), 980)
    mc = m.crop((0, 0, m.width, 580))
    put(c, mc, (W * 3 // 4 - mc.width // 2 + 20, 120), off=(0, 16), blur=20, alpha=90)
    d = ImageDraw.Draw(c)
    d.rectangle((W // 2, 700, W, 712), fill=RED)

    # VS badge
    d.ellipse((W // 2 - 60, 380, W // 2 + 60, 500), fill=BLACK, outline=WHITE, width=5)
    d.text((W // 2, 440), "VS", font=F(ANTON, 60), fill=WHITE, anchor="mm")

    rows = ["Layered contrast trim", "Vintage tiger graphic", "Boxy, cropped fit", "Works baggy or slim"]
    f = F(ARCHIVO, 29)
    y0 = 760
    for i, r in enumerate(rows):
        y = y0 + i * 86
        d.line([(60, y - 20), (W - 60, y - 20)], fill=(220, 218, 212), width=2)
        cross(d, (60, y), 42)
        d.text((118, y + 21), r, font=f, fill=(170, 170, 170), anchor="lm")
        check(d, (W // 2 + 30, y), 42, YELLOW)
        d.text((W // 2 + 88, y + 21), r, font=f, fill=WHITE, anchor="lm")
    d.line([(W // 2 + 42, 0 + y0 + 4 * 86 - 20), (W - 60, y0 + 4 * 86 - 20)], fill=(160, 20, 30), width=2)

    d.text((W // 4, 1150), "boring.", font=F(BODY, 34), fill=MUTED, anchor="mm")
    d.text((W * 3 // 4, 1150), "$39.99", font=F(ANTON, 84), fill=YELLOW, anchor="mm")
    d.rounded_rectangle((W // 2 + 40, 1215, W - 40, 1315), radius=22, fill=YELLOW)
    d.text((W * 3 // 4 + 0, 1265), "UPGRADE  →", font=F(ARCHIVO, 40), fill=BLACK, anchor="mm")
    d.text((W // 4, 1265), "404 CULTURE", font=F(ANTON, 44), fill=INK, anchor="mm")
    save(grain(c, 3, 17), "17_vs_basic_tee.jpg")


# ---------------------------------------------------------------- ad 18
def ad18_three_ways():
    c = Image.new("RGBA", (W, H), BLACK + (255,))
    d = ImageDraw.Draw(c)
    top = offer_bar(d)
    d.text((60, top + 36), "1 TEE.", font=F(ANTON, 124), fill=WHITE)
    d.text((W - 60, top + 36), "3 FITS.", font=F(ANTON, 124), fill=YELLOW, anchor="ra")
    cols = [("2.jpg", 0.3, "BAGGY WHITE DENIM"), ("5.jpg", 0.2, "WIDE-LEG + BOOTS"), ("1.jpg", 0.3, "SLIM + HIGH-TOPS")]
    gap, cw, ch, y = 16, (W - 120 - 32) // 3, 760, 230
    for i, (src, fy, lab) in enumerate(cols):
        x = 60 + i * (cw + gap)
        tile = cover(photo(int(src[0])), cw, ch, fy)
        m = Image.new("L", (cw, ch), 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, cw, ch), radius=20, fill=255)
        c.paste(tile, (x, y), m)
        d.rounded_rectangle((x + 14, y + 14, x + 84, y + 84), radius=14, fill=YELLOW)
        d.text((x + 49, y + 49), f"0{i + 1}", font=F(ANTON, 44), fill=BLACK, anchor="mm")
        d.rounded_rectangle((x, y + ch - 64, x + cw, y + ch), radius=20, fill=(0, 0, 0))
        d.rectangle((x, y + ch - 64, x + cw, y + ch - 40), fill=(0, 0, 0))
        d.text((x + cw / 2, y + ch - 32), lab, font=F(ARCHIVO, 22), fill=WHITE, anchor="mm")
    d.text((60, 1030), "Tiger League Tee", font=F(BODY, 38), fill=WHITE)
    d.text((60, 1078), "Red / Gold  •  layered trim", font=F(BODY, 28), fill=(170, 170, 170))
    d.text((W - 60, 1030), "$39.99", font=F(ANTON, 110), fill=YELLOW, anchor="ra")
    cta(d, 1200, "SHOP NOW  →", bg=YELLOW, fg=BLACK, size=44)
    save(grain(c, 4, 18), "18_one_tee_three_fits.jpg")


# ---------------------------------------------------------------- ad 19
def ad19_product_page():
    c = Image.new("RGBA", (W, H), (236, 234, 230, 255))
    d = ImageDraw.Draw(c)
    top = offer_bar(d)
    # "page" card
    card = (40, top + 40, W - 40, H - 40)
    d.rounded_rectangle((card[0], card[1] + 10, card[2], card[3] + 10), radius=36, fill=(210, 208, 204))
    d.rounded_rectangle(card, radius=36, fill=WHITE)
    # image area with the red model on a soft backdrop
    ia = (70, card[1] + 30, W - 70, card[1] + 640)
    img = radial((ia[2] - ia[0], ia[3] - ia[1]), (505, 260), 600, (252, 236, 226), (240, 206, 196))
    m = fit_h(model(2), 1080)
    mc = m.crop((0, 0, m.width, 620))
    img.alpha_composite(mc, ((img.width - mc.width) // 2, 20))
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, img.width, img.height), radius=26, fill=255)
    c.paste(img, (ia[0], ia[1]), mask)
    d = ImageDraw.Draw(c)
    # carousel dots
    for i in range(4):
        fill = BLACK if i == 0 else (200, 200, 200)
        d.ellipse((W // 2 - 44 + i * 26, ia[3] - 34, W // 2 - 32 + i * 26, ia[3] - 22), fill=fill)

    y = ia[3] + 26
    d.text((80, y), "404 CULTURE", font=F(ARCHIVO, 22), fill=MUTED)
    d.text((80, y + 30), "Tiger League Tee", font=F(ARCHIVO, 48), fill=INK)
    d.text((W - 80, y + 34), "$39.99", font=F(ARCHIVO, 48), fill=INK, anchor="ra")
    # colour swatches
    y += 110
    d.text((80, y), "COLOR:", font=F(ARCHIVO, 22), fill=INK)
    d.text((180, y), "Red / Gold", font=F(BODY, 22), fill=MUTED)
    for i, (col, sel) in enumerate([((200, 24, 34), True), (BLUE, False)]):
        cx = 100 + i * 80
        if sel:
            d.ellipse((cx - 32, y + 38, cx + 32, y + 102), outline=INK, width=4)
        d.ellipse((cx - 24, y + 46, cx + 24, y + 94), fill=col)
    # sizes
    y += 128
    d.text((80, y), "SIZE:", font=F(ARCHIVO, 22), fill=INK)
    for i, sz in enumerate(["S", "M", "L", "XL", "XXL"]):
        x0 = 80 + i * 118
        sel = sz == "L"
        d.rounded_rectangle((x0, y + 36, x0 + 102, y + 100), radius=14, fill=INK if sel else WHITE,
                            outline=INK if sel else (210, 210, 210), width=3)
        d.text((x0 + 51, y + 68), sz, font=F(ARCHIVO, 26), fill=WHITE if sel else INK, anchor="mm")
    # add to cart + finger tap
    y += 130
    d.rounded_rectangle((80, y, W - 80, y + 96), radius=48, fill=RED)
    d.text((W // 2, y + 48), "ADD TO CART  —  $39.99", font=F(ARCHIVO, 36), fill=WHITE, anchor="mm")
    tx, ty = W - 150, y + 64
    for r, a in [(56, 60), (38, 110)]:
        ring = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(ring).ellipse((tx - r, ty - r, tx + r, ty + r), outline=(255, 255, 255, a), width=6)
        c.alpha_composite(ring)
    d = ImageDraw.Draw(c)
    d.ellipse((tx - 20, ty - 20, tx + 20, ty + 20), fill=(255, 255, 255, 200))
    # upsell row
    y += 124
    d.rounded_rectangle((80, y, W - 80, y + 130), radius=20, fill=(246, 244, 240))
    th = fit_h(garment(3), 104)
    c.alpha_composite(th, (100, y + 13))
    d = ImageDraw.Draw(c)
    d.text((100 + th.width + 24, y + 30), "Complete the fit:", font=F(BODY, 22), fill=MUTED)
    d.text((100 + th.width + 24, y + 62), "Culture Thermal  $52.99", font=F(ARCHIVO, 28), fill=INK)
    d.rounded_rectangle((W - 220, y + 38, W - 100, y + 92), radius=27, outline=INK, width=3)
    d.text((W - 160, y + 65), "+ ADD", font=F(ARCHIVO, 22), fill=INK, anchor="mm")
    save(c, "19_product_page.jpg")


# ---------------------------------------------------------------- ad 20
def ad20_pick_your_tiger():
    c = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    d = ImageDraw.Draw(c)
    d.polygon([(0, 0), (W * 0.62, 0), (W * 0.38, H), (0, H)], fill=RED)
    d.polygon([(W * 0.62, 0), (W, 0), (W, H), (W * 0.38, H)], fill=BLUE)
    top = offer_bar(d, BLACK, YELLOW)
    d.text((W // 2, top + 36), "PICK YOUR TIGER", font=fit_font(ANTON, "PICK YOUR TIGER", W - 100, 160), fill=WHITE,
           anchor="ma", stroke_width=6, stroke_fill=BLACK)

    r = fit_h(model(5), 900)
    b = fit_h(model(4), 900)
    put(c, b, (W - b.width + 60, 250), off=(-16, 16), blur=24, alpha=110)
    put(c, r, (-60, 250), off=(16, 16), blur=24, alpha=110)
    d = ImageDraw.Draw(c)

    def tag(x, y, name, fg, bg):
        d.rounded_rectangle((x, y, x + 400, y + 150), radius=20, fill=bg)
        d.text((x + 24, y + 18), name, font=F(ARCHIVO, 28), fill=fg)
        d.text((x + 24, y + 56), "$39.99", font=F(ANTON, 76), fill=fg)
    tag(40, 1000, "RED / GOLD", YELLOW, BLACK)
    tag(W - 440, 1000, "SKY BLUE", NAVY, WHITE)
    d.ellipse((W // 2 - 66, 1010, W // 2 + 66, 1142), fill=YELLOW, outline=BLACK, width=6)
    d.text((W // 2, 1076), "OR", font=F(ANTON, 60), fill=BLACK, anchor="mm")
    cta(d, 1200, "CHOOSE YOURS  →", bg=YELLOW, fg=BLACK, size=42)
    save(grain(c, 4, 20), "20_pick_your_tiger.jpg")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn in (ad16_feature_callouts, ad17_vs_basic, ad18_three_ways, ad19_product_page, ad20_pick_your_tiger):
        fn()
