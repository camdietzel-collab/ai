"""Round 3: five 'real-world object' Meta ads (1080x1350) for 404 CULTURE.

Magazine cover, street flyer with tear-off tabs, itemised receipt, gallery
wall, and stadium jumbotron. Shares helpers with make_ads_v2.
"""
import math
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from make_ads_v2 import (ANTON, ARCHIVO, BLACK, BLUE, BODY, CREAM, DRED, F, H, MARKER, MONO, NAVY, OUT, PIXEL,
                         RED, SERIF, W, WHITE, YELLOW, cover, fit_font, fit_h, fit_w, garment, grain, model,
                         label, photo, pill, put, rot, save, tape, torn)
import os


def barcode(d, x, y, w, h, seed=0, color=BLACK):
    rng = random.Random(seed)
    cx = x
    while cx < x + w:
        bw = rng.choice([2, 2, 3, 4, 6])
        if rng.random() > 0.45:
            d.rectangle((cx, y, cx + bw - 1, y + h), fill=color)
        cx += bw


def radial(size, center, radius, inner, outer):
    yy, xx = np.mgrid[0:size[1], 0:size[0]]
    t = np.clip(np.hypot(xx - center[0], yy - center[1]) / radius, 0, 1)[..., None]
    a = np.array(inner, float) * (1 - t) + np.array(outer, float) * t
    return Image.fromarray(a.astype(np.uint8)).convert("RGBA")


