"""Music + sound design for the "order to outfit" ad, cued to config.py.

120 BPM half-time groove in A minor: filtered intro under the phone taps,
drops on the checkout tap / order notification (4.0 s), foley for packing and
unboxing, street ambience for the fit, final bass hit on the end card.

    python3 audio.py [out.wav]
"""
import os
import sys
import wave

import numpy as np
from scipy import signal

import config as C

SR = 48000
N = int(SR * C.DUR)
rng = np.random.default_rng(404)


# ---------------------------------------------------------------- helpers

def buf():
    return np.zeros(N, np.float32)


def add(dst, x, t, gain=1.0):
    i = int(round(t * SR))
    if i >= N or i + len(x) <= 0:
        return
    if i < 0:
        x, i = x[-i:], 0
    x = x[: N - i]
    dst[i:i + len(x)] += x.astype(np.float32) * gain


def tt(sec):
    return np.arange(int(SR * sec)) / SR


def noise(sec):
    return rng.normal(0, 1, int(SR * sec)).astype(np.float32)


def filt(x, kind, f, order=2):
    sos = signal.butter(order, f, kind, fs=SR, output="sos")
    return signal.sosfilt(sos, x).astype(np.float32)


def bp(x, lo, hi, order=2):
    return filt(x, "bandpass", [lo, min(hi, SR / 2 - 200)], order)


def decay(sec, rate, attack=0.002):
    t = tt(sec)
    return (np.minimum(t / attack, 1) * np.exp(-t * rate)).astype(np.float32)


def sweep_bp(x, f0, f1, width=0.9):
    """Band-pass whose centre glides f0 -> f1 across x (chunked, cross-faded)."""
    n, chunks = len(x), 20
    step = max(1, n // chunks)
    out = np.zeros(n, np.float32)
    for k in range(chunks):
        q = (k + 0.5) / chunks
        fc = f0 * (f1 / f0) ** q
        a, b = max(0, k * step - step), min(n, (k + 2) * step)
        if b - a < 64:
            continue
        seg = bp(x[a:b], fc / (1 + width), fc * (1 + width))
        out[a:b] += seg * np.hanning(b - a).astype(np.float32)
    return out


# ---------------------------------------------------------------- music

def kick(sec=0.5, f0=160, f1=48):
    t = tt(sec)
    f = f1 + (f0 - f1) * np.exp(-t * 30)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6.5)
    click = filt(noise(sec), "highpass", 2500) * np.exp(-t * 260) * 0.35
    return np.tanh(1.7 * (body + click)).astype(np.float32)


def snare():
    t = tt(0.35)
    tone = np.sin(2 * np.pi * 185 * t) * np.exp(-t * 28)
    body = bp(noise(0.35), 1100, 9000) * np.exp(-t * 14)
    clap = np.zeros_like(t, dtype=np.float32)
    for off in (0.0, 0.011, 0.022):
        i = int(off * SR)
        clap[i:] += bp(noise(0.35)[: len(t) - i], 900, 4200) * np.exp(-np.arange(len(t) - i) / SR * 55) * 0.55
    return (0.45 * tone + 0.8 * body + 0.6 * clap).astype(np.float32)


def hat(sec=0.045, rate=95):
    t = tt(sec)
    return (filt(noise(sec), "highpass", 7800, 4) * np.exp(-t * rate)).astype(np.float32)


def bass808(freq, sec, glide_from=None):
    t = tt(sec)
    f = np.full_like(t, freq)
    if glide_from:
        f = freq + (glide_from - freq) * np.exp(-t * 18)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR)
    e = np.minimum(t / 0.004, 1) * np.exp(-t * 2.2) * np.minimum((sec - t) / 0.03, 1)
    return np.tanh(2.2 * x * e).astype(np.float32) * 0.8


def pluck(freq, sec=0.35):
    t = tt(sec)
    mod = np.sin(2 * np.pi * freq * 2.0 * t) * 2.2 * np.exp(-t * 9)
    x = np.sin(2 * np.pi * freq * t + mod) * np.exp(-t * 7)
    return (x * np.minimum(t / 0.003, 1)).astype(np.float32)


def pad(freqs, sec):
    t = tt(sec)
    x = np.zeros_like(t)
    for f in freqs:
        for det in (-0.15, 0.15):
            x += 2 * ((f * (1 + det / 100) * t) % 1.0) - 1
    x = filt((x / (2 * len(freqs))).astype(np.float32), "lowpass", 1200)
    e = np.minimum(t / 0.25, 1) * np.minimum((sec - t) / 0.3, 1)
    return (x * e).astype(np.float32)


# ---------------------------------------------------------------- foley

