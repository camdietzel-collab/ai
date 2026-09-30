"""Round 7: five feed-native / UGC-style Meta ads carrying the BO15OFF offer.

Offer: buy 1, get 1 15% off with code BO15OFF.
Formats: vertical-video screenshot, brand SMS thread, story (9:16),
notes-app how-to, and a creator-annotated phone photo. No invented
reviews, follower/like counts, or customer messages — the only voice is
the brand's own.
"""
import os

from PIL import Image, ImageDraw, ImageFilter

from make_ads_v2 import (BLACK, BLUE, F, H, MARKER, NAVY, OUT, RED, W, WHITE, YELLOW, cover, fit_h, model,
                         photo, rot, save)
from make_ads_v5 import red_tee_box, tight

HERE = os.path.dirname(os.path.abspath(__file__))
IN4 = os.path.join(HERE, "fonts", "Inter-400.ttf")
IN6 = os.path.join(HERE, "fonts", "Inter-600.ttf")
IN8 = os.path.join(HERE, "fonts", "Inter-800.ttf")
EMOJI_FONT = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
EMOJI = set("👋🐯✅👀🔥🧠🔗👇🛒🎵📸")
CODE = "BO15OFF"
OFFER = "Buy 1, get 1 15% off"
INK, GREY_TXT = (18, 18, 18), (138, 138, 142)
BUBBLE = (233, 233, 235)
IOS_BLUE = (10, 132, 255)

_emoji_cache = {}


def emoji(ch, size):
    key = (ch, size)
    if key not in _emoji_cache:
        f = F(EMOJI_FONT, 109)
        im = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((10, 10), ch, font=f, embedded_color=True)
        im = im.crop(im.getbbox())
        _emoji_cache[key] = im.resize((size, round(im.height * size / im.width)), Image.LANCZOS)
    return _emoji_cache[key]


def rich(c, xy, s, font, fill):
    """Draw text with inline colour emoji; returns end x."""
    x, y = xy
    d = ImageDraw.Draw(c)
    asc, _ = font.getmetrics()
    run = ""

    def flush(run, x):
        if run:
            d.text((x, y), run, font=font, fill=fill)
            x += font.getlength(run)
        return x
    for ch in s:
        if ch in EMOJI:
            x = flush(run, x)
            run = ""
            e = emoji(ch, round(asc * 0.95))
            c.alpha_composite(e, (round(x + 2), round(y + asc * 0.08)))
            x += e.width + 6
        else:
            run += ch
    return flush(run, x)


def rich_len(s, font):
    asc, _ = font.getmetrics()
    n = sum(1 for ch in s if ch in EMOJI)
    return font.getlength("".join(ch for ch in s if ch not in EMOJI)) + n * (round(asc * 0.95) + 8)


def rounded(img, r):
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, img.width - 1, img.height - 1), radius=r, fill=255)
    out = img.convert("RGBA")
    out.putalpha(m)
    return out


def vgrad(c, y0, y1, a0, a1):
    ov = Image.new("RGBA", c.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0)
        d.line([(0, y), (c.width, y)], fill=(0, 0, 0, int(a0 + (a1 - a0) * t)))
    c.alpha_composite(ov)


def avatar(d, xy, r, ring=False):
    x, y = xy
    if ring:
        d.ellipse((x - 5, y - 5, x + 2 * r + 5, y + 2 * r + 5), outline=WHITE, width=4)
    d.ellipse((x, y, x + 2 * r, y + 2 * r), fill=YELLOW)
    from make_ads_v2 import ANTON
    d.text((x + r, y + r), "404", font=F(ANTON, int(r * 0.8)), fill=BLACK, anchor="mm")


def save_as(c, name):
    c.convert("RGB").save(os.path.join(OUT, name), quality=95)
    print("wrote", name)


# ---------------------------------------------------------------- icons
def heart(d, cx, cy, s, fill=WHITE):
    r = s * 0.28
    d.ellipse((cx - 2 * r, cy - r * 1.2, cx, cy + r * 0.8), fill=fill)
    d.ellipse((cx, cy - r * 1.2, cx + 2 * r, cy + r * 0.8), fill=fill)
    d.polygon([(cx - 2 * r + 2, cy + r * 0.05), (cx + 2 * r - 2, cy + r * 0.05), (cx, cy + s * 0.55)], fill=fill)


