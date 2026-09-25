"""Render the 15s "order to outfit" ad.

    python3 assemble.py                 # -> 404_culture_order_to_outfit[_animatic]_15s.mp4
    python3 assemble.py --frames 0,60   # stills for review -> build/still_XXX.png

Filmed shots come from footage/<CODE>.(mp4|mov|m4v) when present and fall back
to storyboard cards otherwise, so the same command renders the animatic now and
the finished ad once the clips are in. Per-clip edit settings live in
footage/edit.json (see SHOT_LIST.md).
"""
import json
import math
import os
import subprocess
import sys
from functools import lru_cache
from multiprocessing import Pool

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import config as C

W, H = C.W, C.H
S_W, S_H = 1170, 2532           # phone screen px (390 x 844 css @3x)
STATUS_H, BROWSER_H = 141, 249  # css 47 / 83
WEB_H = S_H - STATUS_H - BROWSER_H
BEZEL, CORNER = 54, 170
D_W, D_H = S_W + 2 * BEZEL, S_H + 2 * BEZEL


# ---------------------------------------------------------------- utils

def ffmpeg():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        return "ffmpeg"


def clamp01(x):
    return max(0.0, min(1.0, x))


def p(t, a, b):
    return clamp01((t - a) / (b - a))


def lerp(a, b, q):
    return a + (b - a) * q


def eo(x, k=3):
    return 1 - (1 - x) ** k


def eio(x):
    return 3 * x * x - 2 * x * x * x


def spring(x):
    """0 -> 1 with a little overshoot."""
    if x >= 1:
        return 1.0
    return 1 - math.exp(-6.5 * x) * math.cos(9.0 * x)


@lru_cache(maxsize=None)
def font(size, bold=True):
    return ImageFont.truetype(C.FONT_BOLD if bold else C.FONT_REG, size)


def text_w(d, s, f, track=0):
    return sum(d.textlength(c, font=f) for c in s) + track * (len(s) - 1)


def draw_tracked(d, xy, s, f, fill, track=0, anchor="l"):
    x, y = xy
    if anchor == "c":
        x -= text_w(d, s, f, track) / 2
    elif anchor == "r":
        x -= text_w(d, s, f, track)
    for ch in s:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + track


def handheld(t, amp=1.0, seed=0.0):
    """Smooth pseudo-random camera drift, in px and degrees."""
    s = seed * 1.7
    dx = (math.sin(t * 1.9 + s) * 0.6 + math.sin(t * 4.3 + 2 * s) * 0.3 + math.sin(t * 9.7 + s) * 0.1) * amp
    dy = (math.sin(t * 1.6 + 1 + s) * 0.6 + math.sin(t * 3.7 + s) * 0.3 + math.sin(t * 8.9 + 3 * s) * 0.1) * amp
    rot = (math.sin(t * 1.3 + s) * 0.7 + math.sin(t * 5.1 + s) * 0.3) * amp * 0.08
    return dx, dy, rot


# ---------------------------------------------------------------- 3D camera onto a flat device

def homography(src, dst):
    """Coefficients mapping dst(x,y) -> src(u,v) for PIL PERSPECTIVE."""
    A, b = [], []
    for (u, v), (x, y) in zip(src, dst):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y])
        b += [u, v]
    return np.linalg.solve(np.array(A, float), np.array(b, float)).tolist()


def project(size, cam):
    """Frame coords of the 4 corners of a size=(w,h) plane under camera cam."""
    w, h = size
    cu, cv, z = cam["cx"], cam["cy"], cam["zoom"]
    r, pit, yaw = (math.radians(cam.get(k, 0.0)) for k in ("roll", "pitch", "yaw"))
    F = 2400.0
    ox, oy = cam.get("ox", 0.0), cam.get("oy", 0.0)
    out = []
    for u, v in ((0, 0), (w, 0), (w, h), (0, h)):
        X, Y, Z = (u - cu) * z, (v - cv) * z, 0.0
        X, Y = X * math.cos(r) - Y * math.sin(r), X * math.sin(r) + Y * math.cos(r)
        Y, Z = Y * math.cos(pit) - Z * math.sin(pit), Y * math.sin(pit) + Z * math.cos(pit)
        X, Z = X * math.cos(yaw) + Z * math.sin(yaw), -X * math.sin(yaw) + Z * math.cos(yaw)
        out.append((W / 2 + ox + F * X / (F + Z), H / 2 + oy + F * Y / (F + Z)))
    return out


def warp(img, cam):
    corners = project(img.size, cam)
    w, h = img.size
    coeffs = homography([(0, 0), (w, 0), (w, h), (0, h)], corners)
    return img.transform((W, H), Image.PERSPECTIVE, coeffs, Image.BICUBIC), corners


@lru_cache(maxsize=None)
def device_mask():
    m = Image.new("L", (D_W, D_H), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, D_W - 1, D_H - 1], CORNER + BEZEL, fill=255)
    s = Image.new("L", (S_W, S_H), 0)
    ImageDraw.Draw(s).rounded_rectangle([0, 0, S_W - 1, S_H - 1], CORNER, fill=255)
    return m, s


