// Effects for designs 2–5: halftone photo prints, thermal heat-map glow,
// gothic line art (bats, barbed wire, thorns, wings), and molten lava fill.
const { rng, f } = require("./lib");

// ---------------------------------------------------------------- halftone
// Scene is a grayscale SVG string (w x h). The page script rasterises it and
// replaces <image id> with dots of `ink` (dark = big dots unless invert).
function halftoneScript(jobs) {
  return `
  (async () => {
    for (const j of ${JSON.stringify(jobs)}) {
      const S = 3, img = new Image();
      img.src = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(j.scene);
      await img.decode();
      const c = document.createElement('canvas'); c.width = j.w * S; c.height = j.h * S;
      const g = c.getContext('2d'); g.drawImage(img, 0, 0, c.width, c.height);
      const px = g.getImageData(0, 0, c.width, c.height).data;
      const o = document.createElement('canvas'); o.width = c.width; o.height = c.height;
      const h = o.getContext('2d'); h.fillStyle = j.ink;
      const p = j.pitch * S, ang = j.angle * Math.PI / 180, ca = Math.cos(ang), sa = Math.sin(ang);
      const R = Math.hypot(c.width, c.height);
      for (let v = -R; v < R; v += p) for (let u = -R; u < R; u += p) {
        const x = c.width / 2 + u * ca - v * sa, y = c.height / 2 + u * sa + v * ca;
        if (x < 0 || y < 0 || x >= c.width || y >= c.height) continue;
        const i = (Math.floor(y) * c.width + Math.floor(x)) * 4;
        let l = (px[i] * 0.3 + px[i + 1] * 0.59 + px[i + 2] * 0.11) / 255;
        if (!j.invert) l = 1 - l;
        l = Math.pow(l, j.gamma);
        if (l < 0.03) continue;
        h.beginPath(); h.arc(x, y, p * 0.62 * Math.sqrt(l), 0, Math.PI * 2); h.fill();
      }
      document.getElementById(j.id).setAttribute('href', o.toDataURL());
    }
    window.__done = true;
  })();`;
}

