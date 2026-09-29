// The ten 404 CULTURE designs: two new takes on each of the five references.
const L = require("./lib");
const E = require("./eagle");
const FX = require("./fx");
const { rng, f } = L;

const D = {};

// ---------------------------------------------------------------- 1: Americana eagle

D["01_eagle_lost_signal_tee"] = () => {
  const r = rng(404);
  const t = L.boxyTee();
  const deg = Math.PI / 180;
  let p = "";
  p += E.wing(r, 540, 610, 390, 390, 160 * deg, 226 * deg, 0.8);
  p += E.wing(r, 680, 600, 820, 400, 20 * deg, -44 * deg, 0.7);
  p += `<ellipse cx="605" cy="660" rx="120" ry="130" fill="${E.BROWN[1]}" stroke="#1e120a" stroke-width="3"/>`;
  for (let i = 0; i < 70; i++) {
    const x = r.range(505, 705), y = r.range(560, 780);
    p += `<path d="M ${f(x - 12)} ${f(y)} q 12 16 24 0" stroke="${r() < 0.5 ? "#2a180c" : "#a0703f"}" stroke-width="2" fill="none" opacity=".8"/>`;
  }
  p += `<g transform="translate(360 735) rotate(9)">${E.flag(r, 520, 215, { id: "f1a", flare: 30, fan: 3 })}</g>`;
  p += `<g transform="translate(540 425) scale(0.86)">${E.head(r)}</g>`;
  p += E.talon(520, 790, 12, 0.95) + E.talon(700, 812, -8, 0.95);
  p += `<g opacity=".92">${E.arch("a1a", "404 CULTURE", 600, 960, 480, { span: 31, size: 66, fill: "#262626", stroke: "#9a9a9a", sw: 2.6 })}</g>`;
  p += `<g font-family="Graduate" font-size="50" text-anchor="middle" fill="#262626" stroke="#9a9a9a" stroke-width="2.2" letter-spacing="3" opacity=".92">
    <text x="600" y="575">NOT FOUND</text><text x="600" y="632">DEPT · 404</text></g>`;
  p += `<text x="600" y="770" transform="rotate(-5 600 770)" text-anchor="middle" font-family="Yellowtail" font-size="118" fill="#e7e2d6" stroke="#1a1a1a" stroke-width="7" paint-order="stroke">Lost Signal</text>`;
  const s = {
    seed: 11, base: "#1d1d1d", light: "#6d6d6d", dark: "#0a0a0a", bg: "#ffffff",
    washAmt: 0.07, wash2Amt: 0.04, fadeAmt: 0.4, printFreq: 0.09, printCrack: 2.2, printKeep: 2.0, foldDark: 0.2,
    holes: [[850, 360, 4, 40], [780, 470, 2, 30], [340, 700, 2, 20], [430, 1000, 3, 50], [880, 640, 4, 40, 4], [930, 480, 3, 30, 4]],
    raw: { hem: 0.5 }, label: L.neckLabel(),
  };
  const tag = L.sleeveTag(1009, 600, -32);
  p = `<g transform="translate(600 640) scale(0.84) translate(-600 -640)">${p}</g>`;
  return L.page(L.garment("g1a", t, s, p, "") + tag, { header: false, footer: ["© 404 CULTURE"] });
};

