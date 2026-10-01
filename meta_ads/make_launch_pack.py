"""Launch pack: the 5 strongest concepts, rebuilt for both Meta placements.

Each ad = a full-bleed background (drawn at the target size) + a 1080x1350
content layer. Feed (4:5, 1080x1350) uses the layer as is. Stories/Reels
(9:16, 1080x1920) scales the layer into the safe zone — 250px clear at the
top, 400px clear at the bottom where the UI/captions sit — while the
background still fills the whole frame.
"""
import os

from PIL import Image, ImageDraw, ImageFilter

from make_ads_v2 import ANTON, BLACK, MARKER, RED, WHITE, YELLOW, F, cover, fit_w, garment, photo, rot
from make_ads_v3 import radial
from make_ads_v7 import CODE, GREY_TXT, IN4, IN6, IN8, INK, emoji, rich, rounded, vgrad
from make_ads_v8 import DISCOUNT, TEE, THERMAL, TWO_TEES, money, red_tee_thumb, thumb_on
from make_ads_v10 import REG, red_tee_crop, shadowed, sticky, strike

HERE = os.path.dirname(os.path.abspath(__file__))
PACK = os.path.join(HERE, "launch_pack")
LW, LH = 1080, 1350
SAFE_TOP, SAFE_BOTTOM = 250, 400
GREEN = (22, 150, 70)


def layer():
    return Image.new("RGBA", (LW, LH), (0, 0, 0, 0))


