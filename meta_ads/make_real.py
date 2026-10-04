"""Real-photo pack: streetwear-brand style ads built only from real photos.

No cut-outs, no fake backgrounds. A restrained film grade (lifted blacks,
split tone, halation, grain, vignette), a small box wordmark and one short
offer line. Formats: full-bleed lookbook frames, disposable-camera date
stamp, cinematic letterbox with subtitles, 35mm strip, contact sheet,
diptych and a printed lookbook grid. Native 4:5 and 9:16.
"""
import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from make_ads_v2 import ANTON, F, MARKER, PIXEL, cover, photo
from make_ads_v7 import CODE, IN4, IN6, IN8
from make_studio import tracked

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "real_pack")
SIZES = {"4x5": (1080, 1350, 48, 48), "9x16": (1080, 1920, 250, 400)}
YEL = (246, 196, 40)
WHITE = (255, 255, 255)
BLACK = (10, 10, 10)
OFFER = f"2 FOR $73.98  •  {CODE}"


# ------------------------------------------------------------ grade
def film(img, warm=0.03, halation=0.16, grain=7, vignette=0.22, seed=0, fade=0.06):
    a = np.asarray(img.convert("RGB")).astype(np.float32) / 255.0
    a = fade + (1 - fade - 0.02) * a                                    # lifted blacks, soft whites
    a = a + 0.10 * (a - 0.5) * (1 - np.abs(a - 0.5) * 2)                # gentle S
    lum = a.mean(axis=2, keepdims=True)
    a = lum + (a - lum) * 0.92                                          # slightly less saturated
    sh = np.clip(1 - lum * 2, 0, 1)
    hi = np.clip(lum * 2 - 1, 0, 1)
    a += sh * np.array([-0.012, 0.010, 0.022]) + hi * np.array([warm, warm * 0.35, -warm * 0.6])
    if halation:
        h = np.clip((lum - 0.78) / 0.22, 0, 1)[..., 0]
        hi_img = Image.fromarray((h * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(14))
        hv = np.asarray(hi_img).astype(np.float32)[..., None] / 255.0
        a += hv * halation * np.array([1.0, 0.35, 0.15])
    H, W = a.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / math.sqrt(2)
    a *= (1 - vignette * r ** 2)[..., None]
    rng = np.random.default_rng(seed)
    a += rng.normal(0, grain / 255.0, (H, W, 1))
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).convert("RGBA")


def shot(n, w, h, fy=0.5, fx=None, **kw):
    src = photo(n)
    if fx is None:
        img = cover(src, w, h, fy)
    else:
        s = max(w / src.width, h / src.height)
        big = src.resize((round(src.width * s), round(src.height * s)), Image.LANCZOS)
        x = round((big.width - w) * fx)
        y = round((big.height - h) * fy)
        img = big.crop((x, y, x + w, y + h))
    return film(img, **kw)


def zoom(n, box, w, h, **kw):
    """Crop a box (fractions of the source) and scale to w x h (cover)."""
    src = photo(n)
    x0, y0, x1, y1 = [int(v) for v in (box[0] * src.width, box[1] * src.height, box[2] * src.width, box[3] * src.height)]
    return film(cover(src.crop((x0, y0, x1, y1)), w, h, 0.5), **kw)


# ------------------------------------------------------------ marks
def box_logo(c, x, y, scale=1.0, anchor="l"):
    f = F(ANTON, int(34 * scale))
    d = ImageDraw.Draw(c)
    tw = sum(f.getlength(ch) for ch in "404 CULTURE") + 3 * 10
    bw, bh = tw + 28 * scale, 56 * scale
    if anchor == "r":
        x -= bw
    elif anchor == "m":
        x -= bw / 2
    d.rectangle((x, y, x + bw, y + bh), fill=YEL)
    tracked(d, (x + 14 * scale, y + 6 * scale), "404 CULTURE", f, BLACK, 3)