D["02_eagle_home_of_the_lost_tee"] = () => {
  const r = rng(808);
  const t = L.boxyTee({ half: 262 });
  const deg = Math.PI / 180;
  let p = "";
  for (let i = 0; i < 16; i++) p += E.star(r.range(400, 800), r.range(420, 560), r.range(5, 11), "#e8e1cf", r.range(-90, -60));
  p += E.wing(r, 565, 615, 385, 455, 158 * deg, 222 * deg, 0.7);
  p += E.wing(r, 635, 615, 815, 455, 22 * deg, -42 * deg, 0.7);
  for (let i = 0; i < 9; i++) p += E.feather(600 + (i - 4) * 9, 720, (90 + (i - 4) * 9) * deg, 120, 16, "#e8e1cf", "#4a4740");
  p += `<ellipse cx="600" cy="660" rx="98" ry="112" fill="${E.BROWN[1]}" stroke="#1e120a" stroke-width="3"/>`;
  for (let i = 0; i < 60; i++) {
    const x = r.range(515, 685), y = r.range(580, 760);
    p += `<path d="M ${f(x - 11)} ${f(y)} q 11 14 22 0" stroke="${r() < 0.5 ? "#2a180c" : "#a0703f"}" stroke-width="2" fill="none" opacity=".8"/>`;
  }
  p += `<g transform="translate(725 438) scale(-0.78 0.78)">${E.head(r)}</g>`;
  p += `<g transform="translate(330 770) rotate(-2)">${E.flag(r, 545, 150, { id: "f1b", amp: 22, k: 0.022, ph: 1.6, minEnd: 0.82, flare: 12, fan: 1 })}</g>`;
  p += E.talon(548, 792, 6, 0.85) + E.talon(655, 796, -6, 0.85);
  p += E.arch("a1b", "Home of the Lost", 600, 920, 540, { span: 27, size: 80, font: "Yellowtail", fill: "#e8e1cf", stroke: "#141414", sw: 8, paint: "stroke", ls: 0 });
  p += `<text x="600" y="1010" text-anchor="middle" font-family="Graduate" font-size="74" letter-spacing="3" fill="#e8e1cf" stroke="#1f2f5c" stroke-width="10" paint-order="stroke">404 CULTURE</text>`;
  p += `<text x="600" y="1052" text-anchor="middle" font-family="Graduate" font-size="26" letter-spacing="6" fill="#b1261f">★ ATHLETIC DIVISION ★</text>`;
  p = `<g transform="translate(600 700) scale(0.86) translate(-600 -700)">${p}</g>`;
  const s = {
    seed: 23, base: "#3a3733", light: "#8b857c", dark: "#1a1816", bg: "#ffffff", inside: "#24221f",
    washAmt: 0.1, wash2Amt: 0.06, fadeAmt: 0.45, printFreq: 0.08, printCrack: 2.5, printKeep: 2.0, printOpacity: 0.85, foldDark: 0.22,
    holes: [[360, 420, 3, 30], [860, 900, 4, 40], [300, 1040, 2, 20], [770, 1100, 3, 40]],
    raw: { hem: 0.9, collar: 0.6 }, label: L.neckLabel("#1c1c1c", "#e8e1cf"),
  };
  return L.page(L.garment("g1b", t, s, p) + L.sleeveTag(190, 590, 32), { header: false, footer: ["© 404 CULTURE"] });
};

const FOOT = ["DM FOR MORE INFO & ORDERS", "PREMADE DESIGNS READY · 404 CULTURE", "ALL RIGHTS RESERVED | DESIGNED BY 404 CULTURE"];

// ---------------------------------------------------------------- 2: halftone photo thermal

D["03_thermal_404_crt_longsleeve"] = () => {
  const t = L.longTee();
  const ink = "#2b2724";
  let p = `<image id="ht2a" x="415" y="385" width="370" height="420" preserveAspectRatio="none"/>`;
  p += `<text x="600" y="862" text-anchor="middle" font-family="Caslon" font-size="46" fill="${ink}">404 Culture</text>`;
  const s = {
    seed: 31, base: "#d9d3c7", light: "#f6f2ea", dark: "#8d877c", bg: "#050505", inside: "#b7b0a3", collar: "#d3cdc0",
    waffle: true, waffleAmt: 0.3, washAmt: 0.0, wash2Amt: 0.0, fadeAmt: 0.25, foldDark: 0.16, foldLight: 0.2, grainAmt: 0.2,
    printFreq: 0.07, printCrack: 2.2, printKeep: 2.3, printBlend: "multiply", thread: "#e8e2d6",
    holes: [[330, 430, 3, 20], [880, 560, 2, 20], [230, 820, 3, 30], [975, 930, 3, 20], [650, 1000, 2, 20], [420, 1050, 3, 40], [860, 330, 2, 10]],
    raw: { hem: 1.4, cuffs: 1.2, collar: 0.8 }, label: L.neckLabel(), shadowAmt: 0,
  };
  const jobs = [{ id: "ht2a", scene: FX.crtScene(370, 420), w: 370, h: 420, pitch: 3.4, angle: 45, gamma: 1.15, ink, invert: false }];
  return L.page(L.garment("g2a", t, s, p), { dark: true, footer: FOOT, code: "0203", script: FX.halftoneScript(jobs) });
};

