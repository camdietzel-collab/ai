"""Render five 1080x1350 (4:5) static Meta feed ads for 404 CULTURE."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "source")
OUT = os.path.join(HERE, "out")
ANTON = os.path.join(HERE, "fonts", "Anton-Regular.ttf")
BODY = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
W, H = 1080, 1350
RED, YELLOW, BLUE, CREAM, BLACK, WHITE = (200, 16, 30), (255, 196, 0), (150, 205, 240), (245, 240, 222), (12, 12, 12), (255, 255, 255)


def font(path, size):
    return ImageFont.truetype(path, size)


def load(name):
    return Image.open(os.path.join(SRC, name)).convert("RGB")


def cover(img, w, h, fy=0.5):
    """Scale to fill w x h, cropping; fy biases the vertical crop (0 top, 1 bottom)."""
    s = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x = (img.width - w) // 2
    y = round((img.height - h) * fy)
    return img.crop((x, y, x + w, y + h))


def gradient(canvas, top, bottom, strength=235, color=(0, 0, 0)):
    """Darken the top `top` px and bottom `bottom` px for text legibility."""
    ov = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for i in range(top):
        d.line([(0, i), (W, i)], fill=color + (int(strength * (1 - i / top) ** 1.6),))
    for i in range(bottom):
        y = H - 1 - i
        d.line([(0, y), (W, y)], fill=color + (int(strength * (1 - i / bottom) ** 1.4),))
    canvas.alpha_composite(ov)


def text(d, xy, s, f, fill, anchor="la", shadow=True):
    if shadow:
        x, y = xy
        d.text((x + 3, y + 4), s, font=f, fill=(0, 0, 0, 150), anchor=anchor)
    d.text(xy, s, font=f, fill=fill, anchor=anchor)


def pill(d, xy, s, f, bg, fg, pad=(34, 18), anchor="l"):
    """Rounded button/badge. xy is left-centre (anchor l) or right-centre (anchor r)."""
    tw = d.textlength(s, font=f)
    asc, desc = f.getmetrics()
    th = asc
    bw, bh = tw + pad[0] * 2, th + pad[1] * 2
    x, y = xy
    if anchor == "r":
        x -= bw
    box = (x, y - bh / 2, x + bw, y + bh / 2)
    d.rounded_rectangle(box, radius=bh / 2, fill=bg)
    d.text((x + bw / 2, y), s, font=f, fill=fg, anchor="mm")
    return box


def brand(d, color=WHITE):
    text(d, (60, 58), "404 CULTURE", font(ANTON, 46), color)


def cta_bar(d, product, price, accent, fg=BLACK):
    """Bottom row: product name + price on the left, SHOP NOW on the right."""
    text(d, (60, H - 150), product, font(BODY, 34), WHITE)
    text(d, (60, H - 108), price, font(ANTON, 72), accent)
    pill(d, (W - 60, H - 88), "SHOP NOW  →", font(BODY, 34), accent, fg, anchor="r")


def save(canvas, name):
    canvas.convert("RGB").save(os.path.join(OUT, name), quality=95)
    print("wrote", name)


def ad1_red_hero():
    c = cover(load("2.jpg"), W, H, 0.35).convert("RGBA")
    gradient(c, 480, 430)
    d = ImageDraw.Draw(c)
    brand(d)
    f = font(ANTON, 112)
    text(d, (60, 130), "THE LEAGUE", f, YELLOW)
    text(d, (60, 252), "IS BACK.", f, WHITE)
    pill(d, (60, 425), "TIGER LEAGUE TEE", font(BODY, 30), RED, WHITE, pad=(26, 14))
    cta_bar(d, "Red / Gold Layered Tee", "$39.99", YELLOW)
    save(c, "01_red_tiger_tee_hero.jpg")


def ad2_blue_hero():
    c = cover(load("4.jpg"), W, H, 0.25).convert("RGBA")
    gradient(c, 470, 430, color=(8, 24, 48))
    d = ImageDraw.Draw(c)
    brand(d)
    f = font(ANTON, 104)
    text(d, (60, 130), "BABY BLUE.", f, BLUE)
    text(d, (60, 244), "BIG ENERGY.", f, WHITE)
    pill(d, (60, 410), "TIGER LEAGUE TEE", font(BODY, 30), BLUE, BLACK, pad=(26, 14))
    cta_bar(d, "Sky Blue Tiger Tee", "$39.99", BLUE)
    save(c, "02_blue_tiger_tee_hero.jpg")


def ad3_thermal():
    c = Image.new("RGBA", (W, H), BLACK + (255,))
    d = ImageDraw.Draw(c)
    # product card
    ph = cover(load("3.jpg"), 900, 900, 0.3)
    mask = Image.new("L", ph.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, 900, 900), radius=36, fill=255)
    c.paste(ph, (90, 250), mask)
    brand(d)
    text(d, (W // 2, 170), "THE CULTURE THERMAL", font(ANTON, 88), CREAM, anchor="mm", shadow=False)
    # price sticker overlapping the card
    cx, cy, r = 900, 1060, 115
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=YELLOW)
    d.text((cx, cy - 8), "$52.99", font=font(ANTON, 64), fill=BLACK, anchor="mm")
    d.text((cx, cy + 44), "ONLY", font=font(BODY, 24), fill=BLACK, anchor="mm")
    text(d, (W // 2, 1195), "WAFFLE KNIT  •  ALL-OVER GRAPHIC  •  SLEEVE PRINT", font(BODY, 30), WHITE, anchor="mm", shadow=False)
    pill(d, (W // 2 - 150, 1275), "SHOP NOW  →", font(BODY, 34), YELLOW, BLACK)
    save(c, "03_culture_thermal.jpg")


def ad4_collection():
    c = Image.new("RGBA", (W, H), BLACK + (255,))
    d = ImageDraw.Draw(c)
    brand(d, YELLOW)
    text(d, (60, 120), "THE DROP", font(ANTON, 130), WHITE, shadow=False)
    text(d, (60, 265), "IS LIVE.", font(ANTON, 130), YELLOW, shadow=False)
    items = [("2.jpg", 0.3, "RED TIGER TEE", "$39.99", RED, WHITE),
             ("4.jpg", 0.25, "BLUE TIGER TEE", "$39.99", BLUE, BLACK),
             ("3.jpg", 0.35, "CULTURE THERMAL", "$52.99", YELLOW, BLACK)]
    gap, top, pw, ph = 20, 450, (W - 120 - 40) // 3, 690
    for i, (src, fy, name, price, bg, fg) in enumerate(items):
        x = 60 + i * (pw + gap)
        tile = cover(load(src), pw, ph, fy)
        m = Image.new("L", (pw, ph), 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, pw, ph), radius=24, fill=255)
        c.paste(tile, (x, top), m)
        d.rounded_rectangle((x, top + ph - 110, x + pw, top + ph), radius=24, fill=bg)
        d.rectangle((x, top + ph - 110, x + pw, top + ph - 80), fill=bg)
        d.text((x + pw / 2, top + ph - 78), name, font=font(BODY, 26), fill=fg, anchor="mm")
        d.text((x + pw / 2, top + ph - 36), price, font=font(ANTON, 50), fill=fg, anchor="mm")
    text(d, (60, 1245), "404 CULTURE LEAGUE", font(BODY, 30), CREAM, anchor="lm", shadow=False)
    pill(d, (W - 60, 1245), "SHOP THE DROP  →", font(BODY, 32), YELLOW, BLACK, anchor="r")
    save(c, "04_full_collection.jpg")


def ad5_two_ways():
    c = Image.new("RGBA", (W, H), RED + (255,))
    d = ImageDraw.Draw(c)
    brand(d, YELLOW)
    text(d, (60, 118), "ONE TEE.", font(ANTON, 140), WHITE)
    text(d, (60, 272), "EVERY FIT.", font(ANTON, 140), YELLOW)
    pw, ph, top = (W - 120 - 24) // 2, 720, 470
    for i, (src, fy, label) in enumerate([("5.jpg", 0.15, "BAGGY DENIM"), ("1.jpg", 0.25, "SLIM + KICKS")]):
        x = 60 + i * (pw + 24)
        tile = cover(load(src), pw, ph, fy)
        m = Image.new("L", (pw, ph), 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, pw, ph), radius=24, fill=255)
        c.paste(tile, (x, top), m)
        pill(d, (x + 20, top + ph - 50), label, font(BODY, 26), BLACK, YELLOW, pad=(22, 12))
    text(d, (60, 1262), "$39.99", font(ANTON, 80), YELLOW, anchor="lm")
    d.text((330, 1262), "Tiger League Tee", font=font(BODY, 30), fill=WHITE, anchor="lm")
    pill(d, (W - 60, 1262), "SHOP NOW  →", font(BODY, 34), YELLOW, BLACK, anchor="r")
    save(c, "05_red_tee_every_fit.jpg")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn in (ad1_red_hero, ad2_blue_hero, ad3_thermal, ad4_collection, ad5_two_ways):
        fn()
