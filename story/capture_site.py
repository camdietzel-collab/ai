"""Capture the phone-screen states of the store's buy flow.

    python3 capture_site.py            # local stand-in (story/site), default
    python3 capture_site.py --live     # https://404cultureclothing.com

Writes build/screens/*.png at iPhone resolution (390 css px wide, 3x) plus
meta.json with the on-page boxes the edit animates taps onto.

Live mode only browses, picks a size and adds one item to a throwaway browser
cart. It never presses "Check out" (the pressed state is a style change) and
never enters any details.
"""
import functools
import http.server
import json
import os
import re
import sys
import threading

from playwright.sync_api import sync_playwright

from config import PRODUCT, PRODUCTS, SCREENS, HERE

VIEW_W, VIEW_H = 390, 714  # web area between the status bar and browser bar
DPR = 3
UA = ("Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 "
      "(KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1")


def build_standin_pages():
    """Stand-in product pages for every listing, from the store's own data."""
    tpl = open(os.path.join(HERE, "site", "product_template.html")).read()
    for p in PRODUCTS.values():
        pills = "\n".join(
            f'          <input type="radio" name="Size" id="s-{v}" value="{v}"><label for="s-{v}">{v}</label>'
            for v in p["sizes"])
        html = tpl.format(title=p["title"], price=p["price"], img=p["site_img"], pills=pills,
                          size=p["size"], copy="".join(f"<p>{c}</p>" for c in p["copy"]))
        out = os.path.join(HERE, "site", "products", p["handle"])
        os.makedirs(out, exist_ok=True)
        with open(os.path.join(out, "index.html"), "w") as fh:
            fh.write(html)


def serve_standin():
    build_standin_pages()
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass

    handler = functools.partial(Quiet, directory=os.path.join(HERE, "site"))
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, f"http://127.0.0.1:{srv.server_address[1]}"


def box(page, locator):
    """Bounding box in page (document) css px."""
    b = locator.bounding_box()
    sy = page.evaluate("window.scrollY")
    return {"x": b["x"], "y": b["y"] + sy, "w": b["width"], "h": b["height"]}


def first_visible(page, *candidates):
    for c in candidates:
        loc = c(page)
        try:
            n = loc.count()
        except Exception:
            continue
        for i in range(n):
            if loc.nth(i).is_visible():
                return loc.nth(i)
    raise RuntimeError("element not found: none of the selectors matched")


def settle(page):
    page.wait_for_load_state("networkidle")
    # trigger lazy images, then back to top
    h = page.evaluate("document.body.scrollHeight")
    for y in range(0, h, 500):
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(60)
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(400)
    page.keyboard.press("Escape")  # close newsletter / cookie pop-ups if any


def capture(live=False):
    os.makedirs(SCREENS, exist_ok=True)
    srv = None
    if live:
        base = "https://404cultureclothing.com"
    else:
        srv, base = serve_standin()
    meta = {"source": base if live else "stand-in", "view": [VIEW_W, VIEW_H], "dpr": DPR}
    handle, size = PRODUCT["handle"], PRODUCT["size"]
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": VIEW_W, "height": VIEW_H},
                                  device_scale_factor=DPR, is_mobile=True,
                                  has_touch=True, user_agent=UA)
        page = ctx.new_page()

        # 1. collection page, full length (scrolled by the edit)
        page.goto(f"{base}/collections/all")
        settle(page)
        card = first_visible(page, lambda pg: pg.locator(f'a[href*="/products/{handle}"]'))
        meta["card"] = box(page, card)
        meta["collection_h"] = page.evaluate("document.documentElement.scrollHeight")
        page.screenshot(path=os.path.join(SCREENS, "collection.png"), full_page=True)

        # 2. product page
        page.goto(f"{base}/products/{handle}")
        settle(page)
        size_opt = first_visible(
            page,
            lambda pg: pg.locator("fieldset label").filter(has_text=re.compile(rf"^\s*{size}\s*$")),
            lambda pg: pg.get_by_role("radio", name=size, exact=True),
            lambda pg: pg.get_by_role("button", name=size, exact=True),
        )
        add = first_visible(
            page,
            lambda pg: pg.locator('form[action*="/cart/add"] [name="add"], .product-form [name="add"]'),
            lambda pg: pg.get_by_role("button", name=re.compile(r"add to (cart|bag)", re.I)),
        )
        # frame the product page so the size row and the button are on screen
        page.evaluate("window.scrollTo(0, 0)")
        meta["size"] = box(page, size_opt)
        meta["add"] = box(page, add)
        meta["title"] = box(page, first_visible(page, lambda pg: pg.locator("h1")))
        meta["product_scroll"] = max(0, meta["add"]["y"] + meta["add"]["h"] + 10 - VIEW_H)
        page.evaluate(f"window.scrollTo(0, {meta['product_scroll']})")
        page.wait_for_timeout(200)
        page.screenshot(path=os.path.join(SCREENS, "product.png"))
        size_opt.click()
        page.wait_for_timeout(500)
        page.screenshot(path=os.path.join(SCREENS, "product_size.png"))
        add.evaluate("el => el.classList.add('pressed')") if not live else \
            add.evaluate("el => el.style.filter = 'brightness(.72)'")
        page.screenshot(path=os.path.join(SCREENS, "product_add_pressed.png"))
        add.evaluate("el => { el.classList.remove('pressed'); el.style.filter = '' }")

        # 3. add to cart -> drawer / cart notification
        add.click()
        page.wait_for_timeout(1500)
        checkout = first_visible(
            page,
            lambda pg: pg.locator('[name="checkout"]'),
            lambda pg: pg.get_by_role("button", name=re.compile(r"check ?out", re.I)),
            lambda pg: pg.get_by_role("link", name=re.compile(r"check ?out", re.I)),
        )
        meta["checkout"] = box(page, checkout)
        item = first_visible(
            page,
            lambda pg: pg.locator("#CartDrawer, cart-drawer, .cart-drawer, #cart-notification, .cart-notification")
            .get_by_text(PRODUCT["title"], exact=True),
            lambda pg: pg.get_by_text(PRODUCT["title"], exact=True),
        )
        meta["item"] = box(page, item)
        meta["cart_scroll"] = page.evaluate("window.scrollY")
        page.screenshot(path=os.path.join(SCREENS, "cart.png"))
        checkout.evaluate("el => el.style.filter = 'brightness(.72)'")
        page.screenshot(path=os.path.join(SCREENS, "cart_pressed.png"))
        # never click checkout
        browser.close()
    if srv:
        srv.shutdown()
    with open(os.path.join(SCREENS, "meta.json"), "w") as fh:
        json.dump(meta, fh, indent=2)
    print("captured", meta["source"], "->", SCREENS)


if __name__ == "__main__":
    capture(live="--live" in sys.argv)