D["04_missed_calls_rotary_longsleeve"] = () => {
  const t = L.longTee({ hem: 1090 });
  const ink = "#e4ddcf";
  let p = `<text x="600" y="425" text-anchor="middle" font-family="Caslon" font-size="34" letter-spacing="9" fill="${ink}">MISSED CALLS</text>`;
  p += `<rect x="432" y="447" width="336" height="396" fill="none" stroke="${ink}" stroke-width="2.5"/>`;
  p += `<image id="ht2b" x="442" y="457" width="316" height="376" preserveAspectRatio="none"/>`;
  p += `<text x="600" y="884" text-anchor="middle" font-family="Caslon" font-size="25" letter-spacing="2" fill="${ink}">404 Culture — Nº 404</text>`;
  const s = {
    seed: 47, base: "#3a3835", light: "#77736c", dark: "#161514", bg: "#050505", inside: "#262422",
    waffle: true, waffleAmt: 0.5, washAmt: 0.08, wash2Amt: 0.05, fadeAmt: 0.4, foldDark: 0.25, foldLight: 0.08,
    printFreq: 0.07, printCrack: 2.4, printKeep: 2.2, printOpacity: 0.88, thread: "#8a857d",
    holes: [[860, 450, 3, 20], [300, 600, 2, 20], [960, 1000, 3, 30], [240, 1080, 3, 20], [700, 960, 2, 20], [360, 900, 2, 20]],
    raw: { hem: 1.1, cuffs: 1.4, collar: 0.5 }, label: L.neckLabel("#e4ddcf", "#111"),
  };
  const jobs = [{ id: "ht2b", scene: FX.phoneScene(316, 376), w: 316, h: 376, pitch: 3.3, angle: 22, gamma: 1.5, ink, invert: true }];
  return L.page(L.garment("g2b", t, s, p), { dark: true, footer: FOOT, code: "0204", script: FX.halftoneScript(jobs) });
};

// ---------------------------------------------------------------- 3: thermal heat-map sigil

D["05_heat_signature_orbit_tee"] = () => {
  const t = L.boxyTee();
  let p = `<defs>${FX.thermalFilter("th3a", "flir", 15)}${FX.paletteGradient("pg3a", "flir")}</defs>`;
  p += `<rect x="410" y="372" width="118" height="46" fill="#d4201c"/><text x="469" y="410" text-anchor="middle" font-family="BarlowXBI" font-size="42" fill="#fff">404</text>`;
  p += `<rect x="532" y="372" width="258" height="46" fill="#e6e03a"/><text x="661" y="410" text-anchor="middle" font-family="BarlowXBI" font-size="42" fill="#111">CULTURE</text>`;
  let grid = "";
  for (let i = 0; i <= 14; i++) {
    const v = 410 + (380 * i) / 14, h = 450 + (380 * i) / 14;
    grid += `<path d="M ${f(v)} 450 V 830 M 410 ${f(h)} H 790" />`;
  }
  p += `<g stroke="#e9e9e9" stroke-width="1.1" opacity=".5">${grid}</g>`;
  p += `<g filter="url(#th3a)" stroke="#fff" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path d="M 600 470 L 622 618 L 735 640 L 622 662 L 600 810 L 578 662 L 465 640 L 578 618 Z" stroke-width="11"/>
    <ellipse cx="600" cy="640" rx="168" ry="60" transform="rotate(28 600 640)" stroke-width="17"/>
    <ellipse cx="600" cy="640" rx="168" ry="60" transform="rotate(-28 600 640)" stroke-width="17"/>
    <path d="M 452 555 l -30 -22 M 748 555 l 30 -22 M 452 725 l -30 22 M 748 725 l 30 22" stroke-width="9"/>
    <path d="M 600 470 V 442 M 600 810 V 838" stroke-width="8"/>
    ${E.star(600, 640, 30, "#fff", -90).replace("<path", '<path stroke="none"')}
  </g>`;
  p += `<rect x="425" y="852" width="230" height="7" fill="url(#pg3a)"/>`;
  for (let i = 0; i <= 10; i++) p += `<path d="M ${f(425 + i * 23)} 862 v 6" stroke="#ddd" stroke-width="1.2"/>`;
  p += `<text x="790" y="872" text-anchor="end" font-family="BarlowXBI" font-size="27" fill="#f2f2f2">404Culture©</text>`;
  p += `<text x="790" y="890" text-anchor="end" font-family="Oswald" font-size="12" letter-spacing="1" fill="#f2f2f2">40.4040°N 74.0404°W</text>`;
  const s = {
    seed: 53, base: "#171717", light: "#5b5b5b", dark: "#060606", bg: "#050505", washAmt: 0.06, wash2Amt: 0.04, fadeAmt: 0.5,
    printFreq: 0.11, printCrack: 1.8, printKeep: 2.2, speckle: 0.3, grainAmt: 0.07, foldDark: 0.3, label: L.neckLabel("#f2f2f2", "#111"), shadowAmt: 0,
  };
  return L.page(L.garment("g3a", t, s, p), { dark: true, footer: FOOT, code: "0305" });
};