def cta(d, y, text, bg=YELLOW, fg=BLACK, size=40):
    d.rounded_rectangle((50, y, LW - 50, y + 110), radius=26, fill=bg)
    d.text((LW // 2, y + 55), text, font=F(IN8, size), fill=fg, anchor="mm")


def chip(d, cx, y, text, size=40, bg=YELLOW, fg=BLACK):
    f = F(IN8, size)
    tw = f.getlength(text)
    d.rounded_rectangle((cx - tw / 2 - 26, y, cx + tw / 2 + 26, y + size + 30), radius=16, fill=bg)
    d.text((cx, y + (size + 30) / 2), text, font=f, fill=fg, anchor="mm")


def build(name, bg_fn, content_fn):
    os.makedirs(PACK, exist_ok=True)
    content = content_fn()
    feed = bg_fn(LW, LH)
    feed.alpha_composite(content)
    feed.convert("RGB").save(os.path.join(PACK, f"{name}_4x5.jpg"), quality=95)
    sh = 1920 - SAFE_TOP - SAFE_BOTTOM
    sw = round(LW * sh / LH)
    story = bg_fn(1080, 1920)
    story.alpha_composite(content.resize((sw, sh), Image.LANCZOS), ((1080 - sw) // 2, SAFE_TOP))
    story.convert("RGB").save(os.path.join(PACK, f"{name}_9x16.jpg"), quality=95)
    print("wrote", name)


# ------------------------------------------------------------ 1. 2 for $73.98
def bg_red(w, h):
    return radial((w, h), (w / 2, h * 0.45), max(w, h) * 0.8, (222, 30, 40), (120, 8, 16))


def content_two_for():
    L = layer()
    d = ImageDraw.Draw(L)
    chip(d, LW // 2, 30, "BUY 1, GET 1 15% OFF", 34, bg=BLACK, fg=YELLOW)
    d.text((LW // 2, 120), "2 TIGER TEES", font=F(ANTON, 110), fill=WHITE, anchor="ma")
    strike(d, (LW // 2, 262), money(REG), F(ANTON, 64), (255, 175, 175), anchor="ma")
    d.text((LW // 2, 330), money(TWO_TEES), font=F(ANTON, 220), fill=YELLOW, anchor="ma")
    b = rot(fit_w(garment(4), 540), -7)
    r = rot(fit_w(red_tee_crop(), 460), 6)
    shadowed(L, b, (LW - b.width - 30, 640), blur=22, alpha=120)
    shadowed(L, r, (30, 610), blur=22, alpha=120)
    d = ImageDraw.Draw(L)
    chip(d, LW // 2, 1086, f"CODE: {CODE}", 42, bg=WHITE, fg=INK)
    cta(d, 1210, f"SHOP 2 FOR {money(TWO_TEES)}  →", bg=BLACK, fg=YELLOW)
    return L


# ------------------------------------------------------------ 2. checkout
def bg_flat(color):
    return lambda w, h: Image.new("RGBA", (w, h), color + (255,))


def content_checkout():
    L = layer()
    d = ImageDraw.Draw(L)
    rich(L, (50, 30), f"2 tiger tees = {money(TWO_TEES)} 🐯", F(IN8, 66), INK)
    d = ImageDraw.Draw(L)
    d.text((52, 120), f"with code {CODE}  •  2nd tee 15% off", font=F(IN6, 34), fill=GREY_TXT)
    card = (40, 200, LW - 40, LH - 20)
    d.rounded_rectangle(card, radius=34, fill=WHITE)
    d.rounded_rectangle((80, 252, 104, 274), radius=4, fill=INK)
    d.arc((84, 236, 100, 260), 180, 360, fill=INK, width=4)
    d.text((120, 244), "Checkout", font=F(IN8, 36), fill=INK)
    d.text((card[2] - 40, 248), "404 CULTURE", font=F(IN6, 26), fill=GREY_TXT, anchor="ra")
    d.line([(80, 310), (card[2] - 40, 310)], fill=(234, 234, 234), width=2)
    y = 334
    for th, name, var in [(red_tee_thumb(130, (252, 232, 226)), "Tiger League Tee", "Red / Gold"),
                          (thumb_on(garment(4), 130, (226, 240, 250)), "Tiger League Tee", "Sky Blue")]:
        L.alpha_composite(th, (80, y))
        d = ImageDraw.Draw(L)
        d.text((240, y + 30), name, font=F(IN6, 36), fill=INK)
        d.text((240, y + 78), var, font=F(IN4, 30), fill=GREY_TXT)
        d.text((card[2] - 40, y + 30), money(TEE), font=F(IN6, 36), fill=INK, anchor="ra")
        y += 156
    d.rounded_rectangle((80, y + 6, card[2] - 230, y + 96), radius=16, outline=(210, 210, 210), width=3)
    d.text((110, y + 51), CODE, font=F(IN8, 38), fill=INK, anchor="lm")
    d.rounded_rectangle((card[2] - 210, y + 6, card[2] - 40, y + 96), radius=16, fill=INK)
    d.text((card[2] - 125, y + 51), "Apply", font=F(IN6, 32), fill=WHITE, anchor="mm")
    y += 116
    txt = f"{CODE}  •  15% off 2nd item"
    cw = F(IN6, 28).getlength(txt) + 84
    d.rounded_rectangle((80, y, 80 + cw, y + 54), radius=27, fill=(226, 244, 232))
    L.alpha_composite(emoji("✅", 30), (96, y + 12))
    d = ImageDraw.Draw(L)
    d.text((138, y + 27), txt, font=F(IN6, 28), fill=GREEN, anchor="lm")
    y += 84
    d.line([(80, y), (card[2] - 40, y)], fill=(234, 234, 234), width=2)
    y += 22
    for k, v, col in [("Subtotal", money(REG), INK), (f"Discount ({CODE})", f"−{money(DISCOUNT)}", GREEN)]:
        d.text((80, y), k, font=F(IN4, 34), fill=col)
        d.text((card[2] - 40, y), v, font=F(IN6, 34), fill=col, anchor="ra")
        y += 56
    y += 6
    d.text((80, y), "Total", font=F(IN8, 46), fill=INK)
    d.text((card[2] - 40, y - 6), money(TWO_TEES), font=F(IN8, 58), fill=INK, anchor="ra")
    by = card[3] - 136
    d.rounded_rectangle((80, by, card[2] - 40, by + 104), radius=22, fill=RED)
    d.text(((80 + card[2] - 40) // 2, by + 52), "Pay now  →", font=F(IN8, 42), fill=WHITE, anchor="mm")
    return L


# ------------------------------------------------------------ 3. lifestyle + tag
def bg_photo(n, fy, top_dark=0, bot_dark=170):
    def f(w, h):
        c = cover(photo(n), w, h, fy).convert("RGBA")
        if top_dark:
            vgrad(c, 0, int(h * 0.25), top_dark, 0)
        vgrad(c, int(h * 0.6), h, 0, bot_dark)
        return c
    return f


def content_tag():
    L = layer()
    tag = Image.new("RGBA", (420, 620), (0, 0, 0, 0))
    td = ImageDraw.Draw(tag)
    td.polygon([(64, 0), (356, 0), (420, 64), (420, 620), (0, 620), (0, 64)], fill=(248, 244, 232))
    td.ellipse((192, 26, 228, 62), fill=(120, 110, 100))
    td.text((210, 96), "404 CULTURE", font=F(IN8, 32), fill=INK, anchor="ma")
    td.text((210, 142), "TIGER LEAGUE TEE", font=F(IN6, 24), fill=GREY_TXT, anchor="ma")
    td.line([(40, 190), (380, 190)], fill=(210, 204, 190), width=3)
    strike(td, (210, 214), money(REG), F(IN6, 48), (150, 150, 150), anchor="ma")
    td.text((210, 292), "2 FOR", font=F(IN8, 46), fill=INK, anchor="ma")
    td.text((210, 336), money(TWO_TEES), font=F(ANTON, 108), fill=RED, anchor="ma")
    td.text((210, 500), "with code", font=F(IN4, 28), fill=INK, anchor="mm")
    td.rounded_rectangle((60, 524, 360, 594), radius=14, fill=YELLOW)
    td.text((210, 559), CODE, font=F(IN8, 40), fill=BLACK, anchor="mm")
    shadowed(L, rot(tag, 7), (30, 380))
    d = ImageDraw.Draw(L)
    f = F(IN8, 46)
    line = "the layered tiger tee 🐯"
    tw = f.getlength(line.replace(" 🐯", "")) + 60
    d.rounded_rectangle(((LW - tw) / 2 - 24, 40, (LW + tw) / 2 + 24, 116), radius=16, fill=WHITE)
    rich(L, ((LW - tw) / 2, 50), line, f, INK)
    d = ImageDraw.Draw(L)
    cta(d, 1210, f"SHOP 2 FOR {money(TWO_TEES)}  →")
    return L


# ------------------------------------------------------------ 4. notes how-to
def content_notes():
    L = layer()
    d = ImageDraw.Draw(L)
    gold = (214, 160, 0)
    d.text((40, 30), "‹ Notes", font=F(IN4, 38), fill=gold)
    d.text((LW - 40, 30), "Done", font=F(IN6, 36), fill=gold, anchor="ra")
    rich(L, (50, 110), "how to get 2 for less 🧠", F(IN8, 66), INK)
    d = ImageDraw.Draw(L)
    f, fb = F(IN4, 42), F(IN8, 42)
    steps = [("add a tiger tee ($39.99)", None), ("add the other color — or the thermal", None),
             (f"use code {CODE} at checkout", CODE), ("2nd item = 15% off ✅", None)]
    y = 230
    for i, (s, hl) in enumerate(steps, 1):
        d.text((56, y), f"{i}.", font=F(IN6, 42), fill=INK)
        if hl:
            pre, post = s.split(hl)
            x = 110 + f.getlength(pre)
            d.rectangle((x - 6, y + 4, x + fb.getlength(hl) + 6, y + 54), fill=(255, 226, 90))
            d.text((110, y), pre, font=f, fill=INK)
            d.text((x, y), hl, font=fb, fill=INK)
            d.text((x + fb.getlength(hl) + 8, y), post, font=f, fill=INK)
        else:
            rich(L, (110, y), s, f, INK)
            d = ImageDraw.Draw(L)
        y += 74
    pw, ph, py = 314, 500, 560
    for i, (n, fy, lab) in enumerate([(2, 0.28, "red $39.99"), (4, 0.15, "blue $39.99"), (3, 0.3, "thermal $52.99")]):
        x = 50 + i * (pw + 18)
        L.alpha_composite(rounded(cover(photo(n), pw, ph, fy), 22), (x, py))
        d = ImageDraw.Draw(L)
        tw = F(IN6, 26).getlength(lab) + 30
        d.rounded_rectangle((x + pw / 2 - tw / 2, py + ph - 60, x + pw / 2 + tw / 2, py + ph - 16), radius=22, fill=(0, 0, 0, 200))
        d.text((x + pw / 2, py + ph - 38), lab, font=F(IN6, 26), fill=WHITE, anchor="mm")
    rich(L, (50, 1098), "that's it. go 👇", F(IN4, 42), INK)
    d = ImageDraw.Draw(L)
    cta(d, 1200, f"SHOP NOW  •  CODE {CODE}", bg=BLACK, fg=YELLOW)
    return L


# ------------------------------------------------------------ 5. thermal sticky
def content_thermal():
    L = layer()
    note = sticky(["don't forget:", CODE, "2nd one 15% off", "(+ a tiger tee)"], 470, 440, sizes=[40, 76, 40, 36])
    shadowed(L, note, (570, 60), blur=14, alpha=120)
    note2 = sticky(["$52.99"], 300, 150, color=(255, 150, 190), deg=5, sizes=[64])
    shadowed(L, note2, (50, 120), blur=12, alpha=110)
    d = ImageDraw.Draw(L)
    d.rounded_rectangle((50, 1086, LW - 50, 1180), radius=20, fill=(255, 255, 255, 235))
    d.text((LW // 2, 1133), "waffle knit  •  all-over graphic  •  sleeve print", font=F(IN6, 32), fill=INK, anchor="mm")
    cta(d, 1210, f"SHOP THE THERMAL — {money(THERMAL)}", bg=INK, fg=YELLOW, size=36)
    return L


ADS = [
    ("01_two_for_7398", bg_red, content_two_for),
    ("02_checkout_savings", bg_flat((245, 245, 247)), content_checkout),
    ("03_lifestyle_price_tag", bg_photo(2, 0.3, top_dark=60), content_tag),
    ("04_notes_how_to", bg_flat((252, 250, 244)), content_notes),
    ("05_thermal_sticky_note", bg_photo(3, 0.3), content_thermal),
]

if __name__ == "__main__":
    for name, bg, content in ADS:
        build(name, bg, content)