def tap():
    """Fingertip on glass: short, bright, tiny body."""
    t = tt(0.05)
    click = filt(noise(0.05), "highpass", 3000) * np.exp(-t * 400)
    thock = np.sin(2 * np.pi * 900 * t) * np.exp(-t * 180) * 0.4
    return (click + thock).astype(np.float32)


def swipe(sec=0.16):
    t = tt(sec)
    x = bp(noise(sec), 2500, 9000) * np.sin(np.pi * t / sec) ** 2
    return (x * 0.5).astype(np.float32)


def ui_blip():
    out = np.zeros(int(0.25 * SR), np.float32)
    for k, f in enumerate((880, 1318.5)):
        t = tt(0.18)
        tone = np.sin(2 * np.pi * f * t) * np.exp(-t * 22) * np.minimum(t / 0.002, 1)
        i = int(k * 0.06 * SR)
        out[i:i + len(t)] += tone.astype(np.float32)
    return out * 0.5


def chime():
    """Notification: two soft bell partials, not any platform's stock sound."""
    out = np.zeros(int(0.9 * SR), np.float32)
    for k, f in enumerate((1318.5, 1760.0)):
        t = tt(0.8)
        mod = np.sin(2 * np.pi * f * 3.5 * t) * 1.2 * np.exp(-t * 6)
        tone = np.sin(2 * np.pi * f * t + mod) * np.exp(-t * 5.5) * np.minimum(t / 0.003, 1)
        i = int(k * 0.1 * SR)
        out[i:i + len(t)] += tone.astype(np.float32)
    return out * 0.6


def buzz(sec=0.26):
    """Phone vibrating on a desk."""
    t = tt(sec)
    gate = (np.sin(2 * np.pi * 11 * t) > -0.2).astype(np.float32)
    motor = np.sign(np.sin(2 * np.pi * 172 * t)) * 0.6 + np.sin(2 * np.pi * 344 * t) * 0.3
    rattle = bp(noise(sec), 180, 1200) * 0.35
    x = filt((motor + rattle).astype(np.float32), "lowpass", 1400) * gate
    return (x * np.minimum(t / 0.01, 1) * np.minimum((sec - t) / 0.02, 1)).astype(np.float32)


def cloth(sec=0.3, bright=1.0):
    t = tt(sec)
    x = bp(noise(sec), 700 * bright, 6500 * bright)
    flutter = 0.55 + 0.45 * np.abs(np.sin(2 * np.pi * rng.uniform(25, 45) * t + rng.uniform(0, 3)))
    shape = np.sin(np.pi * np.clip(t / sec, 0, 1)) ** 1.4
    return (x * flutter * shape).astype(np.float32)


def thump(sec=0.18, f=95):
    t = tt(sec)
    x = np.sin(2 * np.pi * f * t) * np.exp(-t * 32) + filt(noise(sec), "lowpass", 900) * np.exp(-t * 45) * 0.6
    return x.astype(np.float32)


def crinkle(sec=0.35, density=900):
    """Poly mailer: dense random micro-clicks, band-limited."""
    n = int(sec * SR)
    x = np.zeros(n, np.float32)
    idx = rng.integers(0, n, int(density * sec))
    x[idx] = rng.normal(0, 1, len(idx)).astype(np.float32)
    x = bp(x, 2000, 11000) * 3.0
    t = tt(sec)
    return (x * np.sin(np.pi * t / sec) ** 0.7).astype(np.float32)


def peel(sec=0.28):
    t = tt(sec)
    rasp = (np.sin(2 * np.pi * np.cumsum(260 + 900 * t / sec) / SR) > 0.6).astype(np.float32)
    x = bp(noise(sec) * (0.4 + rasp), 900, 7000)
    return (x * np.sin(np.pi * t / sec) ** 0.6).astype(np.float32) * 0.8


def slap():
    t = tt(0.22)
    crack = bp(noise(0.22), 600, 9000) * np.exp(-t * 55)
    body = np.sin(2 * np.pi * 140 * t) * np.exp(-t * 40)
    return (crack + 0.8 * body).astype(np.float32)


def scrape(sec=0.32):
    t = tt(sec)
    x = bp(noise(sec), 250, 2600) * (0.7 + 0.3 * np.sin(2 * np.pi * 30 * t))
    return (x * np.sin(np.pi * t / sec)).astype(np.float32) * 0.8


def rip(sec=0.4):
    """Tear strip: stuttering grains that speed up."""
    n = int(sec * SR)
    x = np.zeros(n, np.float32)
    pos = 0.0
    while pos < sec - 0.01:
        g = min(0.012, sec - pos)
        grain = bp(noise(g), 1200, 8000) * np.hanning(int(g * SR)).astype(np.float32)
        i = int(pos * SR)
        x[i:i + len(grain)] += grain * rng.uniform(0.6, 1.0)
        pos += 0.018 * (1 - 0.6 * pos / sec)
    return x * 1.3


