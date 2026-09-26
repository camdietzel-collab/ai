"""404 CULTURE - Tiger League tees, 15s 9:16 motion promo.

Reuses the campaign renderer (garment cutouts, shadows, grain, motion blur)
with its own timeline: both tees slide in side by side, then the camera flies
into each one for close-up feature details, and both return for the end card.
Garments are only moved, scaled and rotated; their pixels are the original
product photos.

usage: python3 promo.py            -> build/video_only.mp4
       python3 promo.py --frames 0,90,200   -> build/still_XXX.png
"""
import math
import os
import subprocess
import sys
from multiprocessing import Pool

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "campaign"))
import render as R  # noqa: E402

from render import clamp01, draw_text, eio_expo, eo_cubic, eo_expo, lerp, p  # noqa: E402,F401

N = 450
BLUE, NAVY = 3, 4  # campaign cutouts 4.png / 5.png
PAIR_W = 480 / R.FIT  # each tee's scale when shown side by side

# (start, end) frames of every fast move -> multi-sample motion blur

# per tee: hero hold, then 4 detail stops (focus u, v in the cutout, scale, callout)
TOUR = {
    BLUE: dict(t0=75, name=("BABY BLUE", "TIGER LEAGUE TEE", "$39.99"), stops=[
        ((0.50, 0.49), 3.00, "DISTRESSED TIGER CREST"),
        ((0.50, 0.30), 2.50, "404 CULTURE ARCH"),
        ((0.07, 0.50), 3.20, "LAYERED SLEEVE CUFFS"),
        ((0.30, 0.93), 3.00, "DOUBLE-LAYER HEM"),
    ]),
    NAVY: dict(t0=225, name=("NAVY / RED", "TIGER LEAGUE TEE", "$39.99"), stops=[
        ((0.50, 0.08), 2.70, "CONTRAST RINGER COLLAR"),
        ((0.50, 0.49), 3.00, "RED TIGER CREST"),
        ((0.93, 0.50), 3.20, "RED LAYERED SLEEVES"),
        ((0.70, 0.93), 3.00, "RED LAYERED HEM"),
    ]),
}
HERO = 22     # frames of the full-tee hero before the first detail
STOP = 30     # frames per detail stop (one beat pair at 120 BPM)
MOVE = 8      # frames of each fly between stops; every landing is on a beat
HERO_Y = 790


def stop_starts(g):
    c = TOUR[g]
    return [c["t0"]] + [c["t0"] + HERO + k * STOP for k in range(len(c["stops"]))]


# (start, end) frames of every fast move -> multi-sample motion blur
BLUR = [(0, 16), (60, 76), (219, 232), (374, 392)] + [
    (st - 1, st + MOVE + 1) for g in TOUR for st in stop_starts(g)[1:]]


def label(name, t0, t1, t):
    if not (t0 <= t < t1):
        return []
    x, y = 90, 1290
    rows = [(name[0], 64, 2, (255, 255, 255), y), (name[1], 64, 2, (255, 255, 255), y + 74),
            (name[2], 100, 1, (255, 255, 255), y + 156)]
    out = []
    for j, (s, size, tr, col, yy) in enumerate(rows):
        q = p(t, t0 + j * 1.5, t0 + j * 1.5 + 4)
        out.append((s, size, tr, col, x - 30 * (1 - eo_expo(q)), yy, min(1, q * 2), eo_cubic(q), "l"))
    return out


def callout(s, t0, t1, t):
    """Feature name, low in frame, with a short accent rule."""
    if not (t0 <= t < t1):
        return []
    q = p(t, t0, t0 + 5)
    k = 1 - p(t, t1 - 3, t1)
    return [("—", 60, 0, (255, 255, 255), 90, 1600, min(q * 2, k), 1, "band"),
            (s, 56, 4, (255, 255, 255), 165, 1606 + 12 * (1 - eo_expo(q)), min(q * 2, k), eo_cubic(q), "band")]


