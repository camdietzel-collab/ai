"""Launch pack 2: five unique, offer-carrying concepts in 4:5 and 9:16.

Vending machine, RED vs BLUE fight poster, scratch-off card, newspaper
front page and a League member card. Same build() as launch pack 1:
full-bleed background per size + a 1080x1350 content layer that sits in
the Stories/Reels safe zone on 9:16.
"""
import math
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from make_ads_v2 import (ANTON, BLACK, BLUE, MARKER, NAVY, RED, WHITE, YELLOW, F, cover, fit_h, fit_w, garment,
                         grain, model, photo, rot)
from make_ads_v3 import barcode, radial
from make_ads_v5 import tight
from make_ads_v7 import CODE, GREY_TXT, IN4, IN6, IN8, INK, rounded, vgrad
from make_ads_v8 import TEE, THERMAL, TWO_TEES, money, red_tee_thumb, thumb_on
from make_ads_v10 import REG, red_tee_crop, shadowed, strike
from make_launch_pack import LH, LW, build, chip, cta, layer
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BLACKLETTER = os.path.join(HERE, "fonts", "Blackletter.ttf")
OSWALD = os.path.join(HERE, "fonts", "Oswald-700.ttf")
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
LCD = (120, 255, 140)


# ------------------------------------------------------------ 1. vending machine
def bg_night(w, h):
    c = radial((w, h), (w / 2, h * 0.35), max(w, h) * 0.75, (40, 40, 70), (8, 8, 16))
    d = ImageDraw.Draw(c)
    d.rectangle((0, h - 120, w, h), fill=(20, 20, 26))
    return c


