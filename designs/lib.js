// Shared building blocks for the 404 CULTURE design mockups:
// seeded randomness, fonts, tee silhouettes, fabric/wash/distress filters,
// and the page frame (background, header logo, footer).
const fs = require("fs");
const path = require("path");

const W = 1200, H = 1500;

function rng(seed) {
  let a = seed >>> 0;
  const r = () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
  r.range = (lo, hi) => lo + (hi - lo) * r();
  r.pick = (arr) => arr[Math.floor(r() * arr.length)];
  return r;
}

const f = (n) => (Math.round(n * 10) / 10).toString();

const FONTS = {
  Graduate: "Graduate.ttf", Yellowtail: "Yellowtail.ttf", Caslon: "Caslon.ttf",
  BarlowXBI: "BarlowXBI.ttf", BarlowCond: "BarlowCond.ttf", Pirata: "Pirata.ttf",
  Unifraktur: "Unifraktur.ttf", Pinyon: "Pinyon.ttf", Sedgwick: "Sedgwick.ttf",
  ArchivoBlack: "ArchivoBlack.ttf", Oswald: "Oswald.ttf",
};

function fontCSS() {
  return Object.entries(FONTS).map(([name, file]) => {
    const b64 = fs.readFileSync(path.join(__dirname, "fonts", file)).toString("base64");
    return `@font-face{font-family:'${name}';src:url(data:font/ttf;base64,${b64}) format('truetype');}`;
  }).join("\n");
}

// ------------------------------------------------------------ silhouettes
// Each tee returns { body, sleeves, outline, collar, hem, cuffs } in a 1200x1500 frame.

function boxyTee(o = {}) {
  const cx = 600, top = o.top ?? 250, hem = o.hem ?? 1160, half = o.half ?? 270;
  const L = cx - half, R = cx + half;
  const outline =
    `M ${cx - 95} ${top} Q ${cx} ${top + 52} ${cx + 95} ${top}` +
    ` L ${R + 8} ${top + 32} C ${R + 90} ${top + 70} ${R + 150} ${top + 190} ${R + 195} ${top + 318}` +
    ` L ${R + 62} ${top + 398} L ${R + 2} ${top + 318}` +
    ` L ${R + 6} ${hem} Q ${cx} ${hem + 16} ${L - 6} ${hem}` +
    ` L ${L - 2} ${top + 318} L ${L - 62} ${top + 398} L ${L - 195} ${top + 318}` +
    ` C ${L - 150} ${top + 190} ${L - 90} ${top + 70} ${L - 8} ${top + 32} Z`;
  return {
    kind: "short", cx, top, hem, L, R, outline,
    neck: { l: cx - 95, r: cx + 95, y: top, dip: 52 },
    hemLine: [[L - 6, hem], [cx, hem + 8], [R + 6, hem]],
    cuffs: [[[L - 195, top + 318], [L - 62, top + 398]], [[R + 195, top + 318], [R + 62, top + 398]]],
    shoulders: [[L - 8, top + 32, L - 2, top + 318], [R + 8, top + 32, R + 2, top + 318]],
  };
}

function longTee(o = {}) {
  const cx = 600, top = o.top ?? 250, hem = o.hem ?? 1110, half = o.half ?? 262;
  const L = cx - half, R = cx + half, cuffY = o.cuffY ?? 1190;
  const outline =
    `M ${cx - 92} ${top} Q ${cx} ${top + 48} ${cx + 92} ${top}` +
    ` L ${R + 10} ${top + 36} C ${R + 90} ${top + 70} ${R + 130} ${top + 260} ${R + 150} ${top + 520}` +
    ` L ${R + 172} ${cuffY - 10} L ${R + 70} ${cuffY} L ${R + 42} ${top + 560} L ${R + 12} ${top + 360}` +
    ` L ${R + 8} ${hem} Q ${cx} ${hem + 14} ${L - 8} ${hem}` +
    ` L ${L - 12} ${top + 360} L ${L - 42} ${top + 560} L ${L - 70} ${cuffY} L ${L - 172} ${cuffY - 10}` +
    ` L ${L - 150} ${top + 520} C ${L - 130} ${top + 260} ${L - 90} ${top + 70} ${L - 10} ${top + 36} Z`;
  return {
    kind: "long", cx, top, hem, L, R, outline,
    neck: { l: cx - 92, r: cx + 92, y: top, dip: 48 },
    hemLine: [[L - 8, hem], [cx, hem + 7], [R + 8, hem]],
    cuffs: [[[L - 172, cuffY - 10], [L - 70, cuffY]], [[R + 172, cuffY - 10], [R + 70, cuffY]]],
    shoulders: [[L - 10, top + 36, L - 12, top + 360], [R + 10, top + 36, R + 12, top + 360]],
    sleeveLines: [[L - 12, top + 360, L - 42, top + 560], [R + 12, top + 360, R + 42, top + 560]],
  };
}

