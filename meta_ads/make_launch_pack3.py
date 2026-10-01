"""Launch pack 3: five more unique, offer-carrying concepts in 4:5 and 9:16.

Fit Facts label, photo-booth strip, LEAGUE AIR boarding pass, weather
forecast and a movie poster. Same build() as packs 1 and 2.
"""
import random

from PIL import Image, ImageDraw, ImageFilter

from make_ads_v2 import ANTON, ARCHIVO, BLACK, BLUE, MARKER, NAVY, RED, WHITE, YELLOW, F, cover, fit_h, garment, \
    grain, model, photo, rot
from make_ads_v3 import barcode, radial
from make_ads_v5 import tight
from make_ads_v7 import CODE, GREY_TXT, IN4, IN6, IN8, INK, emoji, rich, rounded, vgrad
from make_ads_v8 import DISCOUNT, TEE, THERMAL, TWO_TEES, money, red_tee_thumb, thumb_on
from make_ads_v10 import REG, shadowed, strike
from make_launch_pack import LH, LW, build, chip, cta, layer
from make_launch_pack2 import OSWALD
from make_ads_v7 import EMOJI
EMOJI.update("🔥🐯")

HELV_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
HELV = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


# ------------------------------------------------------------ 1. fit facts
def bg_kraft(w, h):
    return grain(Image.new("RGBA", (w, h), (226, 206, 172, 255)), 7, 21)


def content_fit_facts():
    L = layer()
    lab = Image.new("RGBA", (600, 1140), WHITE + (255,))
    d = ImageDraw.Draw(lab)
    d.rectangle((0, 0, 599, 1139), outline=BLACK, width=6)
    x0, x1 = 22, 578
    d.text((x0, 14), "Fit Facts", font=F(ARCHIVO, 84), fill=BLACK)
    d.line([(x0, 118), (x1, 118)], fill=BLACK, width=2)
    d.text((x0, 128), "Servings per order: 2 (recommended)", font=F(HELV, 26), fill=BLACK)
    d.text((x0, 166), "Serving size", font=F(HELV_B, 32), fill=BLACK)
    d.text((x1, 166), "1 boxy tee", font=F(HELV_B, 32), fill=BLACK, anchor="ra")
    d.rectangle((x0, 214, x1, 234), fill=BLACK)
    d.text((x0, 244), "Amount per fit", font=F(HELV_B, 24), fill=BLACK)
    d.text((x0, 270), "Price", font=F(ARCHIVO, 70), fill=BLACK)
    d.text((x1, 270), money(TEE), font=F(ARCHIVO, 70), fill=BLACK, anchor="ra")
    d.rectangle((x0, 362, x1, 374), fill=BLACK)
    d.text((x1, 384), "% Daily Value*", font=F(HELV_B, 24), fill=BLACK, anchor="ra")
    rows = [("Vintage tiger print", "100%", True), ("Layered contrast trim", "100%", True),
            ("Boxy, cropped fit", "100%", True), ("Goes with baggy denim", "100%", False),
            ("Basic", "0%", True), ("Colorways", "2", False)]
    y = 420
    for k, v, bold in rows:
        d.line([(x0, y), (x1, y)], fill=BLACK, width=2)
        d.text((x0, y + 12), k, font=F(HELV_B if bold else HELV, 30), fill=BLACK)
        d.text((x1, y + 12), v, font=F(HELV_B, 30), fill=BLACK, anchor="ra")
        y += 58
    d.rectangle((x0, y + 4, x1, y + 20), fill=BLACK)
    y += 34
    d.text((x0, y), f"2nd tee w/ {CODE}", font=F(HELV_B, 32), fill=BLACK)
    d.text((x1, y), "15% off", font=F(HELV_B, 32), fill=RED, anchor="ra")
    y += 52
    d.line([(x0, y), (x1, y)], fill=BLACK, width=2)
    d.text((x0, y + 12), "2 tees", font=F(HELV_B, 32), fill=BLACK)
    d.text((x1, y + 12), money(TWO_TEES), font=F(HELV_B, 32), fill=RED, anchor="ra")
    y += 66
    d.rectangle((x0, y, x1, y + 8), fill=BLACK)
    for i, l in enumerate(["*Percent Daily Values are based on a", "404 CULTURE diet. Your fit may vary."]):
        d.text((x0, y + 20 + i * 30), l, font=F(HELV, 22), fill=BLACK)
    shadowed(L, rot(lab, -2), (40, 40), blur=18, alpha=110)
    ph = rounded(cover(photo(2), 350, 740, 0.28), 24)
    shadowed(L, rot(ph, 3), (676, 90), blur=18, alpha=110)
    d = ImageDraw.Draw(L)
    chip(d, 840, 900, "2 FOR " + money(TWO_TEES), 40, bg=RED, fg=WHITE)
    chip(d, 840, 990, f"CODE {CODE}", 36, bg=YELLOW, fg=BLACK)
    cta(d, 1215, "SHOP THE TIGER TEE  →", bg=BLACK, fg=YELLOW)
    return L