D["06_err404_thermal_heart_tee"] = () => {
  const r = rng(91);
  const t = L.boxyTee({ half: 275 });
  let p = `<defs>${FX.thermalFilter("th3b", "iron", 14)}${FX.paletteGradient("pg3b", "iron", true)}</defs>`;
  p += `<rect x="410" y="370" width="380" height="44" fill="none" stroke="#eee" stroke-width="2.5"/>`;
  p += `<text x="600" y="404" text-anchor="middle" font-family="BarlowXBI" font-size="32" letter-spacing="1" fill="#eee">ERR_404 // CULTURE</text>`;
  p += `<circle cx="418" cy="440" r="5" fill="#e0261c"/><text x="430" y="445" font-family="Oswald" font-size="14" fill="#eee" letter-spacing="1">REC</text>`;
  p += `<text x="790" y="445" text-anchor="end" font-family="Oswald" font-size="14" fill="#eee" letter-spacing="1">T-MAX 40.4°C</text>`;
  let hud = "";
  for (const rr of [75, 135, 195]) hud += `<circle cx="600" cy="655" r="${rr}" fill="none"/>`;
  hud += `<path d="M 390 655 H 810 M 600 450 V 860"/>`;
  for (let a = 0; a < 360; a += 10) {
    const c = Math.cos((a * Math.PI) / 180), s = Math.sin((a * Math.PI) / 180), l = a % 30 ? 8 : 16;
    hud += `<path d="M ${f(600 + c * 195)} ${f(655 + s * 195)} L ${f(600 + c * (195 + l))} ${f(655 + s * (195 + l))}"/>`;
  }
  p += `<g stroke="#e9e9e9" stroke-width="1.2" opacity=".45">${hud}</g>`;
  let wings = "";
  for (const sd of [-1, 1]) for (let i = 0; i < 5; i++) {
    const x0 = 600 + sd * 62, y0 = 628 + i * 10, tx = 600 + sd * (175 + i * 8 - (i > 2 ? i * 12 : 0)), ty = 520 + i * 48;
    wings += `<path d="M ${x0} ${y0} Q ${f(600 + sd * (120 + i * 6))} ${f(y0 - 70 + i * 10)} ${f(tx)} ${f(ty)}" stroke-width="${12 - i}"/>`;
  }
  p += `<g filter="url(#th3b)" stroke="#fff" fill="none" stroke-linecap="round" stroke-linejoin="round">
    ${wings}
    <path d="M 600 745 C 520 690 520 600 566 600 C 584 600 596 614 600 630 C 604 614 616 600 634 600 C 680 600 680 690 600 745 Z" stroke-width="15"/>
    <path d="M 492 770 L 712 560" stroke-width="7"/>
    <path d="M 712 560 l -30 4 l 22 20 Z" stroke-width="8"/>
    <path d="M 492 770 l -6 -24 M 492 770 l 24 6 M 504 758 l -6 -24 M 504 758 l 24 6" stroke-width="5"/>
    <circle cx="600" cy="660" r="16" fill="#fff" stroke="none"/>
  </g>`;
  p += `<rect x="818" y="480" width="8" height="330" fill="url(#pg3b)"/>`;
  for (let i = 0; i <= 6; i++) p += `<path d="M 828 ${f(480 + i * 55)} h 6" stroke="#ddd" stroke-width="1.2"/>`;
  p += `<text x="410" y="892" font-family="Oswald" font-size="13" letter-spacing="2" fill="#eee">404 CULTURE · THERMAL DIV.</text>`;
  p += `<text x="790" y="892" text-anchor="end" font-family="Oswald" font-size="13" letter-spacing="2" fill="#eee">SIGNAL LOST 04:04:04</text>`;
  const s = {
    seed: 61, base: "#24221f", light: "#6e6a62", dark: "#0b0a09", bg: "#050505", washAmt: 0.1, wash2Amt: 0.07, fadeAmt: 0.5,
    printFreq: 0.11, printCrack: 1.8, printKeep: 2.2, speckle: 0.3, grainAmt: 0.07, foldDark: 0.3, label: L.neckLabel(), shadowAmt: 0,
    holes: [[860, 420, 3, 20], [360, 980, 3, 30], [820, 1080, 2, 20]], raw: { collar: 0.5 },
  };
  return L.page(L.garment("g3b", t, s, p) + L.sleeveTag(1009, 600, -32), { dark: true, footer: FOOT, code: "0306" });
};