def device(screen, brightness=1.0):
    """Phone body with the screen content inset."""
    body_mask, screen_mask = device_mask()
    dev = Image.new("RGBA", (D_W, D_H), (0, 0, 0, 0))
    body = Image.new("RGBA", (D_W, D_H), (14, 14, 16, 255))
    dev.paste(body, (0, 0), body_mask)
    # thin metal rim highlight
    rim = Image.new("L", (D_W, D_H), 0)
    ImageDraw.Draw(rim).rounded_rectangle([3, 3, D_W - 4, D_H - 4], CORNER + BEZEL - 3, outline=90, width=5)
    dev.paste(Image.new("RGBA", (D_W, D_H), (120, 120, 126, 255)), (0, 0), rim)
    scr = screen.convert("RGB")
    if brightness != 1.0:
        a = np.asarray(scr).astype(np.float32) * brightness
        scr = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    dev.paste(scr, (BEZEL, BEZEL), screen_mask)
    return dev


# ---------------------------------------------------------------- backgrounds

@lru_cache(maxsize=None)
def room_bg():
    """Dim interior with soft warm bokeh (behind the customer's phone)."""
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    a = np.zeros((H, W, 3), np.float32)
    a[:] = np.array([16, 14, 13], np.float32)
    a += (1 - yy / H)[..., None] * np.array([14, 11, 9], np.float32)
    rng = np.random.default_rng(7)
    for _ in range(9):
        cx, cy, r = rng.uniform(0, W), rng.uniform(0, H * 0.7), rng.uniform(60, 190)
        col = np.array(rng.choice([[255, 190, 120], [255, 220, 170], [200, 170, 140]]), np.float32)
        d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
        a += (np.clip(1 - d / r, 0, 1) ** 0.6 * rng.uniform(0.04, 0.10))[..., None] * col
    img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(30))
    return np.asarray(img).astype(np.float32)


