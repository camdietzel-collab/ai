"""Round 2: five collage-style 1080x1350 Meta feed ads for 404 CULTURE.

Uses model cutouts (rembg, see cutouts/) and the studio garment cutouts from
../campaign/cutouts so products and people can be layered with type,
paper, tape and UI elements instead of sitting as a flat photo.
"""
import math
import os
import random

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
FONTS = os.path.join(HERE, "fonts")
ANTON = os.path.join(FONTS, "Anton-Regular.ttf")
ARCHIVO = os.path.join(FONTS, "ArchivoBlack-Regular.ttf")
MARKER = os.path.join(FONTS, "PermanentMarker-Regular.ttf")
PIXEL = os.path.join(FONTS, "VT323-Regular.ttf")
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
BODY = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

W, H = 1080, 1350
RED, DRED, YELLOW = (206, 20, 34), (120, 6, 16), (255, 196, 0)
BLUE, NAVY, CREAM = (150, 205, 240), (14, 30, 60), (244, 238, 220)
BLACK, WHITE, PINK, GREY = (14, 14, 14), (255, 255, 255), (255, 120, 170), (192, 192, 192)


def F(path, size):
    return ImageFont.truetype(path, size)


def model(n):
    return Image.open(os.path.join(HERE, "cutouts", f"model_{n}.png")).convert("RGBA")


def garment(n):
    return Image.open(os.path.join(HERE, "..", "campaign", "cutouts", f"{n}.png")).convert("RGBA")


def photo(n):
    return Image.open(os.path.join(HERE, "source", f"{n}.jpg")).convert("RGB")


def fit_h(img, h):
    return img.resize((round(img.width * h / img.height), h), Image.LANCZOS)


def fit_w(img, w):
    return img.resize((w, round(img.height * w / img.width)), Image.LANCZOS)


def cover(img, w, h, fy=0.5):
    s = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x, y = (img.width - w) // 2, round((img.height - h) * fy)
    return img.crop((x, y, x + w, y + h))


def shadow(canvas, rgba, xy, off=(14, 18), blur=18, alpha=140):
    a = rgba.getchannel("A").point(lambda v: v * alpha // 255)
    pad = blur * 3
    sh = Image.new("RGBA", (rgba.width + pad * 2, rgba.height + pad * 2), (0, 0, 0, 0))
    sh.putalpha(0)
    m = Image.new("L", sh.size, 0)
    m.paste(a, (pad, pad))
    m = m.filter(ImageFilter.GaussianBlur(blur))
    sh = Image.new("RGBA", sh.size, (0, 0, 0, 255))
    sh.putalpha(m)
    canvas.alpha_composite(sh, (xy[0] - pad + off[0], xy[1] - pad + off[1]))


def put(canvas, rgba, xy, drop=True, **kw):
    xy = (round(xy[0]), round(xy[1]))
    if drop:
        shadow(canvas, rgba, xy, **kw)
    canvas.alpha_composite(rgba, xy)


def rot(img, deg):
    return img.rotate(deg, resample=Image.BICUBIC, expand=True)


def grain(canvas, amt=10, seed=1):
    rng = np.random.default_rng(seed)
    a = np.asarray(canvas.convert("RGB")).astype(np.int16)
    n = rng.normal(0, amt, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a + n, 0, 255).astype(np.uint8)).convert("RGBA")


def fit_font(path, s, maxw, start=600):
    size = start
    while F(path, size).getlength(s) > maxw:
        size -= 4
    return F(path, size)


def outline_text(canvas, xy, s, f, color, width):
    """Hollow (stroke-only) text."""
    m1 = Image.new("L", canvas.size, 0)
    m2 = Image.new("L", canvas.size, 0)
    ImageDraw.Draw(m1).text(xy, s, font=f, fill=255, stroke_width=width, stroke_fill=255)
    ImageDraw.Draw(m2).text(xy, s, font=f, fill=255)
    layer = Image.new("RGBA", canvas.size, color + (255,))
    layer.putalpha(ImageChops.subtract(m1, m2))
    canvas.alpha_composite(layer)


def starburst(d, c, ro, ri, n, fill, rot0=0):
    pts = []
    for i in range(n * 2):
        r = ro if i % 2 == 0 else ri
        a = math.pi * i / n + rot0
        pts.append((c[0] + r * math.cos(a), c[1] + r * math.sin(a)))
    d.polygon(pts, fill=fill)