// ---------------------------------------------------------------- 4: gothic faded longsleeve

D["07_memories_dont_load_longsleeve"] = () => {
  const r = rng(113);
  const t = L.longTee();
  const ink = "#b4b4b4", fill = "#0e0e0e";
  let p = `<text x="440" y="440" transform="rotate(-8 440 440)" font-family="Pinyon" font-size="60" fill="${ink}">Memories don't load</text>`;
  p += FX.bat(600, 612, 2.1, 0, fill, ink);
  p += `<g transform="translate(600 635) scale(1.25) translate(-600 -635)">
    <path d="M 600 720 C 510 660 505 575 560 572 C 582 571 596 588 600 604 C 604 588 618 571 640 572 C 695 575 690 660 600 720 Z" fill="${fill}" stroke="${ink}" stroke-width="4"/>
    <path d="M 600 700 C 535 655 530 595 562 592" fill="none" stroke="${ink}" stroke-width="1.8"/>
    <path d="M 572 612 q 12 30 -2 56 M 610 620 q 20 20 12 48 M 590 650 q 8 18 -4 34" stroke="${ink}" stroke-width="1.5" fill="none"/></g>`;
  p += `<g transform="translate(605 640) rotate(32)" fill="${fill}" stroke="${ink}" stroke-width="3">
    <path d="M -10 -40 L 10 -40 L 0 150 Z"/><path d="M 0 -40 L 0 130" stroke-width="1.2"/>
    <rect x="-44" y="-54" width="88" height="14" rx="4"/><rect x="-8" y="-118" width="16" height="64"/>
    <path d="M -8 -110 l 16 8 M -8 -98 l 16 8 M -8 -86 l 16 8 M -8 -74 l 16 8" stroke-width="1.5"/><circle cx="0" cy="-128" r="11"/></g>`;
  p += FX.bat(430, 505, 0.55, -18, fill, ink) + FX.bat(785, 480, 0.45, 14, fill, ink) + FX.bat(775, 805, 0.38, 8, fill, ink) + FX.bat(420, 790, 0.32, -6, fill, ink);
  p += FX.tribal(r, 600, 900, 170, 150, ink, 8);
  p += `<text x="600" y="935" text-anchor="middle" font-family="Unifraktur" font-size="150" fill="${fill}" stroke="${ink}" stroke-width="3.5">404</text>`;
  p += `<text x="600" y="978" text-anchor="middle" font-family="Oswald" font-size="16" letter-spacing="10" fill="${ink}">CULTURE</text>`;
  p += FX.barbedWire(r, 262, 460, 214, 1150, ink) + FX.barbedWire(r, 938, 460, 986, 1150, ink);
  const s = {
    seed: 71, base: "#131313", light: "#3c3c3c", dark: "#050505", bg: "#050505", washAmt: 0.05, wash2Amt: 0.05, fadeAmt: 0.35,
    printFreq: 0.06, printCrack: 3.0, printKeep: 2.3, printOpacity: 0.72, foldDark: 0.35, foldLight: 0.06, thread: "#3a3a3a",
    holes: [[250, 1120, 3, 20], [950, 1130, 3, 20], [700, 1060, 2, 20]], raw: { hem: 1.1, cuffs: 1.2 }, shadowAmt: 0,
    label: L.neckLabel("#2a2a2a", "#9a9a9a"),
  };
  return L.page(L.garment("g4a", t, s, p), { dark: true, footer: FOOT, code: "0407" });
};