def whoosh(sec, f0=300, f1=6000):
    t = tt(sec)
    x = sweep_bp(noise(sec), f0, f1)
    return (x * (t / sec) ** 2 * np.minimum((sec - t) / 0.03, 1)).astype(np.float32)


def impact(size=1.0):
    t = tt(0.9 + size)
    boom = np.sin(2 * np.pi * np.cumsum(40 + 100 * np.exp(-t * 18)) / SR) * np.exp(-t * 4.5 / size)
    crack = bp(noise(len(t) / SR), 400, 8000) * np.exp(-t * 24)
    return np.tanh(1.4 * (boom + 0.6 * crack)).astype(np.float32)


def step():
    t = tt(0.14)
    heel = np.sin(2 * np.pi * 80 * t) * np.exp(-t * 45)
    grit = bp(noise(0.14), 1500, 7000) * np.exp(-t * 60) * 0.35
    return (heel + grit).astype(np.float32)


def street(sec):
    t = tt(sec)
    rumble = filt(noise(sec), "lowpass", 180, 4) * 3.0
    hiss = bp(noise(sec), 1500, 5000) * 0.05
    swell = 0.6 + 0.4 * np.sin(2 * np.pi * 0.35 * t + 1.0)
    car = bp(noise(sec), 300, 1500) * np.exp(-((t - sec * 0.55) / (sec * 0.2)) ** 2) * 0.5
    fade = np.minimum(t / 0.15, 1) * np.minimum((sec - t) / 0.1, 1)
    return ((rumble * swell + hiss + car) * fade).astype(np.float32)


def final_hit():
    t = tt(1.4)
    f = 36 + 130 * np.exp(-t * 14)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.0)
    dist = np.tanh(3.0 * sub) * 0.5
    crack = bp(noise(1.4), 300, 9000) * np.exp(-t * 13)
    return (0.9 * sub + dist + 0.7 * crack).astype(np.float32)


def reverb(x, sec=1.2, mix=0.25):
    ir = filt(noise(sec) * np.exp(-tt(sec) * 5).astype(np.float32), "lowpass", 5000)
    wet = signal.fftconvolve(x, ir)[: len(x)].astype(np.float32)
    wet *= np.abs(x).max() / (np.abs(wet).max() + 1e-9)
    return x + mix * wet


# ---------------------------------------------------------------- arrangement