@lru_cache(maxsize=None)
def desk_bg():
    """Matte dark desk under the owner's phone."""
    rng = np.random.default_rng(11)
    n = rng.normal(0, 1, (H // 4, W // 4)).astype(np.float32)
    n = np.asarray(Image.fromarray(n).resize((W, H), Image.BICUBIC))
    fine = rng.normal(0, 1, (H, W)).astype(np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    base = 24 + 5 * n + 2.2 * fine - 10 * ((yy / H - 0.4) ** 2 + ((xx / W - 0.5) * 0.8) ** 2)
    a = np.stack([base * 1.02, base, base * 0.97], axis=-1)
    return np.clip(a, 0, 255)


# ---------------------------------------------------------------- phone UI chrome

def status_bar(time_text, dark_text=True, bg=(255, 255, 255, 255)):
    im = Image.new("RGBA", (S_W, STATUS_H), bg)
    d = ImageDraw.Draw(im)
    ink = (0, 0, 0, 255) if dark_text else (255, 255, 255, 255)
    draw_tracked(d, (104, 42), time_text, font(51), ink)
    x = S_W - 110
    d.rounded_rectangle([x, 48, x + 76, 84], 11, outline=ink, width=4)
    d.rounded_rectangle([x + 8, 56, x + 58, 76], 5, fill=ink)
    d.rounded_rectangle([x + 80, 60, x + 85, 72], 2, fill=ink)
    wx = x - 62  # wifi
    for r in (34, 23, 12):
        d.arc([wx - r, 82 - r, wx + r, 82 + r], 225, 315, fill=ink, width=6)
    sx = wx - 120  # signal
    for k in range(4):
        h = 12 + k * 8
        d.rounded_rectangle([sx + k * 17, 84 - h, sx + k * 17 + 11, 84], 3, fill=ink)
    return im


@lru_cache(maxsize=None)
def browser_bar():
    im = Image.new("RGBA", (S_W, BROWSER_H), (246, 246, 246, 255))
    d = ImageDraw.Draw(im)
    d.line([0, 0, S_W, 0], fill=(222, 222, 222, 255), width=3)
    d.rounded_rectangle([36, 30, S_W - 36, 150], 42, fill=(255, 255, 255, 255))
    f = font(45, bold=False)
    tw = text_w(d, C.SITE_URL, f)
    lock_x = S_W / 2 - tw / 2 - 40
    d.rounded_rectangle([lock_x - 12, 86, lock_x + 12, 112], 4, fill=(60, 60, 60, 255))
    d.arc([lock_x - 9, 68, lock_x + 9, 96], 180, 360, fill=(60, 60, 60, 255), width=4)
    d.text((S_W / 2 - tw / 2 + 4, 66), C.SITE_URL, font=f, fill=(20, 20, 20, 255))
    d.rounded_rectangle([S_W / 2 - 201, BROWSER_H - 40, S_W / 2 + 201, BROWSER_H - 25], 8, fill=(10, 10, 10, 255))
    return im


def touch(img, x, y, t, tap_t):
    """Translucent fingertip contact + release ripple (screen px)."""
    dt = t - tap_t
    if dt < -0.12 or dt > 0.34:
        return img
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    if dt < 0:
        q = (dt + 0.12) / 0.12
        r, a = lerp(74, 60, q), 0.35 * q
    elif dt < 0.07:
        r, a = 56, 0.45
    else:
        q = (dt - 0.07) / 0.27
        r, a = 56, 0.45 * (1 - q)
        rr = lerp(56, 150, eo(q))
        d.ellipse([x - rr, y - rr, x + rr, y + rr], outline=(255, 255, 255, int(200 * (1 - q))), width=6)
    d.ellipse([x - r, y - r, x + r, y + r], fill=(35, 35, 38, int(255 * a)),
              outline=(255, 255, 255, int(255 * min(1, a * 1.6))), width=5)
    return Image.alpha_composite(img, ov)


# ---------------------------------------------------------------- screens

class Screens:
    def __init__(self):
        d = C.SCREENS
        if not os.path.exists(os.path.join(d, "meta.json")):
            raise SystemExit("run capture_site.py first (build/screens missing)")
        self.meta = json.load(open(os.path.join(d, "meta.json")))
        load = lambda n: Image.open(os.path.join(d, n)).convert("RGB")
        self.collection = load("collection.png")
        self.product = load("product.png")
        self.product_size = load("product_size.png")
        self.product_add = load("product_add_pressed.png")
        self.cart = load("cart.png")
        self.cart_pressed = load("cart_pressed.png")
        self.status = status_bar("4:03")

    def css(self, bx, scroll=0.0):
        """Centre of a meta box in screen px."""
        return (bx["x"] + bx["w"] / 2) * 3, STATUS_H + (bx["y"] + bx["h"] / 2 - scroll) * 3

    def compose(self, web):
        scr = Image.new("RGBA", (S_W, S_H), (255, 255, 255, 255))
        scr.paste(web.crop((0, 0, S_W, WEB_H)), (0, STATUS_H))
        scr.alpha_composite(self.status, (0, 0))
        scr.alpha_composite(browser_bar(), (0, S_H - BROWSER_H))
        return scr

    def collection_view(self, scroll):
        y = int(round(scroll * 3))
        y = max(0, min(y, self.collection.height - WEB_H))
        return self.collection.crop((0, y, S_W, y + WEB_H))

    def max_scroll(self):
        return (self.collection.height - WEB_H) / 3

    def card_scroll(self):
        """Scroll position that parks the hero product card mid-screen."""
        c = self.meta["card"]
        return min(self.max_scroll(), c["y"] + c["h"] / 2 - self.meta["view"][1] * 0.52)

    def web_at(self, t):
        """Web content + tap overlays at absolute time t -> (screen RGBA)."""
        m = self.meta
        s_end = self.card_scroll()
        if t < 1.60:
            scroll = lerp(s_end - 360, s_end, eo(p(t, 0.72, 1.30), 4))
            scr = self.compose(self.collection_view(scroll))
            x, y = self.css(m["card"], s_end)
            return touch(scr, x, y, t, C.TAP_CARD)
        if t < 2.62:
            web = self.product
            if t >= C.TAP_SIZE + 0.03:
                web = self.product_size
            if C.TAP_ADD <= t < C.TAP_ADD + 0.08:
                web = self.product_add
            if t < 1.60 + 0.16:  # navigation push from the collection page
                q = eo(p(t, 1.60, 1.76))
                base = self.collection_view(s_end)
                out = Image.new("RGB", (S_W, WEB_H), (255, 255, 255))
                shift = int(S_W * (1 - q))
                dim = Image.eval(base, lambda v: int(v * (1 - 0.25 * q)))
                out.paste(dim.crop((0, 0, S_W, WEB_H)), (-int(S_W * 0.3 * q), 0))
                out.paste(web.crop((0, 0, S_W, WEB_H)), (shift, 0))
                web = out
            scr = self.compose(web)
            sx, sy = self.css(m["size"], 0)
            scr = touch(scr, sx, sy, t, C.TAP_SIZE)
            ax, ay = self.css(m["add"], 0)
            return touch(scr, ax, ay, t, C.TAP_ADD)
        # drawer slides in over the page
        q = eo(p(t, *C.DRAWER_IN), 4)
        cart = self.cart_pressed if t >= C.TAP_CHECKOUT else self.cart
        if q < 1:
            left = int(max(0, m["checkout"]["x"] - 18) * 3)
            edge = int(lerp(S_W, left, q))
            base = np.asarray(self.product_size.crop((0, 0, S_W, WEB_H))).astype(np.float32)
            base *= 1 - 0.42 * q
            out = Image.fromarray(base.astype(np.uint8))
            drawer = cart.crop((left, 0, S_W, WEB_H))
            out.paste(drawer, (edge, 0))
            web = out
        else:
            web = cart
        scr = self.compose(web)
        ax, ay = self.css(m["add"], 0)
        scr = touch(scr, ax, ay, t, C.TAP_ADD)
        cx, cy = self.css(m["checkout"], 0)
        return touch(scr, cx, cy, t, C.TAP_CHECKOUT)


SCREENS = None


def screens():
    global SCREENS
    if SCREENS is None:
        SCREENS = Screens()
    return SCREENS


def screen_cam(t):
    """Camera on the customer's phone for S1-S4 (device px, BEZEL offset)."""
    sc = screens()
    m = sc.meta
    B = BEZEL
    card = sc.css(m["card"], sc.card_scroll())
    size = sc.css(m["size"], 0)
    add = sc.css(m["add"], 0)
    chk = sc.css(m["checkout"], 0)
    if t < 1.60:     # S1: medium on the phone, drift in toward the card
        q = eio(p(t, 0.90, 1.60))
        cam = dict(cx=lerp(S_W / 2, lerp(S_W / 2, card[0], 0.35), q) + B,
                   cy=lerp(S_H * 0.50, lerp(S_H * 0.5, card[1], 0.45), q) + B,
                   zoom=lerp(0.80, 0.98, q), roll=lerp(-3.0, -1.5, q), yaw=lerp(7, 3, q), pitch=lerp(-5, -3, q))
    elif t < 2.40:   # S2: close on title / sizes
        q = eio(p(t, 1.60, 2.40))
        cam = dict(cx=lerp(S_W / 2, lerp(S_W / 2, size[0], 0.45), q) + B,
                   cy=lerp(size[1] - 420, size[1] - 170, q) + B,
                   zoom=lerp(0.88, 1.16, q), roll=lerp(2.0, 1.0, q), yaw=-4, pitch=-6)
    elif t < C.DRAWER_IN[0]:  # S3a: tight on "Add to cart" for the tap
        hold = p(t, 2.40, C.DRAWER_IN[0])
        cam = dict(cx=add[0] + 10 * hold + B, cy=add[1] - 60 - 30 * hold + B,
                   zoom=1.42 + 0.05 * hold, roll=-1.5, yaw=-3, pitch=-4)
    elif t < 3.20:   # S3b: cut to a medium as the cart drawer slides in
        q = p(t, C.DRAWER_IN[0], 3.20)
        cam = dict(cx=S_W * 0.57 + B, cy=lerp(S_H * 0.43, S_H * 0.41, q) + B,
                   zoom=lerp(0.95, 0.99, q), roll=-2.5, yaw=4, pitch=-4)
    else:            # S4: tight on the cart line, whip down to "Check out"
        item = sc.css(m["item"], 0)
        drift = p(t, 3.20, 3.62)
        q = eio(eio(p(t, 3.62, 3.73)))
        cam = dict(cx=lerp(item[0] - 240, chk[0] - 30, q) + B,
                   cy=lerp(item[1] + 90 + 25 * drift, chk[1] - 60, q) + B,
                   zoom=lerp(1.12 + 0.05 * drift, 1.32, q) + 0.05 * p(t, 3.74, 4.0),
                   roll=lerp(1.5, 0.5, q), yaw=3, pitch=-5)
    dx, dy, dr = handheld(t, 9.0)
    cam["ox"], cam["oy"] = dx, dy
    cam["roll"] += dr
    return cam


def glass(img, corners, strength=0.07, phase=0.0):
    """Faint diagonal glare over the glass."""
    xs = [c[0] for c in corners]
    ys = [c[1] for c in corners]
    band = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(band)
    cx = lerp(min(xs), max(xs), 0.3 + 0.2 * phase)
    d.polygon([(cx - 500, -100), (cx - 120, -100), (cx + 900, H + 100), (cx + 520, H + 100)], fill=int(255 * strength))
    band = band.filter(ImageFilter.GaussianBlur(90))
    poly = Image.new("L", (W, H), 0)
    ImageDraw.Draw(poly).polygon(corners, fill=255)
    a = (np.asarray(band).astype(np.float32) / 255 * np.asarray(poly).astype(np.float32) / 255)[..., None]
    return img + (255 - img) * a


def render_screen(t):
    sc = screens()
    scr = sc.web_at(t)
    dev = device(scr)
    cam = screen_cam(t)
    warped, corners = warp(dev, cam)
    frame = room_bg().copy()
    wa = np.asarray(warped).astype(np.float32)
    a = wa[..., 3:] / 255
    # soft contact shadow + screen glow on the room
    glow = Image.fromarray((a[..., 0] * 255).astype(np.uint8)).resize((W // 8, H // 8)).filter(ImageFilter.GaussianBlur(10))
    g = np.asarray(glow.resize((W, H), Image.BILINEAR)).astype(np.float32)[..., None] / 255
    frame += g * np.array([30, 30, 32], np.float32)
    frame = frame * (1 - a) + wa[..., :3] * a
    return glass(frame, corners, 0.06, p(t, 0.9, 4.0))


# ---------------------------------------------------------------- owner's phone

@lru_cache(maxsize=None)
def lock_wallpaper():
    yy, xx = np.mgrid[0:S_H, 0:S_W].astype(np.float32)
    a = np.zeros((S_H, S_W, 3), np.float32)
    top, bot = np.array([34, 36, 44], np.float32), np.array([8, 8, 11], np.float32)
    a[:] = top + (bot - top) * (yy / S_H)[..., None]
    d = np.sqrt((xx - S_W * 0.8) ** 2 + (yy - S_H * 0.15) ** 2)
    a += (np.clip(1 - d / 1400, 0, 1) ** 2)[..., None] * np.array([40, 36, 52], np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")


@lru_cache(maxsize=None)
def lock_base():
    im = lock_wallpaper().copy()
    d = ImageDraw.Draw(im)
    im.alpha_composite(status_bar("", dark_text=False, bg=(0, 0, 0, 0)), (0, 0))
    # padlock
    lx, ly = S_W / 2, 250
    d.rounded_rectangle([lx - 26, ly, lx + 26, ly + 40], 8, fill=(255, 255, 255, 235))
    d.arc([lx - 18, ly - 30, lx + 18, ly + 14], 180, 360, fill=(255, 255, 255, 235), width=7)
    f = font(300)
    draw_tracked(d, (S_W / 2, 330), C.NOTIFICATION["time"], f, (255, 255, 255, 245), track=-6, anchor="c")
    d.rounded_rectangle([S_W / 2 - 201, S_H - 40, S_W / 2 + 201, S_H - 25], 8, fill=(255, 255, 255, 230))
    return im


@lru_cache(maxsize=None)
def notif_card():
    w, h = S_W - 64, 246
    card = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(card)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 70, fill=(236, 236, 240, 232))
    ix, iy, isz = 42, 54, 138
    d.rounded_rectangle([ix, iy, ix + isz, iy + isz], 32, fill=(12, 12, 12, 255))
    f = font(52)
    tw = text_w(d, "404", f, -1)
    draw_tracked(d, (ix + isz / 2 - tw / 2, iy + 40), "404", f, (255, 255, 255, 255), -1)
    tx = ix + isz + 36
    d.text((tx, 58), C.NOTIFICATION["title"], font=font(50), fill=(10, 10, 10, 255))
    d.text((w - 150, 62), "now", font=font(42, bold=False), fill=(110, 110, 116, 255))
    d.text((tx, 128), C.NOTIFICATION["body"], font=font(47, bold=False), fill=(20, 20, 20, 255))
    return card


def render_notify(t):
    wake = p(t, C.NOTIFY_WAKE, C.NOTIFY_WAKE + 0.1)
    bright = 0.0 if t < C.NOTIFY_WAKE else lerp(0.0, 1.0, wake) * (1 + 0.12 * math.sin(math.pi * wake))
    scr = lock_base().copy()
    q = p(t, C.NOTIFY_IN, C.NOTIFY_IN + 0.32)
    if q > 0:
        card = notif_card()
        k = spring(q)
        cw, ch = card.size
        sc = lerp(0.88, 1.0, min(k, 1.05))
        cimg = card.resize((int(cw * sc), int(ch * sc)), Image.LANCZOS)
        a = np.asarray(cimg).astype(np.float32)
        a[..., 3] *= min(1.0, q * 3)
        cimg = Image.fromarray(a.astype(np.uint8))
        cy = int(lerp(900, 760, k))
        scr.alpha_composite(cimg, (int(S_W / 2 - cimg.width / 2), cy))
    dev = device(scr, brightness=max(bright, 0.0))
    # phone lying on the desk, camera at an angle; haptic buzz jitter
    buzz = 1.0 if C.NOTIFY_IN + 0.03 <= t < C.NOTIFY_IN + 0.3 else 0.0
    dx, dy, dr = handheld(t, 7.0, seed=3)
    q2 = eio(p(t, 4.0, 5.0))
    cam = dict(cx=D_W / 2 + lerp(-10, 10, q2), cy=lerp(820, 860, q2), zoom=lerp(0.90, 0.96, q2),
               roll=lerp(-4, -3, q2) + dr, pitch=16, yaw=-4,
               ox=dx + buzz * 5 * math.sin(t * 190), oy=dy + buzz * 4 * math.cos(t * 170))
    warped, corners = warp(dev, cam)
    frame = desk_bg().copy()
    wa = np.asarray(warped).astype(np.float32)
    a = wa[..., 3:] / 255
    sh = Image.fromarray((a[..., 0] * 255).astype(np.uint8)).resize((W // 8, H // 8)).filter(ImageFilter.GaussianBlur(6))
    sh = np.asarray(sh.resize((W, H), Image.BILINEAR)).astype(np.float32)[..., None] / 255
    frame *= 1 - 0.55 * np.roll(sh, 18, axis=0)
    # light spill from the screen onto the desk
    spill = Image.fromarray((a[..., 0] * 255).astype(np.uint8)).resize((W // 8, H // 8)).filter(ImageFilter.GaussianBlur(22))
    spill = np.asarray(spill.resize((W, H), Image.BILINEAR)).astype(np.float32)[..., None] / 255
    frame += spill * np.array([70, 70, 84], np.float32) * max(0.0, min(bright, 1.1))
    frame = frame * (1 - a) + wa[..., :3] * a
    return glass(frame, corners, 0.05, p(t, 4.0, 5.0))


# ---------------------------------------------------------------- product close-up + end card

@lru_cache(maxsize=None)
def product_plate():
    """Original product photo on its own studio backdrop, extended to 9:16."""
    im = Image.open(C.PRODUCT["photo"]).convert("RGB")
    bg = tuple(int(v) for v in np.asarray(im)[12, 12])
    return im, bg


def render_product(t):
    im, bg = product_plate()
    q = eio(p(t, 13.5, 14.0))
    cut = Image.open(C.PRODUCT["cutout"])
    fu, fv = C.PRODUCT["graphic_focus"]
    # focus point in photo coords (cutout bbox origin found by matching sizes)
    ox, oy = cutout_origin()
    fx, fy = ox + fu * cut.width, oy + fv * cut.height
    s = lerp(1.45, 1.62, q)
    dx, dy, _ = handheld(t, 4.0, seed=5)
    a = 1 / s
    data = (a, 0, fx - (W / 2 + dx) * a, 0, a, fy - (H / 2 + dy) * a)
    out = im.transform((W, H), Image.AFFINE, data, Image.BICUBIC, fillcolor=bg)
    return np.asarray(out).astype(np.float32)


@lru_cache(maxsize=None)
def cutout_origin():
    """Where the cutout sits inside the source photo (for focus maths)."""
    im = np.asarray(Image.open(C.PRODUCT["photo"]).convert("RGB")).astype(np.int16)
    bg = im[12, 12]
    diff = np.abs(im - bg).max(axis=2) > 40
    ys, xs = np.nonzero(diff)
    return int(xs.min()), int(ys.min())


def render_end(t):
    img = Image.new("RGB", (W, H), (11, 11, 12))
    d = ImageDraw.Draw(img)
    head, tag, url = C.END_CARD
    q1 = eo(p(t, 14.0, 14.12))
    q2 = eo(p(t, 14.06, 14.2))
    q3 = eo(p(t, 14.25, 14.4))
    y0 = 800
    col = lambda q, c: tuple(int(11 + (v - 11) * q) for v in c)
    draw_tracked(d, (W / 2, y0 + 24 * (1 - q1)), head, font(126), col(q1, (255, 255, 255)), track=4, anchor="c")
    draw_tracked(d, (W / 2, y0 + 180 + 16 * (1 - q2)), tag, font(50), col(q2, (225, 225, 228)), track=7, anchor="c")
    draw_tracked(d, (W / 2, y0 + 300), url, font(44, bold=False), col(q3, (170, 170, 176)), track=2, anchor="c")
    return np.asarray(img).astype(np.float32)


# ---------------------------------------------------------------- filmed shots

def footage_path(code):
    for ext in ("mp4", "mov", "MOV", "MP4", "m4v"):
        fp = os.path.join(C.FOOTAGE_DIR, f"{code}.{ext}")
        if os.path.exists(fp):
            return fp
    return None


def edit_settings():
    fp = os.path.join(C.FOOTAGE_DIR, "edit.json")
    return json.load(open(fp)) if os.path.exists(fp) else {}


def conform(shot, path, cfg):
    """Cut a clip to its slot once: in-point, speed, 9:16 reframe, exact frame count.

    Writes build/conform/<code>.mp4 at 30 fps. Speed < 1 is slow motion (film at
    60 fps for clean slow-mo); zoom/center reframe inside the 9:16 crop.
    """
    os.makedirs(os.path.join(C.BUILD, "conform"), exist_ok=True)
    out = os.path.join(C.BUILD, "conform", f"{shot['code']}.mp4")
    n = C.frame_of(shot["t1"]) - C.frame_of(shot["t0"])
    speed = float(cfg.get("speed", 1.0))
    zoom = float(cfg.get("zoom", 1.0))
    cx, cy = cfg.get("center", [0.5, 0.5])
    zw, zh = int(W * zoom) // 2 * 2, int(H * zoom) // 2 * 2
    vf = (f"setpts=(PTS-STARTPTS)/{speed},fps={C.FPS},"
          f"scale={zw}:{zh}:force_original_aspect_ratio=increase,"
          f"crop={W}:{H}:(iw-{W})*{cx}:(ih-{H})*{cy}" + (",hflip" if cfg.get("flip") else "") +
          ",tpad=stop_mode=clone:stop_duration=2")
    cmd = [ffmpeg(), "-y", "-v", "error", "-ss", f"{float(cfg.get('in', 0.0)):.3f}", "-i", path,
           "-an", "-vf", vf, "-frames:v", str(n), "-c:v", "libx264", "-crf", "12", "-preset", "fast",
           "-pix_fmt", "yuv420p", out]
    subprocess.run(cmd, check=True)
    return out


def conform_all():
    cfg = edit_settings()
    done = {}
    for s in C.SHOTS:
        if s["kind"] == "film":
            fp = footage_path(s["code"])
            if fp:
                done[s["code"]] = conform(s, fp, cfg.get(s["code"], {}))
                print(f"conformed {s['code']} <- {os.path.basename(fp)}")
    with open(os.path.join(C.BUILD, "conform.json"), "w") as fh:
        json.dump(done, fh)
    return done


@lru_cache(maxsize=1)
def conformed_frames(code):
    path = os.path.join(C.BUILD, "conform", f"{code}.mp4")
    raw = subprocess.run([ffmpeg(), "-v", "error", "-i", path, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    n = len(raw) // (W * H * 3)
    return np.frombuffer(raw[: n * W * H * 3], np.uint8).reshape(n, H, W, 3)


def footage_frame(shot, f):
    frames = conformed_frames(shot["code"])
    i = min(max(f - C.frame_of(shot["t0"]), 0), len(frames) - 1)
    img = frames[i].astype(np.float32)
    # mild, colour-neutral contrast so all clips sit together; no hue shifts
    return np.clip((img - 128) * 1.04 + 128, 0, 255)


FOOTAGE = set()


def load_footage():
    fp = os.path.join(C.BUILD, "conform.json")
    FOOTAGE.clear()
    if os.path.exists(fp):
        FOOTAGE.update(json.load(open(fp)).keys())


# ---------------------------------------------------------------- storyboard cards

@lru_cache(maxsize=None)
def ref_image(kind):
    if kind == "graphic":
        im, bg = product_plate()
        ox, oy = cutout_origin()
        cut = Image.open(C.PRODUCT["cutout"])
        fu, fv = C.PRODUCT["graphic_focus"]
        fx, fy = ox + fu * cut.width, oy + fv * cut.height
        return im.crop((int(fx - 330), int(fy - 250), int(fx + 330), int(fy + 250)))
    if kind == "flatlay":
        cut = Image.open(C.PRODUCT["cutout"])
        plate = Image.new("RGB", (900, 620), (178, 160, 136))
        c = cut.copy()
        c.thumbnail((760, 560))
        plate.paste(c, ((900 - c.width) // 2, (620 - c.height) // 2), c)
        return plate
    if kind == "label":
        lab = Image.open(os.path.join(C.HERE, "props", "staged_shipping_label_4x6.png")).convert("RGB")
        lab.thumbnail((380, 570))
        plate = Image.new("RGB", (900, 620), (196, 196, 192))
        plate.paste(lab.rotate(-4, expand=True, fillcolor=(196, 196, 192)), (250, 20))
        return plate
    if kind == "phone":
        sc = screens()
        scr = sc.compose(sc.collection_view(sc.card_scroll() - 300)).convert("RGB")
        scr.thumbnail((300, 650))
        plate = Image.new("RGB", (900, 700), (24, 22, 20))
        plate.paste(scr, (300, 25))
        return plate
    return None


def render_card(shot, t):
    img = Image.new("RGB", (W, H), (13, 13, 14))
    d = ImageDraw.Draw(img)
    x = 90
    d.text((x, 190), f"TO FILM  ·  {shot['code']}", font=font(40), fill=(150, 150, 156))
    tc = f"{shot['t0']:05.2f}–{shot['t1']:05.2f}s"
    d.text((W - x, 190), tc, font=font(40, bold=False), fill=(110, 110, 116), anchor="ra")
    d.text((x, 270), shot["title"], font=font(98), fill=(255, 255, 255))
    y = 420
    for line in wrap(shot["action"], font(52, bold=False), W - 2 * x, d):
        d.text((x, y), line, font=font(52, bold=False), fill=(235, 235, 238))
        y += 68
    y += 14
    for line in wrap(shot["frame"], font(40, bold=False), W - 2 * x, d):
        d.text((x, y), line, font=font(40, bold=False), fill=(140, 140, 146))
        y += 54
    ref = ref_image(shot.get("ref")) if shot.get("ref") or shot["code"] == "A1" else None
    if shot["code"] == "A1":
        ref = ref_image("phone")
    if ref is not None:
        r = ref.copy()
        r.thumbnail((W - 2 * x, 820))
        img.paste(r, ((W - r.width) // 2, max(y + 60, 760)))
    # slot progress
    q = p(t, shot["t0"], shot["t1"])
    d.rectangle([x, H - 250, W - x, H - 244], fill=(45, 45, 48))
    d.rectangle([x, H - 250, x + (W - 2 * x) * q, H - 244], fill=(235, 235, 238))
    s = lerp(1.0, 1.02, q)
    if s != 1.0:
        img = img.resize((int(W * s), int(H * s)), Image.BILINEAR).crop(
            (int((W * s - W) / 2), int((H * s - H) / 2), int((W * s - W) / 2) + W, int((H * s - H) / 2) + H))
    return np.asarray(img).astype(np.float32)


def wrap(text, f, width, d):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        nxt = (cur + " " + w_).strip()
        if d.textlength(nxt, font=f) <= width:
            cur = nxt
        else:
            lines.append(cur)
            cur = w_
    return lines + ([cur] if cur else [])


# ---------------------------------------------------------------- frame

GRAIN = None


def grain(f):
    global GRAIN
    if GRAIN is None:
        rng = np.random.default_rng(404)
        GRAIN = []
        for _ in range(6):
            n = rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32)
            GRAIN.append(np.asarray(Image.fromarray(n).resize((W, H), Image.BILINEAR))[..., None])
    return GRAIN[f % len(GRAIN)]


# (start, end, samples, smear axis, smear px): extra directional smear fills the
# gaps between samples so fast moves read as blur rather than stacked copies
WHIPS = [(1.58, 1.78, 12, 1, 18), (2.70, 2.98, 12, 1, 14), (3.60, 3.75, 16, 0, None)]
CAM_CUTS = [1.60, C.DRAWER_IN[0]]  # camera cuts inside screen shots; blur never crosses them


def smear(img, axis, length):
    """Box blur of `length` px along one axis (axis 0 = vertical)."""
    L = int(round(length))
    if L < 2:
        return img
    c = np.cumsum(img, axis=axis, dtype=np.float64)
    pad = [(0, 0)] * img.ndim
    pad[axis] = (L, 0)
    c = np.pad(c, pad, mode="edge")
    n = img.shape[axis]
    hi = np.take(c, np.arange(L, L + n), axis=axis)
    lo = np.take(c, np.arange(0, n), axis=axis)
    out = (hi - lo) / L
    return np.roll(out, -L // 2, axis=axis).astype(np.float32)


def cam_speed(t):
    """Frame-space px/frame of the content under the frame centre."""
    a, b = screen_cam(t - 0.5 / C.FPS), screen_cam(t + 0.5 / C.FPS)
    return abs(b["cy"] - a["cy"]) * (a["zoom"] + b["zoom"]) / 2


def render_frame(f):
    t = f / C.FPS
    shot = C.shot_at(f)
    k = shot["kind"]
    whip = [(n, ax, px) for a, b, n, ax, px in WHIPS if a <= t < b]
    if k == "screen" and whip:
        n, ax, px = whip[0]
        lo = max([shot["t0"]] + [c for c in CAM_CUTS if c <= t])
        hi = min([shot["t1"]] + [c for c in CAM_CUTS if c > t])
        ts = [t + (i + 0.5) / n / C.FPS - 0.5 / C.FPS for i in range(n)]
        ts = [max(lo, min(x, hi - 1e-3)) for x in ts]
        img = sum(render_screen(x) for x in ts) / n
        img = smear(img, ax, px if px is not None else cam_speed(t) / n * 1.2)
    elif k == "screen":
        img = render_screen(t)
    elif k == "notify":
        img = render_notify(t)
    elif k == "product":
        img = render_product(t)
    elif k == "endcard":
        img = render_end(t)
    elif shot["code"] in FOOTAGE:
        img = footage_frame(shot, f)
    else:
        img = render_card(shot, t)
    amt = 2.5 if k in ("endcard", "product") else 3.5
    img = img + grain(f) * amt
    return np.clip(img + 0.5, 0, 255).astype(np.uint8)


def init_worker():
    load_footage()


def main():
    args = sys.argv[1:]
    os.makedirs(C.BUILD, exist_ok=True)
    conform_all()
    load_footage()
    if "--frames" in args:
        init_worker()
        for f in [int(v) for v in args[args.index("--frames") + 1].split(",")]:
            Image.fromarray(render_frame(f)).save(os.path.join(C.BUILD, f"still_{f:03d}.png"))
        return
    out = os.path.join(C.BUILD, "video_only.mp4")
    cmd = [ffmpeg(), "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
           "-s", f"{W}x{H}", "-r", str(C.FPS), "-i", "-", "-c:v", "libx264", "-preset", "slow",
           "-crf", "16", "-pix_fmt", "yuv420p", out]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with Pool(min(4, os.cpu_count() or 1), initializer=init_worker) as pool:
        for i, frame in enumerate(pool.imap(render_frame, range(C.N_FRAMES), chunksize=4)):
            proc.stdin.write(frame.tobytes())
            if i % 60 == 0:
                print(f"frame {i}/{C.N_FRAMES}", flush=True)
    proc.stdin.close()
    proc.wait()
    mux(out)


def mux(video):
    """Add the soundtrack, loudness-normalised for social (-14 LUFS)."""
    wav = os.path.join(C.BUILD, "audio.wav")
    if not os.path.exists(wav):
        import audio
        audio.main()
    films = [s["code"] for s in C.SHOTS if s["kind"] == "film"]
    missing = [c for c in films if c not in FOOTAGE]
    name = "404_culture_order_to_outfit_15s.mp4" if not missing else "404_culture_order_to_outfit_animatic_15s.mp4"
    final = os.path.join(C.HERE, name)
    subprocess.run([ffmpeg(), "-y", "-loglevel", "error", "-i", video, "-i", wav,
                    "-af", "loudnorm=I=-14:TP=-1.0:LRA=11", "-ar", "48000",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", final], check=True)
    print("wrote", final)
    if missing:
        print("storyboard cards still stand in for:", " ".join(missing))


if __name__ == "__main__":
    main()