D["08_lost_never_found_longsleeve"] = () => {
  const r = rng(127);
  const t = L.longTee({ hem: 1095 });
  const ink = "#9d9aa3", fill = "#100f12";
  let p = `<text x="600" y="430" transform="rotate(-4 600 430)" text-anchor="middle" font-family="Pinyon" font-size="64" fill="${ink}">lost, never found</text>`;
  p += FX.lineWing(r, 572, 610, -1, 1.0, ink) + FX.lineWing(r, 628, 610, 1, 1.0, ink);
  p += `<ellipse cx="600" cy="515" rx="78" ry="20" fill="none" stroke="${ink}" stroke-width="6" stroke-dasharray="190 26 90 34"/>`;
  p += `<text x="600" y="598" text-anchor="middle" font-family="Unifraktur" font-size="64" fill="${fill}" stroke="${ink}" stroke-width="3">404</text>`;
  p += `<text x="600" y="760" text-anchor="middle" font-family="Pirata" font-size="132" fill="${fill}" stroke="${ink}" stroke-width="3.2">Culture</text>`;
  p += `<path d="M 470 780 q 130 40 260 0" stroke="${ink}" stroke-width="2.5" fill="none"/>`;
  for (const [x, y] of [[465, 812], [730, 800], [520, 560], [690, 560], [600, 850]]) p += `<path d="M ${x} ${y - 14} L ${x + 3} ${y - 3} L ${x + 14} ${y} L ${x + 3} ${y + 3} L ${x} ${y + 14} L ${x - 3} ${y + 3} L ${x - 14} ${y} L ${x - 3} ${y - 3} Z" fill="${ink}"/>`;
  p += FX.web(412, 960, 115, -Math.PI / 2, 0, ink) + FX.web(788, 960, 95, -Math.PI, -Math.PI / 2, ink);
  p += `<text x="600" y="880" text-anchor="middle" font-family="Oswald" font-size="15" letter-spacing="8" fill="${ink}">EST. 404 · NOWHERE</text>`;
  p += FX.thornVine(r, 268, 450, 215, 1150, ink) + FX.thornVine(r, 932, 450, 985, 1150, ink);
  const s = {
    seed: 83, base: "#1a191c", light: "#403e45", dark: "#070608", bg: "#050505", washAmt: 0.07, wash2Amt: 0.06, fadeAmt: 0.4,
    printFreq: 0.06, printCrack: 3.0, printKeep: 2.3, printOpacity: 0.72, foldDark: 0.35, foldLight: 0.06, thread: "#3e3c42",
    holes: [[900, 380, 3, 20], [330, 700, 2, 20], [230, 1100, 3, 20], [880, 1040, 3, 30]], raw: { hem: 1.3, cuffs: 0.8, collar: 0.7 }, shadowAmt: 0,
    label: L.neckLabel(),
  };
  return L.page(L.garment("g4b", t, s, p), { dark: true, footer: FOOT, code: "0408" });
};

