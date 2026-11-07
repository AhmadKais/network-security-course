#!/usr/bin/env node
// Render assets/img/*.svg to high-resolution PNGs (for LaTeX worksheets and previews).
// Usage (from Course_Materials/):  node _build/svg2png.js [outDir]   (default: Worksheets/img)
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

let puppeteer;
try { puppeteer = require('puppeteer'); }
catch (e) {
  const g = execSync('npm root -g').toString().trim();
  puppeteer = require(path.join(g, '@mermaid-js/mermaid-cli/node_modules/puppeteer'));
}

const ROOT = path.dirname(__dirname);
const SRC = path.join(ROOT, 'assets', 'img');
const OUT = path.resolve(ROOT, process.argv[2] || path.join('Worksheets', 'img'));
const cfg = JSON.parse(fs.readFileSync(path.join(__dirname, 'puppeteer.json'), 'utf8'));

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await puppeteer.launch({ headless: 'new', ...cfg });
  const page = await browser.newPage();
  for (const f of fs.readdirSync(SRC).filter(f => f.endsWith('.svg')).sort()) {
    const svg = fs.readFileSync(path.join(SRC, f), 'utf8');
    const m = svg.match(/width="(\d+)" height="(\d+)"/);
    const w = +m[1], h = +m[2];
    await page.setViewport({ width: w, height: h, deviceScaleFactor: 3 });
    await page.setContent(`<html><body style="margin:0;background:#fff">${svg}</body></html>`);
    await page.screenshot({ path: path.join(OUT, f.replace(/\.svg$/, '.png')), clip: { x: 0, y: 0, width: w, height: h } });
    console.log('png', f);
  }
  await browser.close();
})();
