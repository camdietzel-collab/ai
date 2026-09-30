"""Round 6: five feed-native performance ads (1080x1350) for 404 CULTURE.

Formats that read as content first: POV meme, brand tweet card, notes-app
list, premium product hero and a price-framed full-fit bundle. One idea per
ad, product large, price and CTA unmissable. No invented reviews, counts,
discounts or scarcity.
"""
import os

from PIL import Image, ImageDraw, ImageFilter

from make_ads_v2 import (ANTON, ARCHIVO, BLACK, BLUE, BODY, CREAM, F, H, NAVY, OUT, RED, W, WHITE, YELLOW,
                         cover, fit_font, fit_h, fit_w, garment, model, photo, put, rot, save)
from make_ads_v3 import radial
from make_ads_v4 import INK, MUTED, cta
from make_ads_v5 import tight

REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def rounded(img, r):
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, img.width - 1, img.height - 1), radius=r, fill=255)
    out = img.convert("RGBA")
    out.putalpha(m)
    return out


def avatar(d, xy, r):
    x, y = xy
    d.ellipse((x, y, x + 2 * r, y + 2 * r), fill=YELLOW)
    d.text((x + r, y + r), "404", font=F(ANTON, int(r * 0.8)), fill=BLACK, anchor="mm")


# ---------------------------------------------------------------- ad 26
def ad26_pov():
    c = Image.new("RGBA", (W, H), WHITE + (255,))
    d = ImageDraw.Draw(c)
    f = F(BODY, 52)
    for i, line in enumerate(["POV: you found the one tee that", "goes with every pair of jeans", "you own"]):
        d.text((48, 44 + i * 64), line, font=f, fill=BLACK)
    top, ph = 260, H - 260
    cw = W // 3
    for i, (n, fy) in enumerate([(2, 0.3), (5, 0.2), (1, 0.35)]):
        c.paste(cover(photo(n), cw, ph, fy), (i * cw, top))
    d = ImageDraw.Draw(c)
    for i in (1, 2):
        d.line([(i * cw, top), (i * cw, H)], fill=WHITE, width=6)
    for i, lab in enumerate(["baggy denim", "wide-leg", "slim"]):
        tw = F(BODY, 30).getlength(lab) + 36
        x = i * cw + (cw - tw) / 2
        d.rounded_rectangle((x, top + 24, x + tw, top + 74), radius=25, fill=(0, 0, 0, 170))
        d.text((x + tw / 2, top + 49), lab, font=F(BODY, 30), fill=WHITE, anchor="mm")
    # bottom price strip
    d.rounded_rectangle((40, H - 150, W - 40, H - 40), radius=24, fill=BLACK)
    d.text((80, H - 95), "Tiger League Tee  $39.99", font=F(ARCHIVO, 34), fill=WHITE, anchor="lm")
    d.rounded_rectangle((W - 330, H - 132, W - 58, H - 58), radius=37, fill=YELLOW)
    d.text((W - 194, H - 95), "SHOP NOW", font=F(ARCHIVO, 32), fill=BLACK, anchor="mm")
    save(c, "26_pov_every_jeans.jpg")


# ---------------------------------------------------------------- ad 27
def ad27_tweet():
    c = radial((W, H), (W / 2, H / 2), 900, (210, 24, 36), (130, 8, 18))
    d = ImageDraw.Draw(c)
    card = (50, 110, W - 50, 1130)
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle((card[0], card[1] + 24, card[2], card[3] + 24), radius=36, fill=(0, 0, 0, 120))
    c.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(24)))
    d = ImageDraw.Draw(c)
    d.rounded_rectangle(card, radius=36, fill=WHITE)
    avatar(d, (90, 150), 42)
    d.text((196, 158), "404 CULTURE", font=F(ARCHIVO, 32), fill=INK)
    d.text((196, 202), "@404culture", font=F(REG, 28), fill=MUTED)
    f = F(BODY, 50)
    d.text((90, 280), "a $39.99 tee should not", font=f, fill=INK)
    d.text((90, 342), "go this hard", font=f, fill=INK)
    img = rounded(cover(photo(1), card[2] - card[0] - 80, 620, 0.2), 28)
    c.alpha_composite(img, (90, 436))
    d = ImageDraw.Draw(c)
    d.text((90, 1080), "Tiger League Tee  •  Red / Gold  •  also in Sky Blue", font=F(REG, 26), fill=MUTED, anchor="lm")
    cta(d, 1190, "SHOP THE TEE  —  $39.99", bg=YELLOW, fg=BLACK, size=40)
    save(c, "27_brand_tweet.jpg")