def tour(g, t):
    """Camera on one tee: hero, then fly between detail stops."""
    c = TOUR[g]
    t0 = c["t0"]
    states = [((0.5, 0.5), 1.0, None)] + c["stops"]
    starts = stop_starts(g)
    T = []
    k = max(i for i, s in enumerate(starts) if t >= s)
    (fu, fv), s, name = states[k]
    local = t - starts[k]
    # fly in from the previous stop
    if k > 0 and local < MOVE:
        (pu, pv), ps, _ = states[k - 1]
        q = eio_expo(local / MOVE)
        fu, fv, s = lerp(pu, fu, q), lerp(pv, fv, q), lerp(ps, s, q)
    else:
        s *= 1 + 0.04 * p(local, MOVE, STOP)  # slow push while holding
    rot = 2.5 * math.sin((t - t0) / 18 + g)
    X = 540 + 6 * math.sin(t / 11)
    Y = lerp(HERO_Y, 960, min(1.0, (s - 1.0) / 0.8)) if s > 1 else HERO_Y
    if k == 0:
        T += label(c["name"], t0 + 2, starts[1], t)
    else:
        T += callout(name, starts[k] + MOVE - 2, starts[k] + STOP if k < len(starts) - 1 else starts[k] + STOP, t)
    return (g, X, Y, s, rot, fu, fv, 1), T, starts


def scene(t):
    L, T = [], []
    flash, shake, tint = 0.0, 0.0, None

    def hit(at, strength=1.0, dur=6):
        nonlocal flash, shake
        if at <= t < at + dur:
            q = (t - at) / dur
            flash = max(flash, 0.3 * strength * (1 - q) ** 3)
            shake = max(shake, 16 * strength * (1 - q) ** 2)

    if t < 75:  # ---- opening slide: both tees slide in side by side
        qa, qb = eo_expo(p(t, 0, 14)), eo_expo(p(t, 3, 16))
        bob = 6 * math.sin(t / 9)
        fly = eio_expo(p(t, 60, 75))
        s_pair = PAIR_W * (1 + 0.03 * p(t, 16, 60))
        L.append((BLUE, lerp(lerp(-600, 290, qa), 540, fly), lerp(830 + bob, HERO_Y, fly),
                  lerp(s_pair, 1.0, fly), lerp(-25 * (1 - qa), 0, fly), 0.5, 0.5, 1))
        L.append((NAVY, lerp(1680, 790, qb) + 1100 * fly, 830 - bob, s_pair, 25 * (1 - qb) + 20 * fly, 0.5, 0.5, 1))
        hit(14, 0.8)
        if t < 60:
            q1, q2, q3 = p(t, 10, 15), p(t, 16, 21), p(t, 22, 27)
            T.append(("404 CULTURE", 40, 14, (170, 170, 176), 540, 470, min(1, q1 * 2), eo_cubic(q1), "c"))
            T.append(("TIGER LEAGUE", 118, 4, (255, 255, 255), 540, 1110 + 30 * (1 - eo_expo(q2)), min(1, q2 * 2), 1, "c"))
            T.append(("OUT NOW", 60, 18, (255, 255, 255), 540, 1260, min(1, q3 * 2), eo_cubic(q3), "c"))
    elif t < 225:  # ---- baby blue tour
        lay, T2, starts = tour(BLUE, t)
        g, X, Y, s, rot, fu, fv, op = lay
        # exit: whip left into the navy tee
        qx = eio_expo(p(t, 219, 225))
        L.append((g, X - 1500 * qx, Y, s, rot, fu, fv, op))
        T += T2
        for st in starts[1:]:
            hit(st + MOVE, 0.35, 4)
    elif t < 375:  # ---- navy tour
        lay, T2, starts = tour(NAVY, t)
        g, X, Y, s, rot, fu, fv, op = lay
        qx = 1 - eo_expo(p(t, 225, 232))
        L.append((g, X + 1500 * qx, Y, s, rot, fu, fv, op))
        T += T2
        for st in starts[1:]:
            hit(st + MOVE, 0.35, 4)
    else:  # ---- both tees fly back together + end card
        qa, qb = eo_expo(p(t, 375, 391)), eo_expo(p(t, 377, 391))
        bob = 5 * math.sin(t / 10) * p(t, 391, 405)
        s_pair = PAIR_W * (1 + 0.025 * p(t, 391, 450))
        L.append((BLUE, lerp(-700, 290, qa), 700 + bob, lerp(1.6, s_pair, qa), -30 * (1 - qa), 0.5, 0.5, 1))
        L.append((NAVY, lerp(1800, 790, qb), 700 - bob, lerp(1.6, s_pair, qb), 30 * (1 - qb), 0.5, 0.5, 1))
        hit(391, 1.0, 8)
        hit(420, 1.1, 10)
        rows = [("TIGER LEAGUE TEES", 84, 4, (255, 255, 255), 1000, 395),
                ("$39.99", 76, 2, (255, 255, 255), 1108, 400),
                ("PREMADE · 100% COTTON · 3–5 DAY SHIPPING", 36, 4, (200, 200, 205), 1216, 406),
                ("404 CULTURE", 130, 4, (255, 255, 255), 1400, 420),
                ("404cultureclothing.com", 46, 3, (200, 200, 205), 1560, 426)]
        for s, size, tr, col, y, at in rows:
            q = p(t, at, at + 5)
            T.append((s, size, tr, col, 540, y + 18 * (1 - eo_expo(q)), min(1, 2 * q), 1, "c"))
        tint = (56, 56, 60)

    if shake > 0:
        sx, sy = shake * math.sin(t * 7.1), shake * math.cos(t * 5.3)
        L = [(g, X + sx, Y + sy, s, r, fu, fv, op) for g, X, Y, s, r, fu, fv, op in L]
    return L, T, flash, tint


