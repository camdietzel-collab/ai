"""Soundtrack for the Tiger League tees promo, cued to promo.py's timeline.

Reuses the campaign's synth voices: 120 BPM beat, whoosh on every fly,
impact on every detail landing (all on the beat), final bass hit on the logo.
"""
import os
import sys
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "campaign"))
import audio as A  # noqa: E402

import promo  # noqa: E402

fr = A.fr


def build():
    drums, bass, keys, fx = A.buf(), A.buf(), A.buf(), A.buf()
    stop, final = fr(416), fr(420)
    beats = np.arange(0, stop, 0.5)
    for k, bt in enumerate(beats):
        A.add(drums, A.kick(), bt, 1.0)
        if k % 2:
            A.add(drums, A.snare(), bt, 0.5)
    for k, ht in enumerate(np.arange(0.25, stop, 0.25)):
        A.add(drums, A.hat(open_=(k % 4 == 3)), ht, 0.15)
    roots = [55.0, 55.0, 43.65, 49.0]
    for k, bt in enumerate(np.arange(0, stop, 0.25)):
        A.add(bass, A.bass_note(roots[int(bt // 2) % 4] * (2 if k % 4 == 3 else 1), 0.2), bt, 0.4)
    chords = [[220, 261.6, 329.6], [220, 261.6, 329.6], [174.6, 220, 261.6], [196, 246.9, 293.7]]
    for bar in np.arange(0, stop, 2.0):
        A.add(keys, A.stab(chords[int(bar // 2) % 4]), bar, 0.3)
    keys = A.reverb(keys, 1.2, 0.3)

    # opening slide-in
    A.add(fx, A.whoosh(0.4, up=True), 0.0, 0.5)
    A.add(fx, A.impact(0.6), fr(14), 0.7)
    A.add(fx, A.whoosh(0.5, up=True, lo=200, hi=7000), fr(58), 0.55)
    # every fly between details lands on a beat
    for g in promo.TOUR:
        sts = promo.stop_starts(g)
        for st in sts[1:]:
            A.add(fx, A.whoosh(0.26, up=True, lo=300, hi=8000), fr(st) - 0.02, 0.45)
            A.add(fx, A.impact(0.3), fr(st + promo.MOVE), 0.4)
            A.add(fx, A.swish(0.15), fr(st + promo.MOVE), 0.35)
    A.add(fx, A.whoosh(0.3, up=True), fr(217), 0.6)     # whip to navy
    A.add(fx, A.impact(0.6), fr(225), 0.6)
    A.add(fx, A.whoosh(0.55, up=True, lo=150, hi=9000), fr(372), 0.6)
    A.add(fx, A.impact(0.9), fr(391), 0.8)                # both tees land
    for at in (395, 400, 406):
        A.add(fx, A.swish(0.1), fr(at), 0.25)
    A.add(fx, A.final_hit(), final, 1.1)                  # logo

    t = np.arange(A.N) / A.SR
    duck = np.ones(A.N, np.float32)
    for bt in beats:
        i, n = int(bt * A.SR), int(0.2 * A.SR)
        e = 1 - 0.65 * np.exp(-np.arange(n) / A.SR * 18)
        duck[i:i + n] = np.minimum(duck[i:i + n], e[: max(0, min(n, A.N - i))])
    music = drums * 0.85 + bass * duck + keys * duck * 0.8
    music *= np.clip((stop + 0.02 - t) / 0.02, 0, 1)
    mix = (music + fx) * np.clip((A.DUR - t) / 0.3, 0, 1)
    mix = np.tanh(mix * 0.9) / np.tanh(0.9)
    return (mix / (np.abs(mix).max() + 1e-9) * 0.95).astype(np.float32)


if __name__ == "__main__":
    os.makedirs(os.path.join(HERE, "build"), exist_ok=True)
    out = os.path.join(HERE, "build", "audio.wav")
    st = (np.stack([build()] * 2, axis=1) * 32767).astype(np.int16)
    with wave.open(out, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(A.SR)
        w.writeframes(st.tobytes())
    print("wrote", out)