def build():
    drums, bass, keys, fx, amb = buf(), buf(), buf(), buf(), buf()
    DROP = C.frame_of(4.0) / C.FPS
    STOP = 13.97
    bar = 2.0
    roots = [55.0, 43.65, 65.41, 49.0]  # A1 F1 C2 G1

    # intro (0-4): kick on the one, soft hats, filtered 808 pulse
    for b0 in (0.0, 2.0):
        add(drums, kick(), b0, 0.8)
        add(drums, kick(), b0 + 1.5, 0.5)
    for k, ht in enumerate(np.arange(0.5, DROP, 0.25)):
        add(drums, hat(), ht, 0.10 + 0.05 * (k % 2 == 0))
    for b0 in (0.0, 2.0):
        r = roots[int(b0 // bar) % 4]
        add(bass, bass808(r, 1.4), b0, 0.5)
    add(keys, pad([220.0, 261.6, 329.6], 4.0), 0.0, 0.55)

    # groove (4-14): half-time - kick 1 & "and of 2", snare on 3, 16th hats w/ rolls
    for b0 in np.arange(DROP, STOP, bar):
        r = roots[int(round(b0 / bar)) % 4]
        for off, g in ((0.0, 1.0), (0.75, 0.8), (1.25, 0.55)):
            if b0 + off < STOP:
                add(drums, kick(), b0 + off, g)
        if b0 + 1.0 < STOP:
            add(drums, snare(), b0 + 1.0, 0.6)
        for k, ht in enumerate(np.arange(b0, min(b0 + bar, STOP), 0.125)):
            add(drums, hat(), ht, 0.16 if k % 2 == 0 else 0.10)
        if int(round(b0 / bar)) % 2 == 1:  # hat roll into the next bar
            for ht in np.arange(b0 + 1.75, min(b0 + 2.0, STOP), 1 / 24):
                add(drums, hat(0.03, 140), ht, 0.09)
        add(bass, bass808(r, 0.7, glide_from=r * 1.5 if b0 > DROP else None), b0, 0.95)
        add(bass, bass808(r, 0.45), b0 + 0.75, 0.75)
        add(bass, bass808(r * (1.5 if int(round(b0 / bar)) % 2 else 1.0), 0.4), b0 + 1.25, 0.6)
        for k, (off, f) in enumerate(((0.0, 440.0), (0.375, 523.25), (0.75, 659.25), (1.5, 783.99))):
            if b0 + off < STOP:
                add(keys, pluck(f), b0 + off, 0.16)
    keys = reverb(keys, 1.3, 0.3)

    # intro filter: drums/bass open up into the drop
    t = np.arange(N) / SR
    opening = np.clip(t / DROP, 0, 1) ** 2 * 0.45
    opening[t >= DROP] = 1.0
    drums = filt(drums, "lowpass", 900) * (1 - opening) + drums * opening
    # sidechain on the kick
    duck = np.ones(N, np.float32)
    for b0 in np.arange(DROP, STOP, bar):
        for off in (0.0, 0.75, 1.25):
            i, n = int((b0 + off) * SR), int(0.2 * SR)
            e = 1 - 0.6 * np.exp(-np.arange(n) / SR * 20)
            duck[i:i + n] = np.minimum(duck[i:i + n], e[: max(0, min(n, N - i))])

    # ---- phone section
    add(fx, swipe(0.18), 0.10, 0.5)
    add(fx, swipe(0.16), 0.48, 0.45)
    add(fx, swipe(0.20), 0.92, 0.55)
    add(fx, tap(), C.TAP_CARD, 0.9)
    add(fx, swipe(0.12), 1.60, 0.35)
    add(fx, tap(), C.TAP_SIZE, 0.9)
    add(fx, tap(), C.TAP_ADD, 0.9)
    add(fx, ui_blip(), C.TAP_ADD + 0.07, 0.55)
    add(fx, cloth(0.2, 1.4), C.DRAWER_IN[0], 0.25)
    add(fx, swipe(0.12), 3.20, 0.3)                      # cut to the cart close-up
    add(fx, whoosh(0.16, 900, 8000), 3.58, 0.45)         # whip down to "Check out"
    add(fx, whoosh(0.95, 150, 9000), 3.0, 0.45)          # riser into the drop
    add(fx, tap(), C.TAP_CHECKOUT, 1.1)
    # ---- the drop: order lands on the owner's phone
    add(fx, impact(0.9), DROP, 0.9)
    add(fx, chime(), C.NOTIFY_IN, 0.7)
    add(fx, buzz(), C.NOTIFY_IN + 0.03, 0.55)
    # ---- fulfilment
    add(fx, cloth(0.34), 5.00, 1.0)
    add(fx, thump(0.2, 110), 5.30, 0.35)
    add(fx, cloth(0.3, 0.8), 5.75, 0.9)
    add(fx, thump(0.2, 90), 5.95, 0.6)
    add(fx, cloth(0.22, 1.1), 6.15, 0.7)
    add(fx, cloth(0.25), 6.50, 0.85)
    add(fx, thump(0.2, 85), 6.70, 0.7)
    add(fx, crinkle(0.38), 7.00, 0.9)
    add(fx, thump(0.2, 120), 7.22, 0.4)
    add(fx, peel(0.3), 7.50, 1.0)
    add(fx, thump(0.15, 100), 7.88, 0.6)
    add(fx, thump(0.15, 105), 8.02, 0.5)
    add(fx, slap(), 8.25, 1.0)
    add(fx, scrape(0.34), 8.60, 0.8)
    # ---- delivery + unboxing
    add(fx, crinkle(0.3, 600), 9.05, 0.7)
    add(fx, thump(0.22, 75), 9.10, 0.7)
    add(fx, rip(0.42), 9.80, 1.0)
    add(fx, crinkle(0.25, 700), 10.25, 0.5)
    add(fx, cloth(0.42, 0.9), 10.50, 1.0)
    add(fx, whoosh(0.22, 400, 8000), 11.03, 0.6)
    add(fx, impact(0.5), C.frame_of(11.25) / C.FPS, 0.6)
    # ---- the fit
    add(amb, street(1.62), 12.0, 1.0)
    for st in (12.08, 12.44, 12.80, 13.16):
        add(fx, step(), st, 0.55)
    add(fx, cloth(0.2, 1.2), 12.72, 0.35)
    add(fx, impact(0.35), 13.5, 0.45)
    add(fx, final_hit(), 14.0, 1.15)

    music = drums * 0.9 + bass * duck * 0.9 + keys * duck * 0.75
    music *= np.clip((STOP + 0.02 - t) / 0.02, 0, 1)
    music[t < DROP] *= 0.8
    mix = music + fx + amb * 0.5
    mix *= np.clip((C.DUR - t) / 0.3, 0, 1)
    mix = np.tanh(mix * 0.9) / np.tanh(0.9)
    return (mix / (np.abs(mix).max() + 1e-9) * 0.95).astype(np.float32)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(C.BUILD, "audio.wav")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    x = build()
    st = (np.stack([x, x], axis=1) * 32767).astype(np.int16)
    with wave.open(out, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(st.tobytes())
    print("wrote", out)


if __name__ == "__main__":
    main()
