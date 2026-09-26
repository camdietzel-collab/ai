"""404 CULTURE - "New Collection" 15s 9:16 campaign video renderer.

Garments are composited from cutouts/{1..5}.png (source pixels + alpha only).
They are only translated, scaled, rotated and motion-blurred; colour is never
changed. Output: frames piped straight into ffmpeg.

usage: python3 render.py [out.mp4] [--preview N]   (preview = every Nth frame)
"""
import math
import os
import subprocess
import sys
from functools import lru_cache
from multiprocessing import Pool

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS, N = 1080, 1920, 30, 450
FIT = 920.0  # on-screen garment width at scale 1.0
FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- assets

class Garment:
    def __init__(self, i):
        im = Image.open(os.path.join(HERE, "cutouts", f"{i}.png")).convert("RGBA")
        a = np.asarray(im).astype(np.float32)
        alpha = a[..., 3:] / 255.0
        self.w, self.h = im.size
        self.rgb = Image.fromarray((a[..., :3] * alpha).round().astype(np.uint8), "RGB")
        self.alpha = im.getchannel("A")
        m = alpha[..., 0] > 0.9
        self.mean = a[..., :3][m].mean(axis=0)


G = None


def load():
    global G, BG_FALLOFF, VIGNETTE, GRAIN
    G = [Garment(i) for i in range(1, 6)]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    BG_FALLOFF = (xx, yy)
    d = np.sqrt(((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H * 0.45) / (H * 0.62)) ** 2)
    VIGNETTE = np.clip(1.0 - 0.55 * d ** 2.2, 0.35, 1.0)[..., None]
    rng = np.random.default_rng(404)
    GRAIN = []
    for _ in range(8):
        n = rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32)
        n = np.asarray(Image.fromarray(n, "F").resize((W, H), Image.BILINEAR))
        GRAIN.append(n[..., None])


# ---------------------------------------------------------------- easing

def clamp01(x):
    return max(0.0, min(1.0, x))


def p(t, a, b):
    return clamp01((t - a) / (b - a))


def lerp(a, b, q):
    return a + (b - a) * q


def eo_expo(x):
    return 1.0 if x >= 1 else 1 - 2 ** (-10 * x)


def ei_expo(x):
    return 0.0 if x <= 0 else 2 ** (10 * x - 10)


def eio_expo(x):
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    return 2 ** (20 * x - 10) / 2 if x < 0.5 else (2 - 2 ** (-20 * x + 10)) / 2


def eo_back(x, c=1.6):
    x -= 1
    return 1 + (c + 1) * x ** 3 + c * x ** 2


def ei_cubic(x):
    return x ** 3


def eo_cubic(x):
    return 1 - (1 - x) ** 3


# ---------------------------------------------------------------- text

@lru_cache(maxsize=None)
def text_sprite(s, size, track, color):
    """Pre-multiplied RGBA float sprite of tracked, single-line text."""
    font = ImageFont.truetype(FONT, size)
    widths = [font.getlength(c) for c in s]
    tw = int(sum(widths) + track * (len(s) - 1)) + 8
    asc, desc = font.getmetrics()
    im = Image.new("L", (tw, asc + desc + 8), 0)
    d = ImageDraw.Draw(im)
    x = 4
    for c, cw in zip(s, widths):
        d.text((x, 4), c, font=font, fill=255)
        x += cw + track
    a = np.asarray(im).astype(np.float32)[..., None] / 255.0
    col = np.array(color, np.float32)[None, None, :]
    return a * col, a


def text_width(s, size, track):
    return text_sprite(s, size, track, (255, 255, 255))[1].shape[1]


def draw_text(frame, s, size, track, color, x, y, alpha=1.0, reveal=1.0, anchor="l"):
    if alpha <= 0 or reveal <= 0:
        return
    rgb, a = text_sprite(s, size, track, color)
    h, w = a.shape[:2]
    if anchor == "c":
        x -= w / 2
    x, y = int(round(x)), int(round(y))
    vis = int(w * clamp01(reveal))
    x0, y0 = max(x, 0), max(y, 0)
    x1, y1 = min(x + vis, W), min(y + h, H)
    if x1 <= x0 or y1 <= y0:
        return
    sa = a[y0 - y:y1 - y, x0 - x:x1 - x] * alpha
    sr = rgb[y0 - y:y1 - y, x0 - x:x1 - x] * alpha
    reg = frame[y0:y1, x0:x1]
    reg *= 1 - sa
    reg += sr