def sparkle(d, c, r, fill):
    x, y = c
    d.polygon([(x, y - r), (x + r * .22, y - r * .22), (x + r, y), (x + r * .22, y + r * .22),
               (x, y + r), (x - r * .22, y + r * .22), (x - r, y), (x - r * .22, y - r * .22)], fill=fill)


def torn(w, h, color, jag=7, seed=0, alpha=255):
    """A paper strip with ragged edges."""
    rng = random.Random(seed)
    pts = []
    for x in range(0, w + 1, 12):
        pts.append((x, rng.uniform(0, jag)))
    for y in range(0, h + 1, 12):
        pts.append((w - rng.uniform(0, jag), y))
    for x in range(w, -1, -12):
        pts.append((x, h - rng.uniform(0, jag)))
    for y in range(h, -1, -12):
        pts.append((rng.uniform(0, jag), y))
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).polygon(pts, fill=color + (alpha,))
    return im


def label(s, f, bg, fg, pad=(22, 12), deg=0, seed=0, jag=5):
    tw = round(f.getlength(s))
    asc, desc = f.getmetrics()
    im = torn(tw + pad[0] * 2, asc + desc + pad[1] * 2, bg, jag=jag, seed=seed)
    ImageDraw.Draw(im).text((pad[0], pad[1]), s, font=f, fill=fg)
    return rot(im, deg) if deg else im


def tape(w=190, h=56, deg=0, seed=0):
    return rot(torn(w, h, (236, 226, 190), jag=4, seed=seed, alpha=205), deg)


def pill(d, xy, s, f, bg, fg, pad=(34, 18), anchor="l"):
    tw = d.textlength(s, font=f)
    bw, bh = tw + pad[0] * 2, f.getmetrics()[0] + pad[1] * 2
    x, y = xy
    if anchor == "r":
        x -= bw
    elif anchor == "m":
        x -= bw / 2
    d.rounded_rectangle((x, y - bh / 2, x + bw, y + bh / 2), radius=bh / 2, fill=bg)
    d.text((x + bw / 2, y), s, font=f, fill=fg, anchor="mm")


