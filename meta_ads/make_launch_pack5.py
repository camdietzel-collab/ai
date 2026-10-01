"""Launch pack 5: premium depth-type ads — giant type sits BEHIND the subject.

Real photos full-bleed, the subject is re-cut at each output size (rembg)
and composited over the type, so the product stays huge and real.
Rendered natively at 4:5 and 9:16 (text kept out of the Stories/Reels UI).
"""
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from rembg import new_session, remove

from make_ads_v2 import ANTON, BLACK, BLUE, RED, WHITE, YELLOW, F, cover, fit_font, photo
from make_ads_v7 import CODE, IN4, IN6, IN8, INK
from make_ads_v8 import TWO_TEES, money
from make_ads_v10 import REG, strike

HERE = os.path.dirname(os.path.abspath(__file__))
PACK = os.path.join(HERE, "launch_pack")
SIZES = {"4x5": (1080, 1350, 40, 40), "9x16": (1080, 1920, 250, 400)}
_session = None
_mask_cache = {}


def subject(img):
    """RGBA cut-out of the main subject of an RGB image (same size)."""
    global _session
    key = (img.size, img.tobytes()[:4096])
    if key not in _mask_cache:
        if _session is None:
            _session = new_session("isnet-general-use")
        _mask_cache[key] = remove(img, session=_session)
    return _mask_cache[key]


def top_of(cut):
    a = np.asarray(cut.getchannel("A"))
    rows = np.where(a.max(axis=1) > 128)[0]
    return int(rows.min()) if len(rows) else 0


