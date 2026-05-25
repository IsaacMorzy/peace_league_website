import { chromium } from 'playwright';

const BASE = 'http://localhost:4321';

async function main() {
  const browser = await chromium.launch({ headless: true });

  // Desktop check
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 } });
  const page = await ctx.newPage();
  await page.goto(`${BASE}/about`, { waitUntil: 'networkidle' });

  const hero = page.locator('#about-hero');
  const box = await hero.boundingBox();
  const styles = await hero.evaluate(el => {
    const s = window.getComputedStyle(el);
    return {
      paddingTop: s.paddingTop,
      paddingBottom: s.paddingBottom,
      minHeight: s.minHeight,
    };
  });

  const heading = page.locator('#about-hero h1');
  const headingBox = await heading.boundingBox();

  const contentEl = await hero.evaluate(el => {
    const inner = el.querySelector('[class*="max-w-5xl"]');
    if (!inner) return null;
    const s = window.getComputedStyle(inner);
    const r = inner.getBoundingClientRect();
    return { paddingTop: s.paddingTop, paddingBottom: s.paddingBottom, height: r.height, top: r.top };
  });

  console.log('=== About Hero ===');
  console.log('Hero section:', JSON.stringify({ width: box?.width, height: box?.height, ...styles }));
  console.log('Heading:', JSON.stringify(headingBox));
  console.log('Content container:', JSON.stringify(contentEl));
  console.log('');

  // Check all pages for hero-gradient presence
  const pages = ['/', '/about', '/causes', '/donate', '/contact', '/events', '/team',
    '/blog', '/careers', '/faq', '/gallery', '/partner', '/privacy',
    '/sitemap', '/terms', '/testimonials', '/volunteer'];

  for (const route of pages) {
    await page.goto(`${BASE}${route}`, { waitUntil: 'networkidle' });
    const hasAboutHero = await page.locator('#about-hero').count();
    const hgCount = await page.locator('.hero-gradient').count();
    const hgSections = await page.locator('.hero-gradient').evaluateAll(els => 
      els.map(el => el.id || el.className)
    );
    console.log(`${route}: #about-hero=${hasAboutHero > 0}, .hero-gradient count=${hgCount} => ${hgSections.join(', ')}`);
  }

  await browser.close();
}

main().catch(err => { console.error(err); process.exit(1); });
