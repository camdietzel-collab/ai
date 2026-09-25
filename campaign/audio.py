"""Synthesised soundtrack for the 404 CULTURE campaign video.

120 BPM driving instrumental (A minor) + sound design, all cued to the same
frame timeline as render.py (30 fps, 1 beat = 15 frames).
usage: python3 audio.py [out.wav]
"""
import os
import sys
import wave

import numpy as np
from scipy import signal

SR = 48000
DUR = 15.0
N = int(SR * DUR)
BEAT = 0.5
rng = np.random.default_rng(404)


def fr(f):
    return f / 30.0


def buf():
    return np.zeros(N, np.float32)


def add(dst, x, t, gain=1.0):
    i = int(round(t * SR))
    if i >= N:
        return
    x = x[: N - i]
    dst[i:i + len(x)] += x * gain


def env(n, a, d, curve=4.0):
    t = np.arange(n) / SR
    e = np.minimum(t / max(a, 1e-4), 1.0) * np.exp(-curve * np.maximum(t - a, 0) / d)
    return e.astype(np.float32)


def bandpass(x, lo, hi, order=2):
    sos = signal.butter(order, [lo, hi], "bandpass", fs=SR, output="sos")
    return signal.sosfilt(sos, x).astype(np.float32)


def lowpass(x, fc, order=2):
    sos = signal.butter(order, fc, "lowpass", fs=SR, output="sos")
    return signal.sosfilt(sos, x).astype(np.float32)


def highpass(x, fc, order=2):
    sos = signal.butter(order, fc, "highpass", fs=SR, output="sos")
    return signal.sosfilt(sos, x).astype(np.float32)


# ---------------------------------------------------------------- instruments

def kick(n_sec=0.45, f0=150, f1=45, punch=1.0):
    n = int(SR * n_sec)
    t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t * 7)
    click = highpass(rng.normal(0, 1, n).astype(np.float32), 2500) * np.exp(-t * 250) * 0.4 * punch
    return np.tanh(1.6 * (body + click)).astype(np.float32)


def snare():
    n = int(SR * 0.3)
    t = np.arange(n) / SR
    tone = np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30)
    noise = bandpass(rng.normal(0, 1, n).astype(np.float32), 1200, 9000) * np.exp(-t * 16)
    clap = np.zeros(n, np.float32)
    for k, off in enumerate((0, 0.009, 0.018)):
        i = int(off * SR)
        clap[i:] += bandpass(rng.normal(0, 1, n - i).astype(np.float32), 900, 4000) * np.exp(-np.arange(n - i) / SR * 60) * 0.6
    return (0.5 * tone + 0.8 * noise + 0.5 * clap).astype(np.float32)


def hat(open_=False):
    n = int(SR * (0.22 if open_ else 0.05))
    t = np.arange(n) / SR
    x = highpass(rng.normal(0, 1, n).astype(np.float32), 7500, 4)
    return (x * np.exp(-t * (14 if open_ else 90))).astype(np.float32)


def bass_note(freq, dur):
    n = int(SR * dur)
    t = np.arange(n) / SR
    saw = 2 * ((freq * t) % 1.0) - 1
    sub = np.sin(2 * np.pi * freq / 2 * t)
    x = lowpass(saw.astype(np.float32), 420) * 0.55 + sub * 0.8
    e = np.minimum(t / 0.005, 1) * np.minimum((dur - t) / 0.02, 1)
    return np.tanh(1.8 * x * e).astype(np.float32)


def stab(freqs, dur=0.35):
    n = int(SR * dur)
    t = np.arange(n) / SR
    x = np.zeros(n, np.float32)
    for f in freqs:
        for det in (-0.12, 0.0, 0.12):
            x += (2 * ((f * (1 + det / 100) * t) % 1.0) - 1).astype(np.float32)
    x = lowpass(x / len(freqs) / 3, 2200)
    return x * env(n, 0.004, dur, 5)


