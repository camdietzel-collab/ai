"""Studio pack: subjects composited onto seamless studio backdrops.

Seamless sweep with key-light falloff and vignette, contact + cast (or hard
flash) shadows, edge-wrap rim light and a light grade on the subject, film
grain, and restrained tracked typography — no stickers, pills or emoji.
Rendered natively at 4:5 and 9:16 (text inside the Stories/Reels safe area).
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from make_ads_v2 import ANTON, F
from make_ads_v7 import CODE, IN4, IN6, IN8

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "studio_pack")
SIZES = {"4x5": (1080, 1350, 56, 56), "9x16": (1080, 1920, 250, 400)}


def cut(n):
    return Image.open(os.path.join(HERE, "cutouts", f"studio_{n}.png")).convert("RGBA")


# ------------------------------------------------------------ backdrop
def seamless(w, h, wall, floor, horizon, key=(0.35, 0.25), falloff=0.55, grain=3.0, seed=1):
    y = np.arange(h)[:, None].astype(np.float32)
    x = np.arange(w)[None, :].astype(np.float32)
    wall, floor = np.array(wall, np.float32), np.array(floor, np.float32)
    t = np.clip((y - (horizon - 90)) / 180.0, 0, 1)[..., None]          # soft sweep, no hard line
    base = wall * (1 - t) + floor * t
    base = np.broadcast_to(base, (h, w, 3)).copy()
    kx, ky = key[0] * w, key[1] * h
    r = np.sqrt(((x - kx) / w) ** 2 + ((y - ky) / h) ** 2)
    light = 1.08 - falloff * np.clip(r, 0, 1.2) ** 1.6                  # key light pool
    vign = 1 - 0.28 * (np.sqrt(((x - w / 2) / (w / 2)) ** 2 + ((y - h / 2) / (h / 2)) ** 2) / 1.42) ** 2
    img = base * (light * vign)[..., None]
    rng = np.random.default_rng(seed)
    img += rng.normal(0, grain, (h, w, 1))
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).convert("RGBA")


def multiply_shadow(c, mask, opacity):
    a = np.asarray(c).astype(np.float32)
    m = np.asarray(mask).astype(np.float32)[..., None] / 255.0 * opacity
    a[..., :3] *= (1 - m)
    return Image.fromarray(a.astype(np.uint8))


def place(c, subj, cx, bottom, height, tint, rim=(255, 244, 228), rim_amt=0.35, grade=0.06,
          contact=True, cast="soft", cast_dir=1):
    w, h = c.size
    s = subj.resize((round(subj.width * height / subj.height), height), Image.LANCZOS)
    x0, y0 = round(cx - s.width / 2), round(bottom - s.height)
    A = s.getchannel("A")
    full = Image.new("L", (w, h), 0)
    full.paste(A, (x0, y0))
    if cast == "soft":
        # shadow thrown back onto the sweep: squash + shear the silhouette, anchor at the feet
        sq = A.resize((s.width, max(1, int(s.height * 0.22))))
        sh = Image.new("L", (w, h), 0)
        pad = Image.new("L", (sq.width + 400, sq.height), 0)
        pad.paste(sq, (200, 0))
        pad = pad.transform(pad.size, Image.AFFINE, (1, -0.9 * cast_dir, 0.9 * cast_dir * pad.height if cast_dir < 0 else 0, 0, 1, 0))
        sh.paste(pad, (x0 - 200 + int(40 * cast_dir), bottom - sq.height))
        c = multiply_shadow(c, sh.filter(ImageFilter.GaussianBlur(22)), 0.28)
    elif cast == "flash":
        sh = Image.new("L", (w, h), 0)
        sh.paste(A, (x0 + 34, y0 - 14))
        c = multiply_shadow(c, sh.filter(ImageFilter.GaussianBlur(3)), 0.40)
    elif cast == "wall":
        sh = Image.new("L", (w, h), 0)
        sh.paste(A, (x0 + 30, y0 + 40))
        c = multiply_shadow(c, sh.filter(ImageFilter.GaussianBlur(26)), 0.32)
    if contact:
        cm = Image.new("L", (w, h), 0)
        ImageDraw.Draw(cm).ellipse((cx - s.width * 0.42, bottom - 22, cx + s.width * 0.42, bottom + 18), fill=255)
        c = multiply_shadow(c, cm.filter(ImageFilter.GaussianBlur(16)), 0.55)
        cm2 = Image.new("L", (w, h), 0)
        ImageDraw.Draw(cm2).ellipse((cx - s.width * 0.3, bottom - 8, cx + s.width * 0.3, bottom + 6), fill=255)
        c = multiply_shadow(c, cm2.filter(ImageFilter.GaussianBlur(5)), 0.5)
    # grade + rim on the subject
    arr = np.asarray(s).astype(np.float32)
    rgb = arr[..., :3] / 255.0
    rgb = 0.5 + (rgb - 0.5) * 1.06                                       # gentle contrast
    rgb = rgb * (1 - grade) + np.array(tint, np.float32) / 255.0 * grade  # sit it in the room's light
    al = arr[..., 3]
    edge = np.asarray(A).astype(np.float32) - np.asarray(A.filter(ImageFilter.MinFilter(9))).astype(np.float32)
    edge = np.asarray(Image.fromarray(np.clip(edge, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(5))).astype(np.float32) / 255
    rgb = rgb + edge[..., None] * rim_amt * (np.array(rim, np.float32) / 255.0 - rgb)
    out = np.dstack([np.clip(rgb * 255, 0, 255), al]).astype(np.uint8)
    c.alpha_composite(Image.fromarray(out), (x0, y0))
    return c


# ------------------------------------------------------------ type
def tracked(d, xy, text, font, fill, track=0, anchor="l"):
    width = sum(font.getlength(ch) for ch in text) + track * (len(text) - 1)
    x, y = xy
    if anchor == "r":
        x -= width
    elif anchor == "m":
        x -= width / 2
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += font.getlength(ch) + track
    return width


def frame_type(c, st, sb, ink, name, line2, right1, right2, kicker="DROP 04"):
    w, h = c.size
    d = ImageDraw.Draw(c)
    tracked(d, (56, st), "404 CULTURE", F(ANTON, 40), ink, 6)
    tracked(d, (w - 56, st + 10), kicker, F(IN6, 22), ink, 7, anchor="r")
    y = h - sb - 116
    d.line([(56, y - 22), (w - 56, y - 22)], fill=ink + (120,) if len(ink) == 3 else ink, width=2)
    tracked(d, (56, y), name, F(IN8, 40), ink, 5)
    tracked(d, (56, y + 60), line2, F(IN4, 26), ink, 3)
    tracked(d, (w - 56, y + 2), right1, F(IN8, 36), ink, 3, anchor="r")
    tracked(d, (w - 56, y + 60), right2, F(IN6, 24), ink, 5, anchor="r")


def save(c, name, tag):
    os.makedirs(OUT, exist_ok=True)
    c.convert("RGB").save(os.path.join(OUT, f"{name}_{tag}.jpg"), quality=96)


# ------------------------------------------------------------ the five shots
def shot_yellow():
    for tag, (w, h, st, sb) in SIZES.items():
        floor_y = h - sb - 190
        c = seamless(w, h, (226, 178, 34), (238, 196, 70), floor_y - 40, key=(0.3, 0.2))
        c = place(c, cut(2), w * 0.5, floor_y, int((floor_y - st - 90) * 0.98), tint=(240, 190, 60), cast_dir=1)
        frame_type(c, st, sb, (24, 20, 14), "TIGER LEAGUE TEE", "RED / GOLD  —  $39.99",
                   "2 FOR $73.98", f"CODE {CODE}")
        save(c, "S1_yellow_seamless_red_tee", tag)


def shot_blue():
    for tag, (w, h, st, sb) in SIZES.items():
        c = seamless(w, h, (170, 200, 222), (184, 212, 230), h, key=(0.7, 0.18), falloff=0.5)
        subj = cut(4)
        height = int((h - st) * 1.02)
        c = place(c, subj, w * 0.46, st + 110 + height, height, tint=(170, 200, 222), contact=False, cast="wall",
                  rim=(255, 236, 214), rim_amt=0.45)
        # fade the bottom into the backdrop so the crop reads as a framed medium shot
        fade = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        fd = ImageDraw.Draw(fade)
        for y in range(h - sb - 300, h):
            t = (y - (h - sb - 300)) / 300
            fd.line([(0, y), (w, y)], fill=(176, 204, 224, int(255 * min(1, t ** 1.4))))
        c.alpha_composite(fade)
        frame_type(c, st, sb, (16, 34, 62), "TIGER LEAGUE TEE", "SKY BLUE  —  $39.99",
                   "2 FOR $73.98", f"CODE {CODE}")
        save(c, "S2_sky_seamless_blue_tee", tag)


def shot_flash():
    for tag, (w, h, st, sb) in SIZES.items():
        floor_y = h - sb - 190
        c = seamless(w, h, (176, 178, 180), (190, 191, 192), floor_y - 30, key=(0.5, 0.3), falloff=0.35, grain=4)
        c = place(c, cut(5), w * 0.5, floor_y, int((floor_y - st - 90) * 0.98), tint=(200, 200, 205),
                  cast="flash", rim=(255, 255, 255), rim_amt=0.2, grade=0.03)
        frame_type(c, st, sb, (18, 18, 20), "TIGER LEAGUE TEE", "RED / GOLD  —  $39.99",
                   "2 FOR $73.98", f"CODE {CODE}", kicker="FLASH 04")
        save(c, "S3_flash_grey_red_tee", tag)


def apple_box(c, x0, y0, x1, y1):
    d = ImageDraw.Draw(c)
    d.rectangle((x0, y0, x1, y1), fill=(176, 132, 86))
    d.rectangle((x0, y0, x1, y0 + 14), fill=(200, 158, 108))
    for k in range(4):
        yy = y0 + 30 + k * (y1 - y0 - 40) / 4
        d.line([(x0 + 6, yy), (x1 - 6, yy)], fill=(160, 118, 76), width=2)
    hx = (x0 + x1) / 2
    d.rounded_rectangle((hx - 60, y0 + 50, hx + 60, y0 + 84), radius=17, fill=(70, 46, 26))
    d.rectangle((x0, y0, x0 + 6, y1), fill=(150, 110, 70))
    d.rectangle((x1 - 6, y0, x1, y1), fill=(150, 110, 70))


def shot_seated():
    for tag, (w, h, st, sb) in SIZES.items():
        floor_y = h - sb - 170
        c = seamless(w, h, (40, 36, 34), (52, 46, 42), floor_y - 30, key=(0.5, 0.28), falloff=0.75, grain=4)
        spot = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(spot).ellipse((w * 0.12, floor_y - 380, w * 0.88, floor_y + 60), fill=(255, 210, 160, 34))
        c.alpha_composite(spot.filter(ImageFilter.GaussianBlur(80)))
        subj = cut(1)
        height = int((floor_y - st - 80) * 0.97)
        sc = height / subj.height
        seat = floor_y - int(height * 0.47)
        bw = int(subj.width * sc * 0.95)
        c = multiply_shadow(c, Image.new("L", (w, h), 0), 0)
        sh = Image.new("L", (w, h), 0)
        ImageDraw.Draw(sh).ellipse((w / 2 - bw * 0.75, floor_y - 26, w / 2 + bw * 0.75, floor_y + 26), fill=255)
        c = multiply_shadow(c, sh.filter(ImageFilter.GaussianBlur(20)), 0.6)
        apple_box(c, w / 2 - bw / 2 - 30, seat, w / 2 + bw / 2 + 10, floor_y)
        c = place(c, subj, w * 0.5, floor_y + 4, height, tint=(255, 200, 150), contact=False, cast=None,
                  rim=(255, 214, 170), rim_amt=0.55, grade=0.05)
        frame_type(c, st, sb, (238, 228, 214), "TIGER LEAGUE TEE", "RED / GOLD  —  $39.99",
                   "2 FOR $73.98", f"CODE {CODE}")
        save(c, "S4_seated_apple_box_red_tee", tag)


def shot_thermal():
    for tag, (w, h, st, sb) in SIZES.items():
        c = seamless(w, h, (232, 226, 214), (232, 226, 214), h, key=(0.3, 0.2), falloff=0.4)
        rail_y = st + 110
        d = ImageDraw.Draw(c)
        for k, col in enumerate([(120, 122, 126), (200, 202, 206), (240, 242, 244), (170, 172, 176), (110, 112, 116)]):
            d.line([(0, rail_y - 6 + k * 3), (w, rail_y - 6 + k * 3)], fill=col, width=3)
        subj = cut(3)
        height = int((h - sb - 170 - rail_y) * 0.98)
        c = place(c, subj, w * 0.5, rail_y - 4 + height, height, tint=(236, 228, 214), contact=False, cast="wall",
                  rim=(255, 250, 240), rim_amt=0.25, grade=0.03)
        frame_type(c, st, sb, (28, 26, 22), "CULTURE THERMAL", "CREAM WAFFLE KNIT  —  $52.99",
                   "+ A TIGER TEE", f"2ND 15% OFF  •  {CODE}")
        save(c, "S5_thermal_on_rail", tag)


if __name__ == "__main__":
    for fn in (shot_yellow, shot_blue, shot_flash, shot_seated, shot_thermal):
        fn()
        print("done", fn.__name__)