def vgrad(c, y0, y1, a0, a1):
    ov = Image.new("RGBA", c.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for y in range(max(0, y0), min(c.height, y1)):
        t = (y - y0) / max(1, y1 - y0)
        d.line([(0, y), (c.width, y)], fill=(0, 0, 0, int(a0 + (a1 - a0) * t)))
    c.alpha_composite(ov)


def cta(d, w, y, text, bg=YELLOW, fg=BLACK, size=40):
    d.rounded_rectangle((50, y, w - 50, y + 108), radius=26, fill=bg)
    d.text((w // 2, y + 54), text, font=F(IN8, size), fill=fg, anchor="mm")


def code_chip(d, cx, y, size=36, bg=WHITE, fg=INK):
    t = f"CODE {CODE}"
    f = F(IN8, size)
    tw = f.getlength(t)
    d.rounded_rectangle((cx - tw / 2 - 24, y, cx + tw / 2 + 24, y + size + 26), radius=14, fill=bg)
    d.text((cx, y + (size + 26) / 2), t, font=f, fill=fg, anchor="mm")


def word_layer(size, word, color, y, w, outline=False):
    L = Image.new("RGBA", size, (0, 0, 0, 0))
    f = fit_font(ANTON, word, w - 40, 900)
    d = ImageDraw.Draw(L)
    if outline:
        d.text((size[0] // 2, y), word, font=f, fill=(0, 0, 0, 0), anchor="ma", stroke_width=5, stroke_fill=color)
    else:
        d.text((size[0] // 2, y), word, font=f, fill=color, anchor="ma")
    return L, f


def save(c, name, tag):
    os.makedirs(PACK, exist_ok=True)
    c.convert("RGB").save(os.path.join(PACK, f"{name}_{tag}.jpg"), quality=95)


# ------------------------------------------------------------ depth single
def depth_single(name, n, fy, word, word_color, kicker, price_line, cta_text, accent):
    for tag, (w, h, st, sb) in SIZES.items():
        base = cover(photo(n), w, h, fy)
        cut = subject(base)
        c = base.convert("RGBA")
        vgrad(c, 0, int(h * 0.3), 90, 0)
        head = top_of(cut)
        wl, f = word_layer((w, h), word, word_color, 0, w)
        bb = ImageDraw.Draw(wl).textbbox((w // 2, 0), word, font=f, anchor="ma")
        wh = bb[3] - bb[1]
        wy = max(st + 10, head + int(wh * 0.15)) - bb[1]
        wy = min(wy, int(h * 0.42) - bb[1])
        wl, _ = word_layer((w, h), word, word_color, wy, w)
        c.alpha_composite(wl)
        c.alpha_composite(cut)
        # bottom panel
        bottom = h - sb
        vgrad(c, bottom - 520, h, 0, 235)
        d = ImageDraw.Draw(c)
        d.text((60, bottom - 420), kicker, font=F(IN6, 32), fill=(235, 235, 235))
        strike(d, (60, bottom - 360), money(REG), F(IN8, 40), (190, 190, 190))
        d.text((60, bottom - 310), price_line, font=F(ANTON, 120), fill=accent)
        code_chip(d, w - 60 - F(IN8, 34).getlength(f"CODE {CODE}") / 2 - 24, bottom - 200, 34)
        cta(d, w, bottom - 130, cta_text)
        save(c, name, tag)
    print("wrote", name)


# ------------------------------------------------------------ diptych with giant "2"
def ad_diptych(name="24_red_plus_blue"):
    for tag, (w, h, st, sb) in SIZES.items():
        hw = w // 2
        left = cover(photo(5), hw, h, 0.12)
        right = cover(photo(4), w - hw, h, 0.05)
        c = Image.new("RGBA", (w, h))
        c.paste(left, (0, 0))
        c.paste(right, (hw, 0))
        vgrad(c, 0, int(h * 0.25), 80, 0)
        cut_l, cut_r = subject(left), subject(right)
        d = ImageDraw.Draw(c)
        for word, x, col, anc in [("RED", 34, YELLOW, "la"), ("BLUE", hw + 30, WHITE, "la")]:
            d.text((x, st + 6), word, font=F(ANTON, 104), fill=col, anchor=anc, stroke_width=4, stroke_fill=BLACK)
        d.line([(hw, 0), (hw, h)], fill=WHITE, width=6)
        bottom = h - sb
        vgrad(c, bottom - 460, h, 0, 235)
        d = ImageDraw.Draw(c)
        d.text((w // 2, bottom - 400), "RED  +  BLUE  TIGER LEAGUE TEES", font=F(IN8, 34), fill=WHITE, anchor="ma")
        strike(d, (w // 2 - 230, bottom - 336), money(REG), F(IN8, 44), (190, 190, 190), anchor="ma")
        d.text((w // 2 + 90, bottom - 350), money(TWO_TEES), font=F(ANTON, 120), fill=YELLOW, anchor="ma")
        code_chip(d, w // 2, bottom - 196, 34)
        cta(d, w, bottom - 128, "GET BOTH  →")
        save(c, name, tag)
    print("wrote", name)


# ------------------------------------------------------------ thermal depth
def ad_thermal(name="25_culture_thermal_depth"):
    for tag, (w, h, st, sb) in SIZES.items():
        base = cover(photo(3), w, h, 0.32)
        cut = subject(base)
        c = Image.new("RGBA", (w, h), (24, 22, 22, 255))
        bg = base.convert("RGBA").filter(ImageFilter.GaussianBlur(18))
        bg.alpha_composite(Image.new("RGBA", (w, h), (10, 10, 10, 150)))
        c.alpha_composite(bg)
        wl, f = word_layer((w, h), "CULTURE", (245, 240, 225), 0, w)
        bb = ImageDraw.Draw(wl).textbbox((w // 2, 0), "CULTURE", font=f, anchor="ma")
        wy = st + int((h - st - sb) * 0.18) - bb[1]
        wl, _ = word_layer((w, h), "CULTURE", (245, 240, 225), wy, w)
        c.alpha_composite(wl)
        sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        a = cut.getchannel("A").filter(ImageFilter.GaussianBlur(20)).point(lambda v: v * 150 // 255)
        sh.paste((0, 0, 0, 255), (16, 26), a)
        c.alpha_composite(sh)
        c.alpha_composite(cut)
        bottom = h - sb
        vgrad(c, bottom - 440, h, 0, 230)
        d = ImageDraw.Draw(c)
        d.text((60, bottom - 380), "THE CULTURE THERMAL", font=F(IN8, 40), fill=WHITE)
        d.text((60, bottom - 326), "waffle knit  •  all-over graphic  •  sleeve print", font=F(IN4, 30), fill=(220, 220, 220))
        d.text((60, bottom - 280), "$52.99", font=F(ANTON, 110), fill=YELLOW)
        d.text((w - 60, bottom - 250), "+ a tiger tee", font=F(IN6, 30), fill=WHITE, anchor="ra")
        d.text((w - 60, bottom - 210), "2nd one 15% off", font=F(IN8, 34), fill=YELLOW, anchor="ra")
        cta(d, w, bottom - 128, f"SHOP THE THERMAL  •  {CODE}", size=36)
        save(c, name, tag)
    print("wrote", name)


# ------------------------------------------------------------ billboard at night
def ad_billboard(name="23_billboard_at_night"):
    rng = random.Random(12)
    for tag, (w, h, st, sb) in SIZES.items():
        c = Image.new("RGBA", (w, h))
        d = ImageDraw.Draw(c)
        for y in range(h):
            t = y / h
            d.line([(0, y), (w, y)], fill=(int(10 + 30 * t), int(12 + 20 * t), int(40 + 40 * t)))
        # skyline
        x = -20
        while x < w:
            bw = rng.randint(90, 200)
            bh_ = rng.randint(int(h * 0.25), int(h * 0.6))
            top = h - bh_
            d.rectangle((x, top, x + bw, h), fill=(16, 16, 26))
            for wy in range(top + 20, h, 34):
                for wx in range(x + 12, x + bw - 16, 26):
                    if rng.random() < 0.35:
                        d.rectangle((wx, wy, wx + 12, wy + 18), fill=(255, 210, 120))
            x += bw + rng.randint(4, 20)
        # billboard
        avail_top, avail_bot = st + 20, h - sb - 170
        bw_, bh_ = w - 100, min(int((w - 100) * 0.62), avail_bot - avail_top - 120)
        bx, by = 50, avail_top + 60
        glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(glow).rectangle((bx - 40, by - 40, bx + bw_ + 40, by + bh_ + 40), fill=(255, 200, 140, 90))
        c.alpha_composite(glow.filter(ImageFilter.GaussianBlur(50)))
        d = ImageDraw.Draw(c)
        d.rectangle((bx + bw_ // 2 - 20, by + bh_, bx + bw_ // 2 + 20, h), fill=(40, 40, 50))
        d.rectangle((bx - 14, by - 14, bx + bw_ + 14, by + bh_ + 14), fill=(40, 40, 46))
        pw = int(bw_ * 0.5)
        c.paste(cover(photo(1), pw, bh_, 0.28), (bx, by))
        d = ImageDraw.Draw(c)
        d.rectangle((bx + pw, by, bx + bw_, by + bh_), fill=RED)
        cx = bx + pw + (bw_ - pw) // 2
        d.text((cx, by + bh_ * 0.08), "2 TIGER TEES", font=F(ANTON, int(bh_ * 0.12)), fill=WHITE, anchor="ma")
        d.text((cx, by + bh_ * 0.26), money(TWO_TEES), font=F(ANTON, int(bh_ * 0.24)), fill=YELLOW, anchor="ma")
        d.text((cx, by + bh_ * 0.58), "BUY 1, GET 1 15% OFF", font=F(IN8, int(bh_ * 0.055)), fill=WHITE, anchor="ma")
        d.rounded_rectangle((cx - bh_ * 0.32, by + bh_ * 0.7, cx + bh_ * 0.32, by + bh_ * 0.86), radius=10, fill=WHITE)
        d.text((cx, by + bh_ * 0.78), CODE, font=F(IN8, int(bh_ * 0.08)), fill=INK, anchor="mm")
        # spotlights
        for i in range(4):
            lx = bx + 80 + i * (bw_ - 160) // 3
            d.rectangle((lx - 20, by - 46, lx + 20, by - 26), fill=(70, 70, 76))
            beam = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            ImageDraw.Draw(beam).polygon([(lx - 14, by - 26), (lx + 14, by - 26), (lx + 90, by + 120), (lx - 90, by + 120)],
                                         fill=(255, 240, 200, 40))
            c.alpha_composite(beam.filter(ImageFilter.GaussianBlur(10)))
        d = ImageDraw.Draw(c)
        bottom = h - sb
        d.text((w // 2, by + bh_ + 40), "the league is up in lights.", font=F(IN6, 40), fill=WHITE, anchor="ma")
        cta(d, w, bottom - 128, f"SHOP 2 FOR {money(TWO_TEES)}  →")
        save(c, name, tag)
    print("wrote", name)


if __name__ == "__main__":
    depth_single("21_tiger_depth_red", 1, 0.25, "TIGER", YELLOW, "THE TIGER LEAGUE TEE — RED",
                 money(TWO_TEES), f"2 FOR {money(TWO_TEES)}  →", YELLOW)
    depth_single("22_league_depth_blue", 4, 0.05, "LEAGUE", WHITE, "THE TIGER LEAGUE TEE — SKY BLUE",
                 money(TWO_TEES), f"2 FOR {money(TWO_TEES)}  →", BLUE)
    ad_billboard()
    ad_diptych()
    ad_thermal()
