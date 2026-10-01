"""Launch pack 4: five more unique, offer-carrying concepts in 4:5 and 9:16.

Parking ticket, recipe card, WANTED poster, graded test paper and a
cereal box. Same build() as the other packs.
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter

from make_ads_v2 import ANTON, ARCHIVO, BLACK, BLUE, MARKER, NAVY, RED, WHITE, YELLOW, F, cover, fit_h, garment, \
    grain, model, photo, rot, torn
from make_ads_v3 import barcode, radial
from make_ads_v5 import tight
from make_ads_v7 import CODE, GREY_TXT, IN4, IN6, IN8, INK, rounded
from make_ads_v8 import TEE, THERMAL, TWO_TEES, money, red_tee_thumb, thumb_on
from make_ads_v10 import REG, shadowed, strike
from make_ads_v2 import starburst
from make_launch_pack import LH, LW, build, chip, cta, layer
from make_launch_pack2 import OSWALD

HERE = os.path.dirname(os.path.abspath(__file__))
HAND = os.path.join(HERE, "fonts", "Caveat-700.ttf")
RYE = os.path.join(HERE, "fonts", "Rye.ttf")
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
PEN = (210, 30, 40)


def tape_strip(w=170, h=48, deg=0, seed=0):
    return rot(torn(w, h, (236, 226, 190), jag=4, seed=seed, alpha=210), deg)


def check_box(d, x, y, s, checked, color=INK):
    d.rectangle((x, y, x + s, y + s), outline=color, width=3)
    if checked:
        d.line([(x + 5, y + s * .55), (x + s * .4, y + s - 6), (x + s - 4, y + 4)], fill=PEN, width=5)


# ------------------------------------------------------------ 1. parking ticket
def bg_windshield(w, h):
    c = cover(photo(1), w, h, 0.3).filter(ImageFilter.GaussianBlur(18)).convert("RGBA")
    c.alpha_composite(Image.new("RGBA", (w, h), (10, 14, 24, 120)))
    gl = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(gl).polygon([(0, 0), (w * 0.35, 0), (0, h * 0.5)], fill=(255, 255, 255, 25))
    c.alpha_composite(gl)
    return c


def content_ticket():
    L = layer()
    tw, th = 760, 1120
    t = Image.new("RGBA", (tw, th), (252, 248, 226, 255))
    d = ImageDraw.Draw(t)
    d.rectangle((0, 0, tw, 150), fill=(255, 214, 0))
    d.text((tw // 2, 40), "404 CULTURE FIT ENFORCEMENT", font=F(IN8, 30), fill=BLACK, anchor="ma")
    d.text((tw // 2, 78), "NOTICE OF VIOLATION", font=F(ANTON, 58), fill=BLACK, anchor="ma")
    y = 170
    for k, v in [("DATE", "TODAY"), ("LOCATION", "YOUR CLOSET"), ("CITATION #", "404-TL04")]:
        d.text((40, y), k, font=F(MONO, 22), fill=GREY_TXT)
        d.text((260, y - 4), v, font=F(HAND, 44), fill=NAVY)
        y += 60
    d.line([(40, y), (tw - 40, y)], fill=INK, width=2)
    y += 20
    d.text((40, y), "VIOLATION (SEC. 404):", font=F(MONO, 24), fill=INK)
    y += 44
    for txt, ck in [("wearing basic tees", True), ("no layered trim", True), ("zero tiger energy", True),
                    ("already owns both colors", False)]:
        check_box(d, 50, y, 34, ck)
        d.text((104, y - 6), txt, font=F(HAND, 42), fill=NAVY)
        y += 56
    d.line([(40, y + 6), (tw - 40, y + 6)], fill=INK, width=2)
    y += 30
    d.text((40, y), "FINE", font=F(MONO, 24), fill=INK)
    d.text((40, y + 36), "2 Tiger League Tees", font=F(IN8, 40), fill=INK)
    strike(d, (tw - 40, y + 4), money(REG), F(IN8, 34), (150, 150, 150), anchor="ra")
    d.text((tw - 40, y + 40), money(TWO_TEES), font=F(ANTON, 90), fill=RED, anchor="ra")
    y += 150
    d.rounded_rectangle((40, y, tw - 40, y + 90), radius=12, fill=INK)
    d.text((tw // 2, y + 45), f"PAY WITH CODE {CODE}", font=F(IN8, 38), fill=YELLOW, anchor="mm")
    y += 110
    barcode(d, 40, y, 420, 70, seed=3)
    d.text((tw - 40, y + 4), "Officer Tiger", font=F(HAND, 46), fill=NAVY, anchor="ra")
    d.text((tw - 40, y + 52), "badge #404", font=F(MONO, 18), fill=GREY_TXT, anchor="ra")
    t = rot(t, -5)
    shadowed(L, t, (150, 40), blur=20, alpha=140)
    d = ImageDraw.Draw(L)
    # windshield wiper over the top of the ticket
    d.line([(-20, 92), (LW + 20, 22)], fill=(20, 20, 22), width=26)
    d.line([(-20, 92), (LW + 20, 22)], fill=(60, 60, 64), width=8)
    cta(d, 1215, "PAY YOUR FINE  →", bg=YELLOW, fg=BLACK)
    return L


# ------------------------------------------------------------ 2. recipe card
def bg_gingham(w, h):
    c = Image.new("RGBA", (w, h), (250, 246, 240, 255))
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    s = 60
    for x in range(0, w, s * 2):
        d.rectangle((x, 0, x + s, h), fill=(210, 40, 50, 90))
    for y in range(0, h, s * 2):
        d.rectangle((0, y, w, y + s), fill=(210, 40, 50, 90))
    c.alpha_composite(ov)
    return c


def content_recipe():
    L = layer()
    cw, ch = 900, 1010
    card = Image.new("RGBA", (cw, ch), (255, 253, 246, 255))
    d = ImageDraw.Draw(card)
    for y in range(170, ch - 20, 54):
        d.line([(30, y), (cw - 30, y)], fill=(170, 200, 230), width=2)
    d.line([(30, 150), (cw - 30, 150)], fill=PEN, width=4)
    d.text((40, 30), "Recipe: The League Fit", font=F(HAND, 80), fill=INK)
    d.text((40, 120), "SERVES 2  •  PREP: 30 SEC", font=F(IN6, 22), fill=GREY_TXT)
    y = 172
    d.text((40, y), "Ingredients", font=F(HAND, 50), fill=PEN)
    y += 54
    for line in ["1 red tiger tee ($39.99)", "1 blue tiger tee ($39.99)", f"1 code: {CODE}",
                 "baggy denim, to taste"]:
        d.text((60, y), "• " + line, font=F(HAND, 46), fill=INK)
        y += 54
    y += 10
    d.text((40, y), "Directions", font=F(HAND, 50), fill=PEN)
    y += 54
    for line in ["1. add both tees to cart", f"2. stir in {CODE} at checkout", f"3. serve at {money(TWO_TEES)}"]:
        d.text((60, y), line, font=F(HAND, 46), fill=INK)
        y += 54
    card = rot(card, -3)
    shadowed(L, card, (40, 60), blur=20, alpha=120)
    pol = Image.new("RGBA", (330, 400), (252, 252, 248, 255))
    pol.paste(cover(photo(5), 290, 310, 0.15), (20, 20))
    ImageDraw.Draw(pol).text((165, 366), "chef's kiss", font=F(HAND, 40), fill=INK, anchor="mm")
    pol = rot(pol, 8)
    shadowed(L, pol, (700, 640), blur=16, alpha=120)
    L.alpha_composite(tape_strip(150, 44, -30, 2), (760, 630))
    d = ImageDraw.Draw(L)
    cta(d, 1215, f"GET COOKING  •  {CODE}", bg=RED, fg=WHITE)
    return L


# ------------------------------------------------------------ 3. WANTED poster
def bg_wood(w, h):
    c = Image.new("RGBA", (w, h), (110, 70, 40, 255))
    d = ImageDraw.Draw(c)
    rng = random.Random(7)
    for x in range(0, w, 180):
        tone = rng.randint(-14, 14)
        d.rectangle((x, 0, x + 176, h), fill=(110 + tone, 70 + tone, 40 + tone))
        for _ in range(40):
            yy = rng.uniform(0, h)
            d.line([(x + rng.uniform(0, 170), yy), (x + rng.uniform(0, 170), yy + rng.uniform(20, 80))],
                   fill=(90 + tone, 56 + tone, 30 + tone), width=2)
        d.line([(x + 177, 0), (x + 177, h)], fill=(60, 36, 20), width=4)
    return grain(c, 8, 4)


def content_wanted():
    L = layer()
    pw, ph = 880, 1130
    paper = torn(pw, ph, (232, 212, 168), jag=18, seed=9)
    edge = paper.filter(ImageFilter.GaussianBlur(14))
    burn = Image.new("RGBA", (pw, ph), (120, 76, 30, 255))
    burn.putalpha(paper.getchannel("A"))
    inner = paper.copy()
    m = paper.getchannel("A").filter(ImageFilter.GaussianBlur(26)).point(lambda v: 255 if v > 200 else v)
    inner.putalpha(m)
    burn.alpha_composite(inner)
    p = burn
    d = ImageDraw.Draw(p)
    ink = (60, 34, 18)
    d.text((pw // 2, 30), "WANTED", font=F(RYE, 170), fill=ink, anchor="ma")
    d.text((pw // 2, 220), "FOR BEING TOO CLEAN", font=F(RYE, 40), fill=ink, anchor="ma")
    ph_img = cover(photo(2), 420, 470, 0.25)
    d.rectangle((pw // 2 - 222, 282, pw // 2 + 222, 774), fill=ink)
    p.paste(ph_img, (pw // 2 - 210, 294))
    d = ImageDraw.Draw(p)
    d.text((pw // 2, 800), "THE TIGER LEAGUE TEE", font=F(RYE, 50), fill=ink, anchor="ma")
    d.text((pw // 2, 870), "REWARD", font=F(RYE, 44), fill=ink, anchor="ma")
    d.text((pw // 2, 920), "15% OFF THE 2ND", font=F(RYE, 72), fill=(150, 24, 20), anchor="ma")
    d.text((pw // 2, 1010), f"2 for {money(TWO_TEES)}  •  code {CODE}", font=F(RYE, 34), fill=ink, anchor="ma")
    for x, y in [(60, 50), (pw - 60, 50), (60, ph - 50), (pw - 60, ph - 50)]:
        d.ellipse((x - 10, y - 10, x + 10, y + 10), fill=(70, 70, 74))
    shadowed(L, rot(p, -2), (80, 20), blur=18, alpha=150)
    d = ImageDraw.Draw(L)
    cta(d, 1215, "CLAIM YOUR REWARD  →", bg=YELLOW, fg=BLACK)
    return L


# ------------------------------------------------------------ 4. test paper
def bg_desk(w, h):
    c = radial((w, h), (w / 2, h / 2), max(w, h) * 0.8, (196, 160, 120), (140, 104, 70))
    return grain(c, 6, 6)


def content_test():
    L = layer()
    pw, ph = 920, 1140
    p = Image.new("RGBA", (pw, ph), (255, 255, 252, 255))
    d = ImageDraw.Draw(p)
    for y in range(190, ph, 52):
        d.line([(0, y), (pw, y)], fill=(180, 205, 235), width=2)
    d.line([(110, 0), (110, ph)], fill=(240, 150, 150), width=3)
    for y in (120, 520, 920):
        d.ellipse((34, y, 64, y + 30), fill=(150, 120, 90))
    d.text((140, 30), "Name:", font=F(IN6, 28), fill=INK)
    d.text((240, 14), "you", font=F(HAND, 54), fill=NAVY)
    d.text((420, 30), "Class:", font=F(IN6, 28), fill=INK)
    d.text((520, 14), "Fit 101", font=F(HAND, 54), fill=NAVY)
    d.text((140, 96), "FINAL EXAM", font=F(IN8, 40), fill=INK)
    # grade
    d.ellipse((pw - 220, 20, pw - 40, 180), outline=PEN, width=7)
    d.text((pw - 130, 100), "A+", font=F(HAND, 110), fill=PEN, anchor="mm")
    y = 196
    d.text((140, y), "1. Which tiger tee should you get?", font=F(IN6, 32), fill=INK)
    y += 60
    opts = [("a) red", 160), ("b) blue", 380), ("c) both", 620)]
    for t, x in opts:
        d.text((x, y), t, font=F(HAND, 50), fill=NAVY)
    d.ellipse((600, y - 6, 820, y + 64), outline=PEN, width=5)
    d.text((840, y), "yes!", font=F(HAND, 44), fill=PEN)
    y += 110
    d.text((140, y), f"2. 2 tees with {CODE} = ?", font=F(IN6, 32), fill=INK)
    y += 56
    d.text((170, y), money(TWO_TEES), font=F(HAND, 70), fill=NAVY)
    d.line([(400, y + 40), (420, y + 60), (460, y + 10)], fill=PEN, width=6)
    y += 110
    d.text((140, y), "3. What do you enter at checkout?", font=F(IN6, 32), fill=INK)
    y += 56
    d.text((170, y), CODE, font=F(HAND, 70), fill=NAVY)
    d.line([(470, y + 40), (490, y + 60), (530, y + 10)], fill=PEN, width=6)
    y += 110
    d.text((140, y), "4. Bonus: the 2nd item is ___ off", font=F(IN6, 32), fill=INK)
    y += 56
    d.text((170, y), "15%", font=F(HAND, 70), fill=NAVY)
    d.line([(320, y + 40), (340, y + 60), (380, y + 10)], fill=PEN, width=6)
    p.alpha_composite(red_tee_thumb(170, (255, 255, 252)), (pw - 380, 830))
    p.alpha_composite(thumb_on(garment(4), 170, (255, 255, 252)), (pw - 200, 830))
    d = ImageDraw.Draw(p)
    d.text((pw - 290, 1012), "great fit sense!", font=F(HAND, 44), fill=PEN, anchor="ma")
    shadowed(L, rot(p, 2), (60, 20), blur=18, alpha=130)
    d = ImageDraw.Draw(L)
    cta(d, 1215, "PASS THE TEST: SHOP NOW  →", bg=INK, fg=YELLOW, size=36)
    return L


# ------------------------------------------------------------ 5. cereal box
def bg_kitchen(w, h):
    c = radial((w, h), (w / 2, h * 0.35), max(w, h) * 0.8, (255, 236, 200), (240, 190, 120))
    d = ImageDraw.Draw(c)
    d.rectangle((0, int(h * 0.82), w, h), fill=(200, 150, 100))
    return c


def content_cereal():
    L = layer()
    bw, bh = 720, 1100
    box = Image.new("RGBA", (bw + 120, bh + 60), (0, 0, 0, 0))
    d = ImageDraw.Draw(box)
    # side + top faces for depth
    d.polygon([(bw, 60), (bw + 110, 0), (bw + 110, bh), (bw, bh + 60)], fill=(150, 10, 20))
    d.polygon([(0, 60), (110, 0), (bw + 110, 0), (bw, 60)], fill=(230, 60, 60))
    d.rectangle((0, 60, bw, bh + 60), fill=(206, 20, 34))
    for i in range(16):  # sunburst behind mascot
        a0 = i * math.pi / 8
        cx, cy, R = bw / 2, 620, 520
        d.polygon([(cx, cy), (cx + R * math.cos(a0), cy + R * math.sin(a0)),
                   (cx + R * math.cos(a0 + math.pi / 16), cy + R * math.sin(a0 + math.pi / 16))], fill=(222, 40, 50))
    d.rectangle((bw + 1, 0, bw + 120, bh + 60), fill=(0, 0, 0, 0))
    d.rectangle((0, 0, bw + 120, 59), fill=(0, 0, 0, 0))
    d.polygon([(bw, 60), (bw + 110, 0), (bw + 110, bh), (bw, bh + 60)], fill=(150, 10, 20))
    d.polygon([(0, 60), (110, 0), (bw + 110, 0), (bw, 60)], fill=(230, 60, 60))
    d.rectangle((0, 60, bw, 120), fill=(30, 10, 12))
    d.text((bw // 2, 90), "404 CULTURE", font=F(ANTON, 44), fill=YELLOW, anchor="mm")
    d.text((bw // 2, 130), "TIGER", font=F(ANTON, 170), fill=YELLOW, anchor="ma", stroke_width=8, stroke_fill=(120, 6, 16))
    d.text((bw // 2, 310), "TEES", font=F(ANTON, 130), fill=WHITE, anchor="ma", stroke_width=8, stroke_fill=(120, 6, 16))
    m = fit_h(tight(model(2)), 560)
    mc = m.crop((0, 0, m.width, 430))
    box.alpha_composite(mc, ((bw - mc.width) // 2, 500))
    d = ImageDraw.Draw(box)
    starburst(d, (bw - 130, 560), 120, 96, 18, YELLOW)
    d.text((bw - 130, 530), "NOW", font=F(IN8, 26), fill=BLACK, anchor="mm")
    d.text((bw - 130, 570), "2 FOR", font=F(IN8, 30), fill=BLACK, anchor="mm")
    d.text((bw - 130, 612), money(TWO_TEES), font=F(ANTON, 40), fill=RED, anchor="mm")
    d.rounded_rectangle((30, 990, bw - 30, 1070), radius=14, fill=WHITE)
    d.text((bw // 2, 1030), f"PRIZE INSIDE: CODE {CODE}", font=F(IN8, 34), fill=INK, anchor="mm")
    d.text((40, 950), "PART OF A COMPLETE FIT", font=F(IN6, 22), fill=WHITE)
    d.text((bw - 40, 950), "NET WT 2 TEES", font=F(IN6, 22), fill=WHITE, anchor="ra")
    shadowed(L, box, (90, 30), blur=24, alpha=140)
    d = ImageDraw.Draw(L)
    cta(d, 1215, "GRAB A BOX  •  2 FOR $73.98", bg=INK, fg=YELLOW, size=38)
    return L


ADS = [
    ("16_parking_ticket", bg_windshield, content_ticket),
    ("17_recipe_card", bg_gingham, content_recipe),
    ("18_wanted_poster", bg_wood, content_wanted),
    ("19_test_paper_a_plus", bg_desk, content_test),
    ("20_cereal_box", bg_kitchen, content_cereal),
]

if __name__ == "__main__":
    for name, bg, content in ADS:
        build(name, bg, content)
