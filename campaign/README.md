# 404 CULTURE: New Collection (15s, 9:16)

`404_culture_new_collection_15s_9x16.mp4`: 1080x1920, 30 fps, H.264 + AAC, loudness-normalised to -14 LUFS.

| Time | Beat |
|---|---|
| 0:00–0:02 | Tight moving detail of the black thermal print, then a fast pull-back. **404 CULTURE / NEW COLLECTION** |
| 0:02–0:09 | Five pieces in upload order, each with its own transition: whip-out, whip-in, punch-in match cut, spin-out, spin-in, then a hard colour-swap match cut from Baby Blue to Navy/Red. Name and price appear under each garment. |
| 0:09–0:12 | Montage cut on 8th notes (print details and full silhouettes), ending with all five pieces landing in a collection shot. |
| 0:12–0:15 | 100% PREMADE / 100% COTTON / 3–5 DAY SHIPPING / COLLECTION LIVE NOW, then the final bass hit and **404 CULTURE**, 404cultureclothing.com |

## Rebuild

```
pip install pillow numpy scipy imageio-ffmpeg
python3 cutout.py    # source/*.webp -> cutouts/*.png (adds alpha only)
python3 audio.py     # build/audio.wav
python3 render.py    # build/video_only.mp4
ffmpeg -i build/video_only.mp4 -i build/audio.wav -af loudnorm=I=-14:TP=-1 \
  -c:v libx264 -crf 20 -pix_fmt yuv420p -c:a aac -b:a 256k -movflags +faststart \
  404_culture_new_collection_15s_9x16.mp4
```

Product accuracy: garments come straight from the uploaded photos. `cutout.py` adds an alpha channel. Interior pixels are asserted to be bit-identical to the source, and only the 1–2px anti-aliased edge has the studio backdrop un-mixed. The renderer only moves, scales, rotates and motion-blurs the garments. They are never recoloured or redrawn.