def whoosh(dur, up=True, lo=300, hi=6000):
    n = int(SR * dur)
    t = np.linspace(0, 1, n)
    x = rng.normal(0, 1, n).astype(np.float32)
    # sweep a bandpass by filtering in overlapping chunks
    out = np.zeros(n, np.float32)
    chunks = 24
    step = n // chunks
    for k in range(chunks):
        q = (k + 0.5) / chunks
        q = q if up else 1 - q
        fc = lo * (hi / lo) ** q
        a, b = max(0, k * step - step), min(n, (k + 2) * step)
        seg = bandpass(x[a:b], fc * 0.6, min(fc * 1.6, SR / 2 - 100))
        w = np.hanning(b - a).astype(np.float32)
        out[a:b] += seg * w
    shape = (t ** 2.2 if up else (1 - t) ** 1.5) * np.minimum(1, (1 - t) * 30 if up else t * 40)
    return (out * shape).astype(np.float32)


def swish(dur=0.18):
    """Fabric swish: airy noise with a fast cloth flutter."""
    n = int(SR * dur)
    t = np.arange(n) / SR
    x = bandpass(rng.normal(0, 1, n).astype(np.float32), 1800, 7000)
    flutter = 0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 38 * t + rng.uniform(0, 3)))
    shape = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 1.5
    return (x * flutter * shape).astype(np.float32)


def impact(size=1.0):
    n = int(SR * (0.9 + size))
    t = np.arange(n) / SR
    boom = np.sin(2 * np.pi * np.cumsum(38 + 90 * np.exp(-t * 18)) / SR) * np.exp(-t * (4.5 / size))
    crack = bandpass(rng.normal(0, 1, n).astype(np.float32), 400, 8000) * np.exp(-t * 22)
    return np.tanh(1.4 * (boom + 0.7 * crack)).astype(np.float32)


def final_hit():
    n = int(SR * 1.6)
    t = np.arange(n) / SR
    f = 36 + 120 * np.exp(-t * 14)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.9)
    dist = np.tanh(3.0 * sub) * 0.55
    crack = bandpass(rng.normal(0, 1, n).astype(np.float32), 300, 9000) * np.exp(-t * 12)
    tail = lowpass(rng.normal(0, 1, n).astype(np.float32), 900) * np.exp(-t * 3.2) * 0.25
    return (0.9 * sub + dist + 0.8 * crack + tail).astype(np.float32)


def reverb(x, seconds=1.2, mix=0.25):
    n = int(SR * seconds)
    ir = rng.normal(0, 1, n).astype(np.float32) * np.exp(-np.arange(n) / SR * 5)
    ir = lowpass(ir, 5000)
    wet = signal.fftconvolve(x, ir)[: len(x)].astype(np.float32)
    wet *= np.abs(x).max() / (np.abs(wet).max() + 1e-9)
    return x + mix * wet


# ---------------------------------------------------------------- arrangement