// ------------------------------------------------------------ filters

function defs(id, t, s) {
  // s: style { base, wash, washAmt, fade, grain, seed, waffle }
  return `
  <clipPath id="${id}-clip"><path d="${t.outline}"/></clipPath>
  <filter id="${id}-grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="${s.seed}"/>
    <feColorMatrix type="saturate" values="0"/>
  </filter>
  <filter id="${id}-wash" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="${s.washFreq ?? 0.0065}" numOctaves="5" seed="${s.seed + 7}"/>
    <feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  ${s.washGain ?? 3.2} 0 0 0 ${s.washBias ?? -1.35}"/>
  </filter>
  <filter id="${id}-wash2" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.02 0.004" numOctaves="4" seed="${s.seed + 19}"/>
    <feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  2.6 0 0 0 -1.25"/>
  </filter>
  <filter id="${id}-soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="18"/></filter>
  <filter id="${id}-soft2" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="7"/></filter>
  <filter id="${id}-shadow" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur in="SourceAlpha" stdDeviation="14"/><feOffset dy="12"/>
    <feComponentTransfer><feFuncA type="linear" slope="${s.shadowAmt ?? 0.35}"/></feComponentTransfer>
  </filter>
  <filter id="${id}-print" x="-10%" y="-10%" width="120%" height="120%">
    <feTurbulence type="fractalNoise" baseFrequency="${s.printFreq ?? 0.045}" numOctaves="4" seed="${s.seed + 3}" result="n"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  ${-(s.printCrack ?? 3.0)} 0 0 0 ${s.printKeep ?? 2.25}" result="m"/>
    <feTurbulence type="fractalNoise" baseFrequency="0.6" numOctaves="1" seed="${s.seed + 5}" result="n2"/>
    <feColorMatrix in="n2" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  ${-4 * (s.speckle ?? 1)} 0 0 0 ${1 + 2.1 * (s.speckle ?? 1)}" result="m2"/>
    <feComposite in="m" in2="m2" operator="in" result="mm"/>
    <feComposite in="SourceGraphic" in2="mm" operator="in"/>
  </filter>
  ${s.waffle ? `
  <pattern id="${id}-waffle" width="6.5" height="6.5" patternUnits="userSpaceOnUse">
    <rect width="6.5" height="6.5" fill="none"/>
    <path d="M0 0.6 H6.5 M0.6 0 V6.5" stroke="#000" stroke-width="1.1" opacity="0.5"/>
    <rect x="1.6" y="1.6" width="4" height="4" rx="1" fill="#fff" opacity="0.25"/>
  </pattern>` : ""}`;
}

