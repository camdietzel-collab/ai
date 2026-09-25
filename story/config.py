"""Single source of truth for the "order to outfit" 15s ad.

Product data comes from the live Shopify store (404cultureclothing.com):
"Culture thermal", $52.99, variants Small/M/L/XL/2XL, 122 units in stock.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

W, H, FPS = 1080, 1920, 30
DUR = 15.0
N_FRAMES = int(DUR * FPS)
BPM = 120  # 1 beat = 0.5 s = 15 frames, 1 bar = 2 s

FONT_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

SITE_URL = "404cultureclothing.com"

# Hero product. Title, price, sizes and copy are exactly as listed in the store.
PRODUCT = {
    "title": "Culture thermal",
    "handle": "culture-thermal",
    "vendor": "404 Culture Clothing",
    "price": "$52.99",
    "sizes": ["Small", "M", "L", "XL", "2XL"],
    "size": "L",
    "copy": ["Premade", "100% cotton", "3-5 day shipping"],
    # ASSUMPTION: the "Culture thermal" listing is the black "Culture Never Dies"
    # thermal. If it is the cream one, point these at campaign/source/3.webp.
    "photo": os.path.join(ROOT, "campaign", "source", "1.webp"),
    "cutout": os.path.join(ROOT, "campaign", "cutouts", "1.png"),
    # focus point of the chest graphic, normalised in the cutout
    "graphic_focus": (0.49, 0.40),
}

NOTIFICATION = {
    "title": "New order",
    "body": f"{PRODUCT['title']} · Size {PRODUCT['size']} · {PRODUCT['price']}",
    "time": "4:04",
}

END_CARD = ("404 CULTURE", "PREMADE. READY TO SHIP.", SITE_URL)

# ------------------------------------------------------------------ timeline
# kind: film    -> footage/<code>.* when present, otherwise a storyboard card
#       screen  -> captured website screens on the phone
#       notify  -> the owner's phone lighting up with the staged order
#       product -> clean close-up from the real product photo
#       endcard
SHOTS = [
    dict(code="A1", t0=0.00, t1=0.90, kind="film", title="SCROLL",
         action="Thumb scrolling 404cultureclothing.com",
         frame="Close, side angle on hand + phone"),
    dict(code="S1", t0=0.90, t1=1.60, kind="screen", beat="collection"),
    dict(code="S2", t0=1.60, t1=2.40, kind="screen", beat="product"),
    dict(code="S3", t0=2.40, t1=3.20, kind="screen", beat="add"),
    dict(code="S4", t0=3.20, t1=4.00, kind="screen", beat="checkout"),
    dict(code="N1", t0=4.00, t1=5.00, kind="notify"),
    dict(code="F1", t0=5.00, t1=5.75, kind="film", title="PULL FROM STOCK",
         action="Hand pulls one thermal off the stack",
         frame="Stack of the same thermals in frame", ref="stack"),
    dict(code="F2", t0=5.75, t1=6.50, kind="film", title="FOLD",
         action="Lay it flat, fold the sleeves in",
         frame="Top-down on the table", ref="flatlay"),
    dict(code="F3", t0=6.50, t1=7.00, kind="film", title="FOLD IN HALF",
         action="Fold in half, graphic side up",
         frame="Same top-down position as F2", ref="flatlay"),
    dict(code="F4", t0=7.00, t1=7.50, kind="film", title="INTO THE MAILER",
         action="Slide the folded thermal into the mailer",
         frame="Close, 45° from above"),
    dict(code="F5", t0=7.50, t1=8.25, kind="film", title="SEAL",
         action="Peel the strip, press it shut",
         frame="Tight on the flap"),
    dict(code="F6", t0=8.25, t1=9.00, kind="film", title="LABEL",
         action="Slap on the staged label, slide it out",
         frame="Top-down, label fills the frame", ref="label"),
    dict(code="D1", t0=9.00, t1=9.75, kind="film", title="AT THE DOOR",
         action="Package on the doorstep, hand picks it up",
         frame="Low, doorstep level"),
    dict(code="D2", t0=9.75, t1=10.50, kind="film", title="OPEN",
         action="Tear the mailer open",
         frame="Close on hands"),
    dict(code="D3", t0=10.50, t1=11.25, kind="film", title="PULL IT OUT",
         action="Lift the thermal up to the lens",
         frame="End with the graphic filling the frame", ref="graphic"),
    dict(code="D4", t0=11.25, t1=12.00, kind="film", title="WEARING IT",
         action="Same framing, now worn; pull back",
         frame="Match D3's last frame exactly", ref="graphic"),
    dict(code="W1", t0=12.00, t1=13.50, kind="film", title="THE FIT",
         action="Walk, turn to camera, thumbs-up, keep walking",
         frame="Outside, full body, camera walking backwards"),
    dict(code="C1", t0=13.50, t1=14.00, kind="product"),
    dict(code="END", t0=14.00, t1=15.00, kind="endcard"),
]

# screen choreography (seconds, absolute)
TAP_CARD = 1.45
TAP_SIZE = 2.20
TAP_ADD = 2.55
DRAWER_IN = (2.70, 2.96)  # S3 cuts from the button close-up to a medium at 2.70
TAP_CHECKOUT = 3.93
NOTIFY_WAKE = 4.02
NOTIFY_IN = 4.07

# where filmed clips go: footage/<CODE>.mp4|mov, plus optional per-shot edit
# settings in footage/edit.json, e.g. {"F2": {"in": 1.2, "speed": 0.8}}
FOOTAGE_DIR = os.environ.get("STORY_FOOTAGE", os.path.join(HERE, "footage"))
BUILD = os.path.join(HERE, "build")
SCREENS = os.path.join(BUILD, "screens")


def frame_of(t):
    return int(round(t * FPS))


def shot_at(f):
    t = f / FPS
    for s in SHOTS:
        if s["t0"] <= t < s["t1"]:
            return s
    return SHOTS[-1]