# ---------------------------------------------------------------- garments

def place(g, X, Y, s, rot, fu, fv):
    """Affine inverse map + on-screen bbox for garment g."""
    k = s * FIT / g.w
    px, py = fu * g.w, fv * g.h
    c, sn = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    corners = []
    for cx, cy in ((0, 0), (g.w, 0), (0, g.h), (g.w, g.h)):
        dx, dy = (cx - px) * k, (cy - py) * k
        corners.append((X + c * dx - sn * dy, Y + sn * dx + c * dy))
    xs, ys = zip(*corners)
    box = (max(int(min(xs)) - 2, 0), max(int(min(ys)) - 2, 0),
           min(int(max(xs)) + 3, W), min(int(max(ys)) + 3, H))
    return k, px, py, c, sn, box


def render_garment(g, X, Y, s, rot, fu, fv):
    k, px, py, c, sn, (bx0, by0, bx1, by1) = place(g, X, Y, s, rot, fu, fv)
    if bx1 <= bx0 or by1 <= by0:
        return None
    ox, oy = X - bx0, Y - by0
    data = (c / k, sn / k, px - (c * ox + sn * oy) / k,
            -sn / k, c / k, py - (-sn * ox + c * oy) / k)
    size = (bx1 - bx0, by1 - by0)
    resample = Image.BICUBIC if k > 0.6 else Image.BILINEAR
    rgb = g.rgb.transform(size, Image.AFFINE, data, resample=resample)
    al = g.alpha.transform(size, Image.AFFINE, data, resample=resample)
    a = np.asarray(al).astype(np.float32)[..., None] / 255.0
    r = np.minimum(np.asarray(rgb).astype(np.float32), a * 255.0)
    return (bx0, by0, bx1, by1), r, a


# ---------------------------------------------------------------- timeline

LABELS = [
    ("BLACK", "CULTURE THERMAL", "$52.99"),
    ("RED", "CULTURE CREWNECK", "$52.99"),
    ("CREAM GRAPHIC", "CULTURE THERMAL", "$52.99"),
    ("BABY BLUE", "404 CULTURE TEE", "$39.99"),
    ("NAVY/RED", "404 CULTURE TEE", "$39.99"),
]
HERO_Y = 790

# frames where fast motion gets multi-sample motion blur
BLUR = [(22, 38), (97, 112), (137, 145), (143, 152), (180, 197), (262, 270),
        (330, 345)]

# collection shot: (garment, x, y, on-screen width, from-dx, from-dy, from-rot)
COLL = [
    (0, 192, 430, 352, -900, -120, -30),
    (1, 540, 430, 352, 0, -1100, 20),
    (2, 888, 430, 352, 900, -120, 30),
    (3, 295, 810, 480, -800, 900, 25),
    (4, 785, 810, 480, 800, 900, -25),
]
COLL_Y = 0  # vertical offset applied to all collection pieces

# montage 270-330: 8 shots on 8th notes
MONTAGE = [
    # garment, s0, s1, focus0, focus1, rot0, rot1
    (0, 2.9, 3.1, (0.40, 0.37), (0.58, 0.37), 0, 0),
    (1, 1.12, 0.98, (0.5, 0.5), (0.5, 0.5), 0, 0),
    (2, 2.5, 2.6, (0.28, 0.25), (0.70, 0.25), 0, 0),
    (3, 1.0, 1.0, (0.5, 0.5), (0.5, 0.5), -10, 0),
    (4, 3.0, 2.7, (0.5, 0.47), (0.5, 0.47), 0, 0),
    (1, 2.7, 2.9, (0.44, 0.40), (0.56, 0.38), 0, 0),
    (2, 0.95, 1.03, (0.5, 0.5), (0.5, 0.5), 6, 0),
    (0, 1.10, 1.0, (0.5, 0.5), (0.5, 0.5), 0, 0),
]


