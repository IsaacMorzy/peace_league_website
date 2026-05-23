import { chromium } from 'playwright';
import http from 'node:http';

const BASE = 'http://localhost:4321';

const ROUTES = [
  '/', '/about', '/causes', '/donate', '/contact', '/events', '/team',
  '/blog', '/careers', '/faq', '/gallery', '/partner', '/privacy',
  '/sitemap', '/terms', '/testimonials', '/volunteer',
];

async function pageStatus(url) {
  return new Promise((resolve) => {
    http.get(url, (res) => { res.resume(); resolve(res.statusCode); })
      .on('error', () => resolve(null));
  });
}

async function main() {
  const browser = await chromium.launch({ headless: true });
  const results = [];

  // 1. HTTP status checks
  for (const route of ROUTES) {
    const url = `${BASE}${route}`;
    const status = await pageStatus(url);
    const pass = status === 200;
    results.push({ test: `GET ${route}`, pass, detail: `status ${status}` });
  }

  // 2. Mobile browser tests (375x812)
  {
    const ctx = await browser.newContext({ viewport: { width: 375, height: 812 } });
    const page = await ctx.newPage();
    await page.goto(BASE, { waitUntil: 'networkidle' });

    // Mobile menu button exists
    const menuBtn = page.locator('#mobile-menu-btn');
    const menuBtnExists = (await menuBtn.count()) > 0;
    results.push({ test: 'Mobile: menu button exists', pass: menuBtnExists, detail: menuBtnExists ? 'found #mobile-menu-btn' : 'not found' });

    if (menuBtnExists) {
      // Initially drawer should be closed
      const drawerClosed = await page.locator('#mobile-drawer').evaluate(el => !el.classList.contains('open'));
      results.push({ test: 'Mobile: drawer initially closed', pass: drawerClosed, detail: drawerClosed ? 'no open class' : 'has open class' });

      // Click to open
      await menuBtn.click();
      await page.waitForTimeout(600);
      const drawerOpen = await page.locator('#mobile-drawer').evaluate(el => el.classList.contains('open'));
      results.push({ test: 'Mobile: drawer opens on click', pass: drawerOpen, detail: drawerOpen ? 'open class added' : 'still closed' });

      // Close via close button
      const closeBtn = page.locator('#mobile-close-btn');
      const closeBtnExists = (await closeBtn.count()) > 0;
      if (closeBtnExists) {
        await closeBtn.click();
        await page.waitForTimeout(600);
        const drawerClosedAgain = await page.locator('#mobile-drawer').evaluate(el => !el.classList.contains('open'));
        results.push({ test: 'Mobile: drawer closes via close btn', pass: drawerClosedAgain, detail: drawerClosedAgain ? 'closed' : 'still open' });
      }
    }

    // Check donation amounts on home page
    const amounts = page.locator('.donation-amount');
    const count = await amounts.count();
    const texts = [];
    for (let i = 0; i < count; i++) {
      texts.push((await amounts.nth(i).textContent()).trim());
    }
    const expected = ['$25', '$50', '$100', '$500'];
    const match = texts.every((t, i) => t === expected[i]);
    results.push({ test: 'Home: donation amounts correct', pass: match && count === 4, detail: texts.join(', ') || `only ${count} found` });

    await page.close();
    await ctx.close();
  }

  // 3. Desktop browser tests (1280x800)
  {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
    const page = await ctx.newPage();
    await page.goto(BASE, { waitUntil: 'networkidle' });

    // Desktop nav links should be visible
    const nav = page.locator('header#site-header nav[aria-label="Main navigation"]');
    const desktopLinks = nav.locator('a, button').filter({ hasNotText: '' });
    const linkCount = await desktopLinks.count();
    results.push({ test: 'Desktop: nav has interactive elements', pass: linkCount >= 5, detail: `${linkCount} elements found` });

    // Donate CTA button visible (any visible donate link qualifies)
    const donateVisible = await page.locator('a[href="/donate"]').evaluateAll(
      els => els.some(el => {
        const style = window.getComputedStyle(el);
        return style.display !== 'none' && style.visibility !== 'hidden' && el.offsetParent !== null;
      })
    );
    results.push({ test: 'Desktop: donate CTA visible', pass: donateVisible, detail: donateVisible ? 'visible' : 'not found' });

    await page.close();
    await ctx.close();
  }

  await browser.close();

  let passed = 0, failed = 0;
  for (const r of results) {
    const icon = r.pass ? 'PASS' : 'FAIL';
    if (r.pass) passed++; else failed++;
    console.log(`  ${icon}  ${r.test} [${r.detail}]`);
  }
  console.log(`\n${passed} passed, ${failed} failed, ${results.length} total`);
  process.exit(failed > 0 ? 1 : 0);
}

main().catch(err => {
  console.error('Fatal:', err);
  process.exit(1);
});
