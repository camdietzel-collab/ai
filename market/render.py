"""404 CULTURE - GPOE Streetwear Market booth promo.

Vertical (9:16) + feed (4:5) cuts for an Instagram ad announcing the booth.
No filmed clips of the garments being worn exist in this environment, so the
spot is built from the flat-lay product photos (thermal, navy tiger tee,
baby-blue tiger tee) in ../story/site/assets/img/, treated with hard cuts and
punch-in zooms. There is no distressed "404" logo file either; the wordmark
is set in Anton instead.

usage:
    python3 render.py main    -> output/404_culture_market_9x16.mp4  (1080x1920)
    python3 render.py feed    -> output/404_culture_market_4x5.mp4   (1080x1350)
    python3 render.py still   -> output/404_culture_market_opening_frame.jpg
    python3 render.py qa      -> output/qa_<aspect>_<sec>s.png for both aspects
"""
import os
import sys
from functools import lru_cache
from multiprocessing import Pool

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(os.path.dirname(HERE), "story", "site", "assets", "img")
OUT_DIR = os.path.join(HERE, "output")
FPS, N = 30, 360  # 12s @ 30fps

ANTON = os.path.join(HERE, "fonts", "Anton-Regular.ttf")
BEBAS = os.path.join(HERE, "fonts", "BebasNeue-Regular.ttf")

RED = (211, 47, 47)
BLACK = (18, 18, 18)
WHITE = (250, 250, 250)
CONCRETE_BASE = (210, 208, 203)

ASPECTS = {"main": (1080, 1920), "feed": (1080, 1350)}

# ---------------------------------------------------------------- layout
# All y-coordinates are tuned so nothing important falls outside the stated
# safe zones: main keeps text within y=[250,1250] (nothing in the bottom
# 670px); feed has no IG-chrome overlay, so margins are just comfortable
# reading room top/bottom. Both keep >=64px side margins.

LAYOUT = {
    "main": dict(
        hook_head_y=330, hook_sub1_y=470, hook_sub2_y=560, hook_bar_y=406,
        label_y=300, label_bar_y=336, strip_y=1190, strip_h=70,
        end_logo_y=520, end_bar_y=578, end_market_y=660, end_date_y=730,
        end_loc1_y=804, end_loc2_y=858, end_btn_y=1000, end_btn_h=108,
    ),
    "feed": dict(
        hook_head_y=175, hook_sub1_y=300, hook_sub2_y=385, hook_bar_y=230,
        label_y=165, label_bar_y=200, strip_y=1230, strip_h=66,
        end_logo_y=230, end_bar_y=284, end_market_y=372, end_date_y=452,
        end_loc1_y=518, end_loc2_y=568, end_btn_y=700, end_btn_h=100,
        end_follow_y=700, end_follow2_y=772,
    ),
}

MARGIN_X = 64

# ---------------------------------------------------------------- assets

PRODUCTS = {
    "thermal": os.path.join(IMG_DIR, "culture-thermal.jpg"),
    "navy": os.path.join(IMG_DIR, "navy-tiger-tee.jpg"),
    "babyblue": os.path.join(IMG_DIR, "baby-blue-tiger-league.jpg"),
}

_IMG_CACHE = {}


def product(name):
    if name not in _IMG_CACHE:
        _IMG_CACHE[name] = Image.open(PRODUCTS[name]).convert("RGB")
    return _IMG_CACHE[name]