BAND = None


def compose(t):
    """Campaign compositor + a dark lower-third behind feature callouts."""
    global BAND
    L, T, flash, tint = scene(t)
    band = [x for x in T if x[8] == "band"]
    R.scene = lambda _t: (L, [x for x in T if x[8] != "band"], flash, tint)
    frame = ORIG_COMPOSE(t)
    if band:
        if BAND is None:
            y = np.arange(R.H, dtype=np.float32)
            BAND = (np.exp(-((y - 1640) / 150) ** 2) * 0.8)[:, None, None]
        frame *= 1 - BAND * max(x[6] for x in band)
        for s, size, tr, col, x, y, alpha, reveal, _ in band:
            draw_text(frame, s, size, tr, col, x, y, alpha, reveal, "l")
    return frame


ORIG_COMPOSE = R.compose


def setup():
    R.load()
    R.compose = compose
    R.BLUR = BLUR
    R.BLUR_SAMPLES = 16


def main():
    out_dir = os.path.join(HERE, "build")
    os.makedirs(out_dir, exist_ok=True)
    if "--frames" in sys.argv:
        setup()
        for f in [int(v) for v in sys.argv[sys.argv.index("--frames") + 1].split(",")]:
            Image.frombytes("RGB", (R.W, R.H), R.render_frame(f)).save(os.path.join(out_dir, f"still_{f:03d}.png"))
        return
    out = os.path.join(out_dir, "video_only.mp4")
    cmd = [R.ffmpeg_exe(), "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{R.W}x{R.H}", "-r", "30", "-i", "-", "-c:v", "libx264", "-preset", "slow",
           "-crf", "16", "-pix_fmt", "yuv420p", out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with Pool(os.cpu_count(), initializer=setup) as pool:
        for buf in pool.imap(R.render_frame, range(N), chunksize=2):
            proc.stdin.write(buf)
    proc.stdin.close()
    proc.wait()
    print("wrote", out)


if __name__ == "__main__":
    main()
