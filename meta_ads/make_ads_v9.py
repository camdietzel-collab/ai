"""Round 9: ten more feed-native ads carrying the BO15OFF offer.

Reminder post, now-playing card, wallet coupon pass, swipe cards, carousel
cover slide, calculator meme, game inventory, word game, share-code alert
and starter-pack meme. Brand is the only voice; no invented people,
reviews or counts.
"""
import os
import random

from PIL import Image, ImageDraw, ImageFilter

from make_ads_v2 import ANTON, BLACK, BLUE, H, NAVY, OUT, PIXEL, RED, W, WHITE, YELLOW, F, cover, fit_h, garment, \
    model, photo, rot
from make_ads_v3 import radial
from make_ads_v5 import tight
from make_ads_v7 import CODE, GREY_TXT, IN4, IN6, IN8, INK, IOS_BLUE, avatar, emoji, heart, rich, rich_len, \
    rounded, save_as, vgrad
from make_ads_v8 import DISCOUNT, TEE, TWO_TEES, glass, money, red_tee_thumb, thumb_on

OFFER = "Buy 1, get 1 15% off"


def code_chip(d, xy, size=40, anchor="l", bg=YELLOW, fg=BLACK):
    f = F(IN8, size)
    tw = f.getlength(CODE)
    x, y = xy
    if anchor == "m":
        x -= (tw + 40) / 2
    d.rounded_rectangle((x, y, x + tw + 40, y + size + 28), radius=14, fill=bg)
    d.text((x + 20, y + 12), CODE, font=f, fill=fg)
    return x + tw + 40