// ---------------------------------------------------------------- 5: molten burn

D["09_molten_cross_tee"] = () => {
  const r = rng(131);
  const t = L.boxyTee({ hem: 1110 });
  const red = "#c42a1e";
  let p = `<defs>${FX.lavaFilter("lv5a", 7, { core: 22 })}</defs>`;
  p += `<text transform="translate(470 700) rotate(-90)" text-anchor="middle" font-family="Sedgwick" font-size="170" fill="none" stroke="${red}" stroke-width="2.6">404</text>`;
  p += `<text transform="translate(740 640) rotate(90)" text-anchor="middle" font-family="Sedgwick" font-size="112" fill="none" stroke="${red}" stroke-width="2.6">Culture</text>`;
  p += `<g filter="url(#lv5a)"><path d="M 548 430 L 652 430 L 626 596 L 758 572 L 758 676 L 626 652 L 652 910 L 548 910 L 574 652 L 442 676 L 442 572 L 574 596 Z" fill="#fff"/></g>`;
  p += FX.embers(r, 600, 640, 200, 300, 70);
  p += `<path d="M 430 470 l 16 16 m 0 -16 l -16 16 M 770 860 l 14 14 m 0 -14 l -14 14" stroke="${red}" stroke-width="2.4"/>`;
  const s = {
    seed: 97, base: "#282624", light: "#7c776f", dark: "#0f0e0d", bg: "#ffffff", washAmt: 0.13, wash2Amt: 0.12, fadeAmt: 0.6,
    printFreq: 0.09, printCrack: 1.8, printKeep: 2.2, speckle: 0.4, grainAmt: 0.1, foldDark: 0.28, thread: "#6d6861",
    holes: [[330, 420, 2, 20], [860, 380, 3, 30], [900, 820, 2, 20], [380, 980, 3, 30], [650, 1060, 2, 20]],
    raw: { hem: 1.6, cuffs: 1.4, collar: 1.2 }, label: L.neckLabel(),
  };
  return L.page(L.garment("g5a", t, s, p), { header: false, footer: ["© Made By 404 CULTURE"] });
};

D["10_burning_404_tee"] = () => {
  const r = rng(149);
  const t = L.boxyTee({ hem: 1120, half: 265 });
  const red = "#c42a1e";
  let p = `<defs>${FX.lavaFilter("lv5b", 21, { core: 13, rough: 12, glow: 20, flame: 110 })}</defs>`;
  p += `<text transform="translate(600 560) rotate(-8)" text-anchor="middle" font-family="Sedgwick" font-size="150" fill="none" stroke="${red}" stroke-width="2.6">culture</text>`;
  p += `<g filter="url(#lv5b)"><text x="600" y="780" transform="rotate(-4 600 700)" text-anchor="middle" font-family="ArchivoBlack" font-size="250" letter-spacing="-6" fill="#fff">404</text></g>`;
  p += `<text transform="translate(705 875) rotate(-8)" text-anchor="middle" font-family="Sedgwick" font-size="56" fill="none" stroke="${red}" stroke-width="2">est. nowhere</text>`;
  p += FX.embers(r, 600, 640, 260, 260, 80, "#ffa640");
  const s = {
    seed: 101, base: "#2c2622", light: "#83756a", dark: "#110e0c", bg: "#ffffff", washAmt: 0.12, wash2Amt: 0.14, fadeAmt: 0.6,
    printFreq: 0.09, printCrack: 1.8, printKeep: 2.2, speckle: 0.4, grainAmt: 0.1, foldDark: 0.28, thread: "#7a6d62",
    holes: [[860, 450, 3, 30], [330, 620, 2, 20], [840, 980, 3, 30], [420, 1050, 2, 20]],
    raw: { hem: 1.8, cuffs: 1.0, collar: 1.2 }, label: L.neckLabel("#c8201e"),
  };
  return L.page(L.garment("g5b", t, s, p) + L.sleeveTag(190, 590, 32, "#c8201e", "#fff"), { header: false, footer: ["© Made By 404 CULTURE"] });
};

module.exports = D;

