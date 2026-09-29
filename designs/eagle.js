// Vintage Americana graphics: bald eagle, tattered flag, arched collegiate type.
const { rng, f } = require("./lib");

const BROWN = ["#3b2416", "#5a3620", "#7a4a2a", "#96623a", "#b07c4c"];

function feather(x, y, ang, len, wid, fill, edge, curl = 0.12) {
  const c = Math.cos(ang), s = Math.sin(ang), nx = -s, ny = c;
  const tx = x + c * len + nx * len * curl * 0.3, ty = y + s * len + ny * len * curl * 0.3;
  const m1x = x + c * len * 0.55 + nx * wid, m1y = y + s * len * 0.55 + ny * wid;
  const m2x = x + c * len * 0.6 - nx * wid * 0.8, m2y = y + s * len * 0.6 - ny * wid * 0.8;
  const d = `M ${f(x)} ${f(y)} Q ${f(m1x)} ${f(m1y)} ${f(tx)} ${f(ty)} Q ${f(m2x)} ${f(m2y)} ${f(x)} ${f(y)} Z`;
  return `<path d="${d}" fill="${fill}" stroke="${edge}" stroke-width="2"/>` +
    `<path d="M ${f(x)} ${f(y)} Q ${f((x + tx) / 2 + nx * wid * 0.15)} ${f((y + ty) / 2 + ny * wid * 0.15)} ${f(tx)} ${f(ty)}" stroke="#e8d2a8" stroke-opacity=".35" stroke-width="1.4" fill="none"/>`;
}

// Raised wing: arm runs from shoulder (sx, sy) to wrist (wx, wy); feathers hang off the
// arm, sweeping from angle aIn at the shoulder to aOut at the wrist (radians).
function wing(r, sx, sy, wx, wy, aIn, aOut, scale = 1) {
  let out = "";
  const rows = [
    { n: 15, len: [120, 290], wid: 30, col: [0, 1], off: 0 },
    { n: 13, len: [80, 150], wid: 28, col: [1, 2], off: 0.02 },
    { n: 11, len: [50, 85], wid: 24, col: [2, 3], off: 0.05 },
    { n: 9, len: [34, 50], wid: 20, col: [3, 4], off: 0.08 },
  ];
  for (const row of rows) {
    for (let i = 0; i < row.n; i++) {
      const u = i / (row.n - 1);
      const bx = sx + (wx - sx) * (u * 0.96 + row.off), by = sy + (wy - sy) * (u * 0.96 + row.off);
      const a = aIn + (aOut - aIn) * Math.pow(u, 1.2) + r.range(-0.03, 0.03);
      const len = (row.len[0] + (row.len[1] - row.len[0]) * Math.pow(u, 0.8)) * scale * r.range(0.94, 1.04);
      const col = BROWN[r() < 0.5 ? row.col[0] : row.col[1]];
      out += feather(bx, by, a, len, row.wid * scale, col, "#1e120a", 0.1);
    }
  }
  // leading edge of the arm
  out += `<path d="M ${sx} ${sy} Q ${f((sx + wx) / 2 + (wy - sy) * 0.08)} ${f((sy + wy) / 2)} ${wx} ${wy}" stroke="${BROWN[3]}" stroke-width="${f(26 * scale)}" stroke-linecap="round" fill="none"/>`;
  out += `<path d="M ${sx} ${sy} Q ${f((sx + wx) / 2 + (wy - sy) * 0.08)} ${f((sy + wy) / 2)} ${wx} ${wy}" stroke="#1e120a" stroke-width="2" stroke-dasharray="10 5" fill="none" transform="translate(0 8)"/>`;
  return out;
}