function crtScene(w, h) {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">
  <defs>
    <radialGradient id="bg" cx=".55" cy=".35" r=".9"><stop offset="0" stop-color="#5a5a5a"/><stop offset="1" stop-color="#050505"/></radialGradient>
    <linearGradient id="body" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#d8d8d8"/><stop offset=".5" stop-color="#8a8a8a"/><stop offset="1" stop-color="#2a2a2a"/></linearGradient>
    <radialGradient id="scr" cx=".45" cy=".45" r=".7"><stop offset="0" stop-color="#ffffff"/><stop offset=".55" stop-color="#bdbdbd"/><stop offset="1" stop-color="#303030"/></radialGradient>
    <filter id="bl"><feGaussianBlur stdDeviation="6"/></filter>
    <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1.6" fill="#000" opacity=".35"/></pattern>
  </defs>
  <rect width="${w}" height="${h}" fill="url(#bg)"/>
  <path d="M ${w * 0.38} ${h * 0.28} L ${w * 0.2} ${h * 0.02} M ${w * 0.5} ${h * 0.28} L ${w * 0.78} ${h * 0.04}" stroke="#cfcfcf" stroke-width="5"/>
  <circle cx="${w * 0.2}" cy="${h * 0.02}" r="7" fill="#eee"/><circle cx="${w * 0.78}" cy="${h * 0.04}" r="7" fill="#eee"/>
  <ellipse cx="${w * 0.44}" cy="${h * 0.29}" rx="${w * 0.1}" ry="${h * 0.03}" fill="#6a6a6a"/>
  <rect x="${w * 0.02}" y="${h * 0.86}" width="${w * 0.96}" height="${h * 0.2}" fill="#1c1c1c"/>
  <rect x="${w * 0.08}" y="${h * 0.3}" width="${w * 0.84}" height="${h * 0.58}" rx="26" fill="url(#body)"/>
  <rect x="${w * 0.08}" y="${h * 0.3}" width="${w * 0.84}" height="${h * 0.58}" rx="26" fill="none" stroke="#000" stroke-width="4" opacity=".6"/>
  <rect x="${w * 0.13}" y="${h * 0.36}" width="${w * 0.56}" height="${h * 0.44}" rx="34" fill="#111"/>
  <rect x="${w * 0.15}" y="${h * 0.38}" width="${w * 0.52}" height="${h * 0.40}" rx="30" fill="url(#scr)"/>
  <text x="${w * 0.41}" y="${h * 0.64}" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="${w * 0.2}" fill="#1a1a1a" filter="url(#bl)" opacity=".6">404</text>
  <text x="${w * 0.41}" y="${h * 0.64}" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="${w * 0.2}" fill="#2a2a2a">404</text>
  <rect x="${w * 0.15}" y="${h * 0.38}" width="${w * 0.52}" height="${h * 0.40}" rx="30" fill="url(#scan)"/>
  <ellipse cx="${w * 0.3}" cy="${h * 0.44}" rx="${w * 0.1}" ry="${h * 0.03}" fill="#fff" opacity=".7" filter="url(#bl)"/>
  <circle cx="${w * 0.8}" cy="${h * 0.45}" r="${w * 0.055}" fill="#333" stroke="#eee" stroke-width="3"/>
  <circle cx="${w * 0.8}" cy="${h * 0.6}" r="${w * 0.055}" fill="#333" stroke="#eee" stroke-width="3"/>
  ${Array.from({ length: 6 }, (_, i) => `<rect x="${w * 0.74}" y="${h * (0.7 + i * 0.022)}" width="${w * 0.12}" height="${h * 0.01}" fill="#222"/>`).join("")}
  <rect x="0" y="0" width="${w}" height="${h}" fill="none" stroke="#000" stroke-width="40" filter="url(#bl)"/>
  </svg>`;
}

function phoneScene(w, h) {
  const cx = w * 0.5, dy = h * 0.6, R = w * 0.2;
  let holes = "";
  for (let i = 0; i < 10; i++) {
    const a = ((-60 + i * 27) * Math.PI) / 180;
    holes += `<circle cx="${f(cx + Math.cos(a) * R * 0.72)}" cy="${f(dy + Math.sin(a) * R * 0.72)}" r="${f(R * 0.16)}" fill="#1a1a1a" stroke="#f0f0f0" stroke-width="2"/>`;
  }
  let cord = "M " + f(w * 0.12) + " " + f(h * 0.5) + " ";
  for (let i = 0; i <= 140; i++) {
    const u = i / 140, x = w * 0.12 - Math.sin(u * 3) * w * 0.06 + u * w * 0.1, y = h * 0.5 + u * h * 0.45;
    cord += `L ${f(x + Math.cos(u * 90) * 16)} ${f(y + Math.sin(u * 90) * 7)} `;
  }
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">
  <defs>
    <radialGradient id="bg" cx=".4" cy=".3" r="1"><stop offset="0" stop-color="#4a4a4a"/><stop offset=".7" stop-color="#1a1a1a"/><stop offset="1" stop-color="#000"/></radialGradient>
    <linearGradient id="b" x1="0" y1="0" x2=".3" y2="1"><stop offset="0" stop-color="#f4f4f4"/><stop offset=".45" stop-color="#a8a8a8"/><stop offset="1" stop-color="#2a2a2a"/></linearGradient>
    <linearGradient id="hs" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".4" stop-color="#bdbdbd"/><stop offset="1" stop-color="#4a4a4a"/></linearGradient>
    <radialGradient id="dial" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#7a7a7a"/></radialGradient>
    <filter id="bl"><feGaussianBlur stdDeviation="8"/></filter>
  </defs>
  <rect width="${w}" height="${h}" fill="url(#bg)"/>
  <ellipse cx="${cx}" cy="${h * 0.93}" rx="${w * 0.42}" ry="${h * 0.05}" fill="#000" filter="url(#bl)"/>
  <path d="M ${w * 0.12} ${h * 0.92} L ${w * 0.22} ${h * 0.42} Q ${cx} ${h * 0.34} ${w * 0.78} ${h * 0.42} L ${w * 0.88} ${h * 0.92} Z" fill="url(#b)"/>
  <circle cx="${cx}" cy="${dy}" r="${R}" fill="url(#dial)" stroke="#111" stroke-width="4"/>
  ${holes}
  <circle cx="${cx}" cy="${dy}" r="${R * 0.34}" fill="#fafafa" stroke="#333" stroke-width="2"/>
  <text x="${cx}" y="${dy + 7}" text-anchor="middle" font-family="Georgia, serif" font-size="${R * 0.24}" fill="#111">404</text>
  <path d="M ${w * 0.62} ${dy + R * 0.9} l ${R * 0.35} ${-R * 0.18}" stroke="#ddd" stroke-width="6" stroke-linecap="round"/>
  <g transform="rotate(-18 ${cx} ${h * 0.3})">
    <path d="M ${w * 0.1} ${h * 0.3} Q ${cx} ${h * 0.16} ${w * 0.9} ${h * 0.3} L ${w * 0.94} ${h * 0.38} Q ${w * 0.84} ${h * 0.42} ${w * 0.74} ${h * 0.38} L ${w * 0.7} ${h * 0.32} Q ${cx} ${h * 0.27} ${w * 0.3} ${h * 0.32} L ${w * 0.26} ${h * 0.38} Q ${w * 0.16} ${h * 0.42} ${w * 0.06} ${h * 0.38} Z" fill="url(#hs)" stroke="#000" stroke-width="3"/>
    <path d="M ${w * 0.16} ${h * 0.27} Q ${cx} ${h * 0.17} ${w * 0.84} ${h * 0.27}" stroke="#fff" stroke-width="5" fill="none" opacity=".8"/>
  </g>
  <path d="${cord}" stroke="#d0d0d0" stroke-width="5" fill="none"/>
  <path d="${cord}" stroke="#111" stroke-width="2" fill="none" transform="translate(2 3)"/>
  <rect x="0" y="0" width="${w}" height="${h}" fill="none" stroke="#000" stroke-width="50" filter="url(#bl)"/>
  </svg>`;
}