# ---------------------------------------------------------------- ad 28
def ad28_notes():
    c = Image.new("RGBA", (W, H), (252, 250, 244, 255))
    d = ImageDraw.Draw(c)
    d.text((40, 44), "‹ Notes", font=F(BODY, 38), fill=(214, 160, 0))
    d.text((W - 40, 44), "Done", font=F(ARCHIVO, 36), fill=(214, 160, 0), anchor="ra")
    d.text((50, 130), "fits this week", font=F(ARCHIVO, 64), fill=INK)
    items = [(True, "red tiger tee + baggy white denim"), (True, "red tiger tee + wide-leg jeans + boots"),
             (True, "blue tiger tee layered over a thermal"), (False, "grab the culture thermal ($52.99)")]
    y = 250
    for done, text in items:
        cx, cy = 76, y + 26
        if done:
            d.ellipse((cx - 22, cy - 22, cx + 22, cy + 22), fill=(230, 170, 0))
            d.line([(cx - 10, cy), (cx - 3, cy + 8), (cx + 11, cy - 8)], fill=WHITE, width=5)
        else:
            d.ellipse((cx - 22, cy - 22, cx + 22, cy + 22), outline=(190, 190, 190), width=4)
        d.text((120, y + 26), text, font=F(REG, 40), fill=INK if not done else (60, 60, 60), anchor="lm")
        y += 78
    pw, ph, py = 314, 520, 590
    for i, (n, fy) in enumerate([(2, 0.28), (5, 0.18), (4, 0.15)]):
        img = rounded(cover(photo(n), pw, ph, fy), 22)
        c.alpha_composite(img, (50 + i * (pw + 18), py))
    d = ImageDraw.Draw(c)
    d.text((50, 1140), "tees are $39.99. link below ↓", font=F(REG, 40), fill=INK)
    cta(d, 1212, "SHOP NOW  →", bg=BLACK, fg=YELLOW, size=42)
    save(c, "28_notes_fits_this_week.jpg")


# ---------------------------------------------------------------- ad 29
def ad29_product_hero():
    c = radial((W, H), (W / 2, 620), 850, (60, 110, 190), (10, 24, 60))
    d = ImageDraw.Draw(c)
    big = fit_font(ANTON, "TIGER", W - 40, 700)
    ghost = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(ghost).text((W // 2, 640), "TIGER", font=big, fill=(255, 255, 255, 22), anchor="mm")
    c.alpha_composite(ghost)
    d.text((W // 2, 70), "THE TIGER LEAGUE TEE", font=F(ARCHIVO, 40), fill=WHITE, anchor="ma")
    d.text((W // 2, 124), "Layered trim  •  Vintage print  •  Boxy crop", font=F(BODY, 28), fill=BLUE, anchor="ma")
    tee = rot(fit_w(garment(4), 900), -4)
    # floor glow
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((200, 950, 880, 1030), fill=(0, 0, 0, 150))
    c.alpha_composite(glow.filter(ImageFilter.GaussianBlur(26)))
    c.alpha_composite(tee, ((W - tee.width) // 2, 250))
    d = ImageDraw.Draw(c)
    d.text((60, 1030), "$39.99", font=F(ANTON, 110), fill=WHITE)
    for i, col in enumerate([BLUE, (206, 20, 34)]):
        x = W - 190 + i * 76
        yo = -40
        if i == 0:
            d.ellipse((x - 34, 1100 + yo, x + 34, 1168 + yo), outline=WHITE, width=4)
        d.ellipse((x - 25, 1109 + yo, x + 25, 1159 + yo), fill=col)
    d.text((W - 60, 1150), "2 colors", font=F(BODY, 26), fill=BLUE, anchor="ra")
    cta(d, 1214, "SHOP NOW  →", bg=WHITE, fg=NAVY, size=42)
    save(c, "29_product_hero.jpg")


# ---------------------------------------------------------------- ad 30
def ad30_full_fit_under_100():
    c = Image.new("RGBA", (W, H), CREAM + (255,))
    d = ImageDraw.Draw(c)
    d.text((60, 50), "THE FULL FIT.", font=F(ANTON, 118), fill=INK)
    d.text((60, 180), "UNDER $100.", font=F(ANTON, 118), fill=RED)
    m = tight(model(4))
    mm = fit_h(m, 1000)
    c.alpha_composite(mm, (-60, H - mm.height))
    d = ImageDraw.Draw(c)

    def item(img, y, name, price, bg):
        d.rounded_rectangle((560, y, W - 50, y + 300), radius=26, fill=bg)
        t = img.copy()
        t.thumbnail((400, 190), Image.LANCZOS)
        c.alpha_composite(t, (560 + (W - 50 - 560 - t.width) // 2, y + 18))
        d.text((590, y + 262), name, font=F(ARCHIVO, 26), fill=INK, anchor="lm")
        d.text((W - 80, y + 262), price, font=F(ANTON, 50), fill=INK, anchor="rm")
    item(garment(4), 360, "Tiger League Tee", "$39.99", (214, 234, 248))
    d.ellipse((W // 2 + 208, 666, W // 2 + 268, 726), fill=INK)
    d.text((W // 2 + 238, 694), "+", font=F(ARCHIVO, 44), fill=WHITE, anchor="mm")
    item(garment(3), 740, "Culture Thermal", "$52.99", WHITE)
    d.rounded_rectangle((560, 1060, W - 50, 1160), radius=26, fill=INK)
    d.text((590, 1110), "TOTAL", font=F(ARCHIVO, 30), fill=WHITE, anchor="lm")
    d.text((W - 80, 1110), "$92.98", font=F(ANTON, 64), fill=YELLOW, anchor="rm")
    d.rounded_rectangle((560, 1196, W - 50, 1300), radius=26, fill=RED)
    d.text(((560 + W - 50) // 2, 1248), "SHOP THE FIT  →", font=F(ARCHIVO, 36), fill=WHITE, anchor="mm")
    save(c, "30_full_fit_under_100.jpg")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn in (ad26_pov, ad27_tweet, ad28_notes, ad29_product_hero, ad30_full_fit_under_100):
        fn()
