"""Studio pack 2: ten cleaner studio compositions (4:5 + 9:16).

Builds on make_studio.py (seamless sweep, shadows, rim, grade, tracked type).
Adds floating product shots from the studio garment cut-outs, a white
plinth, and a split-frame duo.
"""
import os

from PIL import Image, ImageDraw, ImageFilter

from make_studio import SIZES, cut, frame_type, multiply_shadow, place, save, seamless
from make_ads_v7 import CODE

HERE = os.path.dirname(os.path.abspath(__file__))
RED_LINE = ("TIGER LEAGUE TEE", "RED / GOLD  —  $39.99", "2 FOR $73.98", f"CODE {CODE}")
BLUE_LINE = ("TIGER LEAGUE TEE", "SKY BLUE  —  $39.99", "2 FOR $73.98", f"CODE {CODE}")
THERM_LINE = ("CULTURE THERMAL", "CREAM WAFFLE KNIT  —  $52.99", "+ A TIGER TEE", f"2ND 15% OFF  •  {CODE}")


def flat(n):
    return Image.open(os.path.join(HERE, "..", "campaign", "cutouts", f"{n}.png")).convert("RGBA")


def float_product(c, img, cx, cy, width, tint, lift=34):
    """A product floating just above the sweep with a soft shadow underneath."""
    w, h = c.size
    height = round(img.height * width / img.width)
    bottom = round(cy + height / 2)
    sh = Image.new("L", (w, h), 0)
    ImageDraw.Draw(sh).ellipse((cx - width * 0.42, bottom + lift - 18, cx + width * 0.42, bottom + lift + 22), fill=255)
    c = multiply_shadow(c, sh.filter(ImageFilter.GaussianBlur(26)), 0.38)
    return place(c, img, cx, bottom, height, tint=tint, contact=False, cast=None, rim_amt=0.12, grade=0.03)


def standing(name, n, wall, floor, ink, lines, cast="soft", key=(0.3, 0.2), falloff=0.55, rim=(255, 244, 228),
             rim_amt=0.35, grain=3.0, tint=None, scale=0.98, kicker="DROP 04"):
    for tag, (w, h, st, sb) in SIZES.items():
        floor_y = h - sb - 190
        c = seamless(w, h, wall, floor, floor_y - 40, key=key, falloff=falloff, grain=grain)
        c = place(c, cut(n), w * 0.5, floor_y, int((floor_y - st - 90) * scale), tint=tint or wall, cast=cast,
                  rim=rim, rim_amt=rim_amt)
        frame_type(c, st, sb, ink, *lines, kicker=kicker)
        save(c, name, tag)
    print("wrote", name)


def medium(name, n, wall, ink, lines, rim=(255, 236, 214), key=(0.7, 0.18)):
    for tag, (w, h, st, sb) in SIZES.items():
        c = seamless(w, h, wall, wall, h, key=key, falloff=0.5)
        height = int((h - st) * 1.02)
        c = place(c, cut(n), w * 0.46, st + 110 + height, height, tint=wall, contact=False, cast="wall", rim=rim, rim_amt=0.45)
        fade = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        fd = ImageDraw.Draw(fade)
        for y in range(h - sb - 300, h):
            t = (y - (h - sb - 300)) / 300
            fd.line([(0, y), (w, y)], fill=tuple(wall) + (int(255 * min(1, t ** 1.4)),))
        c.alpha_composite(fade)
        frame_type(c, st, sb, ink, *lines)
        save(c, name, tag)
    print("wrote", name)


def product(name, items, wall, ink, lines, key=(0.5, 0.25)):
    """items: list of (image, cx_frac, cy_frac, width_frac)."""
    for tag, (w, h, st, sb) in SIZES.items():
        c = seamless(w, h, wall, wall, h, key=key, falloff=0.45, grain=2.5)
        top, bot = st + 80, h - sb - 170
        for img, fx, fy, fw in items:
            c = float_product(c, img, w * fx, top + (bot - top) * fy, int(w * fw), tint=wall)
        frame_type(c, st, sb, ink, *lines)
        save(c, name, tag)
    print("wrote", name)


def plinth(c, x0, y0, x1, y1):
    d = ImageDraw.Draw(c)
    for y in range(int(y0), int(y1)):
        t = (y - y0) / max(1, y1 - y0)
        v = int(246 - 22 * t)
        d.line([(x0, y), (x1, y)], fill=(v, v, v - 2))
    d.rectangle((x0, y0, x1, y0 + 10), fill=(252, 252, 250))
    d.line([(x1, y0), (x1, y1)], fill=(200, 200, 198), width=3)