def label_texts(i, t0, t1, t):
    """Name / price flash under the garment (never over it)."""
    out = []
    if not (t0 <= t < t1):
        return out
    x, y = 90, 1285
    rows = [
        (f"0{i + 1} / 05", 32, 8, (150, 150, 156), y),
        (LABELS[i][0], 64, 2, (255, 255, 255), y + 48),
        (LABELS[i][1], 64, 2, (255, 255, 255), y + 122),
        (LABELS[i][2], 100, 1, (255, 255, 255), y + 204),
    ]
    for j, (s, size, tr, col, yy) in enumerate(rows):
        q = p(t, t0 + j * 1.5, t0 + j * 1.5 + 4)
        out.append((s, size, tr, col, x - 30 * (1 - eo_expo(q)), yy, min(1, q * 2), eo_cubic(q), "l"))
    return out


def scene(t):
    """Everything on screen at (fractional) frame t."""
    L, T = [], []  # layers: (gid, X, Y, s, rot, fu, fv, op); texts
    flash, shake, tint = 0.0, 0.0, None

    def hit(at, strength=1.0, dur=6, fl=1.0):
        nonlocal flash, shake
        if at <= t < at + dur:
            q = (t - at) / dur
            flash = max(flash, 0.38 * strength * fl * (1 - q) ** 3)
            shake = max(shake, 18 * strength * (1 - q) ** 2)

    if t < 60:  # ---- intro: tight moving detail -> fast pull back
        if t < 22:
            q = t / 22
            s, fu, fv, Y = 3.0 + 0.2 * q, lerp(0.40, 0.55, q), 0.37, 960
        else:
            q = eio_expo(p(t, 22, 40))
            s = lerp(3.2, 1.0, q) + 0.02 * p(t, 40, 60)
            fu, fv = lerp(0.55, 0.5, q), lerp(0.37, 0.5, q)
            Y = lerp(960, HERO_Y, q)
        L.append((0, 540, Y, s, 0, fu, fv, 1))
        hit(0, 0.8, 8, fl=0.0)
        hit(38, 0.8)
        q = p(t, 34, 38)
        T.append(("404 CULTURE", 128, 4, (255, 255, 255), 540, 1290 + 40 * (1 - eo_expo(q)),
                  min(1, q * 2), 1, "c"))
        q = p(t, 41, 46)
        T.append(("NEW COLLECTION", 54, 16, (205, 205, 210), 540, 1440, min(1, q * 2), eo_cubic(q), "c"))
    elif t < 105:  # ---- 01 black thermal: slow push, whip out left
        s = lerp(1.02, 1.08, p(t, 60, 97))
        X = 540 - 1800 * ei_expo(p(t, 96, 105))
        L.append((0, X, HERO_Y, s, lerp(0, -1.5, p(t, 60, 97)), 0.5, 0.5, 1))
        T += label_texts(0, 60, 97, t)
    elif t < 143:  # ---- 02 red crewneck: whip in from right, punch into print
        q = eo_expo(p(t, 105, 114))
        X = 540 + 1800 * (1 - q)
        qi = ei_expo(p(t, 134, 143))
        s = lerp(lerp(1.0, 1.05, p(t, 114, 134)), 3.8, qi)
        L.append((1, X, lerp(HERO_Y, 960, qi), s, 0, 0.5, lerp(0.5, 0.38, qi), 1))
        T += label_texts(1, 108, 134, t)
    elif t < 188:  # ---- 03 cream thermal: match-cut out of a print close-up, spin out
        q = eo_expo(p(t, 143, 157))
        qo = ei_cubic(p(t, 179, 188))
        s = lerp(3.8, 1.0, q) + 0.04 * p(t, 157, 179)
        s *= lerp(1, 0.05, qo)
        fu, fv = lerp(0.49, 0.5, q), lerp(0.27, 0.5, q)
        L.append((2, 540, lerp(960, HERO_Y, q), s, -110 * qo, fu, fv, 1))
        T += label_texts(2, 154, 179, t)
        hit(143, 0.5)
    elif t < 225:  # ---- 04 baby blue tee: spin in
        q = p(t, 188, 201)
        s = lerp(0.2, 1.0, eo_back(q)) + 0.04 * p(t, 201, 225) if q < 1 else 1.0 + 0.04 * p(t, 201, 225)
        L.append((3, 540, HERO_Y, s, 90 * (1 - eo_expo(q)), 0.5, 0.5, 1))
        T += label_texts(3, 197, 225, t)
        hit(199, 0.5)
    elif t < 270:  # ---- 05 navy/red tee: hard match-cut colour swap, punch out
        s = 1.04 + 0.08 * (1 - eo_cubic(p(t, 225, 232))) + 0.04 * p(t, 232, 262)
        qi = ei_expo(p(t, 262, 270))
        s = lerp(s, 2.8, qi)
        L.append((4, 540, lerp(HERO_Y, 960, qi), s, 0, 0.5, lerp(0.5, 0.47, qi), 1))
        T += label_texts(4, 225, 262, t)
        hit(225, 0.8)
    elif t < 330:  # ---- montage on 8th notes
        k = min(int((t - 270) / 7.5), 7)
        u = (t - 270 - 7.5 * k) / 7.5
        g, s0, s1, f0, f1, r0, r1 = MONTAGE[k]
        ue = eo_cubic(u)
        L.append((g, 540, 960, lerp(s0, s1, ue), lerp(r0, r1, eo_expo(u)),
                  lerp(f0[0], f1[0], u), lerp(f0[1], f1[1], u), 1))
        hit(270 + 7.5 * k, 0.45, 4)
    else:  # ---- collection shot + end card
        for n, (g, x, y, w, dx, dy, dr) in enumerate(COLL):
            q = eo_expo(p(t, 330 + 2 * n, 345))
            bob = 3 * math.sin((t - 345) / 14 + n) * p(t, 345, 360)
            bump = 1 + 0.035 * (1 - eo_cubic(p(t, 405, 413))) * (t >= 405)
            L.append((g, lerp(x + dx, x, q) + (x - 540) * (bump - 1),
                      lerp(y + dy, y, q) + COLL_Y + bob + (y - 660) * (bump - 1),
                      w / FIT * bump, dr * (1 - q), 0.5, 0.5, 1 if t >= 330 + 2 * n else 0))
        hit(345, 1.0, 8, fl=0.6)
        info = [("100% PREMADE", 360), ("100% COTTON", 367.5), ("3–5 DAY SHIPPING", 375)]
        for j, (s, at) in enumerate(info):
            q = p(t, at, at + 5)
            T.append((s, 52, 6, (205, 205, 210), 540, 1085 + 68 * j + 20 * (1 - eo_expo(q)),
                      min(1, 2 * q), 1, "c"))
        q = p(t, 382.5, 388)
        T.append(("COLLECTION LIVE NOW", 70, 4, (255, 255, 255), 540, 1300 + 20 * (1 - eo_expo(q)),
                  min(1, 2 * q), eo_cubic(q), "c"))
        q = p(t, 405, 408)
        T.append(("404 CULTURE", 140, 4, (255, 255, 255), 540, 1420 + 30 * (1 - eo_expo(q)),
                  min(1, 2 * q), 1, "c"))
        q = p(t, 412, 418)
        T.append(("404cultureclothing.com", 46, 3, (205, 205, 210), 540, 1590, min(1, 2 * q), eo_cubic(q), "c"))
        hit(405, 1.2, 10)
        tint = (58, 58, 62)

    if shake > 0:
        sx = shake * math.sin(t * 7.1)
        sy = shake * math.cos(t * 5.3)
        L = [(g, X + sx, Y + sy, s, r, fu, fv, op) for g, X, Y, s, r, fu, fv, op in L]
        T = [tt[:4] + (tt[4] + sx * 0.5, tt[5] + sy * 0.5) + tt[6:] for tt in T]
    return L, T, flash, tint