// ---------------------------------------------------------------- thermal

function sample(stops, n = 24) {
  // stops: [[t, r, g, b, a]] -> per-channel tableValues strings
  const ch = [[], [], [], []];
  for (let i = 0; i < n; i++) {
    const t = i / (n - 1);
    let k = 0;
    while (k < stops.length - 2 && stops[k + 1][0] < t) k++;
    const [t0, ...c0] = stops[k], [t1, ...c1] = stops[k + 1];
    const u = Math.min(1, Math.max(0, (t - t0) / (t1 - t0)));
    for (let c = 0; c < 4; c++) ch[c].push(f((c0[c] + (c1[c] - c0[c]) * u) * 100) / 100);
  }
  return ch.map((a) => a.join(" "));
}

const PAL = {
  flir: [[0, 0, 0, 0.3, 0], [0.1, 0.05, 0.1, 0.7, 0.35], [0.22, 0, 0.55, 1, 0.9], [0.34, 0.05, 0.95, 0.55, 1], [0.46, 0.55, 1, 0.1, 1], [0.58, 1, 0.95, 0.1, 1], [0.7, 1, 0.55, 0.05, 1], [0.82, 0.95, 0.15, 0.08, 1], [1, 0.85, 0.08, 0.06, 1]],
  iron: [[0, 0.05, 0, 0.15, 0], [0.1, 0.2, 0, 0.4, 0.4], [0.24, 0.5, 0, 0.6, 0.95], [0.38, 0.85, 0.05, 0.5, 1], [0.52, 1, 0.3, 0.15, 1], [0.66, 1, 0.6, 0, 1], [0.8, 1, 0.88, 0.25, 1], [1, 1, 1, 0.92, 1]],
};

function thermalFilter(id, pal, spread = 16) {
  const [R, G, B, A] = sample(PAL[pal]);
  return `<filter id="${id}" x="-30%" y="-30%" width="160%" height="160%" color-interpolation-filters="sRGB">
    <feGaussianBlur in="SourceAlpha" stdDeviation="${spread}" result="b1"/>
    <feGaussianBlur in="SourceAlpha" stdDeviation="${spread / 3}" result="b2"/>
    <feComposite in="b1" in2="b2" operator="arithmetic" k2="0.8" k3="0.45" result="h1"/>
    <feComposite in="h1" in2="SourceAlpha" operator="arithmetic" k2="0.85" k3="0.3" result="heat"/>
    <feColorMatrix in="heat" type="matrix" values="0 0 0 1 0  0 0 0 1 0  0 0 0 1 0  0 0 0 0 1"/>
    <feComponentTransfer><feFuncR type="table" tableValues="${R}"/><feFuncG type="table" tableValues="${G}"/><feFuncB type="table" tableValues="${B}"/></feComponentTransfer>
    <feComposite operator="in" in2="heatA"/>
    </filter>`.replace('<feComposite operator="in" in2="heatA"/>', `<feColorMatrix type="identity" result="col"/>
    <feColorMatrix in="heat" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0"/>
    <feComponentTransfer result="alpha"><feFuncA type="table" tableValues="${A}"/></feComponentTransfer>
    <feComposite in="col" in2="alpha" operator="in"/>`);
}