// Soft fold/shade strokes inside the garment.
function folds(t, r, dark = 0.18, light = 0.07, id = "") {
  let out = `<g filter="url(#${id}-soft)">`;
  const { L, R, top, hem } = t;
  for (let i = 0; i < 7; i++) {
    const x = r.range(L + 40, R - 40), y = r.range(top + 350, hem - 80);
    const dx = r.range(-160, 160), dy = r.range(60, 220);
    out += `<path d="M ${f(x)} ${f(y)} q ${f(dx / 2)} ${f(dy / 3)} ${f(dx)} ${f(dy)}" stroke="#000" stroke-width="${f(r.range(18, 40))}" opacity="${dark}" fill="none" stroke-linecap="round"/>`;
    out += `<path d="M ${f(x + 26)} ${f(y - 6)} q ${f(dx / 2)} ${f(dy / 3)} ${f(dx)} ${f(dy)}" stroke="#fff" stroke-width="${f(r.range(10, 22))}" opacity="${light}" fill="none" stroke-linecap="round"/>`;
  }
  // underarm drapes
  for (const s of [-1, 1]) {
    const x = t.cx + s * (R - t.cx - 20);
    out += `<path d="M ${x} ${top + 340} q ${-s * 70} 140 ${-s * 40} 320" stroke="#000" stroke-width="44" opacity="${dark}" fill="none"/>`;
  }
  return out + "</g>";
}

function holes(r, cx, cy, n, spread, bg, rim, sizeMax = 6) {
  let out = "";
  for (let i = 0; i < n; i++) {
    const x = cx + r.range(-spread, spread), y = cy + r.range(-spread * 0.7, spread * 0.7);
    const rad = r.range(1.8, sizeMax), k = 7 + Math.floor(r() * 4);
    let d = "";
    for (let j = 0; j < k; j++) {
      const a = (j / k) * Math.PI * 2, rr = rad * r.range(0.45, 1.25) * (j % 2 ? 0.8 : 1.15);
      d += `${j ? "L" : "M"} ${f(x + Math.cos(a) * rr * 1.5)} ${f(y + Math.sin(a) * rr)} `;
    }
    out += `<path d="${d}Z" fill="none" stroke="${rim}" stroke-width="3.2" opacity="0.55" stroke-dasharray="2 1.5"/>`;
    out += `<path d="${d}Z" fill="${bg}"/>`;
    // loose threads crossing the hole
    if (r() < 0.5) out += `<path d="M ${f(x - rad)} ${f(y + r.range(-2, 2))} q ${f(rad)} ${f(r.range(-4, 4))} ${f(rad * 2)} ${f(r.range(-3, 3))}" stroke="${rim}" stroke-width="1.1" opacity="0.8" fill="none"/>`;
  }
  return out;
}

// Frayed raw edge along a polyline (holes bitten out + hanging threads).
function rawEdge(r, pts, bg, thread, dir = 1, amt = 1) {
  let out = "";
  for (let s = 0; s < pts.length - 1; s++) {
    const [x0, y0] = pts[s], [x1, y1] = pts[s + 1];
    const len = Math.hypot(x1 - x0, y1 - y0), n = Math.floor(len / 9);
    for (let i = 0; i < n; i++) {
      const u = i / n, x = x0 + (x1 - x0) * u, y = y0 + (y1 - y0) * u;
      if (r() < 0.35 * amt) {
        const w = r.range(2, 7), h = r.range(2, 9) * amt;
        out += `<path d="M ${f(x - w)} ${f(y + 2 * dir)} Q ${f(x)} ${f(y - h * dir)} ${f(x + w)} ${f(y + 2 * dir)} Z" fill="${bg}"/>`;
      }
      if (r() < 0.22 * amt) {
        const l = r.range(6, 26);
        out += `<path d="M ${f(x)} ${f(y - 3 * dir)} q ${f(r.range(-6, 6))} ${f(l / 2 * dir)} ${f(r.range(-8, 8))} ${f(l * dir)}" stroke="${thread}" stroke-width="1.3" fill="none" opacity="0.85"/>`;
      }
    }
  }
  return out;
}

function stitches(pts, color, off = 0, opacity = 0.5) {
  const d = pts.map(([x, y], i) => `${i ? "L" : "M"} ${x} ${y + off}`).join(" ");
  return `<path d="${d}" stroke="${color}" stroke-width="1.6" stroke-dasharray="5 4" fill="none" opacity="${opacity}"/>`;
}

// ------------------------------------------------------------ garment

