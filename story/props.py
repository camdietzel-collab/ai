"""Printable props for the shoot.

props/staged_shipping_label_4x6.png/.pdf: a 4x6in thermal-label-sized prop
for shot F6. It carries no customer name, no address and no tracking number;
the barcode encodes nothing.
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from config import FONT_BOLD, FONT_REG, HERE, SITE_URL

DPI = 300
LW, LH = 4 * DPI, 6 * DPI
OUT = os.path.join(HERE, "props")


def font(size, bold=True):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def label():
    rng = np.random.default_rng(404)
    im = Image.new("L", (LW, LH), 255)
    d = ImageDraw.Draw(im)
    m = 36
    d.rectangle([m, m, LW - m, LH - m], outline=0, width=8)

    # sender: brand only
    d.text((m + 36, m + 34), "FROM", font=font(34), fill=0)
    d.text((m + 36, m + 80), "404 CULTURE", font=font(64), fill=0)
    d.text((m + 36, m + 158), SITE_URL, font=font(38, bold=False), fill=0)
    # big routing box
    bx = LW - m - 300
    d.rectangle([bx, m, LW - m, m + 250], fill=0)
    w = d.textlength("404", font=font(120))
    d.text((bx + 150 - w / 2, m + 58), "404", font=font(120), fill=255)
    y = m + 250
    d.line([m, y, LW - m, y], fill=0, width=8)

    # service band
    d.rectangle([m, y, LW - m, y + 150], fill=0)
    w = d.textlength("STANDARD", font=font(92))
    d.text((LW / 2 - w / 2, y + 26), "STANDARD", font=font(92), fill=255)
    y += 150

    # ship-to: deliberately blank bars
    d.text((m + 36, y + 40), "SHIP TO", font=font(34), fill=0)
    for k, frac in enumerate((0.62, 0.78, 0.55)):
        yy = y + 100 + k * 78
        d.rounded_rectangle([m + 36, yy, m + 36 + (LW - 2 * m - 72) * frac, yy + 46], 8, fill=200)
    y += 100 + 3 * 78 + 40
    d.line([m, y, LW - m, y], fill=0, width=8)

    # meaningless barcode (no digits printed)
    bar_top, bar_h = y + 60, 330
    x, ink = m + 70, True
    while x < LW - m - 90:
        bw = int(rng.choice([4, 4, 8, 8, 12, 16]))
        if ink:
            d.rectangle([x, bar_top, x + bw - 1, bar_top + bar_h], fill=0)
        x, ink = x + bw, not ink
    y = bar_top + bar_h + 60
    d.line([m, y, LW - m, y], fill=0, width=8)

    # 2D code block (random, encodes nothing) + weight
    cell, n = 18, 22
    cx0, cy0 = m + 60, y + 50
    grid = rng.random((n, n)) < 0.5
    for i in range(n):
        for j in range(n):
            if grid[i, j]:
                d.rectangle([cx0 + j * cell, cy0 + i * cell, cx0 + (j + 1) * cell - 1, cy0 + (i + 1) * cell - 1], fill=0)
    for (a, b) in ((0, 0), (0, n - 7), (n - 7, 0)):
        d.rectangle([cx0 + b * cell, cy0 + a * cell, cx0 + (b + 7) * cell - 1, cy0 + (a + 7) * cell - 1], fill=255)
        d.rectangle([cx0 + b * cell, cy0 + a * cell, cx0 + (b + 7) * cell - 1, cy0 + (a + 7) * cell - 1], outline=0, width=cell)
        d.rectangle([cx0 + (b + 2) * cell, cy0 + (a + 2) * cell, cx0 + (b + 5) * cell - 1, cy0 + (a + 5) * cell - 1], fill=0)
    tx = cx0 + n * cell + 60
    d.text((tx, cy0 + 10), "WT  1 LB", font=font(46), fill=0)
    d.text((tx, cy0 + 80), "PKG 1 / 1", font=font(46), fill=0)
    d.text((tx, cy0 + 150), "PREMADE", font=font(46), fill=0)
    d.text((tx, cy0 + 220), "READY TO SHIP", font=font(46), fill=0)
    return im


def main():
    os.makedirs(OUT, exist_ok=True)
    im = label()
    im.save(os.path.join(OUT, "staged_shipping_label_4x6.png"), dpi=(DPI, DPI))
    im.convert("RGB").save(os.path.join(OUT, "staged_shipping_label_4x6.pdf"), resolution=DPI)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