# ---------------------------------------------------------------- ad 11
def ad11_magazine():
    c = radial((W, H), (W * 0.55, H * 0.45), 900, (246, 240, 228), (205, 196, 180))
    d = ImageDraw.Draw(c)
    d.text((40, 30), "ISSUE 04  •  FALL / WINTER  •  THE STREET ISSUE", font=F(ARCHIVO, 24), fill=BLACK)
    mast = fit_font(ANTON, "LEAGUE", W - 50, 520)
    d.text((W // 2, 50), "LEAGUE", font=mast, fill=RED, anchor="ma")

    m = fit_h(model(2), 1130)
    put(c, m, (W - m.width - 10, H - m.height + 30), off=(-20, 14), blur=30, alpha=90)
    d = ImageDraw.Draw(c)

    # cover lines (left column)
    y = 540
    d.text((46, y), "THE", font=F(ANTON, 56), fill=BLACK)
    d.text((46, y + 56), "RED", font=F(ANTON, 170), fill=RED)
    d.text((46, y + 226), "ONE.", font=F(ANTON, 170), fill=BLACK)
    for i, line in enumerate(["Why the layered", "Tiger League Tee is", "the only tee you", "need this season."]):
        d.text((50, y + 430 + i * 34), line, font=F(SERIF, 26), fill=BLACK)
    d.rectangle((46, y + 578, 360, y + 583), fill=RED)
    d.text((46, y + 596), "PLUS: THE CULTURE", font=F(ARCHIVO, 24), fill=BLACK)
    d.text((46, y + 628), "THERMAL — $52.99", font=F(ARCHIVO, 24), fill=RED)

    # price roundel
    cx, cy, r = 880, 440, 96
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=YELLOW, outline=BLACK, width=4)
    d.text((cx, cy - 26), "NOW", font=F(ARCHIVO, 24), fill=BLACK, anchor="mm")
    d.text((cx, cy + 16), "$39.99", font=F(ANTON, 58), fill=BLACK, anchor="mm")

    # barcode box
    d.rectangle((46, 1210, 300, 1320), fill=WHITE)
    barcode(d, 60, 1222, 226, 64, seed=4)
    d.text((173, 1302), "0 404 2004 04", font=F(MONO, 16), fill=BLACK, anchor="mm")
    pill(d, (W - 50, 1285), "GET THE ISSUE  →", F(ARCHIVO, 30), BLACK, YELLOW, anchor="r")
    save(grain(c, 7, 11), "11_league_magazine.jpg")


# ---------------------------------------------------------------- ad 12
def ad12_street_flyer():
    rng = random.Random(3)
    c = Image.new("RGBA", (W, H), (58, 56, 54, 255))
    # layers of old half-torn posters
    for i in range(26):
        col = rng.choice([(190, 60, 50), (220, 200, 160), (70, 90, 140), (230, 225, 210), (40, 40, 40), (200, 170, 60)])
        w, h = rng.randint(260, 560), rng.randint(200, 520)
        p = torn(w, h, col, jag=14, seed=i)
        pd = ImageDraw.Draw(p)
        txt = rng.choice(["SHOW", "LIVE", "FRI", "SALE", "NOW", "04", "ROOM", "NIGHT"])
        pd.text((20, 10), txt, font=F(ANTON, rng.randint(80, 180)),
                fill=tuple(max(0, v - 60) for v in col))
        p = rot(p, rng.uniform(-8, 8))
        c.alpha_composite(p, (rng.randint(-200, W - 100), rng.randint(-200, H - 100)))
    c = Image.alpha_composite(c, Image.new("RGBA", (W, H), (20, 18, 16, 90)))
    c = c.filter(ImageFilter.GaussianBlur(1.2))

    # the flyer
    fw, fh = 860, 1180
    fl = Image.new("RGBA", (fw, fh), (0, 0, 0, 0))
    fd = ImageDraw.Draw(fl)
    body_h = fh - 230
    fd.rectangle((0, 0, fw, body_h), fill=(250, 248, 238))
    fd.text((fw // 2, 30), "HAVE YOU", font=F(ANTON, 118), fill=BLACK, anchor="ma")
    fd.text((fw // 2, 150), "SEEN THIS TEE?", font=fit_font(ANTON, "SEEN THIS TEE?", fw - 60, 200), fill=BLACK, anchor="ma")
    tee = rot(fit_w(garment(4), 540), -3)
    put(fl, tee, ((fw - tee.width) // 2, 320), off=(8, 10), blur=10, alpha=90)
    fl.alpha_composite(tape(160, 46, -35, seed=11), (120, 320))
    fl.alpha_composite(tape(160, 46, 30, seed=12), (600, 320))
    fd = ImageDraw.Draw(fl)
    lines = [("LAST SEEN:", "404 Culture"), ("ANSWERS TO:", "\"Tiger League\""), ("DESCRIPTION:", "Sky blue, layered sleeve"),
             ("REWARD:", "looking this good")]
    for i, (k, v) in enumerate(lines):
        yy = 800 + i * 38
        fd.text((70, yy), k, font=F(ARCHIVO, 28), fill=BLACK)
        fd.text((330, yy), v, font=F(MONO, 28), fill=BLACK)
    pl = label("$39.99", F(ANTON, 84), RED, WHITE, pad=(24, 6), deg=7, seed=21, jag=6)
    put(fl, pl, (560, 610), off=(6, 8), blur=8, alpha=120)
    fd = ImageDraw.Draw(fl)
    # tear-off tabs
    n, tw = 8, fw // 8
    for i in range(n):
        if i == 5:
            # torn off: ragged stub
            stub = torn(tw - 4, 34, (250, 248, 238), jag=10, seed=40 + i)
            fl.alpha_composite(stub, (i * tw + 2, body_h))
            continue
        tab = Image.new("RGBA", (220, tw - 6), (250, 248, 238, 255))
        ImageDraw.Draw(tab).text((12, (tw - 6) // 2), "404 CULTURE · $39.99", font=F(MONO, 17), fill=BLACK, anchor="lm")
        tab = tab.rotate(90, expand=True)
        if i == 2:
            tab = rot(tab, 6)
        fl.alpha_composite(tab, (i * tw + 3, body_h))
        fd.line([(i * tw, body_h), (i * tw, body_h + 220)], fill=(160, 160, 150), width=2)
    fd = ImageDraw.Draw(fl)
    fl = rot(fl, 2)
    put(c, fl, ((W - fl.width) // 2, 70), off=(10, 16), blur=18, alpha=170)
    d = ImageDraw.Draw(c)
    for sx, sy in [(200, 92), (880, 104)]:
        d.rectangle((sx, sy, sx + 34, sy + 6), fill=(200, 200, 205))
    note = rot(torn(300, 76, YELLOW, jag=5, seed=2), -7)
    ImageDraw.Draw(note)
    nd = Image.new("RGBA", (300, 76), (0, 0, 0, 0))
    ImageDraw.Draw(nd).text((150, 38), "SHOP NOW →", font=F(MARKER, 40), fill=BLACK, anchor="mm")
    base = torn(300, 76, YELLOW, jag=5, seed=2)
    base.alpha_composite(nd)
    put(c, rot(base, -7), (730, 1250), off=(6, 8), blur=8, alpha=140)
    save(grain(c, 10, 12), "12_have_you_seen_this_tee.jpg")


# ---------------------------------------------------------------- ad 13
def ad13_receipt():
    c = cover(photo(2), W, H, 0.3).convert("RGBA")
    c = Image.alpha_composite(c, Image.new("RGBA", (W, H), (0, 0, 0, 40)))
    rw, rh = 500, 1080
    r = Image.new("RGBA", (rw, rh), (0, 0, 0, 0))
    rd = ImageDraw.Draw(r)
    zig = 14
    pts = [(x, zig if (x // zig) % 2 else 0) for x in range(0, rw + 1, zig)]
    pts += [(x, rh - (zig if (x // zig) % 2 else 0)) for x in range(rw, -1, -zig)]
    rd.polygon(pts, fill=(250, 250, 246))
    f, fb = F(PIXEL, 38), F(PIXEL, 50)
    y = 40
    rd.text((rw // 2, y), "404 CULTURE", font=F(ANTON, 64), fill=BLACK, anchor="ma"); y += 90
    for s in ["STORE #404   REG 04", "09/30/26   THE LEAGUE"]:
        rd.text((rw // 2, y), s, font=f, fill=BLACK, anchor="ma"); y += 38
    y += 10

    def dash(y):
        rd.text((rw // 2, y), "-" * 26, font=f, fill=BLACK, anchor="ma")
    dash(y); y += 44
    items = [("TIGER TEE RED/GOLD", "39.99"), ("  x1  LAYERED FIT", ""), ("TIGER TEE SKY BLUE", "39.99"),
             ("  x1  LAYERED FIT", ""), ("CULTURE THERMAL", "52.99"), ("  x1  WAFFLE KNIT", "")]
    for k, v in items:
        rd.text((34, y), k, font=f, fill=BLACK)
        rd.text((rw - 34, y), v, font=f, fill=BLACK, anchor="ra")
        y += 40
    dash(y); y += 44
    for k, v in [("SUBTOTAL", "132.97"), ("COMPLIMENTS", "UNLIMITED"), ("BASIC FITS", "0.00")]:
        rd.text((34, y), k, font=f, fill=BLACK)
        rd.text((rw - 34, y), v, font=f, fill=BLACK, anchor="ra")
        y += 40
    dash(y); y += 44
    rd.text((34, y), "TOTAL", font=fb, fill=BLACK)
    rd.text((rw - 34, y), "$132.97", font=fb, fill=BLACK, anchor="ra"); y += 70
    rd.text((rw // 2, y), "** NO RETURNS ON **", font=f, fill=BLACK, anchor="ma"); y += 38
    rd.text((rw // 2, y), "** COMPLIMENTS **", font=f, fill=BLACK, anchor="ma"); y += 60
    barcode(rd, 60, y, rw - 120, 90, seed=7); y += 110
    rd.text((rw // 2, y), "THANK YOU. STAY LEAGUE.", font=f, fill=BLACK, anchor="ma")
    r = rot(r, -5)
    put(c, r, (30, 200), off=(18, 22), blur=22, alpha=160)
    c.alpha_composite(tape(180, 52, 8, seed=3), (190, 180))
    d = ImageDraw.Draw(c)
    d.text((W - 50, 40), "THE FULL FIT,", font=F(ANTON, 86), fill=WHITE, anchor="ra", stroke_width=0)
    d.text((W - 50, 130), "ITEMIZED.", font=F(ANTON, 86), fill=YELLOW, anchor="ra")
    pill(d, (W - 50, 1275), "SHOP ALL 3  →", F(ARCHIVO, 34), YELLOW, BLACK, anchor="r")
    save(grain(c, 6, 13), "13_the_full_fit_itemized.jpg")


# ---------------------------------------------------------------- ad 14
def ad14_gallery():
    c = radial((W, H), (700, 380), 820, (250, 249, 246), (214, 212, 206))
    d = ImageDraw.Draw(c)
    floor_y = 1010
    fl = Image.new("RGBA", (W, H - floor_y), (196, 186, 170, 255))
    fd = ImageDraw.Draw(fl)
    for x in range(-400, W + 400, 120):
        fd.line([(x, 0), (x + (x - W / 2) * 0.6, H - floor_y)], fill=(184, 174, 158), width=2)
    c.alpha_composite(fl, (0, floor_y))
    d.line([(0, floor_y), (W, floor_y)], fill=(170, 164, 152), width=3)
    # spotlight
    spot = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(spot).polygon([(640, -20), (820, -20), (1080, 900), (400, 900)], fill=(255, 250, 230, 60))
    c.alpha_composite(spot.filter(ImageFilter.GaussianBlur(40)))

    th = fit_w(garment(3), 560)
    put(c, th, (440, 190), off=(0, 26), blur=30, alpha=90)
    d = ImageDraw.Draw(c)
    # wall placard
    d.rectangle((760, 760, 1020, 900), fill=WHITE, outline=(200, 198, 192), width=2)
    d.text((780, 776), "404 CULTURE", font=F(ARCHIVO, 20), fill=BLACK)
    d.text((780, 806), "Culture Thermal, 2026", font=F(SERIF, 20), fill=BLACK)
    d.text((780, 834), "Waffle knit, all-over print", font=F(BODY, 17), fill=(90, 90, 90))
    d.text((780, 862), "$52.99", font=F(ARCHIVO, 22), fill=RED)

    m = fit_h(model(4), 1060)
    put(c, m, (-80, H - m.height + 20), off=(30, 10), blur=30, alpha=80)
    d = ImageDraw.Draw(c)
    d.text((60, 50), "404 CULTURE GALLERY", font=F(ARCHIVO, 24), fill=BLACK)
    d.text((60, 84), "NOW ON VIEW", font=F(BODY, 20), fill=(110, 110, 110))
    d.text((W - 50, 1110), "WEARABLE", font=F(ANTON, 104), fill=BLACK, anchor="ra")
    d.text((W - 50, 1110 + 106), "ART.", font=F(ANTON, 104), fill=RED, anchor="ra")
    d.text((W - 50, 1110 - 30), "Thermal $52.99  ·  Tiger Tee $39.99", font=F(BODY, 24), fill=BLACK, anchor="ra")
    d.text((W - 300, 1300), "SHOP NOW  →", font=F(ARCHIVO, 30), fill=BLACK, anchor="ra")
    d.line([(W - 300 - F(ARCHIVO, 30).getlength("SHOP NOW  →"), 1306), (W - 300, 1306)], fill=BLACK, width=3)
    save(grain(c, 4, 14), "14_wearable_art.jpg")


# ---------------------------------------------------------------- ad 15
def led(canvas, xy, text, cell, on, off, size=16):
    """Dot-matrix LED text: render tiny, then draw each pixel as a lamp."""
    f = F(PIXEL, size)
    tw = int(f.getlength(text)) + 2
    asc, desc = f.getmetrics()
    m = Image.new("L", (tw, asc + desc), 0)
    ImageDraw.Draw(m).text((1, 0), text, font=f, fill=255)
    a = np.asarray(m)
    rows = [y for y in range(a.shape[0]) if a[y].max() > 100]
    a = a[min(rows): max(rows) + 1]
    glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    d = ImageDraw.Draw(canvas)
    x0, y0 = xy
    r = cell * 0.4
    for y in range(a.shape[0]):
        for x in range(a.shape[1]):
            cx, cy = x0 + x * cell, y0 + y * cell
            if a[y, x] > 100:
                gd.ellipse((cx - r * 2, cy - r * 2, cx + r * 2, cy + r * 2), fill=on + (90,))
                d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=on)
            else:
                d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=off)
    canvas.alpha_composite(glow.filter(ImageFilter.GaussianBlur(cell)))
    return a.shape[1] * cell, a.shape[0] * cell


def ad15_jumbotron():
    rng = random.Random(15)
    c = Image.new("RGBA", (W, H), (6, 10, 24, 255))
    sky = radial((W, H), (W / 2, 0), 1100, (30, 44, 90), (6, 8, 20))
    c.alpha_composite(sky)
    # stadium light rigs + bokeh
    b = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(b)
    for _ in range(60):
        x, y, r = rng.uniform(0, W), rng.uniform(980, 1250), rng.uniform(6, 22)
        bd.ellipse((x - r, y - r, x + r, y + r), fill=rng.choice([(255, 200, 80, 120), (255, 255, 255, 90), (220, 40, 50, 110)]))
    c.alpha_composite(b.filter(ImageFilter.GaussianBlur(6)))
    for rx in (70, 870):
        g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gd = ImageDraw.Draw(g)
        gd.ellipse((rx - 60, -60, rx + 200, 120), fill=(255, 255, 230, 140))
        c.alpha_composite(g.filter(ImageFilter.GaussianBlur(40)))
        d = ImageDraw.Draw(c)
        for i in range(4):
            for j in range(3):
                x, y = rx + i * 36, 12 + j * 30
                d.ellipse((x, y, x + 24, y + 22), fill=(255, 255, 240))

    # screen
    sx0, sy0, sx1, sy1 = 70, 150, 1010, 880
    d = ImageDraw.Draw(c)
    d.rectangle((sx0 - 18, sy0 - 18, sx1 + 18, sy1 + 18), fill=(28, 28, 32))
    d.rectangle((sx1 - 280, sy1 + 18, sx1 - 200, 1300), fill=(22, 22, 26))
    d.rectangle((sx0 + 200, sy1 + 18, sx0 + 280, 1300), fill=(22, 22, 26))
    scr = Image.new("RGBA", (sx1 - sx0, sy1 - sy0), RED + (255,))
    sd = ImageDraw.Draw(scr)
    for x in range(-scr.height, scr.width, 70):
        sd.polygon([(x, scr.height), (x + 35, scr.height), (x + 35 + scr.height, 0), (x + scr.height, 0)], fill=DRED)
    m = fit_h(model(1), scr.height + 40)
    base_x = scr.width // 2 - m.width // 2 + 60
    for k, (dx, a) in enumerate([(-240, 50), (-160, 80), (-80, 120)]):
        ghost = m.copy()
        tint = Image.new("RGBA", m.size, (255, 196, 0, 255))
        tint.putalpha(m.getchannel("A").point(lambda v: v * a // 255))
        scr.alpha_composite(tint, (base_x + dx, 20))
    scr.alpha_composite(m, (base_x, 20))
    sd = ImageDraw.Draw(scr)
    sd.rectangle((24, 24, 290, 80), fill=BLACK)
    sd.ellipse((40, 40, 64, 64), fill=(255, 40, 40))
    sd.text((78, 52), "TIGER CAM", font=F(ARCHIVO, 30), fill=WHITE, anchor="lm")
    sd.text((scr.width - 30, scr.height - 20), "LAYERED TIGER TEE", font=F(ANTON, 60), fill=YELLOW, anchor="rd")
    # scanlines
    for y in range(0, scr.height, 4):
        sd.line([(0, y), (scr.width, y)], fill=(0, 0, 0, 40))
    c.alpha_composite(scr, (sx0, sy0))

    # LED scoreboard
    by0 = 900
    d = ImageDraw.Draw(c)
    d.rectangle((sx0 - 18, by0, sx1 + 18, by0 + 160), fill=(10, 10, 12), outline=(40, 40, 46), width=4)
    amber, dim = (255, 170, 20), (40, 30, 20)
    led(c, (sx0 + 16, by0 + 30), "TIGERS 04", 7, amber, dim, 20)
    led(c, (sx0 + 590, by0 + 30), "$39.99", 7, (255, 60, 60), (40, 18, 18), 20)
    d = ImageDraw.Draw(c)
    d.text((W // 2, 1110), "THE LEAGUE IS IN SESSION.", font=F(ANTON, 72), fill=WHITE, anchor="ma")
    pill(d, (W // 2, 1265), "GET YOURS  →", F(ARCHIVO, 36), YELLOW, BLACK, anchor="m")
    save(grain(c, 8, 15), "15_tiger_cam.jpg")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn in (ad11_magazine, ad12_street_flyer, ad13_receipt, ad14_gallery, ad15_jumbotron):
        fn()