function paletteGradient(id, pal, vertical = false) {
  const st = PAL[pal].slice(1).map(([t, r, g, b]) => `<stop offset="${(t - 0.1) / 0.9}" stop-color="rgb(${r * 255 | 0},${g * 255 | 0},${b * 255 | 0})"/>`).join("");
  return `<linearGradient id="${id}" x1="0" y1="${vertical ? 1 : 0}" x2="${vertical ? 0 : 1}" y2="0">${st}</linearGradient>`;
}

// ---------------------------------------------------------------- gothic line art

function bat(x, y, s, rot, fill, stroke) {
  const half = [[0, -14], [7, -28], [11, -12], [30, -16], [58, -32], [104, -42], [96, -20], [92, 4], [70, -2], [50, 10], [28, 6], [10, 22], [0, 26]];
  const scallop = (pts) => {
    let d = `M ${pts[0][0]} ${pts[0][1]} `;
    for (let i = 1; i < pts.length; i++) {
      const [x0, y0] = pts[i - 1], [x1, y1] = pts[i];
      if (i >= 7 && i <= 11) d += `Q ${f((x0 + x1) / 2)} ${f((y0 + y1) / 2 - 12)} ${x1} ${y1} `;
      else d += `L ${x1} ${y1} `;
    }
    return d;
  };
  const right = scallop(half), left = scallop(half.map(([a, b]) => [-a, b]));
  return `<g transform="translate(${x} ${y}) rotate(${rot}) scale(${s})">
    <path d="${right}Z" fill="${fill}" stroke="${stroke}" stroke-width="3" stroke-linejoin="round"/>
    <path d="${left}Z" fill="${fill}" stroke="${stroke}" stroke-width="3" stroke-linejoin="round"/>
    <path d="M 14 -10 L 62 4 M 18 -12 L 92 -26 M 16 -8 L 36 8" stroke="${stroke}" stroke-width="2" opacity=".7"/>
    <path d="M -14 -10 L -62 4 M -18 -12 L -92 -26 M -16 -8 L -36 8" stroke="${stroke}" stroke-width="2" opacity=".7"/>
    <ellipse cx="0" cy="4" rx="11" ry="18" fill="${fill}" stroke="${stroke}" stroke-width="3"/></g>`;
}

// Barbed wire along a straight line from (x0,y0) to (x1,y1).
function barbedWire(r, x0, y0, x1, y1, color, w = 1) {
  const len = Math.hypot(x1 - x0, y1 - y0), a = Math.atan2(y1 - y0, x1 - x0);
  let s1 = "", s2 = "", barbs = "";
  for (let u = 0; u <= len; u += 4) {
    const o1 = Math.sin(u * 0.16) * 5 * w, o2 = Math.sin(u * 0.16 + Math.PI) * 5 * w;
    s1 += `${u ? "L" : "M"} ${f(u)} ${f(o1)} `;
    s2 += `${u ? "L" : "M"} ${f(u)} ${f(o2)} `;
  }
  for (let u = 30; u < len - 10; u += r.range(55, 80)) {
    barbs += `<path d="M ${f(u - 9)} ${f(-12 * w)} L ${f(u + 9)} ${f(12 * w)} M ${f(u + 9)} ${f(-12 * w)} L ${f(u - 9)} ${f(12 * w)}" stroke="${color}" stroke-width="${2.6 * w}" stroke-linecap="round"/>`;
    barbs += `<ellipse cx="${f(u)}" cy="0" rx="${5 * w}" ry="${6 * w}" fill="none" stroke="${color}" stroke-width="${2.4 * w}"/>`;
  }
  return `<g transform="translate(${x0} ${y0}) rotate(${f((a * 180) / Math.PI)})"><path d="${s1}" stroke="${color}" stroke-width="${2.6 * w}" fill="none"/><path d="${s2}" stroke="${color}" stroke-width="${2.6 * w}" fill="none"/>${barbs}</g>`;
}