def bottom_line(c, sb, left, right, color=WHITE, shade=True):
    w, h = c.size
    y = h - sb - 46
    if shade:
        ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        od = ImageDraw.Draw(ov)
        for yy in range(y - 160, min(h, y + 120)):
            t = (yy - (y - 160)) / 220
            od.line([(0, yy), (w, yy)], fill=(0, 0, 0, int(140 * min(1, max(0, t)) ** 1.3)))
        c.alpha_composite(ov)
    d = ImageDraw.Draw(c)
    tracked(d, (44, y), left, F(IN8, 26), color, 4)
    tracked(d, (w - 44, y), right, F(IN8, 26), color, 4, anchor="r")


def date_stamp(c, xy, text):
    glow = Image.new("RGBA", c.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    f = F(PIXEL, 64)
    gd.text(xy, text, font=f, fill=(255, 120, 30, 255), anchor="rs")
    c.alpha_composite(glow.filter(ImageFilter.GaussianBlur(6)))
    ImageDraw.Draw(c).text(xy, text, font=f, fill=(255, 168, 70), anchor="rs")


def save(c, name, tag):
    os.makedirs(OUT, exist_ok=True)
    c.convert("RGB").save(os.path.join(OUT, f"{name}_{tag}.jpg"), quality=95)


# ------------------------------------------------------------ R01 lookbook frame
def r01():
    for tag, (w, h, st, sb) in SIZES.items():
        c = shot(7, w, h, fy=0.25, seed=1)
        box_logo(c, 44, st + 4)
        bottom_line(c, sb, "TIGER LEAGUE TEE  $39.99", OFFER)
        save(c, "R01_lookbook_brick", tag)


# ------------------------------------------------------------ R02 print detail
def r02():
    for tag, (w, h, st, sb) in SIZES.items():
        c = zoom(8, (0.08, 0.12, 0.92, 0.80), w, h, seed=2, halation=0.2)
        box_logo(c, 44, st + 4)
        bottom_line(c, sb, "LEAGUE CREST  •  LAYERED TRIM", OFFER)
        save(c, "R02_crest_detail", tag)


# ------------------------------------------------------------ R03 disposable stamp
def r03():
    for tag, (w, h, st, sb) in SIZES.items():
        c = shot(9, w, h, fy=0.3, seed=3, warm=0.05, vignette=0.3)
        date_stamp(c, (w - 50, h - sb - 120), "'26 10 04")
        box_logo(c, 44, st + 4, 0.85)
        bottom_line(c, sb, "TIGER LEAGUE TEE", OFFER)
        save(c, "R03_disposable_stamp", tag)


# ------------------------------------------------------------ R04 cinematic letterbox
def r04():
    for tag, (w, h, st, sb) in SIZES.items():
        c = Image.new("RGBA", (w, h), BLACK + (255,))
        fh = int(w / 1.85)
        cy = (st + h - sb) // 2
        frame = shot(6, w, fh, fy=0.22, seed=4, vignette=0.15)
        fd = ImageDraw.Draw(frame)
        f = F(IN6, 44)
        for i, line in enumerate(["I can't pick just one."]):
            fd.text((w / 2, fh - 70), line, font=f, fill=(255, 236, 120), anchor="mm", stroke_width=3,
                    stroke_fill=(0, 0, 0))
        c.alpha_composite(frame, (0, cy - fh // 2))
        d = ImageDraw.Draw(c)
        box_logo(c, w / 2, cy - fh // 2 - 120, 0.9, anchor="m")
        tracked(d, (w / 2, cy + fh // 2 + 60), "SO DON'T.", F(ANTON, 64), WHITE, 6, anchor="m")
        tracked(d, (w / 2, cy + fh // 2 + 160), OFFER, F(IN8, 28), YEL, 4, anchor="m")
        save(c, "R04_cinematic_cant_pick", tag)


# ------------------------------------------------------------ R05 35mm strip
def r05():
    for tag, (w, h, st, sb) in SIZES.items():
        c = Image.new("RGBA", (w, h), (18, 16, 14, 255))
        sw = int(w * 0.62)
        sx = (w - sw) // 2
        top, bot = st + 90, h - sb - 120
        d = ImageDraw.Draw(c)
        d.rectangle((sx, top - 30, sx + sw, bot + 30), fill=(30, 22, 14))
        frames = [(7, 0.2), (9, 0.25), (6, 0.25)]
        gap = 26
        fh = (bot - top - gap * 2) // 3
        fw = sw - 110
        for i, (n, fy) in enumerate(frames):
            y = top + i * (fh + gap)
            c.alpha_composite(shot(n, fw, fh, fy=fy, seed=10 + i, vignette=0.1), (sx + 55, y))
            d = ImageDraw.Draw(c)
            tracked(d, (sx + 55, y + fh + 2), f"404 CULTURE  400   {12 + i}A ▸", F(IN6, 14), (226, 150, 60), 2)
        for side in (sx + 14, sx + sw - 38):
            for y in range(top - 20, bot + 20, 46):
                d.rounded_rectangle((side, y, side + 24, y + 30), radius=5, fill=(18, 16, 14))
        box_logo(c, 44, st + 4, 0.85)
        tracked(d, (w / 2, h - sb - 60), OFFER, F(IN8, 28), YEL, 4, anchor="m")
        save(c, "R05_35mm_strip", tag)


# ------------------------------------------------------------ R06 contact sheet
def grease_circle(c, box, color=(220, 30, 30)):
    rng = random.Random(3)
    ov = Image.new("RGBA", c.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    x0, y0, x1, y1 = box
    for k in range(3):
        j = [rng.uniform(-10, 10) for _ in range(4)]
        d.ellipse((x0 + j[0], y0 + j[1], x1 + j[2], y1 + j[3]), outline=color + (230,), width=9)
    c.alpha_composite(ov.filter(ImageFilter.GaussianBlur(0.8)))


def r06():
    for tag, (w, h, st, sb) in SIZES.items():
        c = Image.new("RGBA", (w, h), (14, 14, 14, 255))
        cols, rows = 2, 3 if tag == "9x16" else 2
        frames = [(7, 0.2), (9, 0.25), (6, 0.25), (8, 0.3), ("z", 9, (0.2, 0.15, 0.85, 0.62)),
                  ("z", 7, (0.15, 0.05, 0.85, 0.55))][: cols * rows]
        top, bot = st + 150, h - sb - 150
        gw = (w - 120 - 40) // cols
        gh = (bot - top - 40 * (rows - 1)) // rows
        d = ImageDraw.Draw(c)
        for i, fr in enumerate(frames):
            x = 60 + (i % cols) * (gw + 40)
            y = top + (i // cols) * (gh + 40)
            if fr[0] == "z":
                img = zoom(fr[1], fr[2], gw, gh - 30, seed=20 + i, vignette=0.08, grain=5)
            else:
                img = shot(fr[0], gw, gh - 30, fy=fr[1], seed=20 + i, vignette=0.08, grain=5)
            c.alpha_composite(img, (x, y))
            d = ImageDraw.Draw(c)
            tracked(d, (x, y + gh - 24), f"{14 + i}", F(IN6, 18), (200, 200, 200), 2)
            tracked(d, (x + gw, y + gh - 24), "404 CULTURE", F(IN6, 14), (150, 150, 150), 2, anchor="r")
        grease_circle(c, (60 - 16, top - 16, 60 + gw + 16, top + gh - 10))
        d = ImageDraw.Draw(c)
        d.text((60 + 290, top - 100), "this one. x2", font=F(MARKER, 50), fill=(230, 40, 40))
        box_logo(c, 44, st + 4, 0.85)
        tracked(d, (w / 2, h - sb - 70), OFFER, F(IN8, 28), YEL, 4, anchor="m")
        save(c, "R06_contact_sheet", tag)


# ------------------------------------------------------------ R07 diptych
def r07():
    for tag, (w, h, st, sb) in SIZES.items():
        c = Image.new("RGBA", (w, h), (246, 244, 238, 255))
        g = 14
        top, bot = st + 100, h - sb - 120
        pw = (w - 3 * g) // 2
        c.alpha_composite(shot(7, pw, bot - top, fy=0.25, seed=30), (g, top))
        c.alpha_composite(shot(9, pw, bot - top, fy=0.3, seed=31), (2 * g + pw, top))
        d = ImageDraw.Draw(c)
        box_logo(c, g + 6, st + 20, 0.85)
        tracked(d, (w - g - 6, st + 36), "TIGER LEAGUE TEE", F(IN8, 24), BLACK, 4, anchor="r")
        tracked(d, (g + 6, bot + 34), "ONE FOR YOU  •  ONE FOR YOUR DAY ONE", F(IN8, 24), BLACK, 3)
        tracked(d, (w - g - 6, bot + 34), OFFER, F(IN8, 24), (200, 20, 30), 3, anchor="r")
        save(c, "R07_diptych", tag)


# ------------------------------------------------------------ R08 printed lookbook grid
def r08():
    for tag, (w, h, st, sb) in SIZES.items():
        c = Image.new("RGBA", (w, h), (242, 238, 230, 255))
        top, bot = st + 110, h - sb - 140
        g = 16
        cw = (w - 2 * 48 - g) // 2
        ch = (bot - top - g) // 2
        cells = [(7, 0.22), (8, 0.3), (6, 0.25), (9, 0.28)]
        for i, (n, fy) in enumerate(cells):
            x = 48 + (i % 2) * (cw + g)
            y = top + (i // 2) * (ch + g)
            c.alpha_composite(shot(n, cw, ch, fy=fy, seed=40 + i, vignette=0.1, grain=5), (x, y))
        d = ImageDraw.Draw(c)
        box_logo(c, 48, st + 26, 0.85)
        tracked(d, (w - 48, st + 44), "LOOKBOOK  04", F(IN8, 24), BLACK, 6, anchor="r")
        tracked(d, (48, bot + 40), "TIGER LEAGUE TEE  —  RED / GOLD", F(IN8, 24), BLACK, 3)
        tracked(d, (w - 48, bot + 40), OFFER, F(IN8, 24), (200, 20, 30), 3, anchor="r")
        save(c, "R08_lookbook_grid", tag)


# ------------------------------------------------------------ R09 get your own
def r09():
    for tag, (w, h, st, sb) in SIZES.items():
        c = shot(8, w, h, fy=0.0, seed=5, halation=0.2)
        d = ImageDraw.Draw(c)
        tracked(d, (w / 2, st + 110), "GET YOUR OWN.", F(ANTON, 96), WHITE, 6, anchor="m")
        box_logo(c, w / 2, st + 10, 0.8, anchor="m")
        bottom_line(c, sb, "TIGER LEAGUE TEE  $39.99", OFFER)
        save(c, "R09_get_your_own", tag)


# ------------------------------------------------------------ R10 flash-night grade
def flash_grade(img):
    a = np.asarray(img.convert("RGB")).astype(np.float32) / 255.0
    H, W = a.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.sqrt(((xx - W * 0.5) / (W * 0.55)) ** 2 + ((yy - H * 0.42) / (H * 0.55)) ** 2)
    falloff = np.clip(1.25 - 0.95 * r ** 1.5, 0.12, 1.25)[..., None]   # on-camera flash: hot centre, dark edges
    a = np.clip(a * falloff, 0, 1)
    a = 0.5 + (a - 0.5) * 1.18
    lum = a.mean(axis=2, keepdims=True)
    a = lum + (a - lum) * 1.08
    a += np.random.default_rng(9).normal(0, 0.03, (H, W, 1))
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).convert("RGBA")


def r10():
    for tag, (w, h, st, sb) in SIZES.items():
        c = flash_grade(cover(photo(7), w, h, 0.25))
        box_logo(c, w / 2, st + 4, 0.85, anchor="m")
        date_stamp(c, (w - 50, h - sb - 120), "'26 10 04")
        bottom_line(c, sb, "TIGER LEAGUE TEE", OFFER, shade=False)
        save(c, "R10_flash_night", tag)


if __name__ == "__main__":
    for fn in (r01, r02, r03, r04, r05, r06, r07, r08, r09, r10):
        fn()
        print(fn.__name__)