def content_vending():
    L = layer()
    d = ImageDraw.Draw(L)
    body = (50, 20, LW - 50, 1180)
    glow = Image.new("RGBA", L.size, (0, 0, 0, 0))
    ImageDraw.Draw(glow).rounded_rectangle(body, radius=40, fill=(255, 60, 60, 120))
    L.alpha_composite(glow.filter(ImageFilter.GaussianBlur(40)))
    d = ImageDraw.Draw(L)
    d.rounded_rectangle(body, radius=40, fill=(196, 20, 32))
    d.rounded_rectangle((80, 44, LW - 80, 150), radius=20, fill=(30, 10, 12))
    d.text((LW // 2, 97), "404 CULTURE", font=F(ANTON, 80), fill=YELLOW, anchor="mm")
    # glass window
    gx0, gy0, gx1, gy1 = 80, 175, 720, 1010
    d.rounded_rectangle((gx0, gy0, gx1, gy1), radius=18, fill=(22, 24, 34))
    slots = [[(red_tee_thumb, None, "A1", money(TEE)), (None, 4, "A2", money(TEE))],
             [(None, 3, "B1", money(THERMAL)), (red_tee_thumb, None, "B2", money(TEE))],
             [(None, 4, "C1", money(TEE)), (None, 3, "C2", money(THERMAL))]]
    sw, sh = (gx1 - gx0 - 30) // 2, (gy1 - gy0 - 20) // 3
    for r, row in enumerate(slots):
        for k, (fn, g, codes, price) in enumerate(row):
            x, y = gx0 + 10 + k * (sw + 10), gy0 + 10 + r * sh
            img = fn(210, (22, 24, 34)) if fn else thumb_on(garment(g), 210, (22, 24, 34))
            L.alpha_composite(img, (x + (sw - 210) // 2, y + 8))
            d = ImageDraw.Draw(L)
            for i in range(7):  # spiral coil
                cx = x + 40 + i * (sw - 80) / 6
                d.ellipse((cx - 16, y + 206, cx + 16, y + 236), outline=(170, 170, 180), width=3)
            d.rectangle((x + 20, y + 238, x + sw - 20, y + 268), fill=(240, 240, 240))
            d.text((x + 34, y + 253), codes, font=F(IN8, 22), fill=INK, anchor="lm")
            d.text((x + sw - 34, y + 253), price, font=F(IN8, 22), fill=RED, anchor="rm")
    # glass glare
    glare = Image.new("RGBA", L.size, (0, 0, 0, 0))
    ImageDraw.Draw(glare).polygon([(gx0 + 60, gy0), (gx0 + 200, gy0), (gx0 + 20, gy1), (gx0, gy1 - 100)], fill=(255, 255, 255, 26))
    L.alpha_composite(glare)
    d = ImageDraw.Draw(L)
    # control panel
    px0, px1 = 745, LW - 80
    d.rounded_rectangle((px0, 175, px1, 1010), radius=16, fill=(150, 14, 24))
    d.rounded_rectangle((px0 + 16, 195, px1 - 16, 330), radius=10, fill=(10, 20, 12))
    d.text(((px0 + px1) // 2, 230), "ENTER CODE", font=F(IN6, 20), fill=(80, 180, 100), anchor="mm")
    d.text(((px0 + px1) // 2, 285), CODE, font=F(IN8, 36), fill=LCD, anchor="mm")
    keys = ["A", "B", "C", "1", "2", "OK"]
    for i, kk in enumerate(keys):
        kx = px0 + 30 + (i % 3) * 60
        ky = 360 + (i // 3) * 64
        d.rounded_rectangle((kx, ky, kx + 48, ky + 48), radius=8, fill=(235, 235, 235) if kk != "OK" else YELLOW)
        d.text((kx + 24, ky + 24), kk, font=F(IN8, 20), fill=INK, anchor="mm")
    d.rounded_rectangle((px0 + 16, 520, px1 - 16, 760), radius=10, fill=(250, 244, 230))
    for i, line in enumerate(["BUY 1", "GET 1", "15% OFF"]):
        d.text(((px0 + px1) // 2, 556 + i * 66), line, font=F(ANTON, 54), fill=RED if i == 2 else INK, anchor="mm")
    d.text(((px0 + px1) // 2, 820), "2 TEES", font=F(IN8, 28), fill=WHITE, anchor="mm")
    d.text(((px0 + px1) // 2, 870), money(TWO_TEES), font=F(ANTON, 60), fill=YELLOW, anchor="mm")
    d.rounded_rectangle((px0 + 70, 930, px1 - 70, 944), radius=7, fill=(40, 10, 14))
    # pickup bin
    d.rounded_rectangle((120, 1040, 680, 1140), radius=14, fill=(40, 10, 14))
    d.text((400, 1090), "PUSH", font=F(IN8, 34), fill=(120, 60, 60), anchor="mm")
    cta(d, 1215, f"GET 2 FOR {money(TWO_TEES)}  •  {CODE}", bg=YELLOW, fg=BLACK, size=36)
    return L


# ------------------------------------------------------------ 2. fight poster
def bg_fight(w, h):
    c = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    d = ImageDraw.Draw(c)
    d.polygon([(0, 0), (w * 0.56, 0), (w * 0.44, h), (0, h)], fill=(170, 14, 26))
    d.polygon([(w * 0.56, 0), (w, 0), (w, h), (w * 0.44, h)], fill=(40, 110, 190))
    spot = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(spot).ellipse((w * 0.1, -h * 0.2, w * 0.9, h * 0.6), fill=(255, 255, 255, 50))
    c.alpha_composite(spot.filter(ImageFilter.GaussianBlur(90)))
    return grain(c, 8, 3)


def content_fight():
    L = layer()
    d = ImageDraw.Draw(L)
    d.text((LW // 2, 30), "404 CULTURE PRESENTS", font=F(OSWALD, 36), fill=WHITE, anchor="ma")
    d.text((LW // 2, 80), "THE MAIN EVENT", font=F(OSWALD, 44), fill=YELLOW, anchor="ma")
    r = fit_h(tight(model(5)), 800)
    b = fit_h(tight(model(4)), 760)
    shadowed(L, b, (LW - b.width + 40, 350), blur=24, alpha=140, off=(-14, 10))
    shadowed(L, r, (-20, 350), blur=24, alpha=140)
    d = ImageDraw.Draw(L)
    f = F(ANTON, 170)
    d.text((40, 140), "RED", font=f, fill=WHITE, stroke_width=8, stroke_fill=BLACK)
    d.text((LW - 40, 140), "BLUE", font=f, fill=WHITE, anchor="ra", stroke_width=8, stroke_fill=BLACK)
    d.ellipse((LW // 2 - 80, 380, LW // 2 + 80, 540), fill=YELLOW, outline=BLACK, width=8)
    d.text((LW // 2, 460), "VS", font=F(ANTON, 90), fill=BLACK, anchor="mm")
    # bout card
    d.rectangle((0, 960, LW, 1186), fill=(0, 0, 0, 225))
    d.text((LW // 2, 978), "WHY CHOOSE? TAKE BOTH.", font=F(OSWALD, 56), fill=WHITE, anchor="ma")
    strike(d, (LW // 2 - 190, 1058), money(REG), F(OSWALD, 52), (170, 170, 170), anchor="ma")
    d.text((LW // 2 + 110, 1046), money(TWO_TEES), font=F(ANTON, 90), fill=YELLOW, anchor="ma")
    cta(d, 1214, f"GET BOTH  •  CODE {CODE}", bg=YELLOW, fg=BLACK, size=38)
    return L


# ------------------------------------------------------------ 3. scratch card
def bg_rays(w, h):
    c = Image.new("RGBA", (w, h), (255, 196, 0, 255))
    d = ImageDraw.Draw(c)
    cx, cy = w / 2, h * 0.45
    for i in range(24):
        a0, a1 = i * math.pi / 12, i * math.pi / 12 + math.pi / 24
        R = max(w, h) * 1.5
        d.polygon([(cx, cy), (cx + R * math.cos(a0), cy + R * math.sin(a0)), (cx + R * math.cos(a1), cy + R * math.sin(a1))],
                  fill=(255, 214, 60))
    return c


def content_scratch():
    L = layer()
    card = Image.new("RGBA", (900, 1060), (0, 0, 0, 0))
    cd = ImageDraw.Draw(card)
    cd.rounded_rectangle((0, 0, 899, 1059), radius=30, fill=(200, 20, 32))
    cd.rounded_rectangle((18, 18, 881, 1041), radius=22, fill=(255, 250, 238))
    cd.text((450, 50), "404 CULTURE", font=F(ANTON, 56), fill=RED, anchor="ma")
    cd.text((450, 126), "LUCKY TIGER", font=F(ANTON, 96), fill=INK, anchor="ma")
    cd.text((450, 252), "SCRATCH TO REVEAL YOUR CODE", font=F(IN8, 30), fill=GREY_TXT, anchor="ma")
    # scratch panel: silver with the code partly revealed
    sx0, sy0, sx1, sy1 = 70, 310, 830, 520
    cd.rounded_rectangle((sx0, sy0, sx1, sy1), radius=20, fill=WHITE)
    cd.text(((sx0 + sx1) // 2, (sy0 + sy1) // 2), CODE, font=F(IN8, 120), fill=RED, anchor="mm")
    foil = Image.new("RGBA", (sx1 - sx0, sy1 - sy0), (0, 0, 0, 0))
    fd = ImageDraw.Draw(foil)
    fd.rounded_rectangle((0, 0, foil.width - 1, foil.height - 1), radius=20, fill=(186, 188, 196))
    rng = random.Random(4)
    for _ in range(900):
        x, y = rng.uniform(0, foil.width), rng.uniform(0, foil.height)
        fd.point((x, y), fill=(220, 222, 230))
    mask = Image.new("L", foil.size, 255)
    md = ImageDraw.Draw(mask)
    for i in range(16):  # scratched strokes over the left ~70%
        y = 18 + i * 12
        md.line([(10 + rng.uniform(0, 30), y + rng.uniform(-6, 6)), (rng.uniform(440, 560), y + rng.uniform(-6, 6))], fill=0, width=26)
    foil.putalpha(Image.fromarray(np.minimum(np.asarray(foil.getchannel("A")), np.asarray(mask))))
    card.alpha_composite(foil, (sx0, sy0))
    cd = ImageDraw.Draw(card)
    # coin
    cx, cy = 790, 520
    cd.ellipse((cx - 56, cy - 56, cx + 56, cy + 56), fill=(214, 170, 40), outline=(160, 120, 20), width=6)
    cd.text((cx, cy), "404", font=F(ANTON, 40), fill=(150, 110, 20), anchor="mm")
    cd.text((450, 590), "BUY 1, GET 1 15% OFF", font=F(ANTON, 72), fill=INK, anchor="ma")
    x = 90
    for img in [red_tee_thumb(220, (246, 238, 222)), thumb_on(garment(4), 220, (246, 238, 222)),
                thumb_on(garment(3), 220, (246, 238, 222))]:
        card.alpha_composite(img, (x, 700))
        x += 250
    cd = ImageDraw.Draw(card)
    for i, p in enumerate([money(TEE), money(TEE), money(THERMAL)]):
        cd.text((200 + i * 250, 940), p, font=F(IN8, 32), fill=INK, anchor="mm")
    cd.text((450, 1000), f"2 tees = {money(TWO_TEES)} with the code", font=F(IN6, 28), fill=RED, anchor="mm")
    shadowed(L, rot(card, -3), (60, 40), blur=24, alpha=120)
    d = ImageDraw.Draw(L)
    cta(d, 1215, f"USE {CODE}  →", bg=BLACK, fg=YELLOW)
    return L


# ------------------------------------------------------------ 4. newspaper
def bg_paper(w, h):
    c = Image.new("RGBA", (w, h), (238, 232, 216, 255))
    return grain(c, 6, 9)


def wrap(text, font, width):
    words, line, out = text.split(), "", []
    for w_ in words:
        t = (line + " " + w_).strip()
        if font.getlength(t) > width:
            out.append(line)
            line = w_
        else:
            line = t
    out.append(line)
    return out


def content_newspaper():
    L = layer()
    d = ImageDraw.Draw(L)
    ink = (24, 22, 20)
    d.text((LW // 2, 16), "The 404 Times", font=F(BLACKLETTER, 116), fill=ink, anchor="ma")
    d.line([(40, 160), (LW - 40, 160)], fill=ink, width=4)
    d.text((40, 170), "VOL. 04", font=F(SERIF, 22), fill=ink)
    d.text((LW // 2, 170), "THE LEAGUE EDITION", font=F(SERIF, 22), fill=ink, anchor="ma")
    d.text((LW - 40, 170), "$39.99", font=F(SERIF, 22), fill=ink, anchor="ra")
    d.line([(40, 204), (LW - 40, 204)], fill=ink, width=2)
    d.text((LW // 2, 220), f"TIGER TEES: 2 FOR {money(TWO_TEES)}", font=F(OSWALD, 92), fill=ink, anchor="ma")
    d.text((LW // 2, 352), f"Code {CODE} takes 15% off the second one, sources confirm", font=F(SERIF_R, 30), fill=ink, anchor="ma")
    d.line([(40, 404), (LW - 40, 404)], fill=ink, width=2)
    # photo column
    ph = cover(photo(2), 600, 640, 0.28)
    L.paste(ph, (40, 424))
    d.text((40, 1074), "Pictured: the red Tiger League Tee, styled with baggy denim.", font=F(SERIF_R, 20), fill=ink)
    # text column
    x0, w = 670, LW - 40 - 670
    y = 424
    d.text((x0, y), "LOCAL FITS", font=F(OSWALD, 40), fill=ink)
    d.text((x0, y + 48), "IMPROVE", font=F(OSWALD, 40), fill=RED)
    y += 110
    body = ("The layered Tiger League Tee lands in red and blue. Boxy fit, contrast trim, a vintage tiger crest. "
            f"Grab two and the second is 15% off with {CODE}.")
    for line in wrap(body, F(SERIF_R, 24), w):
        d.text((x0, y), line, font=F(SERIF_R, 24), fill=ink)
        y += 32
    y += 20
    d.line([(x0, y), (LW - 40, y)], fill=ink, width=2)
    y += 16
    d.text((x0, y), "ALSO INSIDE", font=F(OSWALD, 30), fill=ink)
    y += 44
    L.alpha_composite(thumb_on(garment(3), 140, (238, 232, 216)), (x0, y))
    d = ImageDraw.Draw(L)
    d.text((x0 + 156, y + 24), "Culture", font=F(SERIF, 26), fill=ink)
    d.text((x0 + 156, y + 58), "Thermal", font=F(SERIF, 26), fill=ink)
    d.text((x0 + 156, y + 94), money(THERMAL), font=F(SERIF, 26), fill=RED)
    d.line([(40, 1110), (LW - 40, 1110)], fill=ink, width=4)
    d.text((LW // 2, 1126), "BUY 1, GET 1 15% OFF  •  CODE " + CODE, font=F(OSWALD, 44), fill=ink, anchor="ma")
    cta(d, 1215, "READ MORE: SHOP NOW  →", bg=ink, fg=(238, 232, 216))
    return L


# ------------------------------------------------------------ 5. member card
def bg_member(w, h):
    c = cover(photo(4), w, h, 0.1).filter(ImageFilter.GaussianBlur(26)).convert("RGBA")
    c.alpha_composite(Image.new("RGBA", (w, h), (0, 0, 20, 120)))
    return c


def content_member():
    L = layer()
    d = ImageDraw.Draw(L)
    d.text((LW // 2, 30), "WELCOME TO THE LEAGUE.", font=F(ANTON, 86), fill=WHITE, anchor="ma")
    cw, chh = 960, 620
    card = Image.new("RGBA", (cw, chh), (0, 0, 0, 0))
    cdd = ImageDraw.Draw(card)
    for x in range(cw):  # navy -> blue gradient
        t = x / cw
        cdd.line([(x, 0), (x, chh)], fill=(int(14 + 40 * t), int(30 + 90 * t), int(70 + 120 * t)))
    m = Image.new("L", (cw, chh), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, cw - 1, chh - 1), radius=36, fill=255)
    card.putalpha(m)
    cdd = ImageDraw.Draw(card)
    # holo stripe
    stops = [(255, 120, 200), (120, 220, 255), (255, 240, 140), (170, 140, 255)]
    for x in range(cw):
        t = x / cw * (len(stops) - 1)
        a, b = stops[int(t)], stops[min(int(t) + 1, len(stops) - 1)]
        f_ = t - int(t)
        cdd.line([(x, 96), (x, 118)], fill=tuple(int(a[k] + (b[k] - a[k]) * f_) for k in range(3)))
    cdd.text((40, 30), "404 CULTURE LEAGUE", font=F(IN8, 40), fill=WHITE)
    cdd.text((cw - 40, 38), "MEMBER", font=F(IN6, 28), fill=BLUE, anchor="ra")
    face = rounded(cover(photo(4), 230, 290, 0.08), 18)
    card.alpha_composite(face, (40, 145))
    fields = [("NAME", "YOU"), ("MEMBER SINCE", "TODAY"), ("PERK", "BUY 1, GET 1 15% OFF"), ("CODE", CODE)]
    y = 140
    for k, v in fields:
        cdd.text((300, y), k, font=F(IN6, 20), fill=BLUE)
        cdd.text((300, y + 24), v, font=F(IN8, 36 if k != "PERK" else 30), fill=YELLOW if k == "CODE" else WHITE)
        y += 76
    cdd.rounded_rectangle((40, 470, cw - 40, 580), radius=12, fill=WHITE)
    barcode(cdd, 70, 486, 560, 78, seed=11)
    cdd.text((cw - 70, 525), "Tigers 04", font=F(MARKER, 46), fill=INK, anchor="rm")
    shadowed(L, rot(card, -4), (40, 170), blur=26, alpha=150)
    d = ImageDraw.Draw(L)
    x = 90
    for img, p in [(red_tee_thumb(270, (240, 240, 244)), money(TEE)), (thumb_on(garment(4), 270, (240, 240, 244)), money(TEE)),
                   (thumb_on(garment(3), 270, (240, 240, 244)), money(THERMAL))]:
        L.alpha_composite(img, (x, 860))
        d = ImageDraw.Draw(L)
        d.rounded_rectangle((x + 60, 1100, x + 210, 1150), radius=25, fill=(0, 0, 0, 200))
        d.text((x + 135, 1125), p, font=F(IN8, 28), fill=WHITE, anchor="mm")
        x += 310
    cta(d, 1215, f"CLAIM YOUR PERK  •  {CODE}", bg=YELLOW, fg=BLACK, size=38)
    return L


ADS = [
    ("06_vending_machine", bg_night, content_vending),
    ("07_red_vs_blue_fight_poster", bg_fight, content_fight),
    ("08_scratch_card", bg_rays, content_scratch),
    ("09_the_404_times", bg_paper, content_newspaper),
    ("10_league_member_card", bg_member, content_member),
]

if __name__ == "__main__":
    for name, bg, content in ADS:
        build(name, bg, content)