# ---------------------------------------------------------------- compositing

def compose(t):
    L, T, flash, tint = scene(t)
    # background: dark neutral with a soft key light tinted by the hero garment
    if tint is None and L:
        m = G[L[0][0]].mean
        tint = 0.72 * np.array([56, 56, 60]) + 0.28 * m
    tint = np.array(tint if tint is not None else (56, 56, 60), np.float32)
    xx, yy = BG_FALLOFF
    cy = 820
    d2 = ((xx - 540) / 620) ** 2 + ((yy - cy) / 820) ** 2
    spot = np.exp(-d2 * 1.4)[..., None]
    frame = np.empty((H, W, 3), np.float32)
    frame[:] = np.array([11, 11, 13], np.float32)
    frame += spot * tint

    rendered = [(render_garment(G[g], X, Y, s, r, fu, fv), op) for g, X, Y, s, r, fu, fv, op in L if op > 0]
    rendered = [(rg, op) for rg, op in rendered if rg is not None]

    # contact + drop shadows (hard, low; soft, wide)
    if rendered:
        sh = np.zeros((H // 2, W // 2), np.float32)
        for (b, _, a), op in rendered:
            x0, y0, x1, y1 = b
            a2 = np.asarray(Image.fromarray(a[..., 0] * op).resize(((x1 - x0) // 2 or 1, (y1 - y0) // 2 or 1)))
            ox, oy = x0 // 2 + 6, y0 // 2 + 22
            hh, ww = a2.shape
            hh, ww = min(hh, H // 2 - oy), min(ww, W // 2 - ox)
            if hh > 0 and ww > 0:
                sh[oy:oy + hh, ox:ox + ww] = np.maximum(sh[oy:oy + hh, ox:ox + ww], a2[:hh, :ww])
        shimg = Image.fromarray((np.clip(sh, 0, 1) * 255).astype(np.uint8))
        soft = np.asarray(shimg.filter(ImageFilter.GaussianBlur(26)), np.float32)
        hard = np.asarray(shimg.filter(ImageFilter.GaussianBlur(6)), np.float32)
        shadow = np.clip(0.55 * soft + 0.35 * hard, 0, 0.85 * 255).astype(np.uint8)
        shadow = np.asarray(Image.fromarray(shadow).resize((W, H), Image.BILINEAR), np.float32)[..., None] / 255
        frame *= 1 - shadow

    frame *= VIGNETTE ** 0.9  # light falloff on the set only
    for (b, rgb, a), op in rendered:
        x0, y0, x1, y1 = b
        reg = frame[y0:y1, x0:x1]
        reg *= 1 - a * op
        reg += rgb * op

    for s, size, tr, col, x, y, alpha, reveal, anchor in T:
        draw_text(frame, s, size, tr, col, x, y, alpha, reveal, anchor)
    if flash > 0:
        frame += (255 - frame) * flash
    return frame


BLUR_SAMPLES = 11


def render_frame(f):
    n = 1
    for a, b in BLUR:
        if a <= f < b:
            n = BLUR_SAMPLES
    if n == 1:
        acc = compose(float(f))
    else:
        acc = sum(compose(f - 0.5 + (i + 0.5) / n) for i in range(n)) / n
    acc += GRAIN[f % len(GRAIN)] * 4.0
    return np.clip(acc + 0.5, 0, 255).astype(np.uint8).tobytes()


def ffmpeg_exe():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        return "ffmpeg"


def main():
    args = sys.argv[1:]
    step = 1
    if "--preview" in args:
        i = args.index("--preview")
        step = int(args[i + 1])
        del args[i:i + 2]
    out = args[0] if args else os.path.join(HERE, "build", "video_only.mp4")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    frames = list(range(0, N, step))
    if step > 1:  # contact sheet frames as PNGs
        load()
        for f in frames:
            Image.frombytes("RGB", (W, H), render_frame(f)).save(out.replace(".mp4", f"_{f:03d}.png"))
        return
    cmd = [ffmpeg_exe(), "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "slow",
           "-crf", "15", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with Pool(os.cpu_count(), initializer=load) as pool:
        for k, buf in enumerate(pool.imap(render_frame, frames, chunksize=2)):
            proc.stdin.write(buf)
            if k % 30 == 0:
                print(f"frame {k}/{len(frames)}", flush=True)
    proc.stdin.close()
    proc.wait()


if __name__ == "__main__":
    main()