# ------------------------------------------------------------ 2. photo booth strip
def bg_curtain(w, h):
    c = Image.new("RGBA", (w, h), (90, 10, 18, 255))
    d = ImageDraw.Draw(c)
    for x in range(0, w, 60):
        d.rectangle((x, 0, x + 30, h), fill=(110, 14, 24))
    c = c.filter(ImageFilter.GaussianBlur(12))
    vgrad(c, 0, h, 30, 120)
    return c


def content_booth():
    L = layer()
    sw = 470
    strip = Image.new("RGBA", (sw, 1300), (252, 252, 248, 255))
    sd = ImageDraw.Draw(strip)
    frames = [(2, 0.22, "red"), (5, 0.12, "red again"), (4, 0.1, "blue"), (1, 0.25, "both = $73.98")]
    fh = 284
    for i, (n, fy, cap) in enumerate(frames):
        y = 24 + i * (fh + 14)
        strip.paste(cover(photo(n), sw - 40, fh, fy), (20, y))
        sd = ImageDraw.Draw(strip)
        sd.text((40, y + fh - 64), cap, font=F(MARKER, 42), fill=WHITE, stroke_width=4, stroke_fill=BLACK)
    sd.text((sw // 2, 1268), "404 CULTURE  •  LEAGUE BOOTH", font=F(IN6, 22), fill=GREY_TXT, anchor="mm")
    strip = rot(strip.resize((round(sw * 0.86), round(1300 * 0.86))), -4)
    shadowed(L, strip, (30, 20), blur=20, alpha=150)
    d = ImageDraw.Draw(L)
    x = 520
    d.text((x, 60), "TAKE", font=F(ANTON, 120), fill=WHITE)
    d.text((x, 200), "BOTH.", font=F(ANTON, 120), fill=YELLOW)
    d.text((x, 360), "2 TIGER TEES", font=F(IN8, 40), fill=WHITE)
    strike(d, (x, 420), money(REG), F(IN8, 44), (220, 160, 160))
    d.text((x, 476), money(TWO_TEES), font=F(ANTON, 130), fill=WHITE)
    L.alpha_composite(red_tee_thumb(240, (130, 30, 40)), (x, 690))
    L.alpha_composite(thumb_on(garment(4), 240, (130, 30, 40)), (x + 260, 690))
    d = ImageDraw.Draw(L)
    chip(d, x + 250, 960, f"CODE {CODE}", 40, bg=YELLOW, fg=BLACK)
    d.text((x + 250, 1070), "2nd tee 15% off", font=F(IN6, 34), fill=WHITE, anchor="ma")
    cta(d, 1215, f"GET BOTH FOR {money(TWO_TEES)}  →", bg=YELLOW, fg=BLACK)
    return L


# ------------------------------------------------------------ 3. boarding pass
def bg_sky(w, h):
    c = radial((w, h), (w * 0.5, 0), max(w, h), (150, 200, 240), (60, 120, 200))
    cl = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(cl)
    rng = random.Random(5)
    for _ in range(26):
        x, y, r = rng.uniform(0, w), rng.uniform(0, h), rng.uniform(60, 160)
        d.ellipse((x - r * 1.8, y - r, x + r * 1.8, y + r), fill=(255, 255, 255, 70))
    c.alpha_composite(cl.filter(ImageFilter.GaussianBlur(30)))
    return c


def content_boarding():
    L = layer()
    pw, ph = 940, 1110
    p = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    d = ImageDraw.Draw(p)
    d.rounded_rectangle((0, 0, pw - 1, ph - 1), radius=30, fill=WHITE)
    d.rounded_rectangle((0, 0, pw - 1, 150), radius=30, fill=RED)
    d.rectangle((0, 110, pw - 1, 150), fill=RED)
    d.text((40, 40), "LEAGUE AIR", font=F(ANTON, 70), fill=WHITE)
    d.text((pw - 40, 52), "BOARDING PASS", font=F(IN8, 30), fill=YELLOW, anchor="ra")
    # route
    d.text((60, 190), "FROM", font=F(IN6, 24), fill=GREY_TXT)
    d.text((60, 220), "BSC", font=F(ANTON, 150), fill=INK)
    d.text((62, 400), "Basic tees", font=F(IN6, 28), fill=GREY_TXT)
    d.text((pw - 60, 190), "TO", font=F(IN6, 24), fill=GREY_TXT, anchor="ra")
    d.text((pw - 60, 220), "LGE", font=F(ANTON, 150), fill=RED, anchor="ra")
    d.text((pw - 62, 400), "The League", font=F(IN6, 28), fill=GREY_TXT, anchor="ra")
    cx, cy = pw // 2, 310
    for x in range(cx - 130, cx + 131, 22):
        d.line([(x, cy), (x + 10, cy)], fill=(190, 190, 190), width=4)
    d.ellipse((cx - 50, cy - 50, cx + 50, cy + 50), fill=WHITE)
    d.text((cx, cy), "✈", font=F("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 80), fill=INK, anchor="mm")
    fields = [("PASSENGER", "YOU"), ("FLIGHT", "TL04"), ("GATE", "404"), ("SEAT", "2T"),
              ("BOARDING", "NOW"), ("PROMO", CODE)]
    for i, (k, v) in enumerate(fields):
        x = 60 + (i % 3) * 290
        y = 470 + (i // 3) * 120
        d.text((x, y), k, font=F(IN6, 22), fill=GREY_TXT)
        d.text((x, y + 30), v, font=F(IN8, 46), fill=RED if k == "PROMO" else INK)
    # perforation
    py = 730
    for x in range(30, pw - 30, 28):
        d.ellipse((x, py - 4, x + 10, py + 6), fill=(210, 210, 210))
    d.ellipse((-28, py - 28, 28, py + 28), fill=(0, 0, 0, 0))
    d.ellipse((pw - 28, py - 28, pw + 28, py + 28), fill=(0, 0, 0, 0))
    # stub: fare + carry-on
    d.text((60, 760), "CARRY-ON", font=F(IN6, 22), fill=GREY_TXT)
    p.alpha_composite(red_tee_thumb(150, (246, 238, 236)), (60, 796))
    p.alpha_composite(thumb_on(garment(4), 150, (232, 242, 250)), (226, 796))
    d = ImageDraw.Draw(p)
    d.text((pw - 60, 760), "FARE", font=F(IN6, 22), fill=GREY_TXT, anchor="ra")
    strike(d, (pw - 60, 794), money(REG), F(IN8, 36), (160, 160, 160), anchor="ra")
    d.text((pw - 60, 840), money(TWO_TEES), font=F(ANTON, 100), fill=INK, anchor="ra")
    barcode(d, 60, 980, pw - 120, 90, seed=8)
    shadowed(L, rot(p, -3), (50, 30), blur=24, alpha=130)
    d = ImageDraw.Draw(L)
    cta(d, 1215, f"BOARD NOW  •  CODE {CODE}", bg=YELLOW, fg=BLACK)
    return L


# ------------------------------------------------------------ 4. weather
def bg_weather(w, h):
    c = cover(photo(4), w, h, 0.0).filter(ImageFilter.GaussianBlur(30)).convert("RGBA")
    c.alpha_composite(Image.new("RGBA", (w, h), (20, 40, 90, 110)))
    return c


def content_weather():
    L = layer()
    d = ImageDraw.Draw(L)
    d.text((LW // 2, 20), "YOUR CITY", font=F(IN6, 40), fill=WHITE, anchor="ma")
    d.text((LW // 2, 70), "100%", font=F(IN4, 210), fill=WHITE, anchor="ma")
    d.text((LW // 2, 300), "chance of fits", font=F(IN6, 46), fill=WHITE, anchor="ma")
    d.text((LW // 2, 360), "Feels like: the league   H: fits   L: basic", font=F(IN4, 32), fill=(225, 235, 255), anchor="ma")
    box = (40, 430, LW - 40, 1010)
    d.rounded_rectangle(box, radius=30, fill=(255, 255, 255, 50))
    d.text((80, 452), "📅  5-DAY FORECAST".replace("📅  ", ""), font=F(IN6, 26), fill=(225, 235, 255))
    days = [("Mon", red_tee_thumb(80, (200, 210, 230)), "red tiger tee"),
            ("Tue", thumb_on(garment(4), 80, (200, 210, 230)), "blue tiger tee"),
            ("Wed", thumb_on(garment(3), 80, (200, 210, 230)), "culture thermal"),
            ("Thu", red_tee_thumb(80, (200, 210, 230)), "red again (obviously)"),
            ("Fri", None, f"{CODE} day")]
    y = 500
    for day, th, desc in days:
        d.line([(80, y - 6), (LW - 80, y - 6)], fill=(255, 255, 255, 70), width=2)
        d.text((90, y + 40), day, font=F(IN6, 40), fill=WHITE, anchor="lm")
        if th is not None:
            L.alpha_composite(th, (220, y))
        else:
            L.alpha_composite(emoji("🐯", 70), (225, y + 6))
        d = ImageDraw.Draw(L)
        d.text((330, y + 40), desc, font=F(IN6, 36), fill=WHITE if th is not None else YELLOW, anchor="lm")
        y += 100
    d.rounded_rectangle((40, 1036, LW - 40, 1176), radius=30, fill=(255, 255, 255, 60))
    d.text((80, 1056), "UV INDEX", font=F(IN6, 24), fill=(225, 235, 255))
    d.text((80, 1090), f"{CODE}  •  buy 1, get 1 15% off", font=F(IN8, 40), fill=WHITE)
    cta(d, 1215, "GET THE FORECAST FIT  →", bg=YELLOW, fg=BLACK)
    return L


# ------------------------------------------------------------ 5. movie poster
def bg_cinema(w, h):
    c = radial((w, h), (w / 2, h * 0.4), max(w, h) * 0.7, (90, 10, 16), (6, 4, 6))
    return grain(c, 7, 31)


def content_movie():
    L = layer()
    d = ImageDraw.Draw(L)
    d.text((LW // 2, 20), "THIS FALL, ONE TEE ISN'T ENOUGH.", font=F(OSWALD, 40), fill=(235, 220, 210), anchor="ma")
    m = fit_h(tight(model(5)), 780)
    glow = Image.new("RGBA", L.size, (0, 0, 0, 0))
    a = m.getchannel("A").filter(ImageFilter.GaussianBlur(20))
    g = Image.new("RGBA", m.size, (255, 60, 40, 255))
    g.putalpha(a)
    glow.alpha_composite(g, ((LW - m.width) // 2, 110))
    L.alpha_composite(glow.filter(ImageFilter.GaussianBlur(10)))
    L.alpha_composite(m, ((LW - m.width) // 2, 110))
    vg = Image.new("RGBA", L.size, (0, 0, 0, 0))
    vd = ImageDraw.Draw(vg)
    for y in range(640, 900):
        vd.line([(0, y), (LW, y)], fill=(6, 4, 6, int(255 * (y - 640) / 260)))
    vd.rectangle((0, 900, LW, LH), fill=(6, 4, 6, 255))
    L.alpha_composite(vg)
    d = ImageDraw.Draw(L)
    d.text((LW // 2, 700), "TIGER", font=F(ANTON, 200), fill=YELLOW, anchor="ma", stroke_width=3, stroke_fill=(120, 60, 0))
    d.text((LW // 2, 900), "LEAGUE", font=F(ANTON, 120), fill=WHITE, anchor="ma")
    d.text((LW // 2, 1046), f"NOW SHOWING  •  2 FOR {money(TWO_TEES)}  •  CODE {CODE}", font=F(OSWALD, 34), fill=YELLOW, anchor="ma")
    billing = ("404 CULTURE PRESENTS A LEAGUE PRODUCTION  STARRING THE RED TEE  THE BLUE TEE  "
               "AND THE CULTURE THERMAL  MUSIC BY THE STREETS  FIT BY YOU")
    f = F(OSWALD, 22)
    words, line, lines = billing.split("  "), "", []
    for w_ in words:
        t = (line + "  " + w_).strip()
        if f.getlength(t) > LW - 420:
            lines.append(line)
            line = w_
        else:
            line = t
    lines.append(line)
    for i, l in enumerate(lines):
        d.text((LW // 2 + 70, 1100 + i * 30), l, font=f, fill=(170, 160, 160), anchor="ma")
    d.rectangle((60, 1100, 170, 1160), outline=(170, 160, 160), width=3)
    d.text((115, 1130), "F", font=F(OSWALD, 40), fill=(200, 190, 190), anchor="mm")
    d.text((115, 1172), "FOR FIT", font=F(OSWALD, 16), fill=(170, 160, 160), anchor="ma")
    cta(d, 1215, "GET TICKETS: SHOP NOW  →", bg=YELLOW, fg=BLACK)
    return L


ADS = [
    ("11_fit_facts_label", bg_kraft, content_fit_facts),
    ("12_photo_booth_strip", bg_curtain, content_booth),
    ("13_league_air_boarding_pass", bg_sky, content_boarding),
    ("14_weather_100_chance_of_fits", bg_weather, content_weather),
    ("15_tiger_league_movie_poster", bg_cinema, content_movie),
]

if __name__ == "__main__":
    for name, bg, content in ADS:
        build(name, bg, content)
