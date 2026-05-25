import { chromium } from 'playwright';
import { mkdirSync } from 'fs';

const BASE = 'http://localhost:4321';
const OUT = '/home/crowd/frappe-bench/tmp/screenshots';
mkdirSync(OUT, { recursive: true });

const ROUTES = [
  '/', '/about', '/causes', '/donate', '/contact', '/events', '/team',
  '/blog', '/careers', '/faq', '/gallery', '/partner', '/privacy',
  '/sitemap', '/terms', '/testimonials', '/volunteer',
];

async function main() {
  const browser = await chromium.launch({ headless: true });

  // Desktop 1280x800
  const desktopCtx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  for (const route of ROUTES) {
    const page = await desktopCtx.newPage();
    await page.goto(`${BASE}${route}`, { waitUntil: 'networkidle', timeout: 15000 }).catch(() => {});
    await page.screenshot({ path: `${OUT}/${route === '/' ? 'index' : route.slice(1)}-desktop.png`, fullPage: true });
    await page.close();
  }
  await desktopCtx.close();

  // Mobile 375x812
  const mobileCtx = await browser.newContext({ viewport: { width: 375, height: 812 } });
  for (const route of ROUTES) {
    const page = await mobileCtx.newPage();
    await page.goto(`${BASE}${route}`, { waitUntil: 'networkidle', timeout: 15000 }).catch(() => {});
    await page.screenshot({ path: `${OUT}/${route === '/' ? 'index' : route.slice(1)}-mobile.png`, fullPage: true });
    await page.close();
  }
  await mobileCtx.close();

  await browser.close();
  console.log(`Screenshots saved to ${OUT}`);
}

main().catch(err => { console.error(err); process.exit(1); });
