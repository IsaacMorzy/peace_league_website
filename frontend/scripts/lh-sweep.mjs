import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(__dirname, '..');

function routeToSlug(route) {
  if (route === '/' || route === '') return 'home';
  return route.replace(/^\//, '').replace(/\/$/, '').replace(/\//g, '-');
}

function readRoutesFile(filePath) {
  const raw = fs.readFileSync(filePath, 'utf8');
  return raw.split(/\r?\n/).map(l => l.trim()).filter(Boolean);
}

const routes = readRoutesFile(path.join(repoRoot, 'lighthouse-reports/routes.txt'));
const reportsRoot = path.join(repoRoot, 'lighthouse-reports');
const baseUrl = 'http://127.0.0.1:4321';
const modes = ['mobile'];

for (const mode of modes) fs.mkdirSync(path.join(reportsRoot, mode), { recursive: true });

const { launch } = await import('chrome-launcher');
const lh = await import('lighthouse');

const chrome = await launch({
  chromePath: '/snap/chromium/3423/usr/lib/chromium-browser/chrome',
  port: 0,
  chromeFlags: ['--headless', '--disable-gpu', '--no-sandbox', '--disable-dev-shm-usage']
});
console.log('Chrome on port:', chrome.port);

const summary = {
  generatedAt: new Date().toISOString(),
  baseUrl,
  routes,
  results: { mobile: {}, desktop: {} }
};

for (const route of routes) {
  const slug = routeToSlug(route);
  for (const mode of modes) {
    const url = `${baseUrl}${route}`;
    process.stdout.write(`[${mode}] ${url} ... `);

    const config = {
      extends: 'lighthouse:default',
      settings: {
        onlyCategories: ['performance', 'accessibility', 'best-practices', 'seo'],
        formFactor: mode === 'desktop' ? 'desktop' : 'mobile',
        throttlingMethod: 'simulate'
      }
    };
    if (mode === 'desktop') {
      config.settings.screenEmulation = { mobile: false, width: 1350, height: 940, deviceScaleFactor: 1, disabled: false };
    }

    const result = await lh.default(url, { port: chrome.port }, config);
    const lhr = result.lhr;

    const outputBase = path.join(reportsRoot, mode, slug);
    fs.writeFileSync(`${outputBase}.report.json`, JSON.stringify(lhr, null, 2));

    function extractMetrics(lhr) {
      const score = (key) => (lhr.categories[key]?.score ?? 0) * 100;
      const audit = (key) => lhr.audits[key]?.numericValue ?? null;
      const inp = lhr.audits['interactive']?.numericValue ?? null;
      const netReqs = lhr.audits['network-requests']?.details?.items?.length ?? null;
      return {
        performance: Math.round(score('performance')),
        accessibility: Math.round(score('accessibility')),
        bestPractices: Math.round(score('best-practices')),
        seo: Math.round(score('seo')),
        lcp: audit('largest-contentful-paint'),
        cls: audit('cumulative-layout-shift'),
        tbt: audit('total-blocking-time'),
        inp,
        networkRequests: netReqs
      };
    }

    const m = extractMetrics(lhr);
    summary.results[mode][route] = m;
    console.log(`perf=${m.performance} lcp=${m.lcp?.toFixed(0)}ms tbt=${m.tbt?.toFixed(0)}ms`);
  }
}

const summaryPath = path.join(reportsRoot, 'summary.json');
fs.writeFileSync(summaryPath, `${JSON.stringify(summary, null, 2)}\n`);
console.log('\nDone. Summary written to', summaryPath);

await chrome.kill();