def bubble_icon(d, cx, cy, s, fill=WHITE):
    d.ellipse((cx - s * .5, cy - s * .42, cx + s * .5, cy + s * .38), fill=fill)
    d.polygon([(cx - s * .3, cy + s * .2), (cx - s * .45, cy + s * .55), (cx - s * .05, cy + s * .3)], fill=fill)


def share_icon(d, cx, cy, s, fill=WHITE):
    d.polygon([(cx + s * .5, cy), (cx, cy - s * .45), (cx, cy - s * .18), (cx - s * .5, cy - s * .1),
               (cx - s * .5, cy + s * .45), (cx - s * .1, cy + s * .12), (cx, cy + s * .12), (cx, cy + s * .45)], fill=fill)


def bookmark_icon(d, cx, cy, s, fill=WHITE):
    d.polygon([(cx - s * .35, cy - s * .5), (cx + s * .35, cy - s * .5), (cx + s * .35, cy + s * .5),
               (cx, cy + s * .22), (cx - s * .35, cy + s * .5)], fill=fill)


# ---------------------------------------------------------------- ad 31
def ad31_vertical_video():
    c = cover(photo(5), W, H, 0.12).convert("RGBA")
    vgrad(c, 0, 260, 110, 0)
    vgrad(c, 820, H, 0, 215)
    d = ImageDraw.Draw(c)
    # caption stickers (short-video style: white boxes per line)
    f = F(IN8, 50)
    y = 560
    for line in ["when the tee comes in 2 colors", "so you have to get both"]:
        tw = f.getlength(line)
        x = (W - tw) / 2
        d.rounded_rectangle((x - 22, y - 10, x + tw + 22, y + 66), radius=14, fill=WHITE)
        d.text((x, y), line, font=f, fill=INK)
        y += 78
    # right action column (no fabricated counts)
    x = W - 80
    avatar(d, (x - 40, 640), 40, ring=True)
    heart(d, x, 800, 70)
    bubble_icon(d, x, 910, 66)
    bookmark_icon(d, x, 1010, 60)
    share_icon(d, x, 1100, 64)
    # caption block
    d.text((40, 1000), "@404culture", font=F(IN8, 38), fill=WHITE)
    rich(c, (40, 1054), f"{OFFER} 🐯", F(IN6, 34), WHITE)
    d = ImageDraw.Draw(c)
    d.text((40, 1098), "code ", font=F(IN6, 34), fill=WHITE)
    cx = 40 + F(IN6, 34).getlength("code ")
    d.rounded_rectangle((cx - 6, 1094, cx + F(IN8, 34).getlength(CODE) + 8, 1142), radius=8, fill=YELLOW)
    d.text((cx, 1098), CODE, font=F(IN8, 34), fill=BLACK)
    rich(c, (40, 1150), "🎵 original sound – 404culture", F(IN4, 28), (230, 230, 230))
    d = ImageDraw.Draw(c)
    # product card
    card = (30, 1210, W - 30, 1320)
    d.rounded_rectangle(card, radius=18, fill=(255, 255, 255, 240))
    rm = tight(model(5))
    x0, y0, x1, y1 = red_tee_box(rm)
    th = rm.crop((x0 - 40, y0 - 60, x1 + 40, y1 + 20))
    th.thumbnail((86, 86))
    tb = Image.new("RGBA", (86, 86), (250, 232, 226, 255))
    tb.alpha_composite(th, ((86 - th.width) // 2, (86 - th.height) // 2))
    c.alpha_composite(rounded(tb, 12), (card[0] + 12, card[1] + 12))
    d = ImageDraw.Draw(c)
    d.text((card[0] + 118, card[1] + 22), "Tiger League Tee", font=F(IN8, 30), fill=INK)
    d.text((card[0] + 118, card[1] + 62), "$39.99  •  2 colors", font=F(IN4, 26), fill=(90, 90, 90))
    d.rounded_rectangle((card[2] - 190, card[1] + 26, card[2] - 20, card[3] - 26), radius=29, fill=RED)
    d.text((card[2] - 105, (card[1] + card[3]) // 2), "Shop", font=F(IN8, 30), fill=WHITE, anchor="mm")
    save_as(c, "31_vertical_video_both_colors.jpg")


# ---------------------------------------------------------------- ad 32
def ad32_brand_sms():
    c = Image.new("RGBA", (W, H), WHITE + (255,))
    d = ImageDraw.Draw(c)
    d.rectangle((0, 0, W, 196), fill=(247, 247, 247))
    d.line([(0, 196), (W, 196)], fill=(222, 222, 222), width=2)
    d.text((34, 64), "‹", font=F(IN4, 80), fill=IOS_BLUE)
    avatar(d, (W // 2 - 48, 30), 48)
    d.text((W // 2, 140), "404 CULTURE ›", font=F(IN6, 28), fill=INK, anchor="ma")
    d.text((W // 2, 212), "Text Message • Today", font=F(IN4, 24), fill=GREY_TXT, anchor="ma")

    y = 256
    f = F(IN4, 44)

    def bubble(text, y, bg=BUBBLE, fg=INK, highlight=None):
        tw = rich_len(text, f)
        bx0, bx1 = 40, 40 + tw + 56
        bh = 94
        d.rounded_rectangle((bx0, y, bx1, y + bh), radius=40, fill=bg)
        if highlight:
            pre = text.split(highlight)[0]
            hx = bx0 + 28 + f.getlength(pre)
            d.rounded_rectangle((hx - 6, y + 16, hx + F(IN8, 44).getlength(highlight) + 6, y + bh - 16), radius=8, fill=YELLOW)
            d.text((bx0 + 28, y + 20), pre, font=f, fill=fg)
            d.text((hx, y + 20), highlight, font=F(IN8, 44), fill=BLACK)
        else:
            rich(c, (bx0 + 28, y + 20), text, f, fg)
        return y + bh + 14

    y = bubble("yo 👋 it's 404 CULTURE", y)
    y = bubble("the tiger tees come in 2 colors 🐯", y)
    # photo attachment
    pw, ph = 420, 450
    for i, (n, fy) in enumerate([(2, 0.3), (4, 0.18)]):
        c.alpha_composite(rounded(cover(photo(n), pw, ph, fy), 30), (40 + i * (pw + 12), y))
    d = ImageDraw.Draw(c)
    y += ph + 14
    y = bubble(f"buy 1, get 1 15% off w/ {CODE}", y, highlight=CODE)
    # link preview card
    lw = 700
    d.rounded_rectangle((40, y, 40 + lw, y + 170), radius=30, fill=BUBBLE)
    thumb = rounded(cover(photo(1), 144, 144, 0.3), 18)
    c.alpha_composite(thumb, (54, y + 13))
    d = ImageDraw.Draw(c)
    d.text((222, y + 26), "404 CULTURE", font=F(IN4, 26), fill=GREY_TXT)
    d.text((222, y + 60), "Tiger League Tee", font=F(IN8, 36), fill=INK)
    d.text((222, y + 108), "Shop now  →", font=F(IN6, 30), fill=IOS_BLUE)
    y += 180
    d.text((60, y + 2), "Delivered", font=F(IN4, 22), fill=GREY_TXT)
    # input bar
    d.rounded_rectangle((110, H - 100, W - 40, H - 36), radius=32, outline=(210, 210, 210), width=3)
    d.text((140, H - 68), "Text Message", font=F(IN4, 30), fill=(190, 190, 190), anchor="lm")
    d.ellipse((30, H - 96, 86, H - 40), fill=(232, 232, 232))
    d.text((58, H - 68), "+", font=F(IN4, 40), fill=GREY_TXT, anchor="mm")
    save_as(c, "32_brand_text_message.jpg")


# ---------------------------------------------------------------- ad 33
def ad33_story():
    SW, SH = 1080, 1920
    src = photo(2)
    c = cover(src, SW, SH, 0.0).filter(ImageFilter.GaussianBlur(40)).convert("RGBA")
    c.alpha_composite(Image.new("RGBA", (SW, SH), (0, 0, 0, 60)))
    fg = cover(src, SW, SH - 300, 0.0).convert("RGBA")
    fm = Image.new("L", fg.size, 255)
    fmd = ImageDraw.Draw(fm)
    for yy in range(120):
        fmd.line([(0, yy), (SW, yy)], fill=int(255 * yy / 120))
    c.paste(fg, (0, 300), fm)
    vgrad(c, 0, 300, 120, 0)
    vgrad(c, 1500, SH, 0, 160)
    d = ImageDraw.Draw(c)
    seg = (SW - 40 - 2 * 8) / 3
    for i in range(3):
        x = 20 + i * (seg + 8)
        d.rounded_rectangle((x, 24, x + seg, 30), radius=3, fill=(255, 255, 255, 255 if i == 0 else 110))
    avatar(d, (30, 52), 34)
    d.text((112, 70), "404culture", font=F(IN6, 32), fill=WHITE)
    d.text((112 + F(IN6, 32).getlength("404culture") + 16, 72), "now", font=F(IN4, 30), fill=(225, 225, 225))

    def sticker(text, font, bg, fg, deg, xy):
        tw = font.getlength(text)
        asc, desc = font.getmetrics()
        im = Image.new("RGBA", (round(tw) + 50, asc + desc + 26), (0, 0, 0, 0))
        ImageDraw.Draw(im).rounded_rectangle((0, 0, im.width - 1, im.height - 1), radius=18, fill=bg)
        ImageDraw.Draw(im).text((25, 10), text, font=font, fill=fg)
        im = rot(im, deg)
        c.alpha_composite(im, (round(xy[0] - im.width / 2), xy[1]))
    sticker("BUY 1, GET 1", F(IN8, 92), YELLOW, BLACK, 4, (SW // 2, 190))
    sticker("15% OFF", F(IN8, 150), RED, WHITE, -3, (SW // 2, 330))

    # poll sticker (unvoted)
    px0, py0, pw = 170, 1180, 740
    d = ImageDraw.Draw(c)
    d.rounded_rectangle((px0, py0, px0 + pw, py0 + 300), radius=30, fill=WHITE)
    tx = px0 + (pw - rich_len("which tiger? 🐯", F(IN8, 46))) / 2
    rich(c, (tx, py0 + 30), "which tiger? 🐯", F(IN8, 46), INK)
    d = ImageDraw.Draw(c)
    for i, (lab, col) in enumerate([("RED", RED), ("BLUE", (60, 150, 220))]):
        bx = px0 + 30 + i * ((pw - 80) // 2 + 20)
        bw = (pw - 80) // 2
        d.rounded_rectangle((bx, py0 + 130, bx + bw, py0 + 260), radius=20, fill=(242, 242, 242))
        d.text((bx + bw // 2, py0 + 195), lab, font=F(IN8, 52), fill=col, anchor="mm")

    # link sticker
    lt = f"SHOP  •  CODE {CODE}"
    lf = F(IN8, 40)
    lw = lf.getlength(lt) + 150
    lx = (SW - lw) / 2
    d.rounded_rectangle((lx, 1540, lx + lw, 1640), radius=24, fill=WHITE)
    e = emoji("🔗", 44)
    c.alpha_composite(e, (round(lx + 36), 1568))
    d = ImageDraw.Draw(c)
    d.text((lx + 100, 1590), lt, font=lf, fill=IOS_BLUE, anchor="lm")
    d.text((SW // 2, 1668), "$39.99 tees  •  2nd one 15% off", font=F(IN6, 34), fill=WHITE, anchor="ma")
    # reply bar
    d.rounded_rectangle((30, SH - 130, SW - 190, SH - 50), radius=40, outline=(255, 255, 255, 200), width=3)
    d.text((70, SH - 90), "Send message", font=F(IN4, 32), fill=(235, 235, 235), anchor="lm")
    heart(d, SW - 130, SH - 96, 60)
    share_icon(d, SW - 55, SH - 90, 52)
    save_as(c, "33_story_9x16_buy1get1.jpg")


# ---------------------------------------------------------------- ad 34
def ad34_notes_howto():
    c = Image.new("RGBA", (W, H), (252, 250, 244, 255))
    d = ImageDraw.Draw(c)
    gold = (214, 160, 0)
    d.text((40, 44), "‹ Notes", font=F(IN4, 38), fill=gold)
    d.text((W - 40, 44), "Done", font=F(IN6, 36), fill=gold, anchor="ra")
    rich(c, (50, 124), "how to get 2 for less 🧠", F(IN8, 64), INK)
    d = ImageDraw.Draw(c)
    steps = ["add a tiger tee ($39.99)", "add the other color — or the thermal", f"use code {CODE} at checkout",
             "2nd item = 15% off ✅"]
    f = F(IN4, 42)
    y = 246
    for i, s in enumerate(steps, 1):
        d.text((56, y), f"{i}.", font=F(IN6, 42), fill=INK)
        if CODE in s:
            pre = s.split(CODE)[0]
            x = 110 + f.getlength(pre)
            d.rectangle((x - 6, y + 4, x + F(IN8, 42).getlength(CODE) + 6, y + 52), fill=(255, 226, 90))
            d.text((110, y), pre, font=f, fill=INK)
            d.text((x, y), CODE, font=F(IN8, 42), fill=INK)
            d.text((x + F(IN8, 42).getlength(CODE) + 8, y), s.split(CODE)[1], font=f, fill=INK)
        else:
            rich(c, (110, y), s, f, INK)
            d = ImageDraw.Draw(c)
        y += 72
    pw, ph, py = 314, 470, 560
    for i, (n, fy) in enumerate([(2, 0.28), (4, 0.15), (3, 0.3)]):
        c.alpha_composite(rounded(cover(photo(n), pw, ph, fy), 22), (50 + i * (pw + 18), py))
    d = ImageDraw.Draw(c)
    for i, lab in enumerate(["red $39.99", "blue $39.99", "thermal $52.99"]):
        x = 50 + i * (pw + 18) + pw / 2
        tw = F(IN6, 26).getlength(lab) + 30
        d.rounded_rectangle((x - tw / 2, py + ph - 60, x + tw / 2, py + ph - 16), radius=22, fill=(0, 0, 0, 180))
        d.text((x, py + ph - 38), lab, font=F(IN6, 26), fill=WHITE, anchor="mm")
    rich(c, (50, 1070), "that's it. go 👇", F(IN4, 42), INK)
    d = ImageDraw.Draw(c)
    d.rounded_rectangle((50, 1170, W - 50, 1290), radius=26, fill=BLACK)
    d.text((W // 2, 1230), f"SHOP NOW  •  CODE {CODE}", font=F(IN8, 40), fill=YELLOW, anchor="mm")
    save_as(c, "34_notes_how_to_get_2.jpg")


# ---------------------------------------------------------------- ad 35
def marker_text(c, xy, s, size, fill=WHITE, deg=0, anchor="la"):
    f = F(MARKER, size)
    bb = ImageDraw.Draw(c).textbbox((0, 0), s, font=f, stroke_width=6)
    im = Image.new("RGBA", (bb[2] - bb[0] + 20, bb[3] - bb[1] + 20), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((10 - bb[0], 10 - bb[1]), s, font=f, fill=fill, stroke_width=6, stroke_fill=BLACK)
    im = rot(im, deg)
    x, y = xy
    if anchor == "ra":
        x -= im.width
    elif anchor == "ma":
        x -= im.width // 2
    c.alpha_composite(im, (round(x), round(y)))


def marker_arrow(d, pts, color=WHITE, width=7):
    import math
    d.line(pts, fill=BLACK, width=width + 6, joint="curve")
    d.line(pts, fill=color, width=width, joint="curve")
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    a = math.atan2(y2 - y1, x2 - x1)
    for s in (2.5, -2.5):
        e = (x2 + 34 * math.cos(a + s), y2 + 34 * math.sin(a + s))
        d.line([(x2, y2), e], fill=BLACK, width=width + 6)
        d.line([(x2, y2), e], fill=color, width=width)


def ad35_creator_annotated():
    c = cover(photo(3), W, H, 0.35).convert("RGBA")
    vgrad(c, 0, 300, 90, 0)
    vgrad(c, 1000, H, 0, 170)
    d = ImageDraw.Draw(c)
    marker_text(c, (W // 2, 40), "this thermal is crazy", 76, WHITE, -2, "ma")
    d = ImageDraw.Draw(c)
    marker_text(c, (20, 520), "all-over\ngraphic", 50, YELLOW, 6)
    d = ImageDraw.Draw(c)
    marker_arrow(d, [(150, 680), (230, 720), (300, 700)])
    marker_text(c, (W - 20, 300), "sleeve print\ntoo", 50, YELLOW, -6, "ra")
    d = ImageDraw.Draw(c)
    marker_arrow(d, [(930, 440), (960, 520), (930, 590)])
    marker_text(c, (W - 30, 900), "waffle knit", 48, YELLOW, -4, "ra")
    d = ImageDraw.Draw(c)
    marker_arrow(d, [(860, 970), (800, 1000), (730, 990)])
    # bottom caption stickers
    f = F(IN8, 44)
    y = 1118
    for line, bg, fg in [("$52.99  •  pair it with a tiger tee", WHITE, INK), (f"buy 1, get 1 15% off: {CODE}", YELLOW, BLACK)]:
        tw = f.getlength(line)
        x = (W - tw) / 2
        d.rounded_rectangle((x - 24, y - 10, x + tw + 24, y + 64), radius=16, fill=bg)
        d.text((x, y), line, font=f, fill=fg)
        y += 92
    d.text((W // 2, 1310), "@404culture", font=F(IN6, 28), fill=WHITE, anchor="ma")
    save_as(c, "35_creator_thermal.jpg")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn in (ad31_vertical_video, ad32_brand_sms, ad33_story, ad34_notes_howto, ad35_creator_annotated):
        fn()