// Thorny vine: wavy stem with triangular thorns and small leaves.
function thornVine(r, x0, y0, x1, y1, color, w = 1) {
  const len = Math.hypot(x1 - x0, y1 - y0), a = Math.atan2(y1 - y0, x1 - x0);
  let d = "", th = "";
  for (let u = 0; u <= len; u += 5) d += `${u ? "L" : "M"} ${f(u)} ${f(Math.sin(u * 0.035) * 14 * w)} `;
  for (let u = 20; u < len; u += r.range(22, 38)) {
    const y = Math.sin(u * 0.035) * 14 * w, s = r() < 0.5 ? -1 : 1;
    th += `<path d="M ${f(u - 5)} ${f(y)} L ${f(u + 6)} ${f(y + s * 16 * w)} L ${f(u + 5)} ${f(y)} Z" fill="${color}"/>`;
  }
  return `<g transform="translate(${x0} ${y0}) rotate(${f((a * 180) / Math.PI)})"><path d="${d}" stroke="${color}" stroke-width="${4 * w}" fill="none"/>
    <path d="${d}" stroke="${color}" stroke-width="${1.4 * w}" fill="none" transform="translate(0 7)" opacity=".7"/>${th}</g>`;
}

// Spiky "tribal" flame shape around a center, for gothic lettering backdrops.
function tribal(r, cx, cy, wdt, hgt, color, n = 9) {
  let out = "";
  for (let side of [-1, 1]) for (let i = 0; i < n; i++) {
    const u = i / (n - 1), x = cx + side * wdt * (0.15 + 0.85 * u), y = cy + (u - 0.5) * hgt * 0.35;
    const L = hgt * (0.35 + 0.5 * Math.sin(u * Math.PI)) * r.range(0.8, 1.1), ang = -Math.PI / 2 + side * (0.25 + u * 0.9);
    const tx = x + Math.cos(ang) * L, ty = y + Math.sin(ang) * L;
    const bw = 14 + 10 * (1 - u);
    out += `<path d="M ${f(x - bw)} ${f(y)} Q ${f(x + side * bw * 1.8)} ${f((y + ty) / 2)} ${f(tx)} ${f(ty)} Q ${f(x - side * bw * 0.2)} ${f((y + ty) / 2 + 10)} ${f(x + bw)} ${f(y)} Z" fill="none" stroke="${color}" stroke-width="3"/>`;
  }
  return out;
}

// Line-art feathered wing (outline only) rooted at (x, y), dir = +1 right / -1 left.
function lineWing(r, x, y, dir, s, color) {
  let out = "";
  const rows = [{ n: 9, r0: 40, len: [110, 190], w: 20 }, { n: 8, r0: 20, len: [70, 110], w: 18 }, { n: 7, r0: 0, len: [40, 60], w: 15 }];
  for (const row of rows) for (let i = 0; i < row.n; i++) {
    const u = i / (row.n - 1), a = dir > 0 ? -1.35 + u * 1.5 : Math.PI + 1.35 - u * 1.5;
    const L = (row.len[0] + (row.len[1] - row.len[0]) * Math.sin(u * 2.6)) * s * r.range(0.95, 1.05);
    const bx = x + Math.cos(a) * row.r0 * s, by = y + Math.sin(a) * row.r0 * s;
    const c = Math.cos(a), si = Math.sin(a), nx = -si, ny = c, wd = row.w * s;
    const tx = bx + c * L, ty = by + si * L;
    out += `<path d="M ${f(bx)} ${f(by)} Q ${f(bx + c * L * 0.55 + nx * wd)} ${f(by + si * L * 0.55 + ny * wd)} ${f(tx)} ${f(ty)} Q ${f(bx + c * L * 0.6 - nx * wd * 0.7)} ${f(by + si * L * 0.6 - ny * wd * 0.7)} ${f(bx)} ${f(by)} Z" fill="#0c0c0c" stroke="${color}" stroke-width="2.6"/>`;
    out += `<path d="M ${f(bx)} ${f(by)} L ${f(bx + c * L * 0.85)} ${f(by + si * L * 0.85)}" stroke="${color}" stroke-width="1.2" opacity=".7"/>`;
  }
  return out;
}

function web(cx, cy, R, a0, a1, color) {
  let out = "";
  const spokes = 7;
  const pts = (rr) => Array.from({ length: spokes }, (_, i) => {
    const a = a0 + ((a1 - a0) * i) / (spokes - 1);
    return [cx + Math.cos(a) * rr, cy + Math.sin(a) * rr];
  });
  for (const [x, y] of pts(R)) out += `<path d="M ${cx} ${cy} L ${f(x)} ${f(y)}" stroke="${color}" stroke-width="2"/>`;
  for (let k = 1; k <= 5; k++) {
    const p = pts((R * k) / 5.4);
    let d = `M ${f(p[0][0])} ${f(p[0][1])} `;
    for (let i = 1; i < p.length; i++) d += `Q ${f((p[i - 1][0] + p[i][0]) / 2 + (cx - (p[i - 1][0] + p[i][0]) / 2) * 0.12)} ${f((p[i - 1][1] + p[i][1]) / 2 + (cy - (p[i - 1][1] + p[i][1]) / 2) * 0.12)} ${f(p[i][0])} ${f(p[i][1])} `;
    out += `<path d="${d}" stroke="${color}" stroke-width="1.8" fill="none"/>`;
  }
  return out;
}

