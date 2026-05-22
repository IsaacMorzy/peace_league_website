import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, '..');

export function routeToSlug(route) {
  if (route === '/' || route === '') return 'home';
  return route.replace(/^\//, '').replace(/\/$/, '').replace(/\//g, '-');
}

function readRoutesFile(filePath) {
  const raw = fs.readFileSync(filePath, 'utf8');
  return raw.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
}

function getArgValue(flag, fallback = null) {
  const idx = process.argv.indexOf(flag);
  if (idx === -1) return fallback;
  return process.argv[idx + 1] || fallback;
}

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function runLighthouse({ url, mode, port, outputBase }) {
  const lighthouseBin = path.resolve(repoRoot, 'node_modules/.bin/lighthouse');
  if (!fs.existsSync(lighthouseBin)) {
    throw new Error(`Missing lighthouse binary at ${lighthouseBin}`);
  }

  const baseArgs = [
    url,
    `--port=${port}`,
    '--only-categories=performance,accessibility,best-practices,seo',
    '--throttling-method=simulate',
    '--quiet',
    '--output=html,json',
    `--output-path=${outputBase}`
  ];

  if (mode === 'desktop') {
    baseArgs.push('--preset=desktop');
  }

  const result = spawnSync(lighthouseBin, baseArgs, { stdio: 'inherit' });
  if (result.status !== 0) {
    throw new Error(`Lighthouse run failed for ${url} (${mode})`);
  }
}

function extractMetrics(lhr) {
  const score = (key) => (lhr.categories[key]?.score ?? 0) * 100;
  const audit = (key) => lhr.audits[key]?.numericValue ?? null;
  const inp = lhr.audits['interactive']?.numericValue ?? null;
  const networkRequests = lhr.audits['network-requests']?.details?.items?.length ?? null;

  return {
    performance: Math.round(score('performance')),
    accessibility: Math.round(score('accessibility')),
    bestPractices: Math.round(score('best-practices')),
    seo: Math.round(score('seo')),
    lcp: audit('largest-contentful-paint'),
    cls: audit('cumulative-layout-shift'),
    tbt: audit('total-blocking-time'),
    inp,
    networkRequests
  };
}

async function main() {
  const baseUrl = getArgValue('--base-url', 'http://localhost:4321');
  const routesFile = getArgValue(
    '--routes-file',
    path.resolve(repoRoot, 'lighthouse-reports/routes.txt')
  );
  const port = parseInt(getArgValue('--port', '9222'), 10);

  const routes = readRoutesFile(routesFile);
  const reportsRoot = path.resolve(repoRoot, 'lighthouse-reports');
  const modes = ['mobile', 'desktop'];

  ensureDir(reportsRoot);
  for (const mode of modes) {
    ensureDir(path.join(reportsRoot, mode));
  }

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
      const outputBase = path.join(reportsRoot, mode, slug);

      console.log(`\n[${mode}] ${url}`);
      runLighthouse({ url, mode, port, outputBase });

      const outputJson = `${outputBase}.report.json`;
      if (!fs.existsSync(outputJson)) {
        throw new Error(`Expected report not found: ${outputJson}`);
      }
      const lhr = JSON.parse(fs.readFileSync(outputJson, 'utf8'));
      summary.results[mode][route] = extractMetrics(lhr);
      const m = summary.results[mode][route];
      console.log(`  perf=${m.performance} a11y=${m.accessibility} bp=${m.bestPractices} seo=${m.seo} lcp=${m.lcp?.toFixed(0)}ms`);
    }
  }

  const summaryPath = path.join(reportsRoot, 'summary.json');
  fs.writeFileSync(summaryPath, `${JSON.stringify(summary, null, 2)}\n`);

  const csvLines = ['route,mode,performance,accessibility,bestPractices,seo,lcp,cls,tbt,inp,networkRequests'];
  for (const mode of modes) {
    for (const route of routes) {
      const row = summary.results[mode][route];
      csvLines.push([
        route,
        mode,
        row.performance,
        row.accessibility,
        row.bestPractices,
        row.seo,
        row.lcp ?? '',
        row.cls ?? '',
        row.tbt ?? '',
        row.inp ?? '',
        row.networkRequests ?? ''
      ].join(','));
    }
  }
  fs.writeFileSync(path.join(reportsRoot, 'summary.csv'), `${csvLines.join('\n')}\n`);

  console.log('\nDone. Summary written to', summaryPath);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