@lru_cache(maxsize=4)
def concrete_texture(w, h, seed=404):
    """Light, subtly mottled concrete-gray canvas with fine grain."""
    rng = np.random.default_rng(seed)
    base = np.array(CONCRETE_BASE, np.float32)
    low = rng.normal(0, 1, (h // 24 + 2, w // 24 + 2)).astype(np.float32)
    low = np.asarray(Image.fromarray(low, "F").resize((w, h), Image.BICUBIC))
    fine = rng.normal(0, 1, (h, w)).astype(np.float32)
    mottle = low * 7.0 + fine * 2.2
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt(((xx - w / 2) / (w * 0.75)) ** 2 + ((yy - h * 0.5) / (h * 0.75)) ** 2)
    vignette = np.clip(1.0 - 0.10 * d ** 2, 0.85, 1.0)
    frame = (base[None, None, :] + mottle[..., None]) * vignette[..., None]
    return np.clip(frame, 0, 255).astype(np.uint8)


def background(aspect):
    w, h = ASPECTS[aspect]
    return Image.fromarray(concrete_texture(w, h))


# ---------------------------------------------------------------- easing

def clamp01(x):
    return max(0.0, min(1.0, x))


def p(t, a, b):
    return clamp01((t - a) / (b - a))


def lerp(a, b, q):
    return a + (b - a) * q


def eo_cubic(x):
    return 1 - (1 - x) ** 3


# ---------------------------------------------------------------- text

@lru_cache(maxsize=None)
def font(path, size):
    return ImageFont.truetype(path, size)


def draw_tracked(draw, text, fnt, fill, cx, cy, track=0, shadow=None):
    widths = [fnt.getlength(c) for c in text]
    total = sum(widths) + track * (len(text) - 1)
    asc, desc = fnt.getmetrics()
    x = cx - total / 2
    y = cy - (asc + desc) / 2
    if shadow is not None:
        xs = x
        for c, w in zip(text, widths):
            draw.text((xs + 3, y + 4), c, font=fnt, fill=shadow)
            xs += w + track
    for c, w in zip(text, widths):
        draw.text((x, y), c, font=fnt, fill=fill)
        x += w + track
    return total


def text_height(fnt):
    asc, desc = fnt.getmetrics()
    return asc


# ---------------------------------------------------------------- image crop

def cover_crop(img, out_w, out_h, fu, fv, zoom):
    iw, ih = img.size
    base_scale = max(out_w / iw, out_h / ih)
    scale = base_scale * zoom
    cw, ch = out_w / scale, out_h / scale
    cx, cy = fu * iw, fv * ih
    x0 = min(max(cx - cw / 2, 0), max(iw - cw, 0))
    y0 = min(max(cy - ch / 2, 0), max(ih - ch, 0))
    crop = img.crop((x0, y0, x0 + cw, y0 + ch))
    return crop.resize((out_w, out_h), Image.LANCZOS)


# ---------------------------------------------------------------- shots

# (t0, t1, product, focus_u, focus_v, zoom0, zoom1)
SHOTS = [
    (0.000, 2.000, "thermal", 0.50, 0.45, 1.05, 1.18),
    (2.000, 3.333, "thermal", 0.50, 0.50, 1.00, 1.06),
    (3.333, 4.667, "thermal", 0.50, 0.40, 1.50, 1.65),
    (4.667, 6.000, "thermal", 0.23, 0.58, 1.90, 2.05),
    (6.000, 7.000, "navy", 0.50, 0.40, 1.00, 1.06),
    (7.000, 8.000, "navy", 0.50, 0.40, 1.60, 1.75),
    (8.000, 9.000, "babyblue", 0.50, 0.40, 1.00, 1.06),
    (9.000, 10.000, "babyblue", 0.50, 0.40, 1.60, 1.75),
]

HOOK_LINES = ("GREENSBORO", "WED OCT 28 · 12–5 PM", "ELM & BAIN")
STRIP_TEXT = "OCT 28 · ELM & BAIN · 12–5 PM"
HANDLE = "@404CULTURE"  # placeholder - no real handle found; confirm before posting


def current_shot(t):
    for t0, t1, name, fu, fv, z0, z1 in SHOTS:
        if t0 <= t < t1 or (t1 == 10.0 and t >= 9.999):
            q = eo_cubic(p(t, t0, t1))
            return name, fu, fv, lerp(z0, z1, q)
    return SHOTS[-1][2], SHOTS[-1][3], SHOTS[-1][4], SHOTS[-1][6]


def dark_band(img, w, y0, y1, strength=0.60, x0=0, x1=None):
    x1 = w if x1 is None else x1
    overlay = Image.new("RGBA", (x1 - x0, y1 - y0), (8, 8, 10, int(255 * strength)))
    img.paste(Image.alpha_composite(img.crop((x0, y0, x1, y1)).convert("RGBA"), overlay).convert("RGB"), (x0, y0))


def gray_cutout(img, aspect, y0, y1, x0=0, x1=None):
    """Replace a region with solid concrete-gray, independent of what's under
    it - guarantees label/strip text never sits on top of a garment print."""
    w, h = ASPECTS[aspect]
    x1 = w if x1 is None else x1
    tex = Image.fromarray(concrete_texture(w, h))
    img.paste(tex.crop((x0, y0, x1, y1)), (x0, y0))


def red_bar(draw, cx, y, w=150, h=10):
    draw.rectangle([cx - w / 2, y - h / 2, cx + w / 2, y + h / 2], fill=RED)


def rounded_button(draw, cx, cy, w, h, fill):
    draw.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=h / 2, fill=fill)


# ---------------------------------------------------------------- compose

def compose(f, aspect):
    t = f / FPS
    w, h = ASPECTS[aspect]
    L = LAYOUT[aspect]
    img = background(aspect)

    if t < 10.0:
        name, fu, fv, zoom = current_shot(t)
        shot = cover_crop(product(name), w, h, fu, fv, zoom)
        img.paste(shot, (0, 0))

    draw = ImageDraw.Draw(img, "RGBA")

    if t < 2.0:
        # HOOK - fully on from frame 0, no fade-in of the facts themselves
        dark_band(img, w, 0, int(L["hook_sub2_y"] + 90), strength=0.62)
        draw = ImageDraw.Draw(img, "RGBA")
        head_f = font(ANTON, 150)
        draw_tracked(draw, HOOK_LINES[0], head_f, WHITE, w / 2, L["hook_head_y"], track=2, shadow=(0, 0, 0))
        red_bar(draw, w / 2, L["hook_bar_y"], w=170, h=9)
        sub_f = font(ANTON, 58)
        draw_tracked(draw, HOOK_LINES[1], sub_f, WHITE, w / 2, L["hook_sub1_y"], track=1, shadow=(0, 0, 0))
        draw_tracked(draw, HOOK_LINES[2], sub_f, WHITE, w / 2, L["hook_sub2_y"], track=2, shadow=(0, 0, 0))

    elif t < 10.0:
        label = "THE THERMALS" if t < 6.0 else "TIGER LEAGUE TEE"
        # solid concrete-gray cutouts for label + strip: guarantees the print
        # is never hidden behind text, regardless of the shot's crop/zoom
        lbl_f = font(BEBAS, 54)
        lw = sum(lbl_f.getlength(c) for c in label) + 2 * (len(label) - 1)
        pad = 34
        bx0, bx1 = w / 2 - lw / 2 - pad, w / 2 + lw / 2 + pad
        gray_cutout(img, aspect, int(L["label_y"] - 46), int(L["label_bar_y"] + 20),
                    x0=int(max(bx0, 0)), x1=int(min(bx1, w)))
        gray_cutout(img, aspect, int(L["strip_y"] - L["strip_h"] / 2), int(L["strip_y"] + L["strip_h"] / 2))
        draw = ImageDraw.Draw(img, "RGBA")
        draw_tracked(draw, label, lbl_f, BLACK, w / 2, L["label_y"], track=2)
        red_bar(draw, w / 2, L["label_bar_y"], w=90, h=6)
        strip_f = font(BEBAS, 46)
        draw_tracked(draw, STRIP_TEXT, strip_f, BLACK, w / 2, L["strip_y"], track=1)

    else:
        # END CARD - plain concrete-gray background
        logo_f = font(ANTON, 150)
        draw_tracked(draw, "404 CULTURE", logo_f, BLACK, w / 2, L["end_logo_y"], track=2)
        red_bar(draw, w / 2, L["end_bar_y"], w=190, h=10)
        market_f = font(ANTON, 72)
        draw_tracked(draw, "GPOE STREETWEAR MARKET", market_f, BLACK, w / 2, L["end_market_y"], track=1)
        date_f = font(ANTON, 52)
        draw_tracked(draw, "WED OCT 28 · 12–5 PM", date_f, BLACK, w / 2, L["end_date_y"], track=1)
        loc_f = font(ANTON, 46)
        draw_tracked(draw, "ELM & BAIN", loc_f, BLACK, w / 2, L["end_loc1_y"], track=1)
        draw_tracked(draw, "620 S ELM ST, GREENSBORO", loc_f, BLACK, w / 2, L["end_loc2_y"], track=1)
        btn_f = font(BEBAS, 44)
        btn_w = max(560, sum(btn_f.getlength(c) for c in HANDLE + " FOR DROP-DAY UPDATES") + 90)
        rounded_button(draw, w / 2, L["end_btn_y"], min(btn_w, w - 2 * MARGIN_X), L["end_btn_h"], RED)
        draw_tracked(draw, f"FOLLOW {HANDLE}", btn_f, WHITE, w / 2, L["end_btn_y"] - 18, track=1)
        draw_tracked(draw, "FOR DROP-DAY UPDATES", btn_f, WHITE, w / 2, L["end_btn_y"] + 22, track=1)

    return img


def render_frame_bytes(args):
    f, aspect = args
    return np.asarray(compose(f, aspect).convert("RGB")).tobytes()


def ffmpeg_exe():
    return "ffmpeg"


def encode(aspect, out_path):
    w, h = ASPECTS[aspect]
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    cmd = [ffmpeg_exe(), "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{w}x{h}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", "-an", out_path]
    import subprocess
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    args = [(f, aspect) for f in range(N)]
    with Pool(min(4, os.cpu_count() or 1)) as pool:
        for k, buf in enumerate(pool.imap(render_frame_bytes, args, chunksize=4)):
            proc.stdin.write(buf)
            if k % 60 == 0:
                print(f"[{aspect}] frame {k}/{N}", flush=True)
    proc.stdin.close()
    proc.wait()
    print("wrote", out_path)


def still(aspect, t, out_path, quality=95):
    f = round(t * FPS)
    img = compose(f, aspect).convert("RGB")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path, quality=quality)
    print("wrote", out_path)


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "main"
    if mode == "main":
        encode("main", os.path.join(OUT_DIR, "404_culture_market_9x16.mp4"))
    elif mode == "feed":
        encode("feed", os.path.join(OUT_DIR, "404_culture_market_4x5.mp4"))
    elif mode == "still":
        still("main", 0.0, os.path.join(OUT_DIR, "404_culture_market_opening_frame.jpg"))
    elif mode == "qa":
        for aspect in ("main", "feed"):
            for sec in (0.0, 1.0, 2.5, 6.0, 9.0, 11.0):
                still(aspect, sec, os.path.join(OUT_DIR, f"qa_{aspect}_{sec:04.1f}s.png"))
    else:
        print("usage: render.py [main|feed|still|qa]")