// ---------------------------------------------------------------- lava / fire

function lavaFilter(id, seed, o = {}) {
  return `<filter id="${id}" x="-60%" y="-60%" width="220%" height="220%" color-interpolation-filters="sRGB">
    <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="3" seed="${seed}" result="tn"/>
    <feDisplacementMap in="SourceAlpha" in2="tn" scale="${o.rough ?? 16}" xChannelSelector="R" yChannelSelector="G" result="shape"/>
    <feGaussianBlur in="shape" stdDeviation="${o.core ?? 20}" result="coreB"/>
    <feColorMatrix in="coreB" type="matrix" values="0 0 0 ${o.heat ?? 1.15} 0  0 0 0 ${o.heat ?? 1.15} 0  0 0 0 ${o.heat ?? 1.15} 0  0 0 0 0 1" result="coreG"/>
    <feComponentTransfer in="coreG" result="hot">
      <feFuncR type="table" tableValues="0.4 0.78 1 1 1 1"/>
      <feFuncG type="table" tableValues="0.03 0.1 0.3 0.55 0.78 0.92"/>
      <feFuncB type="table" tableValues="0 0 0.01 0.05 0.2 0.5"/>
    </feComponentTransfer>
    <feComposite in="hot" in2="shape" operator="in" result="hotShape"/>
    <feTurbulence type="fractalNoise" baseFrequency="${o.plate ?? 0.045}" numOctaves="4" seed="${seed + 9}" result="pn"/>
    <feColorMatrix in="pn" type="matrix" values="0 0 0 0 0.09  0 0 0 0 0.05  0 0 0 0 0.035  ${o.gain ?? 14} 0 0 0 ${o.bias ?? -6.2}" result="plates"/>
    <feComposite in="plates" in2="shape" operator="in" result="plateShape"/>
    <feMorphology in="shape" operator="erode" radius="3" result="inner"/>
    <feComposite in="shape" in2="inner" operator="out" result="rim"/>
    <feFlood flood-color="#2a0c02"/><feComposite in2="rim" operator="in" result="rimC"/>
    <feGaussianBlur in="shape" stdDeviation="${o.glow ?? 26}" result="g1"/>
    <feFlood flood-color="#ff4a0a" flood-opacity="${o.glowAmt ?? 0.75}"/><feComposite in2="g1" operator="in" result="glow"/>
    <feGaussianBlur in="shape" stdDeviation="${(o.glow ?? 26) * 2.6}" result="g2"/>
    <feFlood flood-color="#b3200a" flood-opacity="${(o.glowAmt ?? 0.75) * 0.7}"/><feComposite in2="g2" operator="in" result="glow2"/>
    <feTurbulence type="fractalNoise" baseFrequency="0.05 0.011" numOctaves="3" seed="${seed + 4}" result="fn"/>
    <feGaussianBlur in="shape" stdDeviation="10" result="fb"/>
    <feOffset in="fb" dy="-22" result="fbo"/>
    <feDisplacementMap in="fbo" in2="fn" scale="${o.flame ?? 90}" xChannelSelector="R" yChannelSelector="B" result="fl"/>
    <feFlood flood-color="#ff9a1a" flood-opacity="0.8"/><feComposite in2="fl" operator="in" result="flames"/>
    <feMerge><feMergeNode in="glow2"/><feMergeNode in="glow"/><feMergeNode in="flames"/><feMergeNode in="hotShape"/><feMergeNode in="plateShape"/><feMergeNode in="rimC"/></feMerge>
    </filter>`;
}

function embers(r, cx, cy, w, h, n, color = "#ffb347") {
  let out = "";
  for (let i = 0; i < n; i++) {
    const x = cx + r.range(-w, w), y = cy + r.range(-h, h * 0.6), s = r.range(0.8, 3.2);
    out += `<circle cx="${f(x)}" cy="${f(y)}" r="${f(s)}" fill="${color}" opacity="${f(r.range(0.4, 1))}"/>`;
  }
  return out;
}

module.exports = { halftoneScript, crtScene, phoneScene, thermalFilter, paletteGradient, PAL, bat, barbedWire, thornVine, tribal, lineWing, web, lavaFilter, embers };