def halftone_bg(size, color, dot, spacing=18, fade_from=0.0):
    """Dot pattern that grows toward the bottom."""
    im = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for y in range(0, size[1], spacing):
        t = max(0.0, (y / size[1] - fade_from) / (1 - fade_from))
        r = dot * t
        if r < 0.6:
            continue
        for x in range((y // spacing % 2) * spacing // 2, size[0], spacing):
            d.ellipse((x - r, y - r, x + r, y + r), fill=color)
    return im


def save(canvas, name):
    canvas.convert("RGB").save(os.path.join(OUT, name), quality=95)
    print("wrote", name)


# ---------------------------------------------------------------- ad 06
def ad06_fit_not_found():
    """Retro OS error dialog: the '404' in the brand name as the joke."""
    c = Image.new("RGBA", (W, H), YELLOW + (255,))
    d = ImageDraw.Draw(c)
    for x in range(0, W, 36):
        d.line([(x, 0), (x, H)], fill=(235, 176, 0), width=2)
    for y in range(0, H, 36):
        d.line([(0, y), (W, y)], fill=(235, 176, 0), width=2)

    def window(box, title, bar=RED):
        x0, y0, x1, y1 = box
        d.rectangle((x0 + 12, y0 + 12, x1 + 12, y1 + 12), fill=BLACK)
        d.rectangle(box, fill=GREY, outline=BLACK, width=4)
        d.line([(x0 + 4, y0 + 4), (x1 - 4, y0 + 4)], fill=WHITE, width=3)
        d.line([(x0 + 4, y0 + 4), (x0 + 4, y1 - 4)], fill=WHITE, width=3)
        d.rectangle((x0 + 10, y0 + 10, x1 - 10, y0 + 62), fill=bar)
        d.text((x0 + 24, y0 + 36), title, font=F(PIXEL, 44), fill=WHITE, anchor="lm")
        for i, g in enumerate(["x", "□", "_"]):
            bx = x1 - 58 - i * 52
            d.rectangle((bx, y0 + 16, bx + 42, y0 + 56), fill=GREY, outline=BLACK, width=3)
            d.text((bx + 21, y0 + 34), g, font=F(MONO, 26), fill=BLACK, anchor="mm")
        return (x0 + 14, y0 + 68, x1 - 14, y1 - 14)

    d.text((60, 44), "404 CULTURE", font=F(ANTON, 44), fill=BLACK)
    d.text((W - 60, 44), "C:\\LEAGUE\\DROP_04", font=F(PIXEL, 44), fill=BLACK, anchor="ra")

    # main photo window
    ix0, iy0, ix1, iy1 = window((60, 120, 1020, 1030), "tiger_league_tee.jpg")
    inner = Image.new("RGBA", (ix1 - ix0, iy1 - iy0), CREAM + (255,))
    di = ImageDraw.Draw(inner)
    big = fit_font(ANTON, "404", inner.width - 40)
    di.text((inner.width // 2, inner.height // 2 - 30), "404", font=big, fill=RED, anchor="mm")
    m = fit_h(model(2), inner.height - 20)
    inner.alpha_composite(m, ((inner.width - m.width) // 2 + 150, inner.height - m.height + 60))
    c.alpha_composite(inner, (ix0, iy0))

    # error dialog
    bx0, by0, bx1, by1 = 40, 790, 690, 1175
    ex0, ey0, ex1, ey1 = window((bx0, by0, bx1, by1), "ERROR 404", bar=NAVY)
    tri = [(ex0 + 70, ey0 + 30), (ex0 + 120, ey0 + 118), (ex0 + 20, ey0 + 118)]
    d.polygon(tri, fill=YELLOW, outline=BLACK, width=4)
    d.text((ex0 + 70, ey0 + 84), "!", font=F(ARCHIVO, 54), fill=BLACK, anchor="mm")
    d.text((ex0 + 150, ey0 + 24), "FIT NOT FOUND.", font=F(ARCHIVO, 44), fill=BLACK)
    d.text((ex0 + 150, ey0 + 84), "Install Tiger League Tee?", font=F(PIXEL, 40), fill=BLACK)
    yes = (ex0 + 30, ey1 - 104, ex0 + 390, ey1 - 26)
    d.rectangle((yes[0] + 6, yes[1] + 6, yes[2] + 6, yes[3] + 6), fill=BLACK)
    d.rectangle(yes, fill=YELLOW, outline=BLACK, width=4)
    d.text(((yes[0] + yes[2]) / 2, (yes[1] + yes[3]) / 2), "YES — $39.99", font=F(ARCHIVO, 36), fill=BLACK, anchor="mm")
    no = (ex0 + 420, ey1 - 104, ex1 - 30, ey1 - 26)
    d.rectangle(no, fill=GREY, outline=(120, 120, 120), width=3)
    d.text(((no[0] + no[2]) / 2, (no[1] + no[3]) / 2), "NO", font=F(ARCHIVO, 36), fill=(150, 150, 150), anchor="mm")
    d.line([(no[0] + 40, (no[1] + no[3]) / 2), (no[2] - 40, (no[1] + no[3]) / 2)], fill=RED, width=5)

    # cursor clicking YES
    cx, cy = yes[2] - 70, yes[3] - 30
    cur = [(0, 0), (0, 64), (16, 49), (28, 76), (40, 71), (28, 45), (50, 45)]
    d.polygon([(cx + x * 1.3, cy + y * 1.3) for x, y in cur], fill=WHITE, outline=BLACK, width=4)

    starburst(d, (870, 1130), 150, 118, 18, RED)
    d.text((870, 1100), "SHOP", font=F(ANTON, 54), fill=YELLOW, anchor="mm")
    d.text((870, 1162), "NOW →", font=F(ANTON, 54), fill=WHITE, anchor="mm")
    d.text((60, 1262), "RED / GOLD LAYERED TIGER TEE", font=F(PIXEL, 46), fill=BLACK)
    save(grain(c, 6, 6), "06_fit_not_found.jpg")


# ---------------------------------------------------------------- ad 07
def ad07_giant_type():
    """Model in front of massive stacked type, halftone + grain poster."""
    c = Image.new("RGBA", (W, H), RED + (255,))
    c.alpha_composite(halftone_bg((W, H), DRED + (255,), 10, 20, 0.35))
    d = ImageDraw.Draw(c)
    f1 = fit_font(ANTON, "TIGER", W - 60)
    d.text((W // 2, 40), "TIGER", font=f1, fill=YELLOW, anchor="ma")
    f2 = fit_font(ANTON, "LEAGUE", W - 60)
    tb = d.textbbox((0, 0), "TIGER", font=f1, anchor="la")
    outline_text(c, ((W - f2.getlength("LEAGUE")) / 2, 40 + tb[3] - 30), "LEAGUE", f2, YELLOW, 6)

    m = fit_h(model(5), 1180)
    put(c, m, ((W - m.width) // 2 + 20, H - m.height + 40), off=(24, 10), blur=26, alpha=150)

    d = ImageDraw.Draw(c)
    # vertical side text
    side = Image.new("RGBA", (620, 60), (0, 0, 0, 0))
    ImageDraw.Draw(side).text((0, 0), "EST. 2004  •  404 CULTURE", font=F(ARCHIVO, 34), fill=WHITE)
    c.alpha_composite(side.rotate(90, expand=True), (30, 420))

    starburst(d, (870, 760), 150, 122, 20, YELLOW, 0.1)
    d.text((870, 735), "$39.99", font=F(ANTON, 76), fill=RED, anchor="mm")
    d.text((870, 800), "LAYERED TEE", font=F(ARCHIVO, 22), fill=BLACK, anchor="mm")

    lab = label("wear the league.", F(MARKER, 52), BLACK, WHITE, deg=-6, seed=3)
    c.alpha_composite(lab, (50, 1080))
    d = ImageDraw.Draw(c)
    pill(d, (W - 60, 1270), "SHOP NOW  →", F(ARCHIVO, 34), YELLOW, BLACK, anchor="r")
    save(grain(c, 9, 7), "07_tiger_league_poster.jpg")


# ---------------------------------------------------------------- ad 08
def card(n, fy, colorway, panel, accent, text_on_panel, size=(560, 790), seed=0):
    """A collectible sports card with the model breaking out of the frame."""
    w, h = size
    im = Image.new("RGBA", (w, h + 120), (0, 0, 0, 0))   # headroom for pop-out
    top = 120
    # holo border
    holo = Image.new("RGBA", (w, h))
    hd = ImageDraw.Draw(holo)
    stops = [(255, 120, 200), (120, 220, 255), (255, 240, 140), (170, 140, 255), (120, 255, 200)]
    for i in range(w + h):
        t = i / (w + h) * (len(stops) - 1)
        a, b = stops[int(t)], stops[min(int(t) + 1, len(stops) - 1)]
        f = t - int(t)
        col = tuple(round(a[k] + (b[k] - a[k]) * f) for k in range(3))
        hd.line([(i, 0), (i - h, h)], fill=col, width=2)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), radius=28, fill=255)
    im.paste(holo, (0, top), mask)
    d = ImageDraw.Draw(im)
    ib = (22, top + 22, w - 22, top + h - 22)
    d.rounded_rectangle(ib, radius=18, fill=panel)
    # diagonal stripes in panel
    stripes = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stripes)
    for x in range(-h, w, 44):
        sd.line([(x, 0), (x + h, h)], fill=(255, 255, 255, 22), width=16)
    pm = Image.new("L", (w, h), 0)
    ImageDraw.Draw(pm).rounded_rectangle((22, 22, w - 23, h - 23), radius=18, fill=255)
    stripes.putalpha(ImageChops.multiply(stripes.getchannel("A"), pm))
    im.alpha_composite(stripes, (0, top))
    d = ImageDraw.Draw(im)
    d.text((w // 2, top + 60), "404", font=F(ANTON, 300), fill=tuple(min(255, v + 30) for v in panel), anchor="ma")
    # model — clipped at the bottom of the panel, free to break out at the top
    m = fit_h(model(n), round(h * 0.98))
    mx, my = (w - m.width) // 2, top + h - 170 - m.height + round(m.height * fy)
    clip = Image.new("L", im.size, 0)
    ImageDraw.Draw(clip).rectangle((0, 0, w, top + h - 170), fill=255)
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    layer.alpha_composite(m, (mx, max(my, 0)))
    layer.putalpha(ImageChops.multiply(layer.getchannel("A"), clip))
    im.alpha_composite(layer)
    d = ImageDraw.Draw(im)
    # nameplate
    ny = top + h - 170
    d.polygon([(22, ny), (w - 22, ny - 26), (w - 22, top + h - 22), (22, top + h - 22)], fill=accent)
    d.text((44, ny + 18), "TIGER LEAGUE TEE", font=F(ANTON, 60), fill=text_on_panel)
    d.text((46, ny + 96), colorway, font=F(ARCHIVO, 26), fill=text_on_panel)
    d.text((w - 44, ny + 92), "$39.99", font=F(ANTON, 48), fill=text_on_panel, anchor="ra")
    # rookie badge
    d.ellipse((w - 150, top + 44, w - 44, top + 150), fill=BLACK, outline=WHITE, width=5)
    d.text((w - 97, top + 84), "'04", font=F(ANTON, 44), fill=YELLOW, anchor="mm")
    d.text((w - 97, top + 122), "ROOKIE", font=F(ARCHIVO, 14), fill=WHITE, anchor="mm")
    return im


def ad08_trading_cards():
    c = Image.new("RGBA", (W, H), (10, 10, 18, 255))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((90, 330, 990, 1230), fill=(70, 60, 150, 170))
    c.alpha_composite(glow.filter(ImageFilter.GaussianBlur(140)))
    d = ImageDraw.Draw(c)
    d.text((W // 2, 50), "404 CULTURE LEAGUE", font=F(ARCHIVO, 34), fill=YELLOW, anchor="ma")
    d.text((W // 2, 100), "COLLECT THE SET", font=F(ANTON, 124), fill=WHITE, anchor="ma")

    blue = rot(card(4, 0.05, "SKY BLUE / WHITE", (70, 140, 200), BLUE, NAVY, seed=2), -9)
    red = rot(card(1, 0.02, "RED / GOLD", (170, 14, 26), YELLOW, DRED, seed=1), 7)
    put(c, blue, (20, 290), off=(10, 24), blur=30, alpha=170)
    put(c, red, (450, 260), off=(10, 24), blur=30, alpha=170)
    d = ImageDraw.Draw(c)
    for p, r in [((110, 300), 26), ((980, 330), 34), ((70, 1150), 20), ((540, 330), 16)]:
        sparkle(d, p, r, (255, 240, 180))
    pill(d, (W // 2, 1275), "2 COLORWAYS  •  SHOP NOW  →", F(ARCHIVO, 34), YELLOW, BLACK, anchor="m")
    save(grain(c, 5, 8), "08_collect_the_set.jpg")


# ---------------------------------------------------------------- ad 09
def arrow(d, pts, color, width=6):
    d.line(pts, fill=color, width=width, joint="curve")
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    a = math.atan2(y2 - y1, x2 - x1)
    for s in (2.6, -2.6):
        d.line([(x2, y2), (x2 + 30 * math.cos(a + s), y2 + 30 * math.sin(a + s))], fill=color, width=width)


def ad09_layer_up():
    """Moodboard flat-lay: thermal + blue tee = the fit, with proof polaroid."""
    c = Image.new("RGBA", (W, H), (232, 222, 200, 255))
    d = ImageDraw.Draw(c)
    for y in range(0, H, 40):
        d.line([(0, y), (W, y)], fill=(214, 204, 182), width=2)
    d.text((60, 40), "404 CULTURE", font=F(ANTON, 44), fill=BLACK)
    d.text((60, 92), "LAYER UP.", font=F(ANTON, 170), fill=BLACK)

    th = rot(fit_w(garment(3), 640), 8)
    put(c, th, (-20, 390), off=(10, 16), blur=16, alpha=110)
    tee = rot(fit_w(garment(4), 600), -6)
    put(c, tee, (330, 560), off=(12, 18), blur=16, alpha=120)

    # polaroid of how it's worn
    ph = cover(photo(4), 300, 330, 0.12)
    pol = Image.new("RGBA", (340, 430), (250, 250, 246, 255))
    pol.paste(ph, (20, 20))
    ImageDraw.Draw(pol).text((170, 396), "how it's worn ↑", font=F(MARKER, 30), fill=BLACK, anchor="mm")
    pol = rot(pol, -8)
    put(c, pol, (690, 120), off=(10, 14), blur=14, alpha=120)
    c.alpha_composite(tape(150, 46, 20, seed=4), (790, 105))

    d = ImageDraw.Draw(c)
    d.text((70, 330), "the culture thermal", font=F(MARKER, 40), fill=RED)
    d.text((70, 376), "$52.99", font=F(MARKER, 56), fill=RED)
    arrow(d, [(260, 450), (290, 500), (300, 540)], RED)
    d.text((620, 1180), "tiger league tee  $39.99", font=F(MARKER, 40), fill=RED, anchor="ma")
    arrow(d, [(430, 1180), (410, 1140), (430, 1095)], RED)
    c.alpha_composite(tape(170, 50, -30, seed=1), (300, 470))
    c.alpha_composite(tape(170, 50, 25, seed=2), (820, 600))

    d = ImageDraw.Draw(c)
    d.rectangle((0, 1240, W, H), fill=BLACK)
    d.text((60, 1295), "TEE + THERMAL = THE FIT", font=F(ANTON, 58), fill=YELLOW, anchor="lm")
    pill(d, (W - 50, 1295), "SHOP  →", F(ARCHIVO, 32), YELLOW, BLACK, anchor="r")
    save(grain(c, 7, 9), "09_layer_up.jpg")


# ---------------------------------------------------------------- ad 10
def splatter(d, rng, c, r, color):
    d.ellipse((c[0] - r, c[1] - r, c[0] + r, c[1] + r), fill=color)
    for _ in range(rng.randint(6, 14)):
        a = rng.uniform(0, 2 * math.pi)
        dist = rng.uniform(r * 1.1, r * 3.2)
        rr = rng.uniform(r * 0.08, r * 0.32)
        x, y = c[0] + dist * math.cos(a), c[1] + dist * math.sin(a)
        d.ellipse((x - rr, y - rr, x + rr, y + rr), fill=color)


def ransom(canvas, xy, word, size, seed):
    rng = random.Random(seed)
    fonts = [ANTON, SERIF, MARKER, ARCHIVO, MONO]
    combos = [(BLACK, WHITE), (RED, WHITE), (YELLOW, BLACK), (WHITE, BLACK), (PINK, BLACK), (BLUE, BLACK), (CREAM, RED)]
    x, y = xy
    for ch in word:
        if ch == " ":
            x += size * 0.35
            continue
        f = F(rng.choice(fonts), round(size * rng.uniform(0.82, 1.0)))
        bg, fg = rng.choice(combos)
        tw = f.getlength(ch)
        asc, desc = f.getmetrics()
        tile = torn(round(tw + 26), asc + desc + 14, bg, jag=4, seed=rng.randint(0, 999))
        ImageDraw.Draw(tile).text((13, 5), ch, font=f, fill=fg)
        tile = rot(tile, rng.uniform(-8, 8))
        put(canvas, tile, (x, y + rng.randint(-10, 10)), off=(4, 6), blur=5, alpha=110)
        x += tile.width - 8
    return x


def ad10_culture_zine():
    c = Image.new("RGBA", (W, H), CREAM + (255,))
    d = ImageDraw.Draw(c)
    rng = random.Random(11)
    for col in [(222, 30, 40), (40, 120, 220), (250, 190, 0), (240, 110, 170), (20, 20, 20)]:
        for _ in range(3):
            edge = rng.choice(["l", "r", "b"])
            if edge == "l":
                p = (rng.uniform(0, 160), rng.uniform(300, 1200))
            elif edge == "r":
                p = (rng.uniform(920, W), rng.uniform(300, 1200))
            else:
                p = (rng.uniform(0, W), rng.uniform(1050, 1250))
            splatter(d, rng, p, rng.uniform(8, 22), col)
    d.text((W // 2, 44), "404 CULTURE", font=F(ANTON, 44), fill=BLACK, anchor="ma")
    endx = ransom(c, (70, 120), "WEAR THE", 104, 5)
    ransom(c, (120, 250), "CULTURE", 118, 8)

    th = rot(fit_w(garment(3), 900), -4)
    put(c, th, ((W - th.width) // 2, 400), off=(14, 20), blur=22, alpha=120)
    c.alpha_composite(tape(180, 54, -38, seed=6), (130, 430))
    c.alpha_composite(tape(180, 54, 36, seed=7), (770, 430))

    price = label("$52.99", F(ANTON, 96), BLACK, YELLOW, pad=(30, 8), deg=8, seed=5, jag=7)
    put(c, price, (730, 1030), off=(8, 10), blur=10, alpha=120)
    note = label("waffle knit thermal", F(MARKER, 44), RED, WHITE, deg=-4, seed=9)
    put(c, note, (60, 1120), off=(6, 8), blur=8, alpha=110)
    d = ImageDraw.Draw(c)
    pill(d, (W // 2, 1275), "SHOP THE THERMAL  →", F(ARCHIVO, 34), BLACK, YELLOW, anchor="m")
    save(grain(c, 8, 10), "10_wear_the_culture.jpg")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn in (ad06_fit_not_found, ad07_giant_type, ad08_trading_cards, ad09_layer_up, ad10_culture_zine):
        fn()