// Bald eagle head facing right, local coords ~ (0..340, 0..290).
function head(r) {
  const outline = "M 0 262 C -12 180 0 92 60 50 C 110 15 190 22 232 68 L 252 86 L 246 120 L 252 152 C 232 176 216 202 206 232 C 198 252 192 264 186 276 Z";
  let s = `<clipPath id="headclip"><path d="${outline}"/></clipPath>`;
  s += `<radialGradient id="headshade" cx="0.62" cy="0.3" r="0.8"><stop offset="0" stop-color="#f4f0e6"/><stop offset="0.6" stop-color="#d9d4c8"/><stop offset="1" stop-color="#8e8a80"/></radialGradient>`;
  s += `<path d="${outline}" fill="url(#headshade)"/>`;
  let strokes = "";
  for (let i = 0; i < 420; i++) {
    const x = r.range(-10, 250), y = r.range(30, 290);
    const a = Math.PI + r.range(-0.55, 0.25) + (y - 150) * 0.0025, l = r.range(9, 28);
    const dark = r() < 0.55;
    strokes += `<path d="M ${f(x)} ${f(y)} q ${f(Math.cos(a) * l * 0.5)} ${f(Math.sin(a) * l * 0.5 + 3)} ${f(Math.cos(a) * l)} ${f(Math.sin(a) * l)}" stroke="${dark ? "#6f6b63" : "#ffffff"}" stroke-opacity="${f(r.range(0.35, 0.8))}" stroke-width="${f(r.range(1, 2.2))}" fill="none" stroke-linecap="round"/>`;
  }
  s += `<g clip-path="url(#headclip)">${strokes}<path d="M 0 150 C 40 210 120 260 190 270 L 190 300 L -20 300 Z" fill="#000" opacity=".18"/></g>`;
  // ragged neck feathers overlapping the body
  let tips = "M 186 272 ";
  for (let x = 186, i = 0; x > 0; x -= 14, i++) tips += `L ${f(x - 7)} ${f(272 + (i % 2 ? 0 : 1) * 30 + r.range(0, 14) - x * 0.06)} L ${f(x - 14)} ${f(268 - x * 0.05)} `;
  s += `<path d="${tips} L 0 250 L 186 250 Z" fill="#cfcabd" stroke="#6f6b63" stroke-width="1.5"/>`;
  // beak
  s += `<path d="M 236 80 C 276 76 322 100 336 142 C 342 162 332 182 318 190 C 322 172 314 160 300 158 L 250 164 C 242 150 238 118 236 80 Z" fill="#e2a82e" stroke="#3a2608" stroke-width="3"/>`;
  s += `<path d="M 250 160 L 302 162 C 292 176 270 180 250 175 Z" fill="#c98a1c" stroke="#3a2608" stroke-width="2.5"/>`;
  s += `<path d="M 252 152 L 306 156" stroke="#3a2608" stroke-width="3"/>`;
  s += `<path d="M 262 90 C 290 92 318 110 328 136" stroke="#fff3c4" stroke-opacity=".6" stroke-width="4" fill="none"/>`;
  s += `<ellipse cx="266" cy="112" rx="6" ry="3.5" fill="#3a2608"/>`;
  // eye + angry brow
  s += `<circle cx="222" cy="102" r="10" fill="#e8c34a" stroke="#222" stroke-width="2.5"/><circle cx="224" cy="102" r="5" fill="#111"/><circle cx="226" cy="99" r="1.6" fill="#fff"/>`;
  s += `<path d="M 180 86 L 254 80 L 240 96 C 226 90 204 90 180 86 Z" fill="#4a4740"/>`;
  s += `<path d="M 200 108 L 176 112" stroke="#4a4740" stroke-width="3"/>`;
  return s;
}

// Talon gripping at (x, y), rotated by rot degrees.
function talon(x, y, rot, sc = 1) {
  const toe = (d) => `<path d="${d}" stroke="#2a1c06" stroke-width="22" fill="none" stroke-linecap="round"/><path d="${d}" stroke="#d9a53a" stroke-width="16" fill="none" stroke-linecap="round"/><path d="${d}" stroke="#f3cf73" stroke-width="4" stroke-dasharray="3 6" fill="none" stroke-linecap="round"/>`;
  const claw = (x0, y0, a) => `<path d="M ${x0} ${y0} q ${f(Math.cos(a) * 14)} ${f(Math.sin(a) * 14)} ${f(Math.cos(a + 1.1) * 22)} ${f(Math.sin(a + 1.1) * 22)} l ${f(-Math.cos(a) * 6)} ${f(-Math.sin(a) * 6)} Z" fill="#111" stroke="#111" stroke-width="3"/>`;
  return `<g transform="translate(${x} ${y}) rotate(${rot}) scale(${sc})">
    <path d="M -18 -70 L 18 -70 L 12 -8 L -12 -8 Z" fill="#c9952e" stroke="#2a1c06" stroke-width="3"/>
    ${toe("M 0 -6 q 30 4 44 30")}${toe("M 0 -6 q 6 22 2 40")}${toe("M 0 -6 q -26 6 -38 28")}${toe("M 0 -10 q -14 -8 -28 -2")}
    ${claw(44, 26, 1.2)}${claw(2, 36, 1.7)}${claw(-38, 24, 2.2)}${claw(-28, -2, 3.4)}</g>`;
}