def cta_bar(d, y, text, bg=YELLOW, fg=BLACK, size=38):
    d.rounded_rectangle((40, y, W - 40, y + 100), radius=22, fill=bg)
    d.text((W // 2, y + 50), text, font=F(IN8, size), fill=fg, anchor="mm")


def product_row(c, y, size=150, x0=None, gap=16, bg=(245, 245, 245)):
    thumbs = [red_tee_thumb(size, bg), thumb_on(garment(4), size, bg), thumb_on(garment(3), size, bg)]
    total = size * 3 + gap * 2
    x = (W - total) // 2 if x0 is None else x0
    for t in thumbs:
        c.alpha_composite(t, (x, y))
        x += size + gap


# ---------------------------------------------------------------- 41
def ad41_reminder():
    c = cover(photo(1), W, H, 0.3).filter(ImageFilter.GaussianBlur(28)).convert("RGBA")
    c.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 90)))
    d = ImageDraw.Draw(c)
    card = (70, 150, W - 70, 1120)
    d.rounded_rectangle(card, radius=40, fill=WHITE)
    avatar(d, (120, 200), 34)
    d.text((200, 212), "404culture", font=F(IN8, 32), fill=INK)
    f = F(IN8, 84)
    y = 330
    for line, col in [("reminder:", GREY_TXT), ("buy 1, get 1", INK), ("15% off", RED), ("is live.", INK)]:
        d.text((120, y), line, font=f, fill=col)
        y += 104
    d.text((120, y + 20), "use code", font=F(IN6, 40), fill=INK)
    code_chip(d, (320, y + 8), 44)
    product_row(c, y + 120, 170, x0=120, gap=20)
    d = ImageDraw.Draw(c)
    cta_bar(d, 1170, "SHOP NOW  →")
    d.text((W // 2, 1300), "tees $39.99  •  thermal $52.99", font=F(IN6, 30), fill=WHITE, anchor="mm")
    save_as(c, "41_reminder_post.jpg")


# ---------------------------------------------------------------- 42
def ad42_now_playing():
    c = Image.new("RGBA", (W, H))
    top, bot = (170, 20, 30), (24, 6, 8)
    d = ImageDraw.Draw(c)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(top[k] + (bot[k] - top[k]) * t) for k in range(3)))
    d.text((W // 2, 50), "PLAYING FROM", font=F(IN6, 24), fill=(235, 200, 200), anchor="ma")
    d.text((W // 2, 82), "404 CULTURE", font=F(IN8, 30), fill=WHITE, anchor="ma")
    art = rounded(cover(photo(5), 780, 780, 0.15), 24)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((150, 170, 930, 950), radius=24, fill=(0, 0, 0, 150))
    c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(30)))
    c.alpha_composite(art, (150, 150))
    d = ImageDraw.Draw(c)
    d.text((150, 966), "Tiger League", font=F(IN8, 58), fill=WHITE)
    d.text((150, 1036), "404 CULTURE  •  $39.99", font=F(IN4, 34), fill=(230, 190, 190))
    heart(d, 900, 1010, 64, fill=YELLOW)
    # progress
    d.rounded_rectangle((150, 1100, 930, 1108), radius=4, fill=(255, 255, 255, 90))
    d.rounded_rectangle((150, 1100, 330, 1108), radius=4, fill=WHITE)
    d.ellipse((318, 1092, 342, 1116), fill=WHITE)
    d.text((150, 1122), "0:40", font=F(IN4, 24), fill=(230, 190, 190))
    d.text((930, 1122), "-4:04", font=F(IN4, 24), fill=(230, 190, 190), anchor="ra")
    # controls
    cx, cy = W // 2, 1200
    d.ellipse((cx - 50, cy - 50, cx + 50, cy + 50), fill=WHITE)
    d.polygon([(cx - 14, cy - 24), (cx - 14, cy + 24), (cx + 24, cy)], fill=BLACK)
    for s in (-1, 1):
        bx = cx + s * 190
        d.polygon([(bx - s * 18, cy - 20), (bx - s * 18, cy + 20), (bx + s * 14, cy)], fill=WHITE)
        d.rectangle((bx + s * 14 - 3, cy - 20, bx + s * 14 + 3, cy + 20), fill=WHITE)
    # offer pill
    txt = f"{OFFER}  •  "
    f = F(IN6, 32)
    tw = f.getlength(txt) + F(IN8, 32).getlength(CODE) + 60
    x = (W - tw) / 2
    d.rounded_rectangle((x, 1268, x + tw, 1326), radius=29, fill=(0, 0, 0, 120))
    d.text((x + 30, 1297), txt, font=f, fill=WHITE, anchor="lm")
    d.text((x + 30 + f.getlength(txt), 1297), CODE, font=F(IN8, 32), fill=YELLOW, anchor="lm")
    save_as(c, "42_now_playing.jpg")


# ---------------------------------------------------------------- 43
def ad43_wallet_pass():
    c = Image.new("RGBA", (W, H), (12, 12, 14, 255))
    d = ImageDraw.Draw(c)
    rich(c, (60, 50), "your code is ready 👇", F(IN8, 56), WHITE)
    d = ImageDraw.Draw(c)
    p = (70, 160, W - 70, 1150)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle(p, radius=34, fill=(200, 20, 30, 120))
    c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(40)))
    d.rounded_rectangle(p, radius=34, fill=(196, 18, 30))
    avatar(d, (110, 196), 34)
    d.text((196, 208), "404 CULTURE", font=F(IN8, 34), fill=WHITE)
    d.text((p[2] - 40, 196), "OFFER", font=F(IN6, 22), fill=(255, 200, 200), anchor="ra")
    d.text((p[2] - 40, 224), "Active", font=F(IN8, 30), fill=WHITE, anchor="ra")
    # strip image
    strip = Image.new("RGB", (p[2] - p[0], 300))
    strip.paste(cover(photo(2), strip.width // 2, 300, 0.3), (0, 0))
    strip.paste(cover(photo(4), strip.width - strip.width // 2, 300, 0.15), (strip.width // 2, 0))
    c.paste(strip, (p[0], 290))
    d = ImageDraw.Draw(c)
    d.text((110, 620), "BUY 1, GET 1", font=F(IN8, 80), fill=WHITE)
    d.text((110, 710), "15% OFF", font=F(IN8, 120), fill=YELLOW)
    cols = [("CODE", CODE), ("TEES", "$39.99"), ("THERMAL", "$52.99")]
    for i, (k, v) in enumerate(cols):
        x = 110 + i * 290
        d.text((x, 870), k, font=F(IN6, 22), fill=(255, 200, 200))
        d.text((x, 900), v, font=F(IN8, 40), fill=WHITE)
    d.rounded_rectangle((110, 990, p[2] - 40, 1110), radius=20, fill=WHITE)
    d.text(((110 + p[2] - 40) // 2, 1030), CODE, font=F(IN8, 52), fill=INK, anchor="mm")
    d.text(((110 + p[2] - 40) // 2, 1082), "enter at checkout", font=F(IN4, 24), fill=GREY_TXT, anchor="mm")
    cta_bar(d, 1200, "SHOP NOW  →")
    save_as(c, "43_wallet_coupon_pass.jpg")


# ---------------------------------------------------------------- 44
def ad44_swipe():
    c = radial((W, H), (W / 2, 300), 1000, (255, 244, 240), (246, 226, 222))
    d = ImageDraw.Draw(c)
    d.text((W // 2, 40), "404 CULTURE", font=F(ANTON, 50), fill=RED, anchor="ma")
    cw, ch = 880, 960
    back = rounded(cover(photo(4), cw, ch, 0.12), 32)
    back = rot(back, -5)
    c.alpha_composite(back, ((W - back.width) // 2 - 20, 150))
    front = cover(photo(2), cw, ch, 0.28).convert("RGBA")
    vgrad(front, ch - 360, ch, 0, 220)
    fd = ImageDraw.Draw(front)
    fd.text((40, ch - 250), "Tiger League Tee", font=F(IN8, 58), fill=WHITE)
    fd.text((40, ch - 176), "$39.99  •  also in blue", font=F(IN6, 34), fill=WHITE)
    x = 40
    for chip in ["boxy fit", "layered trim", "vintage print"]:
        tw = F(IN6, 28).getlength(chip) + 36
        fd.rounded_rectangle((x, ch - 110, x + tw, ch - 60), radius=25, fill=(255, 255, 255, 255))
        fd.text((x + tw / 2, ch - 85), chip, font=F(IN6, 28), fill=INK, anchor="mm")
        x += tw + 14
    front = rounded(front, 32)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle(((W - cw) // 2, 150, (W + cw) // 2, 150 + ch), radius=32, fill=(0, 0, 0, 90))
    c.alpha_composite(sh.filter(ImageFilter.GaussianBlur(24)), (0, 14))
    c.alpha_composite(front, ((W - cw) // 2, 140))
    d = ImageDraw.Draw(c)
    by = 1180
    for cx, r, kind in [(W // 2 - 170, 62, "x"), (W // 2, 44, "star"), (W // 2 + 170, 62, "heart")]:
        d.ellipse((cx - r, by - r, cx + r, by + r), fill=WHITE, outline=(230, 225, 225), width=3)
        if kind == "x":
            d.line([(cx - 22, by - 22), (cx + 22, by + 22)], fill=(170, 170, 170), width=9)
            d.line([(cx + 22, by - 22), (cx - 22, by + 22)], fill=(170, 170, 170), width=9)
        elif kind == "heart":
            heart(d, cx, by - 4, 64, fill=RED)
        else:
            d.polygon([(cx, by - 20), (cx + 6, by - 6), (cx + 20, by - 6), (cx + 9, by + 4), (cx + 13, by + 19),
                       (cx, by + 10), (cx - 13, by + 19), (cx - 9, by + 4), (cx - 20, by - 6), (cx - 6, by - 6)], fill=IOS_BLUE)
    txt = "swipe right = "
    f = F(IN6, 32)
    tw = f.getlength(txt) + F(IN8, 32).getlength(CODE) + 40 + f.getlength("  (buy 1, get 1 15% off)")
    x = (W - tw) / 2
    d.text((x, 1290), txt, font=f, fill=INK, anchor="lm")
    x = code_chip(d, (x + f.getlength(txt), 1268), 28)
    d.text((x + 8, 1290), " (buy 1, get 1 15% off)", font=f, fill=INK, anchor="lm")
    save_as(c, "44_swipe_right.jpg")


# ---------------------------------------------------------------- 45
def ad45_carousel_cover():
    c = Image.new("RGBA", (W, H), (244, 239, 228, 255))
    d = ImageDraw.Draw(c)
    ph = rounded(cover(photo(2), 520, 1000, 0.3), 30)
    c.alpha_composite(ph, (W - 520 - 40, 150))
    d = ImageDraw.Draw(c)
    d.text((50, 50), "404 CULTURE", font=F(IN8, 30), fill=INK)
    d.rounded_rectangle((W - 140, 44, W - 40, 92), radius=24, fill=(0, 0, 0, 200))
    d.text((W - 90, 68), "1/4", font=F(IN6, 26), fill=WHITE, anchor="mm")
    f = F(ANTON, 128)
    y = 170
    for line, col in [("3 WAYS", INK), ("TO WEAR", INK), ("THE", INK), ("TIGER", RED), ("TEE", RED)]:
        d.text((50, y), line, font=f, fill=col)
        y += 150
    d.text((52, y + 20), "a quick styling guide", font=F(IN4, 34), fill=GREY_TXT)
    d.rounded_rectangle((W - 290, 1080, W - 70, 1140), radius=30, fill=WHITE)
    d.text((W - 180, 1110), "swipe  →", font=F(IN8, 30), fill=INK, anchor="mm")
    d.rectangle((0, 1190, W, H), fill=INK)
    d.text((50, 1270), OFFER, font=F(IN8, 40), fill=WHITE, anchor="lm")
    code_chip(d, (W - 50 - F(IN8, 38).getlength(CODE) - 40, 1236), 38)
    save_as(c, "45_carousel_cover_3_ways.jpg")


# ---------------------------------------------------------------- 46
def ad46_calculator():
    c = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    d = ImageDraw.Draw(c)
    cap = "me doing the math on BO15OFF"
    f = F(IN8, 44)
    tw = f.getlength(cap)
    d.rounded_rectangle((40, 40, 40 + tw + 44, 118), radius=14, fill=WHITE)
    d.text((62, 52), cap, font=f, fill=INK)
    c.alpha_composite(red_tee_thumb(110, (40, 40, 40)), (W - 270, 30))
    c.alpha_composite(thumb_on(garment(4), 110, (40, 40, 40)), (W - 150, 30))
    d = ImageDraw.Draw(c)
    d.text((W - 60, 250), f"{TEE} + {TEE} − {DISCOUNT:.2f}", font=F(IN4, 52), fill=(160, 160, 160), anchor="ra")
    d.text((W - 60, 310), f"{TWO_TEES:.2f}", font=F(IN4, 220), fill=WHITE, anchor="ra")
    d.text((W - 60, 560), "2 tiger tees, 2nd one 15% off", font=F(IN6, 32), fill=YELLOW, anchor="ra")
    keys = [["AC", "+/−", "%", "÷"], ["7", "8", "9", "×"], ["4", "5", "6", "−"], ["1", "2", "3", "+"], ["0", "", ".", "="]]
    ks, gap, top = 180, 40, 630
    x0 = (W - (4 * ks + 3 * gap)) // 2
    for r, row in enumerate(keys):
        for k, lab in enumerate(row):
            if r == 4 and k == 1:
                continue
            x, y = x0 + k * (ks + gap), top + r * (ks * 0.6 + 10)
            h = ks * 0.6
            w = ks * 2 + gap if (r == 4 and k == 0) else ks
            col = (255, 159, 10) if k == 3 else ((165, 165, 165) if r == 0 else (51, 51, 51))
            if lab == "=":
                col = YELLOW
            d.rounded_rectangle((x, y, x + w, y + h), radius=h / 2, fill=col)
            d.text((x + (ks / 2 if w == ks else 64), y + h / 2), lab, font=F(IN6, 54),
                   fill=BLACK if r == 0 or lab == "=" else WHITE, anchor="mm")
    d.rounded_rectangle((40, H - 110, W - 40, H - 30), radius=20, fill=WHITE)
    d.text((W // 2, H - 70), f"SHOP BOTH  •  CODE {CODE}", font=F(IN8, 34), fill=INK, anchor="mm")
    save_as(c, "46_calculator_math.jpg")


# ---------------------------------------------------------------- 47
def ad47_inventory():
    c = Image.new("RGBA", (W, H), (14, 16, 34, 255))
    d = ImageDraw.Draw(c)
    for x in range(0, W, 40):
        d.line([(x, 0), (x, H)], fill=(24, 28, 56), width=2)
    for y in range(0, H, 40):
        d.line([(0, y), (W, y)], fill=(24, 28, 56), width=2)
    d.text((50, 30), "INVENTORY", font=F(PIXEL, 110), fill=YELLOW)
    d.text((W - 50, 64), "404 CULTURE", font=F(PIXEL, 50), fill=(150, 160, 220), anchor="ra")
    # character
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((60, 1000, 480, 1080), fill=(255, 196, 0, 120))
    c.alpha_composite(glow.filter(ImageFilter.GaussianBlur(24)))
    m = fit_h(tight(model(2)), 860)
    c.alpha_composite(m, (270 - m.width // 2, 1040 - m.height + 20))
    d = ImageDraw.Draw(c)
    d.text((270, 1090), "LVL 99  •  FIT: MAXED", font=F(PIXEL, 40), fill=WHITE, anchor="ma")
    # item slots
    items = [(red_tee_thumb(170, (34, 30, 60)), "TIGER TEE (RED)", "LEGENDARY", (255, 170, 0), "$39.99"),
             (thumb_on(garment(4), 170, (34, 30, 60)), "TIGER TEE (BLUE)", "LEGENDARY", (255, 170, 0), "$39.99"),
             (thumb_on(garment(3), 170, (34, 30, 60)), "CULTURE THERMAL", "EPIC", (180, 110, 255), "$52.99")]
    y = 190
    for img, name, rarity, col, price in items:
        box = (540, y, W - 40, y + 250)
        d.rectangle(box, fill=(26, 28, 58), outline=col, width=5)
        c.alpha_composite(img, (560, y + 40))
        d = ImageDraw.Draw(c)
        d.text((750, y + 34), name, font=F(PIXEL, 44), fill=WHITE)
        d.text((750, y + 84), rarity, font=F(PIXEL, 40), fill=col)
        d.text((750, y + 132), "DRIP", font=F(PIXEL, 34), fill=(170, 175, 220))
        for k in range(8):
            d.rectangle((840 + k * 24, y + 140, 858 + k * 24, y + 164), fill=col)
        d.text((750, y + 180), price, font=F(PIXEL, 48), fill=YELLOW)
        y += 280
    d.rectangle((40, 1150, W - 40, 1310), fill=(26, 28, 58), outline=YELLOW, width=5)
    d.text((70, 1170), "> BUY 1, GET 1 15% OFF", font=F(PIXEL, 60), fill=WHITE)
    d.text((70, 1236), f"> ENTER CODE: {CODE}", font=F(PIXEL, 60), fill=YELLOW)
    d.rectangle((W - 290, 1190, W - 70, 1270), fill=YELLOW)
    d.text((W - 180, 1230), "EQUIP", font=F(PIXEL, 60), fill=BLACK, anchor="mm")
    save_as(c, "47_game_inventory.jpg")


# ---------------------------------------------------------------- 48
def ad48_word_game():
    c = Image.new("RGBA", (W, H), WHITE + (255,))
    d = ImageDraw.Draw(c)
    rich(c, (W // 2 - rich_len("today's word 🐯", F(IN8, 56)) / 2, 40), "today's word 🐯", F(IN8, 56), INK)
    d = ImageDraw.Draw(c)
    G, Y, X = (106, 170, 100), (201, 180, 88), (120, 124, 126)
    target = "TIGER"

    def score(guess):
        res = [X] * 5
        for i, ch in enumerate(guess):
            if target[i] == ch:
                res[i] = G
            elif ch in target:
                res[i] = Y
        return res
    guesses = ["SHIRT", "TRIBE", "TIGER"]
    ts, gap = 120, 12
    x0 = (W - (5 * ts + 4 * gap)) // 2
    for r in range(5):
        for k in range(5):
            x, y = x0 + k * (ts + gap), 150 + r * (ts + gap)
            if r < len(guesses):
                col = score(guesses[r])[k]
                d.rectangle((x, y, x + ts, y + ts), fill=col)
                d.text((x + ts / 2, y + ts / 2), guesses[r][k], font=F(IN8, 64), fill=WHITE, anchor="mm")
            else:
                d.rectangle((x, y, x + ts, y + ts), outline=(212, 214, 218), width=4)
    y = 150 + 5 * (ts + gap) + 20
    d.text((W // 2, y), "3/6 — and the prize is a code:", font=F(IN6, 40), fill=INK, anchor="ma")
    code_chip(d, (W // 2, y + 64), 52, anchor="m")
    d.text((W // 2, y + 170), f"{OFFER} on the tiger tees + thermal", font=F(IN4, 32), fill=GREY_TXT, anchor="ma")
    product_row(c, y + 230, 150)
    d = ImageDraw.Draw(c)
    cta_bar(d, H - 130, "CLAIM IT  →", bg=(106, 170, 100), fg=WHITE)
    save_as(c, "48_word_game_tiger.jpg")


# ---------------------------------------------------------------- 49
def ad49_share_alert():
    c = cover(photo(4), W, H, 0.1).convert("RGBA")
    c = c.filter(ImageFilter.GaussianBlur(6))
    c.alpha_composite(Image.new("RGBA", (W, H), (0, 0, 0, 110)))
    box = (110, 250, W - 110, 1110)
    glass(c, box, r=44, tint=(250, 250, 250, 225))
    d = ImageDraw.Draw(c)
    tile = Image.new("RGBA", (140, 140), (0, 0, 0, 0))
    avatar(ImageDraw.Draw(tile), (0, 0), 70)
    c.alpha_composite(rounded(tile, 32), (W // 2 - 70, 300))
    d = ImageDraw.Draw(c)
    d.text((W // 2, 470), "“404 CULTURE” would like", font=F(IN6, 42), fill=INK, anchor="ma")
    d.text((W // 2, 522), "to share a code with you", font=F(IN6, 42), fill=INK, anchor="ma")
    code_chip(d, (W // 2, 600), 56, anchor="m")
    d.text((W // 2, 712), OFFER, font=F(IN4, 36), fill=(70, 70, 70), anchor="ma")
    product_row(c, 780, 150, bg=(236, 236, 236))
    d = ImageDraw.Draw(c)
    d.line([(box[0], 976), (box[2], 976)], fill=(205, 205, 210), width=2)
    d.line([(W // 2, 976), (W // 2, box[3])], fill=(205, 205, 210), width=2)
    d.text(((box[0] + W // 2) // 2, 1043), "Decline", font=F(IN4, 42), fill=IOS_BLUE, anchor="mm")
    d.text(((W // 2 + box[2]) // 2, 1043), "Accept", font=F(IN8, 42), fill=IOS_BLUE, anchor="mm")
    # tap on Accept
    tx, ty = (W // 2 + box[2]) // 2 + 130, 1075
    for r, a in [(60, 70), (40, 120)]:
        ring = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(ring).ellipse((tx - r, ty - r, tx + r, ty + r), outline=(255, 255, 255, a), width=6)
        c.alpha_composite(ring)
    d = ImageDraw.Draw(c)
    d.ellipse((tx - 22, ty - 22, tx + 22, ty + 22), fill=(255, 255, 255, 210))
    d.text((W // 2, 1190), "tees $39.99  •  thermal $52.99", font=F(IN6, 34), fill=WHITE, anchor="ma")
    save_as(c, "49_share_code_alert.jpg")


# ---------------------------------------------------------------- 50
def ad50_starter_pack():
    c = Image.new("RGBA", (W, H), WHITE + (255,))
    d = ImageDraw.Draw(c)
    title = F("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 78)
    d.text((W // 2, 40), "the 404 starter pack", font=title, fill=BLACK, anchor="ma")
    lab = F("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 32)
    p5, p1 = photo(5), photo(1)
    jeans = p5.crop((420, 720, 860, 1330))
    boots = photo(2).crop((440, 1320, 880, 1500))
    chain = p5.crop((0, 40, 420, 360))
    items = [
        (red_tee_thumb(330, (255, 255, 255)), (40, 170), "the red tiger tee"),
        (thumb_on(garment(4), 330, (255, 255, 255)), (380, 150), "the blue one too"),
        (thumb_on(garment(3), 330, (255, 255, 255)), (720, 180), "the culture thermal"),
        (jeans.resize((240, round(jeans.height * 240 / jeans.width))).convert("RGBA"), (70, 610), "baggy denim"),
        (chain.resize((230, round(chain.height * 230 / chain.width))).convert("RGBA"), (420, 640), "a brick wall to pose on"),
        (boots.resize((300, round(boots.height * 300 / boots.width))).convert("RGBA"), (720, 700), "tan boots"),
    ]
    for img, (x, y), text in items:
        c.alpha_composite(img, (x, y))
        d = ImageDraw.Draw(c)
        d.text((x + img.width // 2, y + img.height + 8), text, font=lab, fill=BLACK, anchor="ma")
    # the code as a ticket
    tk = Image.new("RGBA", (440, 150), (0, 0, 0, 0))
    td = ImageDraw.Draw(tk)
    td.rounded_rectangle((0, 0, 439, 149), radius=16, fill=YELLOW, outline=BLACK, width=4)
    td.ellipse((-30, 45, 30, 105), fill=WHITE, outline=BLACK, width=4)
    td.ellipse((410, 45, 470, 105), fill=WHITE, outline=BLACK, width=4)
    td.text((220, 50), CODE, font=F(IN8, 64), fill=BLACK, anchor="mm")
    td.text((220, 112), "buy 1, get 1 15% off", font=F(IN6, 26), fill=BLACK, anchor="mm")
    tk = rot(tk, -4)
    c.alpha_composite(tk, (560, 1000))
    d = ImageDraw.Draw(c)
    d.text((780, 1180), "the code", font=lab, fill=BLACK, anchor="ma")
    d.text((60, 1050), "tees $39.99", font=F(IN8, 44), fill=BLACK)
    d.text((60, 1108), "thermal $52.99", font=F(IN8, 44), fill=BLACK)
    cta_bar(d, H - 124, "GET THE PACK  →", bg=BLACK, fg=YELLOW)
    save_as(c, "50_starter_pack.jpg")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn in (ad41_reminder, ad42_now_playing, ad43_wallet_pass, ad44_swipe, ad45_carousel_cover,
               ad46_calculator, ad47_inventory, ad48_word_game, ad49_share_alert, ad50_starter_pack):
        fn()
