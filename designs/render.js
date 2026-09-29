// Renders every design in designs.js to out/<name>.png via headless Chromium.
// usage: node render.js [name-filter]
const fs = require("fs");
const path = require("path");
const { chromium } = require(path.join(process.env.NODE_PATH || "/opt/node22/lib/node_modules", "playwright"));
const DESIGNS = require("./designs");

(async () => {
  const only = process.argv[2];
  const outDir = path.join(__dirname, "out");
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch();
  const pg = await browser.newPage({ viewport: { width: 1200, height: 1500 }, deviceScaleFactor: 1.5 });
  for (const [name, build] of Object.entries(DESIGNS)) {
    if (only && !name.includes(only)) continue;
    const html = build();
    const tmp = path.join(outDir, `.${name}.html`);
    fs.writeFileSync(tmp, html);
    await pg.goto("file://" + tmp);
    await pg.waitForFunction(() => window.__done === true, null, { timeout: 60000 });
    await pg.evaluate(() => document.fonts.ready);
    await pg.waitForTimeout(150);
    await pg.screenshot({ path: path.join(outDir, `${name}.png`), clip: { x: 0, y: 0, width: 1200, height: 1500 } });
    fs.unlinkSync(tmp);
    console.log("rendered", name);
  }
  await browser.close();
})();
