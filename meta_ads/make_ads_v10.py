"""Round 10: ten deal-forward, feed-native ads for BO15OFF.

Every ad makes the saving concrete (2 tees $73.98 vs $79.98, $36.99 a tee)
and keeps one CTA. Totals are only shown where the maths is unambiguous
(two tees); tee + thermal combos say "15% off one" instead of a total.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFilter

from make_ads_v2 import ANTON, BLACK, BLUE, H, MARKER, NAVY, OUT, RED, W, WHITE, YELLOW, F, cover, fit_h, fit_w, \
    garment, model, photo, rot
from make_ads_v5 import red_tee_box, tight
from make_ads_v7 import EMOJI, CODE, GREY_TXT, IN4, IN6, IN8, INK, avatar, emoji, rich, rich_len, rounded, \
    save_as, vgrad
from make_ads_v8 import DISCOUNT, TEE, THERMAL, TWO_TEES, money, red_tee_thumb, thumb_on
from make_ads_v9 import code_chip, cta_bar

EMOJI.update("🙅😎🎁💸🛍")
REG = TEE * 2                    # 79.98
EACH = round(TWO_TEES / 2, 2)    # 36.99
GREEN = (22, 150, 70)


def red_tee_crop():
    rm = tight(model(2))
    x0, y0, x1, y1 = red_tee_box(rm)
    pad = int((x1 - x0) * 0.08)
    return rm.crop((x0 - pad, y0 - pad * 2, x1 + pad, y1 + pad))


def strike(d, xy, text, font, fill, anchor="la"):
    d.text(xy, text, font=font, fill=fill, anchor=anchor)
    bb = d.textbbox(xy, text, font=font, anchor=anchor)
    my = (bb[1] + bb[3]) / 2
    d.line([(bb[0] - 4, my), (bb[2] + 4, my)], fill=fill, width=max(3, font.size // 12))


def shadowed(c, img, xy, blur=18, alpha=110, off=(10, 16)):
    a = img.getchannel("A").point(lambda v: v * alpha // 255)
    sh = Image.new("RGBA", img.size, (0, 0, 0, 255))
    sh.putalpha(a)
    pad = blur * 3
    big = Image.new("RGBA", (img.width + 2 * pad, img.height + 2 * pad), (0, 0, 0, 0))
    big.alpha_composite(sh, (pad, pad))
    c.alpha_composite(big.filter(ImageFilter.GaussianBlur(blur)), (xy[0] - pad + off[0], xy[1] - pad + off[1]))
    c.alpha_composite(img, xy)


# ---------------------------------------------------------------- 51
def ad51_price_tag():
    c = cover(photo(2), W, H, 0.3).convert("RGBA")
    d = ImageDraw.Draw(c)
    tag = Image.new("RGBA", (400, 600), (0, 0, 0, 0))
    td = ImageDraw.Draw(tag)
    td.polygon([(60, 0), (340, 0), (400, 60), (400, 600), (0, 600), (0, 60)], fill=(248, 244, 232))
    td.ellipse((182, 26, 218, 62), fill=(120, 110, 100))
    td.text((200, 96), "404 CULTURE", font=F(IN8, 30), fill=INK, anchor="ma")
    td.text((200, 140), "TIGER LEAGUE TEE", font=F(IN6, 24), fill=GREY_TXT, anchor="ma")
    td.line([(40, 188), (360, 188)], fill=(210, 204, 190), width=3)
    strike(td, (200, 214), money(REG), F(IN6, 46), (150, 150, 150), anchor="ma")
    td.text((200, 290), "2 FOR", font=F(IN8, 44), fill=INK, anchor="ma")
    td.text((200, 340), money(TWO_TEES), font=F(ANTON, 116), fill=RED, anchor="ma")
    td.rounded_rectangle((60, 492, 340, 556), radius=12, fill=YELLOW)
    td.text((200, 524), CODE, font=F(IN8, 36), fill=BLACK, anchor="mm")
    td.text((200, 462), "with code", font=F(IN4, 26), fill=INK, anchor="mm")
    tag = rot(tag, 7)
    tx, ty = 40, 430
    # string from sleeve to tag hole
    hole = (tx + 205, ty + 50)
    d.line([(470, 430), (390, 380), hole], fill=(240, 236, 226), width=4, joint="curve")
    shadowed(c, tag, (tx, ty))
    d = ImageDraw.Draw(c)
    cta_bar(d, H - 136, f"SHOP 2 FOR {money(TWO_TEES)}  →")
    save_as(c, "51_price_tag_2_for.jpg")


# ---------------------------------------------------------------- 52
def ad52_per_tee():
    c = Image.new("RGBA", (W, H), (250, 248, 243, 255))
    d = ImageDraw.Draw(c)
    d.text((60, 50), f"{money(EACH)} a tee.", font=F(IN8, 104), fill=INK)
    d.text((62, 180), f"when you grab 2 with code {CODE}", font=F(IN6, 38), fill=GREY_TXT)
    r = red_tee_thumb(460, (252, 232, 226))
    b = thumb_on(garment(4), 460, (226, 240, 250))
    c.alpha_composite(r, (60, 270))
    c.alpha_composite(b, (W - 520, 270))
    d = ImageDraw.Draw(c)
    d.ellipse((W // 2 - 44, 456, W // 2 + 44, 544), fill=INK)
    d.text((W // 2, 500), "+", font=F(IN8, 60), fill=WHITE, anchor="mm")
    # comparison rows
    y = 780
    rows = [("1 tee", money(TEE), f"{money(TEE)} each", False), ("2 tees", money(TWO_TEES), f"{money(EACH)} each", True)]
    for k, total, each, best in rows:
        box = (60, y, W - 60, y + 150)
        d.rounded_rectangle(box, radius=24, fill=(226, 244, 232) if best else WHITE,
                            outline=GREEN if best else (226, 222, 214), width=4)
        d.text((100, y + 40), k, font=F(IN8, 46), fill=INK)
        d.text((100, y + 98), each, font=F(IN6, 30), fill=GREEN if best else GREY_TXT)
        d.text((W - 100, y + 75), total, font=F(IN8, 64), fill=INK, anchor="rm")
        if best:
            d.rounded_rectangle((330, y + 36, 560, y + 84), radius=24, fill=GREEN)
            d.text((445, y + 60), f"save {money(DISCOUNT)}", font=F(IN8, 28), fill=WHITE, anchor="mm")
        y += 176
    cta_bar(d, H - 136, "GET 2  →", bg=INK, fg=YELLOW)
    save_as(c, "52_per_tee_price.jpg")


# ---------------------------------------------------------------- 53
def ad53_cart_progress():
    c = Image.new("RGBA", (W, H), (242, 242, 245, 255))
    d = ImageDraw.Draw(c)
    d.text((60, 44), "1 more item =", font=F(IN8, 88), fill=INK)
    d.text((60, 150), "15% off it.", font=F(IN8, 88), fill=RED)
    card = (40, 290, W - 40, 1180)
    d.rounded_rectangle(card, radius=34, fill=WHITE)
    d.text((80, 330), "Your bag (1)", font=F(IN8, 40), fill=INK)
    # progress
    d.rounded_rectangle((80, 410, card[2] - 40, 434), radius=12, fill=(232, 232, 236))
    mid = (80 + card[2] - 40) // 2
    d.rounded_rectangle((80, 410, mid, 434), radius=12, fill=RED)
    d.ellipse((mid - 22, 400, mid + 22, 444), fill=RED)
    d.ellipse((card[2] - 62, 400, card[2] - 18, 444), fill=(232, 232, 236))
    g = emoji("🎁", 30)
    c.alpha_composite(g, (card[2] - 55, 406))
    d = ImageDraw.Draw(c)
    d.text((80, 462), f"Add 1 more to unlock 15% off with {CODE}", font=F(IN6, 32), fill=INK)
    # item in bag
    c.alpha_composite(red_tee_thumb(160, (252, 232, 226)), (80, 530))
    d = ImageDraw.Draw(c)
    d.text((270, 560), "Tiger League Tee", font=F(IN8, 36), fill=INK)
    d.text((270, 610), "Red / Gold", font=F(IN4, 30), fill=GREY_TXT)
    d.text((card[2] - 40, 560), money(TEE), font=F(IN8, 36), fill=INK, anchor="ra")
    d.line([(80, 720), (card[2] - 40, 720)], fill=(236, 236, 236), width=2)
    d.text((80, 745), "Complete it:", font=F(IN6, 32), fill=GREY_TXT)
    sugg = [(thumb_on(garment(4), 150, (226, 240, 250)), "Tiger League Tee", "Sky Blue", money(TEE)),
            (thumb_on(garment(3), 150, (246, 242, 230)), "Culture Thermal", "Cream", money(THERMAL))]
    y = 800
    for th, name, var, price in sugg:
        c.alpha_composite(th, (80, y))
        d = ImageDraw.Draw(c)
        d.text((260, y + 26), name, font=F(IN8, 34), fill=INK)
        d.text((260, y + 74), f"{var}  •  {price}", font=F(IN4, 28), fill=GREY_TXT)
        d.rounded_rectangle((card[2] - 210, y + 44, card[2] - 40, y + 108), radius=32, fill=INK)
        d.text((card[2] - 125, y + 76), "+ Add", font=F(IN8, 30), fill=WHITE, anchor="mm")
        y += 180
    cta_bar(d, H - 136, "ADD THE 2ND  →", bg=RED, fg=WHITE)
    save_as(c, "53_cart_progress_unlock.jpg")


# ---------------------------------------------------------------- 54
def ad54_faq():
    c = Image.new("RGBA", (W, H), (16, 16, 18, 255))
    d = ImageDraw.Draw(c)
    d.text((60, 50), CODE, font=F(IN8, 96), fill=YELLOW)
    d.text((60, 162), "explained in 10 seconds", font=F(IN6, 40), fill=WHITE)
    qa = [("how does it work?", "grab 2 pieces, enter the code, the 2nd one is 15% off."),
          ("what can I get?", "tiger tee in red or blue ($39.99), culture thermal ($52.99)."),
          ("what do I save?", f"2 tees = {money(TWO_TEES)} instead of {money(REG)}."),
          ("where do I use it?", "at checkout. that's it.")]
    y = 260
    for q, a in qa:
        d.rounded_rectangle((50, y, W - 50, y + 190), radius=26, fill=(34, 34, 38))
        d.text((90, y + 30), q, font=F(IN8, 40), fill=WHITE)
        words, line, lines = a.split(), "", []
        for w_ in words:
            test = (line + " " + w_).strip()
            if F(IN4, 32).getlength(test) > W - 190:
                lines.append(line)
                line = w_
            else:
                line = test
        lines.append(line)
        for i, l in enumerate(lines[:2]):
            d.text((90, y + 92 + i * 42), l, font=F(IN4, 32), fill=(200, 200, 206))
        y += 210
    cta_bar(d, H - 136, f"SHOP NOW  •  {CODE}")
    save_as(c, "54_bo15off_explained.jpg")


# ---------------------------------------------------------------- 55
def ad55_one_for_you():
    c = Image.new("RGBA", (W, H), WHITE + (255,))
    d = ImageDraw.Draw(c)
    rich(c, (50, 40), "1 for you. 1 for your day one 🎁", F(IN8, 56), INK)
    d = ImageDraw.Draw(c)
    d.text((52, 118), "the 2nd one is 15% off", font=F(IN6, 38), fill=RED)
    pw, ph, top = (W - 110) // 2, 900, 200
    for i, (n, fy, lab) in enumerate([(2, 0.28, "you"), (4, 0.12, "your day one")]):
        x = 40 + i * (pw + 30)
        c.alpha_composite(rounded(cover(photo(n), pw, ph, fy), 28), (x, top))
        d = ImageDraw.Draw(c)
        tw = F(IN8, 34).getlength(lab) + 44
        d.rounded_rectangle((x + 20, top + 20, x + 20 + tw, top + 80), radius=30, fill=WHITE)
        d.text((x + 20 + tw / 2, top + 50), lab, font=F(IN8, 34), fill=INK, anchor="mm")
        d.rounded_rectangle((x + 20, top + ph - 90, x + pw - 20, top + ph - 20), radius=20, fill=(0, 0, 0, 170))
        price = money(TEE) if i == 0 else f"{money(round(TEE - DISCOUNT, 2))}"
        d.text((x + 44, top + ph - 55), "Tiger League Tee", font=F(IN6, 28), fill=WHITE, anchor="lm")
        d.text((x + pw - 44, top + ph - 55), price, font=F(IN8, 34), fill=YELLOW if i else WHITE, anchor="rm")
    d.text((W // 2, 1140), f"both for {money(TWO_TEES)} with code", font=F(IN6, 36), fill=INK, anchor="ma")
    cta_bar(d, H - 136, f"USE {CODE}  →")
    save_as(c, "55_one_for_your_day_one.jpg")


# ---------------------------------------------------------------- 56
def ad56_meme():
    c = Image.new("RGBA", (W, H), WHITE + (255,))
    d = ImageDraw.Draw(c)
    rows = [("🙅", "buying 1 tee for $39.99", [red_tee_thumb(300, (238, 238, 238))], (250, 250, 250)),
            ("😎", f"buying 2 with {CODE} and getting the 2nd 15% off",
             [red_tee_thumb(250, (255, 244, 214)), thumb_on(garment(4), 250, (255, 244, 214))], (255, 244, 214))]
    rh = 560
    for i, (em, text, imgs, bg) in enumerate(rows):
        y = 20 + i * (rh + 10)
        d.rectangle((0, y, W, y + rh), fill=bg)
        c.alpha_composite(emoji(em, 210), (70, y + 60))
        d = ImageDraw.Draw(c)
        words, line, lines = text.split(), "", []
        for w_ in words:
            test = (line + " " + w_).strip()
            if F(IN8, 40).getlength(test) > 380:
                lines.append(line)
                line = w_
            else:
                line = test
        lines.append(line)
        for k, l in enumerate(lines):
            d.text((50, y + 320 + k * 50), l, font=F(IN8, 40), fill=INK)
        x = 470 if len(imgs) == 1 else 450
        for im in imgs:
            c.alpha_composite(im, (x + (560 - 300) // 2 if len(imgs) == 1 else x, y + (rh - im.height) // 2))
            x += im.width + 20
        d = ImageDraw.Draw(c)
    d.line([(0, 20 + rh + 5), (W, 20 + rh + 5)], fill=(200, 200, 200), width=4)
    cta_bar(d, H - 136, f"BE THE 2ND GUY  •  {CODE}", bg=INK, fg=YELLOW)
    save_as(c, "56_meme_1_vs_2.jpg")


# ---------------------------------------------------------------- 57
def ad57_shop_grid():
    c = Image.new("RGBA", (W, H), WHITE + (255,))
    d = ImageDraw.Draw(c)
    d.text((W // 2, 34), "404 CULTURE", font=F(ANTON, 60), fill=INK, anchor="ma")
    d.ellipse((50, 50, 90, 90), outline=INK, width=5)
    d.line([(84, 84), (100, 100)], fill=INK, width=6)
    d.rounded_rectangle((W - 100, 56, W - 56, 100), radius=6, outline=INK, width=5)
    d.arc((W - 90, 38, W - 66, 70), 180, 360, fill=INK, width=5)
    d.rectangle((0, 130, W, 200), fill=INK)
    d.text((W // 2, 165), f"BUY 1, GET 1 15% OFF  •  CODE {CODE}", font=F(IN8, 32), fill=YELLOW, anchor="mm")
    gw, gh, gap, top = (W - 90) // 2, 500, 30, 230
    tiles = [(cover(photo(2), gw, gh - 130, 0.3), "Tiger League Tee — Red", money(TEE)),
             (cover(photo(4), gw, gh - 130, 0.12), "Tiger League Tee — Blue", money(TEE)),
             (cover(photo(3), gw, gh - 130, 0.3), "Culture Thermal", money(THERMAL))]
    for i, (img, name, price) in enumerate(tiles):
        x = 30 + (i % 2) * (gw + gap)
        y = top + (i // 2) * (gh + gap)
        c.alpha_composite(rounded(img, 18), (x, y))
        d = ImageDraw.Draw(c)
        d.rounded_rectangle((x + 14, y + 14, x + 200, y + 60), radius=10, fill=RED)
        d.text((x + 107, y + 37), "15% OFF 2ND", font=F(IN8, 22), fill=WHITE, anchor="mm")
        d.text((x, y + gh - 116), name, font=F(IN6, 28), fill=INK)
        d.text((x, y + gh - 72), price, font=F(IN8, 34), fill=INK)
    x, y = 30 + gw + gap, top + gh + gap
    d.rounded_rectangle((x, y, x + gw, y + gh - 40), radius=18, fill=YELLOW)
    d.text((x + gw / 2, y + 90), "MIX ANY 2", font=F(ANTON, 90), fill=BLACK, anchor="ma")
    d.text((x + gw / 2, y + 210), "2nd one 15% off", font=F(IN6, 34), fill=BLACK, anchor="ma")
    d.rounded_rectangle((x + 60, y + 290, x + gw - 60, y + 370), radius=16, fill=BLACK)
    d.text((x + gw / 2, y + 330), CODE, font=F(IN8, 44), fill=YELLOW, anchor="mm")
    cta_bar(d, H - 120, "SHOP THE DROP  →", bg=INK, fg=WHITE, size=36)
    save_as(c, "57_shop_grid.jpg")


# ---------------------------------------------------------------- 58
def sticky(lines, w=440, h=440, color=(255, 230, 90), deg=-6, sizes=None):
    im = Image.new("RGBA", (w, h), color + (255,))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, w, 40), fill=tuple(max(0, v - 18) for v in color))
    y = 60
    for i, l in enumerate(lines):
        s = sizes[i] if sizes else 48
        d.text((30, y), l, font=F(MARKER, s), fill=(30, 30, 40))
        y += s + 18
    return rot(im, deg)


def ad58_sticky_note():
    c = cover(photo(3), W, H, 0.3).convert("RGBA")
    note = sticky(["don't forget:", CODE, "2nd one 15% off", "(+ a tiger tee)"], 470, 440, sizes=[40, 76, 40, 36])
    shadowed(c, note, (570, 80), blur=14, alpha=120)
    note2 = sticky(["$52.99"], 300, 150, color=(255, 150, 190), deg=5, sizes=[64])
    shadowed(c, note2, (60, 140), blur=12, alpha=110)
    d = ImageDraw.Draw(c)
    cta_bar(d, H - 136, "SHOP THE THERMAL  →", bg=INK, fg=YELLOW)
    save_as(c, "58_sticky_note_thermal.jpg")


# ---------------------------------------------------------------- 59
def ad59_menu_board():
    c = Image.new("RGBA", (W, H), (28, 32, 30, 255))
    d = ImageDraw.Draw(c)
    d.rectangle((20, 20, W - 20, H - 20), outline=(120, 90, 60), width=18)
    d.text((W // 2, 60), "404 CULTURE MENU", font=F(MARKER, 76), fill=WHITE, anchor="ma")
    d.line([(120, 170), (W - 120, 170)], fill=(200, 200, 190), width=3)
    combos = [("#1  THE DUO", "red + blue tiger tee", money(TWO_TEES), f"reg {money(REG)}",
               [red_tee_thumb(130, (40, 46, 44)), thumb_on(garment(4), 130, (40, 46, 44))]),
              ("#2  THE LAYER", "tiger tee + culture thermal", "15% OFF ONE", "",
               [red_tee_thumb(130, (40, 46, 44)), thumb_on(garment(3), 130, (40, 46, 44))]),
              ("#3  THE DOUBLE", "2 of the same tee", money(TWO_TEES), f"reg {money(REG)}",
               [thumb_on(garment(4), 130, (40, 46, 44)), thumb_on(garment(4), 130, (40, 46, 44))])]
    y = 200
    for name, desc, price, reg, thumbs in combos:
        x = 70
        for t in thumbs:
            c.alpha_composite(t, (x, y + 20))
            x += 140
        d = ImageDraw.Draw(c)
        d.text((370, y + 16), name, font=F(MARKER, 50), fill=YELLOW)
        d.text((370, y + 86), desc, font=F(MARKER, 34), fill=(220, 220, 210))
        d.text((W - 70, y + 16), price, font=F(MARKER, 50 if "$" in price else 38), fill=WHITE, anchor="ra")
        if reg:
            strike(d, (W - 70, y + 90), reg, F(MARKER, 30), (170, 170, 160), anchor="ra")
        y += 250
        d.line([(120, y - 34), (W - 120, y - 34)], fill=(70, 76, 74), width=2)
    d.text((W // 2, y + 10), "order with code", font=F(MARKER, 42), fill=WHITE, anchor="ma")
    d.text((W // 2, y + 70), CODE, font=F(MARKER, 96), fill=YELLOW, anchor="ma")
    cta_bar(d, H - 160, "ORDER NOW  →")
    save_as(c, "59_menu_board.jpg")


# ---------------------------------------------------------------- 60
def ad60_two_for():
    c = Image.new("RGBA", (W, H), RED + (255,))
    d = ImageDraw.Draw(c)
    d.text((W // 2, 40), "2 TIGER TEES", font=F(ANTON, 96), fill=WHITE, anchor="ma")
    strike(d, (W // 2, 170), money(REG), F(ANTON, 70), (255, 170, 170), anchor="ma")
    d.text((W // 2, 250), money(TWO_TEES), font=F(ANTON, 230), fill=YELLOW, anchor="ma")
    r = rot(fit_w(red_tee_crop(), 470), 6)
    b = rot(fit_w(garment(4), 540), -7)
    shadowed(c, b, (W - b.width - 30, 590), blur=22, alpha=120)
    shadowed(c, r, (30, 560), blur=22, alpha=120)
    d = ImageDraw.Draw(c)
    d.rounded_rectangle((W // 2 - 280, 1060, W // 2 + 280, 1140), radius=18, fill=WHITE)
    d.text((W // 2, 1100), f"with code {CODE}", font=F(IN8, 40), fill=INK, anchor="mm")
    cta_bar(d, H - 136, "GET BOTH  →", bg=BLACK, fg=YELLOW)
    save_as(c, "60_2_for_7398.jpg")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn in (ad51_price_tag, ad52_per_tee, ad53_cart_progress, ad54_faq, ad55_one_for_you, ad56_meme,
               ad57_shop_grid, ad58_sticky_note, ad59_menu_board, ad60_two_for):
        fn()