def seated_plinth(name="C08_seated_white_plinth"):
    for tag, (w, h, st, sb) in SIZES.items():
        floor_y = h - sb - 170
        c = seamless(w, h, (214, 214, 212), (224, 224, 222), floor_y - 30, key=(0.4, 0.2), falloff=0.4)
        subj = cut(1)
        height = int((floor_y - st - 80) * 0.97)
        bw = int(subj.width * height / subj.height * 0.95)
        seat = floor_y - int(height * 0.47)
        sh = Image.new("L", (w, h), 0)
        ImageDraw.Draw(sh).ellipse((w / 2 - bw * 0.8, floor_y - 24, w / 2 + bw * 0.8, floor_y + 24), fill=255)
        c = multiply_shadow(c, sh.filter(ImageFilter.GaussianBlur(22)), 0.45)
        plinth(c, w / 2 - bw / 2 - 40, seat, w / 2 + bw / 2 + 20, floor_y)
        c = place(c, subj, w * 0.5, floor_y + 4, height, tint=(220, 220, 220), contact=False, cast=None,
                  rim_amt=0.25, grade=0.03)
        frame_type(c, st, sb, (24, 24, 26), *RED_LINE)
        save(c, name, tag)
    print("wrote", name)


def split_duo(name="C10_split_red_blue"):
    for tag, (w, h, st, sb) in SIZES.items():
        hw = w // 2
        floor_y = h - sb - 190
        left = seamless(hw, h, (226, 178, 34), (238, 196, 70), floor_y - 40, key=(0.5, 0.2), seed=3)
        left = place(left, cut(2), hw * 0.5, floor_y, int((floor_y - st - 90) * 0.92), tint=(240, 190, 60))
        right = seamless(w - hw, h, (170, 200, 222), (184, 212, 230), h, key=(0.5, 0.2), seed=4)
        height = int((h - st) * 0.98)
        right = place(right, cut(4), (w - hw) * 0.5, st + 110 + height, height, tint=(170, 200, 222),
                      contact=False, cast="wall", rim_amt=0.4)
        c = Image.new("RGBA", (w, h))
        c.paste(left, (0, 0))
        c.paste(right, (hw, 0))
        fade = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        fd = ImageDraw.Draw(fade)
        for y in range(h - sb - 260, h):
            t = (y - (h - sb - 260)) / 260
            fd.line([(hw, y), (w, y)], fill=(176, 204, 224, int(255 * min(1, t ** 1.4))))
        c.alpha_composite(fade)
        ImageDraw.Draw(c).line([(hw, 0), (hw, h)], fill=(250, 250, 248), width=4)
        frame_type(c, st, sb, (20, 22, 30), "RED + BLUE", "$39.99 EACH",
                   "BOTH $73.98", f"CODE {CODE}")
        save(c, name, tag)
    print("wrote", name)


if __name__ == "__main__":
    standing("C01_offwhite_red_tee", 2, (232, 229, 222), (238, 235, 229), (26, 24, 22), RED_LINE)
    standing("C02_red_tonal_flash", 5, (178, 22, 32), (190, 30, 40), (255, 238, 214), RED_LINE, cast="flash",
             key=(0.5, 0.3), falloff=0.4, rim=(255, 255, 255), rim_amt=0.15, grain=3.5, tint=(200, 40, 50))
    standing("C03_black_lowkey_red_tee", 2, (20, 20, 22), (28, 27, 28), (236, 226, 210), RED_LINE,
             key=(0.5, 0.3), falloff=0.9, rim=(255, 210, 160), rim_amt=0.7, grain=4, tint=(60, 50, 44))
    product("C04_blue_tee_product", [(flat(4), 0.5, 0.5, 0.78)], (196, 220, 236), (16, 34, 62), BLUE_LINE)
    product("C05_thermal_product", [(flat(3), 0.5, 0.5, 0.74)], (214, 208, 198), (30, 28, 24), THERM_LINE)
    product("C06_the_set_product", [(flat(4), 0.3, 0.38, 0.5), (flat(3), 0.68, 0.62, 0.5)], (238, 232, 220),
            (30, 28, 24), ("THE SET", "TIGER TEE $39.99  •  THERMAL $52.99", "2ND 15% OFF", f"CODE {CODE}"))
    medium("C07_cream_blue_tee", 4, (232, 226, 214), (40, 36, 30), BLUE_LINE, key=(0.25, 0.2))
    seated_plinth()
    standing("C09_navy_red_tee", 5, (22, 34, 64), (30, 44, 78), (240, 232, 218), RED_LINE, key=(0.45, 0.25),
             falloff=0.7, rim=(255, 200, 150), rim_amt=0.5, tint=(60, 70, 110))
    split_duo()