// style: { base, light, dark, seed, washAmt, wash2Amt, fadeAmt, bg, holes:[[x,y,n,spread]], raw:{hem,cuffs,collar}, waffle, label:{...} }
// print: SVG string placed on the chest (already positioned in page coords)
function garment(id, t, s, print, extra = "") {
  const r = rng(s.seed);
  const neckBack = `M ${t.neck.l} ${t.neck.y} Q ${t.cx} ${t.neck.y - 26} ${t.neck.r} ${t.neck.y} Q ${t.cx} ${t.neck.y + t.neck.dip - 6} ${t.neck.l} ${t.neck.y} Z`;
  const collar = `M ${t.neck.l - 4} ${t.neck.y - 2} Q ${t.cx} ${t.neck.y + t.neck.dip + 8} ${t.neck.r + 4} ${t.neck.y - 2}`;
  let body = "";
  body += `<path d="${t.outline}" fill="${s.base}"/>`;
  if (s.waffle) body += `<rect width="${W}" height="${H}" fill="url(#${id}-waffle)" opacity="${s.waffleAmt ?? 0.35}"/>`;
  // acid wash blotches + vertical streaks
  body += `<rect width="${W}" height="${H}" filter="url(#${id}-wash)" opacity="${(s.washAmt ?? 0.12) * 0.55}" style="mix-blend-mode:screen"/>`;
  body += `<rect width="${W}" height="${H}" filter="url(#${id}-wash2)" opacity="${(s.wash2Amt ?? 0.06) * 0.6}" style="mix-blend-mode:screen"/>`;
  // sun-faded seams / edges
  body += `<path d="${t.outline}" fill="none" stroke="${s.light}" stroke-width="50" opacity="${(s.fadeAmt ?? 0.35) * 0.6}" filter="url(#${id}-soft)"/>`;
  for (const [x0, y0, x1, y1] of t.shoulders)
    body += `<path d="M ${x0} ${y0} L ${x1} ${y1}" stroke="${s.light}" stroke-width="26" opacity="${(s.fadeAmt ?? 0.35) * 0.8}" filter="url(#${id}-soft2)"/>`;
  body += `<path d="${collar}" fill="none" stroke="${s.light}" stroke-width="40" opacity="${(s.fadeAmt ?? 0.35) * 0.7}" filter="url(#${id}-soft)"/>`;
  body += folds(t, r, s.foldDark ?? 0.3, s.foldLight ?? 0.1, id);
  // print sits in the fabric
  body += `<g filter="url(#${id}-print)" opacity="${s.printOpacity ?? 0.92}" style="mix-blend-mode:${s.printBlend ?? "normal"}">${print}</g>`;
  // grain over everything
  body += `<rect width="${W}" height="${H}" filter="url(#${id}-grain)" opacity="${s.grainAmt ?? 0.16}" style="mix-blend-mode:overlay"/>`;
  // seams
  for (const [x0, y0, x1, y1] of t.shoulders)
    body += `<path d="M ${x0} ${y0} L ${x1} ${y1}" stroke="${s.dark}" stroke-width="2" opacity="0.5"/>`;
  if (t.sleeveLines) for (const [x0, y0, x1, y1] of t.sleeveLines)
    body += `<path d="M ${x0} ${y0} L ${x1} ${y1}" stroke="${s.dark}" stroke-width="2" opacity="0.4"/>`;
  if (!s.raw?.hem) body += stitches(t.hemLine, s.light, -22, 0.35);
  if (!s.raw?.cuffs) for (const c of t.cuffs) body += stitches(c.map(([x, y]) => [x, y - 20]), s.light, 0, 0.3);
  body += extra;

  let out = `<g filter="url(#${id}-shadow)"><path d="${t.outline}" fill="#000"/></g>`;
  out += `<g clip-path="url(#${id}-clip)">${body}</g>`;
  // inside back neck + label
  out += `<path d="${neckBack}" fill="${s.inside ?? s.dark}"/>`;
  out += `<path d="${neckBack}" fill="#000" opacity="0.25"/>`;
  if (s.label) out += s.label(t);
  // rib collar
  out += `<path d="${collar}" fill="none" stroke="${s.collar ?? s.base}" stroke-width="20"/>`;
  out += `<path d="${collar}" fill="none" stroke="${s.dark}" stroke-width="20" stroke-dasharray="1.2 3.2" opacity="0.5"/>`;
  out += `<path d="${collar}" fill="none" stroke="${s.light}" stroke-width="20" opacity="${(s.fadeAmt ?? 0.35) * 0.45}"/>`;
  out += `<path d="M ${t.neck.l - 4} ${t.neck.y - 2} Q ${t.cx} ${t.neck.y - 30} ${t.neck.r + 4} ${t.neck.y - 2}" fill="none" stroke="${s.collar ?? s.base}" stroke-width="14"/>`;
  // distress: holes, raw edges
  const bg = s.bg;
  for (const [x, y, n, spread, sz] of s.holes ?? []) out += holes(r, x, y, n, spread, bg, s.light, sz);
  if (s.raw?.hem) out += rawEdge(r, t.hemLine, bg, s.thread ?? s.light, 1, s.raw.hem);
  if (s.raw?.cuffs) for (const c of t.cuffs) out += rawEdge(r, c, bg, s.thread ?? s.light, 1, s.raw.cuffs);
  if (s.raw?.collar) out += rawEdge(r, [[t.neck.l - 6, t.neck.y - 6], [t.cx, t.neck.y + t.neck.dip - 12], [t.neck.r + 6, t.neck.y - 6]], s.dark, s.thread ?? s.light, -1, s.raw.collar);
  return `<defs>${defs(id, t, s)}</defs>${out}`;
}

