"""Cut garments out of their flat studio backgrounds.

Only the outer 1-2px boundary gets a soft alpha (with the backdrop colour
un-mixed out of those anti-aliased pixels); every interior garment pixel is
kept bit-for-bit.

Background = region connected to the image border whose colour is within a
per-image tolerance of the backdrop colour.
"""
import os

import numpy as np
from PIL import Image
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "source", "{}.webp")
OUT = os.path.join(HERE, "cutouts", "{}.png")
# Dark garments take a wide tolerance (kills the light anti-alias halo);
# light garments / white trims need a tight one.
TOL = {1: 45, 2: 14, 3: 5, 4: 4, 5: 3}


def cutout(i, tol):
    im = Image.open(SRC.format(i)).convert("RGB")
    c = np.asarray(im).astype(np.float32)
    bgc = c[12, 12]
    d = np.abs(c - bgc).max(axis=2)
    cand = d <= tol
    # some sources carry a faint 1-3px frame line; treat the outer ring as background
    ring = np.zeros_like(cand)
    ring[:4], ring[-4:], ring[:, :4], ring[:, -4:] = True, True, True, True
    # flood from the border through an opened candidate mask so the fill can't
    # leak through spots where a white trim touches the white backdrop ...
    opened = ndimage.binary_opening(cand, structure=np.ones((5, 5))) | ring
    lab, _ = ndimage.label(opened)
    keep = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    bg = np.isin(lab, keep[keep > 0])
    # ... then let it grow back a few px into the true edge pixels
    bg = ndimage.binary_dilation(bg, iterations=3, mask=cand | ring)

    fg = ~bg
    lab2, n = ndimage.label(fg)
    sizes = ndimage.sum(fg, lab2, range(1, n + 1))
    fg = np.isin(lab2, 1 + np.flatnonzero(sizes > 0.01 * sizes.max()))

    # soft edge on the 2px boundary band: alpha from distance to backdrop
    interior = ndimage.binary_erosion(fg, iterations=2)
    band = fg & ~interior
    dloc = ndimage.maximum_filter(np.where(interior, d, 0), size=9)
    alpha = np.where(interior, 1.0, 0.0).astype(np.float32)
    ab = np.clip(d / np.maximum(dloc, 1.0), 0, 1)
    ab = np.where(dloc > 1, ab, 1.0)
    alpha[band] = ab[band]
    # un-mix the backdrop from the partially transparent edge pixels
    rgb = c.copy()
    safe = band & (alpha > 0.05)
    rgb[safe] = np.clip(bgc + (c[safe] - bgc) / alpha[safe][:, None], 0, 255)

    out = np.dstack([rgb, alpha * 255]).round().astype(np.uint8)
    ys, xs = np.nonzero(alpha > 0.02)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    Image.fromarray(out[y0:y1, x0:x1], "RGBA").save(OUT.format(i))
    assert np.array_equal(out[interior][:, :3], np.asarray(im)[interior])
    print(i, "backdrop", bgc.astype(int).tolist(), "bbox", (x0, y0, x1, y1))


if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    for i in range(1, 6):
        cutout(i, TOL[i])