// Tattered waving flag in local coords; strips flare apart toward the torn end.
function flag(r, w, h, o = {}) {
  const n = 13, sh = h / n, amp = o.amp ?? 16, k = o.k ?? 0.018, ph = o.ph ?? 0.4;
  const RED = o.red ?? "#b1261f", WHITE = o.white ?? "#e8e1cf", BLUE = o.blue ?? "#1f2f5c";
  const wave = (x) => amp * (0.4 + x / w) * Math.sin(k * x + ph) + 6 * Math.sin(k * 2.7 * x);
  const flare = [];
  for (let i = 0; i < n; i++) flare.push(r.range(-1, 1) * (o.flare ?? 26) + (i - n / 2) * (o.fan ?? 5));
  const yOf = (i, x) => i * sh + wave(x) + flare[Math.min(i, n - 1)] * Math.pow(x / w, 2.2);
  let grad = `<linearGradient id="${o.id}-shade" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="${w}" y2="0">`;
  for (let x = 0; x <= w; x += w / 40) {
    const sl = Math.cos(k * x + ph);
    grad += `<stop offset="${f(x / w)}" stop-color="${sl < 0 ? "#000" : "#fff"}" stop-opacity="${f(Math.abs(sl) * (sl < 0 ? 0.38 : 0.12))}"/>`;
  }
  grad += "</linearGradient>";
  let out = `<defs>${grad}</defs>`;
  for (let i = 0; i < n; i++) {
    const end = w * r.range(o.minEnd ?? 0.66, 1.0);
    let top = "", bot = "";
    for (let x = 0; x <= end; x += 8) {
      top += `${x ? "L" : "M"} ${f(x)} ${f(yOf(i, x))} `;
      bot = `L ${f(x)} ${f(yOf(i, x) + sh + 0.8)} ` + bot;
    }
    // jagged torn tip
    let tear = "";
    const steps = 4;
    for (let j = 0; j <= steps; j++) {
      const yy = yOf(i, end) + (sh * j) / steps;
      tear += `L ${f(end + (j % 2 ? r.range(4, 26) : r.range(-12, 4)))} ${f(yy)} `;
    }
    const d = top + tear + bot.replace(/^L/, "L") + "Z";
    out += `<path d="${d}" fill="${i % 2 ? WHITE : RED}"/><path d="${d}" fill="url(#${o.id}-shade)"/>`;
    // tiny rips inside the stripe
    if (r() < 0.6) {
      const x = r.range(w * 0.45, end - 20), y = yOf(i, x) + sh * 0.5;
      out += `<path d="M ${f(x)} ${f(y)} l ${f(r.range(10, 30))} ${f(r.range(-3, 3))} l ${f(-r.range(4, 12))} ${f(r.range(2, 5))} Z" fill="#0e0e0e"/>`;
    }
  }
  // canton
  const cw = w * 0.4, cn = 7;
  let cd = "";
  for (let x = 0; x <= cw; x += 8) cd += `${x ? "L" : "M"} ${f(x)} ${f(yOf(0, x))} `;
  for (let x = cw; x >= 0; x -= 8) cd += `L ${f(x)} ${f(yOf(cn - 1, x) + sh)} `;
  out += `<path d="${cd}Z" fill="${BLUE}"/><path d="${cd}Z" fill="url(#${o.id}-shade)"/>`;
  for (let row = 0; row < 9; row++) for (let col = 0; col < (row % 2 ? 5 : 6); col++) {
    const x = (col + (row % 2 ? 1 : 0.5)) * (cw / 6.2) + 4, y = yOf(0, x) + (row + 0.7) * (cn * sh) / 9.6;
    out += star(x, y, 6.5, WHITE);
  }
  return out;
}

function star(x, y, R, fill, rot = -90) {
  let d = "";
  for (let i = 0; i < 10; i++) {
    const a = ((rot + i * 36) * Math.PI) / 180, rr = i % 2 ? R * 0.42 : R;
    d += `${i ? "L" : "M"} ${f(x + Math.cos(a) * rr)} ${f(y + Math.sin(a) * rr)} `;
  }
  return `<path d="${d}Z" fill="${fill}"/>`;
}

// Arched collegiate text along a circle of radius R centered at (cx, cy).
function arch(id, text, cx, cy, R, o = {}) {
  const a = ((o.span ?? 70) * Math.PI) / 180;
  const x0 = cx - R * Math.sin(a), y0 = cy - R * Math.cos(a), x1 = cx + R * Math.sin(a);
  const sweep = o.down ? 0 : 1;
  const yy = o.down ? cy + R * Math.cos(a) : y0;
  return `<path id="${id}" d="M ${f(x0)} ${f(yy)} A ${R} ${R} 0 0 ${sweep} ${f(x1)} ${f(yy)}" fill="none"/>
    <text font-family="${o.font ?? "Graduate"}" font-size="${o.size ?? 64}" letter-spacing="${o.ls ?? 2}" fill="${o.fill ?? "#2b2b2b"}" stroke="${o.stroke ?? "#8d8d8d"}" stroke-width="${o.sw ?? 2.4}" paint-order="${o.paint ?? "normal"}" text-anchor="middle">
      <textPath href="#${id}" startOffset="50%">${text}</textPath></text>`;
}

module.exports = { wing, head, talon, flag, star, arch, feather, BROWN };
