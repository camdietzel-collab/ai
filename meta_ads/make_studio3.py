"""Studio pack 3: ten more engaging studio compositions (4:5 + 9:16).

Same studio language as make_studio / make_studio2 (seamless sweep, real
shadows, minimal tracked type) with one hook per ad: a question, scale
play, a lineup, motion, a sculpture, a slider.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps

from make_ads_v2 import ANTON, F, fit_font
from make_ads_v7 import CODE, IN4, IN6, IN8, emoji
from make_studio import SIZES, apple_box, cut, frame_type, multiply_shadow, place, save, seamless, tracked
from make_studio2 import BLUE_LINE, RED_LINE, THERM_LINE, flat, float_product

INK = (22, 22, 24)
CREAM = (240, 232, 218)
RED = (206, 24, 36)
YELLOW = (240, 190, 40)


def hook(c, text, y, size, ink, track=4):
    d = ImageDraw.Draw(c)
    f = F(ANTON, size)
    tracked(d, (c.width / 2, y), text, f, ink, track, anchor="m")


def sub(c, text, y, ink, size=30):
    d = ImageDraw.Draw(c)
    tracked(d, (c.width / 2, y), text, F(IN6, size), ink, 3, anchor="m")


# ------------------------------------------------------------ E01 red or blue
def e01_red_or_blue():
    for tag, (w, h, st, sb) in SIZES.items():
        hw = w // 2
        floor_y = h - sb - 190
        top = st + 300
        left = seamless(hw, h, (226, 178, 34), (238, 196, 70), floor_y - 40, key=(0.5, 0.2), seed=3)
        left = place(left, cut(2), hw * 0.5, floor_y, floor_y - top, tint=(240, 190, 60))
        right = seamless(w - hw, h, (170, 200, 222), (184, 212, 230), h, key=(0.5, 0.2), seed=4)
        hgt = int((h - top) * 1.0)
        right = place(right, cut(4), (w - hw) * 0.5, top + hgt, hgt, tint=(170, 200, 222), contact=False, cast="wall",
                      rim_amt=0.4)
        c = Image.new("RGBA", (w, h))
        c.paste(left, (0, 0))
        c.paste(right, (hw, 0))
        fade = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        fd = ImageDraw.Draw(fade)
        for y in range(h - sb - 260, h):
            t = (y - (h - sb - 260)) / 260
            fd.line([(hw, y), (w, y)], fill=(176, 204, 224, int(255 * min(1, t ** 1.4))))
        c.alpha_composite(fade)
        ImageDraw.Draw(c).line([(hw, st + 230), (hw, h)], fill=(250, 250, 248), width=4)
        hook(c, "RED OR BLUE?", st + 70, 120, INK, 6)
        sub(c, "which one's yours?", st + 222, INK, 30)
        frame_type(c, st, sb, INK, "TIGER LEAGUE TEE", "$39.99 EACH", "BOTH $73.98", f"CODE {CODE}")
        save(c, "E01_red_or_blue", tag)
    print("E01")


# ------------------------------------------------------------ E02 giant type behind
def e02_tiger_depth():
    for tag, (w, h, st, sb) in SIZES.items():
        floor_y = h - sb - 190
        c = seamless(w, h, (188, 189, 190), (198, 199, 200), floor_y - 30, key=(0.5, 0.3), falloff=0.35, grain=4)
        height = int((floor_y - st - 90) * 0.98)
        f = fit_font(ANTON, "TIGER", w - 40, 900)
        d = ImageDraw.Draw(c)
        bb = d.textbbox((0, 0), "TIGER", font=f)
        y = floor_y - height + int(height * 0.08) - bb[1]
        d.text((w / 2, y), "TIGER", font=f, fill=RED, anchor="ma")
        c = place(c, cut(5), w * 0.5, floor_y, height, tint=(200, 200, 205), cast="flash", rim=(255, 255, 255),
                  rim_amt=0.2, grade=0.03)
        frame_type(c, st, sb, INK, *RED_LINE)
        save(c, "E02_tiger_type_behind", tag)
    print("E02")


# ------------------------------------------------------------ E03 lineup
def e03_lineup():
    for tag, (w, h, st, sb) in SIZES.items():
        floor_y = h - sb - 190
        c = seamless(w, h, (214, 206, 194), (224, 216, 204), floor_y - 40, key=(0.5, 0.2), falloff=0.5)
        stand_h = int((floor_y - st - 200) * 0.98)
        seat_h = int(stand_h * 0.8)
        sub1 = cut(1)
        bw = int(sub1.width * seat_h / sub1.height * 0.9)
        seat = floor_y - int(seat_h * 0.47)
        sh = Image.new("L", (w, h), 0)
        ImageDraw.Draw(sh).ellipse((w / 2 - bw * 0.7, floor_y - 22, w / 2 + bw * 0.7, floor_y + 22), fill=255)
        c = multiply_shadow(c, sh.filter(ImageFilter.GaussianBlur(20)), 0.5)
        apple_box(c, w / 2 - bw / 2 - 20, seat, w / 2 + bw / 2 + 10, floor_y)
        c = place(c, sub1, w * 0.5, floor_y + 4, seat_h, tint=(220, 210, 196), contact=False, cast=None, rim_amt=0.3)
        c = place(c, cut(2), w * 0.19, floor_y, stand_h, tint=(220, 210, 196), cast_dir=-1)
        c = place(c, cut(5), w * 0.81, floor_y, int(stand_h * 0.97), tint=(220, 210, 196))
        hook(c, "THE LEAGUE.", st + 70, 104, INK, 8)
        frame_type(c, st, sb, INK, "TIGER LEAGUE TEE", "RED / GOLD  —  $39.99", "2 FOR $73.98", f"CODE {CODE}")
        save(c, "E03_the_league_lineup", tag)
    print("E03")


# ------------------------------------------------------------ E04 scale play
def e04_giant_tee():
    for tag, (w, h, st, sb) in SIZES.items():
        floor_y = h - sb - 190
        c = seamless(w, h, (190, 214, 232), (200, 222, 238), floor_y - 40, key=(0.4, 0.2), falloff=0.45)
        tee = flat(4)
        tw = int(w * 0.96)
        th = round(tee.height * tw / tee.width)
        cy = st + 90 + th / 2
        c = float_product(c, tee, w * 0.5, cy, tw, tint=(190, 214, 232), lift=int(floor_y - (cy + th / 2) - 20))
        c = place(c, cut(2), w * 0.78, floor_y, int((floor_y - st) * 0.36), tint=(200, 220, 236))
        frame_type(c, st, sb, (16, 34, 62), *BLUE_LINE)
        save(c, "E04_giant_blue_tee", tag)
    print("E04")


# ------------------------------------------------------------ E05 spotlight
def e05_spotlight():
    for tag, (w, h, st, sb) in SIZES.items():
        floor_y = h - sb - 190
        c = seamless(w, h, (14, 14, 16), (20, 20, 22), floor_y - 30, key=(0.5, 0.6), falloff=0.95, grain=4)
        beam = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(beam).polygon([(w * 0.44, 0), (w * 0.56, 0), (w * 0.86, floor_y + 20), (w * 0.14, floor_y + 20)],
                                     fill=(255, 236, 200, 46))
        c.alpha_composite(beam.filter(ImageFilter.GaussianBlur(30)))
        pool = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(pool).ellipse((w * 0.12, floor_y - 40, w * 0.88, floor_y + 70), fill=(255, 230, 190, 70))
        c.alpha_composite(pool.filter(ImageFilter.GaussianBlur(26)))
        hook(c, "2 FOR $73.98", st + 80, 110, CREAM, 6)
        c = place(c, cut(5), w * 0.5, floor_y, int((floor_y - st - 250) * 0.98), tint=(255, 220, 180), cast=None,
                  rim=(255, 220, 170), rim_amt=0.6, grade=0.05)
        frame_type(c, st, sb, CREAM, *RED_LINE)
        save(c, "E05_spotlight", tag)
    print("E05")


# ------------------------------------------------------------ E06 motion trail
def hblur(im, k):
    small = im.resize((max(1, im.width // k), im.height), Image.BILINEAR)
    return small.resize(im.size, Image.BILINEAR)


def e06_motion():
    for tag, (w, h, st, sb) in SIZES.items():
        floor_y = h - sb - 190
        c = seamless(w, h, (232, 229, 222), (238, 235, 229), floor_y - 40, key=(0.3, 0.2))
        height = int((floor_y - st - 230) * 0.98)
        s = cut(5)
        s = s.resize((round(s.width * height / s.height), height), Image.LANCZOS)
        for dx, a in [(-330, 40), (-230, 70), (-130, 110)]:
            g = hblur(s, 10)
            al = g.getchannel("A").point(lambda v: v * a // 255)
            g.putalpha(al)
            c.alpha_composite(g, (int(w * 0.58 - s.width / 2 + dx), floor_y - height))
        c = place(c, cut(5), w * 0.58, floor_y, height, tint=(232, 229, 222))
        hook(c, "MOVE IN IT.", st + 80, 96, INK, 8)
        frame_type(c, st, sb, INK, *RED_LINE)
        save(c, "E06_motion_trail", tag)
    print("E06")


# ------------------------------------------------------------ E07 triptych
def e07_triptych():
    for tag, (w, h, st, sb) in SIZES.items():
        pw = w // 3
        top, bot = st + 230, h - sb - 230
        panels = []
        p = seamless(pw, h, (210, 30, 40), (222, 42, 52), bot - 40, key=(0.5, 0.2), seed=5)
        p = place(p, cut(5), pw * 0.5, bot, int((bot - top) * 0.98), tint=(220, 50, 60), rim_amt=0.25)
        panels.append((p, "RED  $39.99"))
        p = seamless(pw, h, (176, 204, 224), (176, 204, 224), h, key=(0.5, 0.2), seed=6)
        p = float_product(p, flat(4), pw * 0.5, (top + bot) / 2, int(pw * 0.9), tint=(176, 204, 224))
        panels.append((p, "BLUE  $39.99"))
        p = seamless(w - 2 * pw, h, (226, 218, 204), (226, 218, 204), h, key=(0.5, 0.2), seed=7)
        p = float_product(p, flat(3), (w - 2 * pw) * 0.5, (top + bot) / 2, int(pw * 0.9), tint=(226, 218, 204))
        panels.append((p, "THERMAL  $52.99"))
        c = Image.new("RGBA", (w, h))
        for i, (p, lab) in enumerate(panels):
            c.paste(p, (i * pw, 0))
            d = ImageDraw.Draw(c)
            col = (255, 240, 225) if i == 0 else INK
            tracked(d, (i * pw + pw / 2, bot + 30), lab, F(IN8, 26), col, 3, anchor="m")
        d = ImageDraw.Draw(c)
        for i in (1, 2):
            d.line([(i * pw, 0), (i * pw, h)], fill=(250, 250, 248), width=3)
        band = Image.new("RGBA", (w, 190), (250, 248, 244, 240))
        c.alpha_composite(band, (0, st + 64))
        hook(c, "PICK YOUR 2", st + 84, 104, INK, 8)
        low = Image.new("RGBA", (w, 170), (18, 18, 20, 225))
        c.alpha_composite(low, (0, h - sb - 150))
        frame_type(c, st, sb, (250, 248, 244), "MIX ANY TWO", "2ND ONE 15% OFF", "", f"CODE {CODE}")
        save(c, "E07_pick_your_2", tag)
    print("E07")


# ------------------------------------------------------------ E08 giant 2 sculpture
def e08_giant_two():
    for tag, (w, h, st, sb) in SIZES.items():
        floor_y = h - sb - 190
        c = seamless(w, h, (222, 220, 216), (232, 230, 226), floor_y - 40, key=(0.25, 0.2), falloff=0.5)
        size = int((floor_y - st - 120) * 0.95)
        f = F(ANTON, size)
        d = ImageDraw.Draw(c)
        bb = d.textbbox((0, 0), "2", font=f)
        x = w * 0.36 - (bb[2] - bb[0]) / 2 - bb[0]
        y = floor_y - bb[3]
        sh = Image.new("L", (w, h), 0)
        ImageDraw.Draw(sh).ellipse((x + bb[0] - 10, floor_y - 26, x + bb[2] + 70, floor_y + 26), fill=255)
        c = multiply_shadow(c, sh.filter(ImageFilter.GaussianBlur(20)), 0.45)
        d = ImageDraw.Draw(c)
        depth = 34
        for i in range(depth, 0, -1):
            v = int(150 - i * 1.6)
            d.text((x + i, y - i * 0.5), "2", font=f, fill=(v + 40, v - 10, 10))
        face = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        fd = ImageDraw.Draw(face)
        fd.text((x, y), "2", font=f, fill=(246, 196, 40))
        # soft top-left key on the face
        grad = Image.new("L", (w, h), 0)
        gd = ImageDraw.Draw(grad)
        for yy in range(h):
            gd.line([(0, yy), (w, yy)], fill=int(40 * (1 - yy / h)))
        lit = Image.new("RGBA", (w, h), (255, 255, 255, 0))
        lit.putalpha(Image.fromarray(np.minimum(np.asarray(grad), np.asarray(face.getchannel("A")))))
        c.alpha_composite(face)
        c.alpha_composite(lit)
        c = place(c, cut(2), w * 0.74, floor_y, int((floor_y - st - 90) * 0.92), tint=(230, 226, 220))
        frame_type(c, st, sb, INK, "2 TIGER LEAGUE TEES", "RED + BLUE  —  $79.98", "NOW $73.98", f"CODE {CODE}")
        save(c, "E08_giant_2", tag)
    print("E08")


# ------------------------------------------------------------ E09 rate this fit
def e09_rate():
    for tag, (w, h, st, sb) in SIZES.items():
        floor_y = h - sb - 190
        c = seamless(w, h, (226, 224, 220), (234, 232, 228), floor_y - 40, key=(0.3, 0.2))
        c = place(c, cut(2), w * 0.5, floor_y, int((floor_y - st - 300) * 0.98), tint=(226, 224, 220))
        card = (w * 0.16, st + 70, w * 0.84, st + 250)
        sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle((card[0], card[1] + 14, card[2], card[3] + 14), radius=34, fill=(0, 0, 0, 60))
        c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
        d = ImageDraw.Draw(c)
        d.rounded_rectangle(card, radius=34, fill=(255, 255, 255))
        d.text((w / 2, card[1] + 34), "rate this fit", font=F(IN8, 44), fill=INK, anchor="ma")
        x0, x1, ty = card[0] + 60, card[2] - 60, card[1] + 130
        tr = Image.new("RGBA", (int(x1 - x0), 16), (0, 0, 0, 0))
        trd = ImageDraw.Draw(tr)
        for i in range(tr.width):
            t = i / tr.width
            trd.line([(i, 0), (i, 15)], fill=(int(255), int(200 - 150 * t), int(60 - 40 * t)))
        m = Image.new("L", tr.size, 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, tr.width - 1, 15), radius=8, fill=255)
        tr.putalpha(m)
        c.alpha_composite(tr, (int(x0), int(ty)))
        e = emoji("🔥", 74)
        c.alpha_composite(e, (int(x0 + (x1 - x0) * 0.9 - e.width / 2), int(ty - e.height / 2 + 8)))
        frame_type(c, st, sb, INK, *RED_LINE)
        save(c, "E09_rate_this_fit", tag)
    print("E09")


# ------------------------------------------------------------ E10 basic -> league slider
def e10_slider():
    for tag, (w, h, st, sb) in SIZES.items():
        floor_y = h - sb - 190
        c = seamless(w, h, (226, 178, 34), (238, 196, 70), floor_y - 40, key=(0.5, 0.2))
        c = place(c, cut(5), w * 0.5, floor_y, int((floor_y - st - 90) * 0.98), tint=(240, 190, 60))
        left = ImageOps.grayscale(c.crop((0, 0, w // 2, h))).convert("RGBA")
        left = Image.blend(left, Image.new("RGBA", left.size, (150, 150, 150, 255)), 0.15)
        c.paste(left, (0, 0))
        d = ImageDraw.Draw(c)
        d.line([(w // 2, 0), (w // 2, h)], fill=(255, 255, 255), width=5)
        cy = (st + h - sb) // 2
        d.ellipse((w // 2 - 46, cy - 46, w // 2 + 46, cy + 46), fill=(255, 255, 255))
        for s in (-1, 1):
            d.polygon([(w // 2 + s * 30, cy), (w // 2 + s * 12, cy - 14), (w // 2 + s * 12, cy + 14)], fill=INK)
        tracked(d, (w * 0.25, st + 90), "BASIC", F(ANTON, 72), (235, 235, 235), 8, anchor="m")
        tracked(d, (w * 0.75, st + 90), "LEAGUE", F(ANTON, 72), INK, 8, anchor="m")
        frame_type(c, st, sb, INK, *RED_LINE)
        save(c, "E10_basic_to_league", tag)
    print("E10")


if __name__ == "__main__":
    import make_ads_v7
    make_ads_v7.EMOJI.update("🔥")
    for fn in (e01_red_or_blue, e02_tiger_depth, e03_lineup, e04_giant_tee, e05_spotlight, e06_motion,
               e07_triptych, e08_giant_two, e09_rate, e10_slider):
        fn()
