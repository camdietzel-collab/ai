"""Cinematic pack: Culture Never Dies drop + Tiger League, film-style ads.

Dark sets lit by beams with haze and dust, products relit from above with a
rim, film grade (from make_real.film), letterbox bars, movie-title type and
subtitles. Mixes the new product shots with real photos. Native 4:5 + 9:16.
Offers: Buy 1 Get 1 15% off (BO15OFF) and Buy 2 Get 1 50% off.
"""
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from make_ads_v2 import ANTON, F, cover, photo
from make_ads_v7 import CODE, IN4, IN6, IN8
from make_real import film
from make_studio import tracked

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "cinema_pack")
SIZES = {"4x5": (1080, 1350, 40, 40), "9x16": (1080, 1920, 250, 400)}
JP_SERIF = os.path.join(HERE, "fonts", "NotoSerifJP-600.ttf")
JP_SANS = os.path.join(HERE, "fonts", "NotoSansJP-700.ttf")
JP = "文化は決して滅びない"
WHITE, BLACK = (255, 255, 255), (6, 6, 8)
YEL, RED = (246, 196, 40), (214, 34, 40)
SOFT = (210, 206, 198)
OFFER_A = f"BUY 1, GET 1 15% OFF  •  CODE {CODE}"
OFFER_B = "BUY 2, GET 1 50% OFF"


def prod(name):
    return Image.open(os.path.join(HERE, "cutouts", f"prod_{name}.png")).convert("RGBA")


def newphoto(name):
    return Image.open(os.path.join(HERE, "source", "new", f"{name}.png")).convert("RGB")