def build():
    drums, bass, keys, fx = buf(), buf(), buf(), buf()
    END_MUSIC = fr(397)   # drop-out right before the final bass hit
    FINAL = fr(405)

    beats = np.arange(0, END_MUSIC, BEAT)
    for k, bt in enumerate(beats):
        add(drums, kick(), bt, 1.0)
        if k % 2 == 1 and bt >= 1.0:
            add(drums, snare(), bt, 0.55)
    # montage: double-time kicks + snare roll into the collection landing
    for bt in np.arange(fr(270) + 0.25, fr(330), BEAT):
        add(drums, kick(0.3, punch=0.6), bt, 0.7)
    for bt in np.arange(fr(315), fr(345), 0.125):
        add(drums, snare(), bt, 0.18 + 0.3 * (bt - fr(315)) / 1.0)
    # hats: 16ths from 0.5s
    for k, ht in enumerate(np.arange(0.5, END_MUSIC, 0.125)):
        add(drums, hat(open_=(k % 8 == 6)), ht, 0.16 if k % 2 else 0.24)

    # bass: A A F G per bar (2 s), 8th-note pulse
    roots = [55.0, 55.0, 43.65, 49.0]
    for k, bt in enumerate(np.arange(0.0, END_MUSIC, 0.25)):
        bar = int(bt // 2.0) % 4
        f = roots[bar] * (2 if (k % 8) in (3, 7) else 1)
        add(bass, bass_note(f, 0.22), bt, 0.42)
    # sidechain duck bass & keys on every kick
    duck = np.ones(N, np.float32)
    for bt in beats:
        i = int(bt * SR)
        n = int(0.22 * SR)
        e = 1 - 0.7 * np.exp(-np.arange(n) / SR * 18)
        duck[i:i + n] = np.minimum(duck[i:i + n], e[: max(0, min(n, N - i))])

    # dark minor stabs on bar downbeats + offbeat hits
    chords = [[220, 261.6, 329.6], [220, 261.6, 329.6], [174.6, 220, 261.6], [196, 246.9, 293.7]]
    for bar_t in np.arange(0, END_MUSIC, 2.0):
        c = chords[int(bar_t // 2) % 4]
        add(keys, stab(c), bar_t, 0.35)
        add(keys, stab([x * 2 for x in c], 0.18), bar_t + 0.75, 0.18)
        add(keys, stab([x * 2 for x in c], 0.18), bar_t + 1.25, 0.14)
    keys = reverb(keys, 1.4, 0.35)

    # ---- sound design, cued to the edit
    add(fx, impact(0.8), 0.0, 0.9)                       # cold open hit
    add(fx, whoosh(0.5, up=False, lo=200, hi=5000), fr(20), 0.5)  # pull back
    add(fx, impact(0.5), fr(38), 0.55)                   # title slam
    add(fx, swish(0.22), fr(58), 0.45)                   # 01 settles
    add(fx, whoosh(0.35, up=True), fr(94), 0.6)          # whip out
    add(fx, swish(0.25), fr(103), 0.6)                   # 02 whip in
    add(fx, impact(0.4), fr(105), 0.5)
    add(fx, whoosh(0.3, up=True, lo=150, hi=4000), fr(134), 0.55)  # punch in
    add(fx, impact(0.5), fr(143), 0.6)                   # 03 match cut
    add(fx, swish(0.2), fr(146), 0.4)
    add(fx, whoosh(0.35, up=True, lo=400, hi=8000), fr(177), 0.5)  # spin out
    add(fx, swish(0.3), fr(188), 0.5)                    # 04 spin in
    add(fx, impact(0.4), fr(199), 0.4)
    add(fx, impact(0.6), fr(225), 0.65)                  # 05 colour-swap cut
    add(fx, swish(0.18), fr(226), 0.4)
    add(fx, whoosh(0.3, up=True, lo=150, hi=5000), fr(261), 0.55)
    add(fx, whoosh(0.9, up=True, lo=200, hi=9000), fr(243), 0.35)  # riser into montage
    for k in range(8):                                   # montage cuts
        add(fx, swish(0.12), fr(270 + 7.5 * k), 0.35)
    add(fx, whoosh(1.0, up=True, lo=150, hi=9000), fr(315), 0.5)   # riser to collection
    add(fx, impact(0.9), fr(345), 0.85)                  # collection lands
    for k, at in enumerate((360, 367.5, 375, 382.5)):    # info ticks
        add(fx, swish(0.09), fr(at), 0.25)
    add(fx, whoosh(0.3, up=True, lo=100, hi=3000), fr(397), 0.55)  # suck-in before hit
    add(fx, final_hit(), FINAL, 1.1)                    # final bass hit
    add(fx, swish(0.15), fr(412), 0.25)

    music = drums * 0.85 + bass * duck + keys * duck * 0.8
    # music fades under the end card, then cuts for the final hit
    t = np.arange(N) / SR
    music *= np.where(t < fr(345), 1.0, np.clip(1 - (t - fr(345)) / 3.0 * 0.35, 0.65, 1))
    music *= np.clip((END_MUSIC + 0.02 - t) / 0.02, 0, 1)
    mix = music + fx
    mix *= np.clip((DUR - t) / 0.35, 0, 1)             # clean tail
    mix = np.tanh(mix * 0.9) / np.tanh(0.9)
    mix /= np.abs(mix).max() + 1e-9
    return (mix * 0.95).astype(np.float32)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "build", "audio.wav")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    x = build()
    st = np.stack([x, x], axis=1)
    with wave.open(out, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())
    print("wrote", out)


if __name__ == "__main__":
    main()