// Woven neck label "404" and small sleeve tag.
function neckLabel(color = "#c8201e", text = "#fff") {
  return (t) => `<g transform="translate(${t.cx} ${t.neck.y - 4})">
    <rect x="-34" y="-3" width="68" height="24" rx="2" fill="${color}"/>
    <rect x="-34" y="-3" width="68" height="24" rx="2" fill="none" stroke="#000" stroke-opacity=".25"/>
    <text x="0" y="15" text-anchor="middle" font-family="ArchivoBlack" font-size="15" fill="${text}" letter-spacing="1">404</text></g>`;
}

function sleeveTag(x, y, rot, color = "#e9e6df", text = "#111") {
  return `<g transform="translate(${x} ${y}) rotate(${rot})">
    <rect x="-9" y="-19" width="18" height="38" fill="${color}"/>
    <text transform="rotate(-90)" x="0" y="4" text-anchor="middle" font-family="Oswald" font-size="11" fill="${text}" letter-spacing="1">404</text></g>`;
}

// ------------------------------------------------------------ page

function page(svgBody, o = {}) {
  const dark = o.dark;
  const bg = o.bg ?? (dark ? "#050505" : "#ffffff");
  const fg = dark ? "#e8e8e8" : "#111";
  let chrome = "";
  if (o.header !== false) {
    chrome += `<g transform="translate(600 70)">
      <text x="0" y="0" text-anchor="middle" font-family="Pirata" font-size="40" fill="${fg}">404</text>
      <text x="0" y="22" text-anchor="middle" font-family="ArchivoBlack" font-size="13" letter-spacing="5" fill="${fg}">CULTURE</text>
      <rect x="-66" y="30" width="132" height="11" fill="${fg}"/>
      <text x="0" y="38.5" text-anchor="middle" font-family="Oswald" font-size="7.5" letter-spacing="1.2" fill="${bg}">PREMADE DESIGN · 404-${o.code ?? "000"}</text></g>`;
  }
  if (o.footer) {
    chrome += `<g font-family="ArchivoBlack" font-size="15" fill="${fg}" text-anchor="middle" letter-spacing="1.2">
      ${o.footer.map((l, i) => `<text x="600" y="${1400 + i * 22}">${l}</text>`).join("")}</g>`;
  }
  return `<!doctype html><html><head><meta charset="utf-8"><style>${fontCSS()}
    html,body{margin:0;background:${bg}}svg{display:block}</style></head><body>
    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
    <rect width="${W}" height="${H}" fill="${bg}"/>${o.backdrop ?? ""}${svgBody}${chrome}</svg>
    ${o.script ? `<script>${o.script}</script>` : "<script>window.__done=true</script>"}</body></html>`;
}

module.exports = { W, H, rng, f, boxyTee, longTee, garment, neckLabel, sleeveTag, page };