# ------------------------------------------------------------ set + light
def stage(w, h, beams=((0.5, 0.5),), base=(9, 9, 11), glow=(255, 236, 205), beam_alpha=34, seed=0, floor=0.78):
    c = Image.new("RGBA", (w, h), base + (255,))
    for bx, spread in beams:
        b = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        top = (w * bx - w * 0.05, -10, w * bx + w * 0.05, -10)
        ImageDraw.Draw(b).polygon([(top[0], 0), (top[2], 0), (w * bx + w * spread * 0.5, h * floor),
                                   (w * bx - w * spread * 0.5, h * floor)], fill=glow + (beam_alpha,))
        c.alpha_composite(b.filter(ImageFilter.GaussianBlur(40)))
        p = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(p).ellipse((w * bx - w * spread * 0.55, h * floor - 50, w * bx + w * spread * 0.55, h * floor + 70),
                                  fill=glow + (int(beam_alpha * 1.6),))
        c.alpha_composite(p.filter(ImageFilter.GaussianBlur(40)))
    rng = np.random.default_rng(seed)
    haze = rng.normal(0, 1, (h // 24, w // 24))
    hz = Image.fromarray(np.clip(128 + haze * 40, 0, 255).astype(np.uint8)).resize((w, h), Image.BICUBIC).filter(
        ImageFilter.GaussianBlur(30))
    hl = Image.new("RGBA", (w, h), glow + (0,))
    hl.putalpha(hz.point(lambda v: max(0, v - 120) // 3))
    c.alpha_composite(hl)
    dust = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dust)
    r = random.Random(seed)
    for bx, spread in beams:
        for _ in range(70):
            x = w * bx + r.uniform(-0.4, 0.4) * w * spread
            y = r.uniform(0.05, floor) * h
            s = r.uniform(1, 3)
            dd.ellipse((x - s, y - s, x + s, y + s), fill=glow + (r.randint(40, 120),))
    c.alpha_composite(dust.filter(ImageFilter.GaussianBlur(0.8)))
    return c


def relight(img, top=1.18, bottom=0.62, rim=(255, 236, 210), rim_amt=0.5):
    a = np.asarray(img).astype(np.float32)
    H, W = a.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W]
    g = top + (bottom - top) * (yy / H) ** 1.2
    g *= 1 - 0.22 * (np.abs(xx - W / 2) / (W / 2)) ** 2
    rgb = a[..., :3] * g[..., None]
    A = img.getchannel("A")
    edge = np.asarray(A).astype(np.float32) - np.asarray(A.filter(ImageFilter.MinFilter(7))).astype(np.float32)
    edge = np.asarray(Image.fromarray(np.clip(edge, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(4))).astype(np.float32) / 255
    edge *= np.clip(1.2 - yy / H, 0, 1)                       # rim mostly on top edges
    rgb += edge[..., None] * rim_amt * (np.array(rim, np.float32) - rgb)
    return Image.fromarray(np.dstack([np.clip(rgb, 0, 255), a[..., 3]]).astype(np.uint8))


def put(c, img, cx, cy, width, rim_amt=0.5, shadow=True, sharpen=True):
    s = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
    if sharpen:
        s = s.filter(ImageFilter.UnsharpMask(radius=1.6, percent=60, threshold=2))
    s = relight(s, rim_amt=rim_amt)
    x0, y0 = round(cx - s.width / 2), round(cy - s.height / 2)
    if shadow:
        sh = Image.new("RGBA", c.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).ellipse((cx - s.width * 0.38, y0 + s.height + 18, cx + s.width * 0.38, y0 + s.height + 52),
                                   fill=(0, 0, 0, 200))
        c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
    c.alpha_composite(s, (x0, y0))
    return (x0, y0, x0 + s.width, y0 + s.height)


def finish(c, seed=0):
    return film(c, warm=0.02, halation=0.12, grain=6, vignette=0.28, seed=seed, fade=0.03)


def bars(c, top, bottom):
    d = ImageDraw.Draw(c)
    if top:
        d.rectangle((0, 0, c.width, top), fill=BLACK)
    if bottom:
        d.rectangle((0, c.height - bottom, c.width, c.height), fill=BLACK)


def mark(c, x, y, anchor="l", scale=0.8):
    f = F(ANTON, int(34 * scale))
    d = ImageDraw.Draw(c)
    tw = sum(f.getlength(ch) for ch in "404 CULTURE") + 30
    bw, bh = tw + 28 * scale, 56 * scale
    if anchor == "m":
        x -= bw / 2
    elif anchor == "r":
        x -= bw
    d.rectangle((x, y, x + bw, y + bh), fill=YEL)
    tracked(d, (x + 14 * scale, y + 6 * scale), "404 CULTURE", f, BLACK, 3)


def title_jp(c, y, size=64, font=JP_SERIF, color=WHITE, glow=True):
    f = F(font, size)
    if glow:
        g = Image.new("RGBA", c.size, (0, 0, 0, 0))
        ImageDraw.Draw(g).text((c.width / 2, y), JP, font=f, fill=color + (160,), anchor="ma")
        c.alpha_composite(g.filter(ImageFilter.GaussianBlur(10)))
    ImageDraw.Draw(c).text((c.width / 2, y), JP, font=f, fill=color, anchor="ma")


def spaced(c, y, text, size=26, color=SOFT, track=12, font=IN6, x=None, anchor="m"):
    tracked(ImageDraw.Draw(c), (c.width / 2 if x is None else x, y), text, F(font, size), color, track, anchor=anchor)


def subtitle(c, xy, text, size=40, color=(255, 236, 120)):
    ImageDraw.Draw(c).text(xy, text, font=F(IN6, size), fill=color, anchor="mm", stroke_width=3, stroke_fill=(0, 0, 0))


def offer_block(c, y, line1, offer, color=YEL):
    spaced(c, y, line1, 24, SOFT, 8)
    spaced(c, y + 46, offer, 30, color, 6, font=IN8)


def save(c, name, tag):
    os.makedirs(OUT, exist_ok=True)
    c.convert("RGB").save(os.path.join(OUT, f"{name}_{tag}.jpg"), quality=95)


def area(h, st, sb):
    return st, h - sb


# ------------------------------------------------------------ X01 title card — black crewneck
def x01():
    for tag, (w, h, st, sb) in SIZES.items():
        top, bot = area(h, st, sb)
        c = stage(w, h, beams=((0.5, 0.75),), seed=1)
        put(c, prod("crew_black"), w / 2, top + (bot - top) * 0.53, int(w * 0.66))
        c = finish(c, 1)
        bars(c, st, sb)
        title_jp(c, top + 60, 62)
        spaced(c, top + 160, "CULTURE  NEVER  DIES", 26, SOFT, 14)
        offer_block(c, bot - 120, "THE CREWNECK  —  BLACK  /  GREY", OFFER_A)
        save(c, "X01_title_card_crew_black", tag)


# ------------------------------------------------------------ X02 two spotlights — black + grey
def x02():
    for tag, (w, h, st, sb) in SIZES.items():
        top, bot = area(h, st, sb)
        c = stage(w, h, beams=((0.27, 0.48), (0.73, 0.48)), seed=2)
        cy = top + (bot - top) * 0.52
        put(c, prod("crew_black"), w * 0.27, cy, int(w * 0.46))
        put(c, prod("crew_grey"), w * 0.73, cy, int(w * 0.46))
        c = finish(c, 2)
        bars(c, st, sb)
        spaced(c, top + 50, "CULTURE NEVER DIES", 52, WHITE, 10, font=IN8)
        spaced(c, top + 124, "THE CREWNECK  •  IN BLACK  •  IN GREY", 22, SOFT, 8)
        spaced(c, cy + w * 0.29, "BLACK", 22, SOFT, 10, x=w * 0.27)
        spaced(c, cy + w * 0.29, "GREY", 22, SOFT, 10, x=w * 0.73)
        offer_block(c, bot - 110, "GET BOTH", OFFER_A)
        save(c, "X02_black_and_grey", tag)


# ------------------------------------------------------------ X03 detail grid — black crewneck
def x03():
    base = prod("crew_black")
    big = Image.new("RGBA", (base.width + 80, base.height + 80), (12, 12, 14, 255))
    big.alpha_composite(relight(base, top=1.25, bottom=0.85, rim_amt=0.35), (40, 40))
    crops = [((190, 30, 470, 230), "01  RAW-CUT COLLAR"), ((170, 140, 490, 330), "02  FRONT SCRIPT"),
             ((170, 290, 490, 520), "03  KANGAROO POCKET"), ((330, 470, 620, 650), "04  WAVY RAW HEM")]
    for tag, (w, h, st, sb) in SIZES.items():
        top, bot = area(h, st, sb)
        c = Image.new("RGBA", (w, h), BLACK + (255,))
        g = 14
        fw = (w - 80 - g) // 2
        fh = (bot - top - 170 - 160 - g) // 2
        for i, (box, lab) in enumerate(crops):
            x = 40 + (i % 2) * (fw + g)
            y = top + 170 + (i // 2) * (fh + g)
            fr = cover(big.crop(box).convert("RGB"), fw, fh, 0.5).filter(ImageFilter.UnsharpMask(1.8, 80, 2))
            c.alpha_composite(film(fr, grain=7, vignette=0.3, seed=30 + i, halation=0.1), (x, y))
            d = ImageDraw.Draw(c)
            tw_ = sum(F(IN8, 18).getlength(ch) for ch in lab) + 4 * len(lab) + 32
            d.rectangle((x, y, x + tw_, y + 40), fill=(0, 0, 0, 230))
            tracked(d, (x + 16, y + 10), lab, F(IN8, 18), (255, 236, 120), 4)
        spaced(c, top + 40, "THE DETAILS.", 60, WHITE, 12, font=IN8)
        ImageDraw.Draw(c).text((w / 2, top + 118), JP, font=F(JP_SANS, 26), fill=SOFT, anchor="ma")
        offer_block(c, bot - 104, "CULTURE NEVER DIES  —  CREWNECK", OFFER_B)
        save(c, "X03_details_storyboard", tag)


# ------------------------------------------------------------ X04 grey crewneck callouts
def x04():
    for tag, (w, h, st, sb) in SIZES.items():
        top, bot = area(h, st, sb)
        c = stage(w, h, beams=((0.5, 0.8),), base=(16, 16, 18), seed=4)
        pw = int(w * 0.6)
        cy = top + (bot - top) * 0.52
        g = prod("crew_grey")
        box = put(c, g, w / 2, cy, pw)
        c = finish(c, 4)
        bars(c, st, sb)
        s = pw / g.width
        P = lambda x, y: (box[0] + x * s, box[1] + y * s)
        notes = [(P(205, 22), "l", "RAW-CUT COLLAR"), (P(430, 165), "r", "JAPANESE FRONT SCRIPT"),
                 (P(55, 150), "l", "DROPPED SHOULDERS"), (P(455, 330), "r", "KANGAROO POCKET"),
                 (P(120, 560), "l", "WAVY RAW HEM"), (P(548, 470), "r", "VINTAGE WASH")]
        d = ImageDraw.Draw(c)
        for (px, py), side, lab in notes:
            lx = 40 if side == "l" else w - 40
            d.line([(px, py), (lx, py)], fill=(235, 230, 220, 200), width=2)
            d.ellipse((px - 7, py - 7, px + 7, py + 7), fill=YEL)
            tracked(d, (lx, py - 30), lab, F(IN8, 18), (240, 236, 226), 3, anchor="l" if side == "l" else "r")
        spaced(c, top + 46, "CULTURE NEVER DIES", 48, WHITE, 10, font=IN8)
        spaced(c, top + 112, "THE CREWNECK  —  GREY", 22, SOFT, 10)
        offer_block(c, bot - 110, "BLACK  /  GREY", OFFER_B)
        save(c, "X04_grey_features", tag)


# ------------------------------------------------------------ X05 hoodie — glitch title
def glitch_title(c, y, size=70):
    f = F(JP_SANS, size)
    w, h = c.size
    layer = Image.new("RGBA", (w, size + 60), (0, 0, 0, 0))
    for dx, col in [(-4, (255, 40, 60, 170)), (4, (40, 220, 255, 170)), (0, (255, 255, 255, 255))]:
        t = Image.new("RGBA", layer.size, (0, 0, 0, 0))
        ImageDraw.Draw(t).text((w / 2 + dx, 20), JP, font=f, fill=col, anchor="ma")
        layer.alpha_composite(t)
    rng = random.Random(5)
    for _ in range(2):
        y0 = rng.randint(size // 2, size + 20)
        hh = rng.randint(3, 6)
        strip = layer.crop((0, y0, w, y0 + hh))
        layer.paste((0, 0, 0, 0), (0, y0, w, y0 + hh))
        layer.alpha_composite(strip, (rng.randint(-14, 14), y0))
    sl = ImageDraw.Draw(layer)
    for yy in range(0, layer.height, 4):
        sl.line([(0, yy), (w, yy)], fill=(0, 0, 0, 70))
    c.alpha_composite(layer, (0, int(y)))


def x05():
    for tag, (w, h, st, sb) in SIZES.items():
        top, bot = area(h, st, sb)
        c = stage(w, h, beams=((0.5, 0.8),), base=(7, 8, 12), glow=(200, 220, 255), seed=5)
        put(c, prod("hoodie_black"), w / 2, top + (bot - top) * 0.55, int(w * 0.68), rim_amt=0.6)
        c = finish(c, 5)
        bars(c, st, sb)
        glitch_title(c, top + 30, 70)
        spaced(c, top + 160, "CULTURE  NEVER  DIES  —  THE HOODIE", 22, SOFT, 10)
        offer_block(c, bot - 110, "WASHED BLACK  •  DISTRESSED  •  KANGAROO POCKET", OFFER_B)
        save(c, "X05_hoodie_glitch", tag)


# ------------------------------------------------------------ X06 bullseye — on target
def x06():
    for tag, (w, h, st, sb) in SIZES.items():
        top, bot = area(h, st, sb)
        c = stage(w, h, beams=((0.5, 0.85),), base=(8, 10, 16), glow=(230, 236, 255), seed=6)
        t = prod("bullseye_tee")
        tw = int(w * 0.72)
        box = put(c, t, w / 2, top + (bot - top) * 0.56, tw)
        c = finish(c, 6)
        bars(c, st, sb)
        s = tw / t.width
        rx, ry = box[0] + 312 * s, box[1] + 160 * s
        d = ImageDraw.Draw(c)
        col = (255, 70, 70)
        gap = 120
        d.line([(0, ry), (rx - gap, ry)], fill=col, width=2)
        d.line([(rx + gap, ry), (w, ry)], fill=col, width=2)
        d.line([(rx, top), (rx, ry - gap)], fill=col, width=2)
        d.line([(rx, ry + gap), (rx, bot)], fill=col, width=2)
        for sx, sy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
            cx, cy = rx + sx * gap, ry + sy * gap
            d.line([(cx, cy), (cx - sx * 30, cy)], fill=col, width=4)
            d.line([(cx, cy), (cx, cy - sy * 30)], fill=col, width=4)
        tracked(d, (44, top + 30), "TARGET: CULTURE", F(IN6, 18), col, 6)
        tracked(d, (w - 44, top + 30), "LOCKED", F(IN6, 18), col, 6, anchor="r")
        spaced(c, top + 70, "ON TARGET.", 72, WHITE, 10, font=IN8)
        offer_block(c, bot - 110, "THE BULLSEYE TEE  —  CULTURE NEVER DIES", OFFER_A)
        save(c, "X06_bullseye_on_target", tag)


# ------------------------------------------------------------ X07 navy tiger tee — real photo letterbox
def x07():
    src = newphoto("navy_tee_photo")
    for tag, (w, h, st, sb) in SIZES.items():
        top, bot = area(h, st, sb)
        c = Image.new("RGBA", (w, h), BLACK + (255,))
        fh = int(w / 1.5)
        cy = (top + bot) // 2
        frame = film(cover(src, w, fh, 0.05), warm=0.04, halation=0.18, vignette=0.3, seed=7)
        subtitle(frame, (w / 2, fh - 60), "navy. red. the league.", 42)
        c.alpha_composite(frame, (0, cy - fh // 2))
        mark(c, w / 2, cy - fh // 2 - 110, anchor="m")
        offer_block(c, cy + fh // 2 + 50, "TIGER LEAGUE TEE  —  NAVY / RED", OFFER_A)
        save(c, "X07_navy_tiger_letterbox", tag)


# ------------------------------------------------------------ X08 trailer stills
def x08():
    stills = [("photo", 7, 0.22, "this fall."), ("new", "navy_tee_photo", 0.08, "the league returns."),
              ("photo", 9, 0.28, "culture never dies.")]
    for tag, (w, h, st, sb) in SIZES.items():
        top, bot = area(h, st, sb)
        c = Image.new("RGBA", (w, h), BLACK + (255,))
        fh = int((bot - top - 260) / 3)
        y = top + 100
        for i, (kind, n, fy, line) in enumerate(stills):
            img = photo(n) if kind == "photo" else newphoto(n)
            fr = film(cover(img, w, fh, fy), warm=0.03, halation=0.15, vignette=0.35, seed=80 + i)
            subtitle(fr, (w / 2, fh - 44), line, 36)
            c.alpha_composite(fr, (0, y))
            y += fh + 10
        spaced(c, top + 34, "404  CULTURE  PRESENTS", 24, SOFT, 14)
        spaced(c, bot - 130, OFFER_B, 50, YEL, 6, font=IN8)
        spaced(c, bot - 60, "TEES  •  CREWNECKS  •  HOODIES", 22, SOFT, 10)
        save(c, "X08_trailer_stills", tag)


# ------------------------------------------------------------ X09 the collection
def x09():
    items = [("crew_black", "CREWNECK — BLACK"), ("crew_grey", "CREWNECK — GREY"), ("hoodie_black", "HOODIE"),
             ("bullseye_tee", "BULLSEYE TEE")]
    for tag, (w, h, st, sb) in SIZES.items():
        top, bot = area(h, st, sb)
        c = stage(w, h, beams=((0.27, 0.45), (0.73, 0.45)), seed=9, beam_alpha=26)
        gy0, gy1 = top + 190, bot - 170
        cell_h = (gy1 - gy0) / 2
        pw = int(min(w * 0.4, cell_h * 0.82))
        centers = []
        for i, (n, lab) in enumerate(items):
            cx = w * (0.27 if i % 2 == 0 else 0.73)
            cy = gy0 + cell_h * (i // 2) + cell_h * 0.45
            put(c, prod(n), cx, cy, pw)
            centers.append((cx, cy, lab))
        c = finish(c, 9)
        bars(c, st, sb)
        for cx, cy, lab in centers:
            spaced(c, cy + pw * 0.56, lab, 18, SOFT, 6, font=IN8, x=cx)
        title_jp(c, top + 40, 52)
        spaced(c, top + 124, "THE  CULTURE  NEVER  DIES  COLLECTION", 22, SOFT, 10)
        offer_block(c, bot - 110, "MIX ANY THREE", OFFER_B)
        save(c, "X09_collection", tag)


# ------------------------------------------------------------ X10 buy 2 get 1 — three frames
def x10():
    items = [("crew_black", "1"), ("hoodie_black", "2"), ("bullseye_tee", "3")]
    for tag, (w, h, st, sb) in SIZES.items():
        top, bot = area(h, st, sb)
        c = Image.new("RGBA", (w, h), BLACK + (255,))
        fw = (w - 80 - 2 * 16) // 3
        fh = int(fw * 1.45)
        y = top + 260 + ((bot - top - 260 - 200 - fh) // 2)
        for i, (n, num) in enumerate(items):
            x = 40 + i * (fw + 16)
            fr = stage(fw, fh, beams=((0.5, 0.9),), seed=100 + i, beam_alpha=40, floor=0.86)
            put(fr, prod(n), fw / 2, fh * 0.5, int(fw * 0.86), shadow=True)
            fr = film(fr, grain=6, vignette=0.3, seed=110 + i, halation=0.1)
            c.alpha_composite(fr, (x, y))
            d = ImageDraw.Draw(c)
            for sy in (y - 30, y + fh + 8):
                for k in range(6):
                    sx = x + 14 + k * (fw - 28) / 5
                    d.rounded_rectangle((sx - 9, sy, sx + 9, sy + 20), radius=4, fill=(40, 40, 44))
            tracked(d, (x + fw / 2, y + fh + 50), num, F(ANTON, 70), WHITE if i < 2 else YEL, 2, anchor="m")
            if i == 2:
                stamp = Image.new("RGBA", (260, 110), (0, 0, 0, 0))
                sd = ImageDraw.Draw(stamp)
                sd.rounded_rectangle((4, 4, 255, 105), radius=12, outline=RED + (255,), width=7)
                sd.text((130, 56), "50% OFF", font=F(ANTON, 64), fill=RED + (255,), anchor="mm")
                stamp = stamp.rotate(-12, resample=Image.BICUBIC, expand=True)
                c.alpha_composite(stamp, (int(x + fw / 2 - stamp.width / 2), int(y + fh * 0.62)))
        spaced(c, top + 40, "BUY 2.", 92, WHITE, 8, font=IN8)
        spaced(c, top + 150, "GET THE 3RD 50% OFF.", 44, YEL, 6, font=IN8)
        spaced(c, bot - 70, "CULTURE NEVER DIES  —  TEES  •  CREWNECKS  •  HOODIES", 20, SOFT, 6)
        save(c, "X10_buy2_get1_frames", tag)


if __name__ == "__main__":
    for fn in (x01, x02, x03, x04, x05, x06, x07, x08, x09, x10):
        fn()
        print(fn.__name__)
