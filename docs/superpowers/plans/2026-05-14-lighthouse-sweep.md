# Lighthouse Sweep (All Pages) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Run Lighthouse on every Astro page in mobile + desktop, apply shared performance fixes, and re-sweep to confirm site-wide improvements.

**Architecture:** Use Node scripts in `frontend/scripts/` to collect routes and run Lighthouse CLI against a local preview server. Store reports per route/mode, build a summary JSON/CSV, then apply shared fixes in `Layout.astro` and `global.css` only.

**Tech Stack:** Astro, Tailwind CSS, Node.js 22, Lighthouse CLI, Playwright Chromium.

---

## File Structure

- Create: `frontend/scripts/collect-routes.mjs`
  - Responsibility: derive stable route list from `frontend/src/pages/` (skip dynamic + API pages).
- Create: `frontend/scripts/collect-routes.test.mjs`
  - Responsibility: verify route derivation logic.
- Create: `frontend/scripts/lighthouse-sweep.mjs`
  - Responsibility: run Lighthouse (mobile + desktop) for all routes, write reports + summary.
- Create: `frontend/scripts/lighthouse-sweep.test.mjs`
  - Responsibility: verify deterministic helper logic (route → slug).
- Modify: `frontend/src/layouts/Layout.astro`
  - Responsibility: shared JS guards and conditional speculation rules injection.
- Modify: `frontend/src/styles/global.css`
  - Responsibility: mobile-only animation reductions.
- Create/Update: `frontend/lighthouse-reports/*`
  - Responsibility: HTML/JSON reports + summary files.

---

### Task 1: Add route collection script

**Files:**
- Create: `frontend/scripts/collect-routes.test.mjs`
- Create: `frontend/scripts/collect-routes.mjs`

- [ ] **Step 1: Write the failing test**

```js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';

import { collectRoutesFromPages } from './collect-routes.mjs';

test('collectRoutesFromPages builds expected routes', () => {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'pla-pages-'));
  const pages = path.join(tmp, 'pages');
  fs.mkdirSync(pages, { recursive: true });

  fs.writeFileSync(path.join(pages, 'index.astro'), '');
  fs.writeFileSync(path.join(pages, 'about.astro'), '');

  fs.mkdirSync(path.join(pages, 'blog'), { recursive: true });
  fs.writeFileSync(path.join(pages, 'blog', 'index.astro'), '');
  fs.writeFileSync(path.join(pages, 'blog', '[slug].astro'), '');

  fs.mkdirSync(path.join(pages, 'api'), { recursive: true });
  fs.writeFileSync(path.join(pages, 'api', 'ping.astro'), '');

  const routes = collectRoutesFromPages(pages);
  assert.deepEqual(routes, ['/', '/about', '/blog']);
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test frontend/scripts/collect-routes.test.mjs`

Expected: FAIL (module not found: `collect-routes.mjs`).

- [ ] **Step 3: Write the implementation**

```js
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function walk(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...walk(fullPath));
    } else {
      files.push(fullPath);
    }
  }
  return files;
}

function isDynamicRoute(filePath) {
  return filePath.includes('[') && filePath.includes(']');
}

function isApiRoute(filePath) {
  return filePath.split(path.sep).includes('api');
}

export function collectRoutesFromPages(pagesRoot) {
  const astroFiles = walk(pagesRoot).filter((file) => file.endsWith('.astro'));
  const routes = [];

  for (const filePath of astroFiles) {
    const rel = path.relative(pagesRoot, filePath);
    const parsed = path.parse(rel);

    if (isDynamicRoute(rel) || isApiRoute(rel)) {
      continue;
    }

    if (parsed.name === '404') {
      continue;
    }

    const segments = rel
      .replace(/\.astro$/, '')
      .split(path.sep)
      .filter(Boolean);

    if (segments.length > 0 && segments[segments.length - 1] === 'index') {
      segments.pop();
    }

    const route = `/${segments.join('/')}`.replace(/\/$/, '') || '/';
    routes.push(route === '' ? '/' : route);
  }

  return Array.from(new Set(routes)).sort();
}

function getArgValue(flag) {
  const idx = process.argv.indexOf(flag);
  if (idx === -1) return null;
  return process.argv[idx + 1] || null;
}

if (process.argv[1] === __filename) {
  const pagesRoot = getArgValue('--pages') || path.resolve(__dirname, '../src/pages');
  const outFile = getArgValue('--out');
  const routes = collectRoutesFromPages(path.resolve(pagesRoot));
  const output = `${routes.join('\n')}\n`;

  if (outFile) {
    fs.mkdirSync(path.dirname(outFile), { recursive: true });
    fs.writeFileSync(outFile, output);
  } else {
    process.stdout.write(output);
  }
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `node --test frontend/scripts/collect-routes.test.mjs`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add frontend/scripts/collect-routes.mjs frontend/scripts/collect-routes.test.mjs
git commit -m "chore: add route collection utility"
```

---

### Task 2: Add Lighthouse sweep script

**Files:**
- Create: `frontend/scripts/lighthouse-sweep.test.mjs`
- Create: `frontend/scripts/lighthouse-sweep.mjs`

- [ ] **Step 1: Write the failing test**

```js
import { test } from 'node:test';
import assert from 'node:assert/strict';

import { routeToSlug } from './lighthouse-sweep.mjs';

test('routeToSlug converts routes to stable slugs', () => {
  assert.equal(routeToSlug('/'), 'home');
  assert.equal(routeToSlug('/about'), 'about');
  assert.equal(routeToSlug('/about/team'), 'about-team');
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test frontend/scripts/lighthouse-sweep.test.mjs`

Expected: FAIL (module not found: `lighthouse-sweep.mjs`).

- [ ] **Step 3: Write the implementation**

```js
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import { chromium } from 'playwright';

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

function runLighthouse({ url, mode, chromePath, outputHtml, outputJson }) {
  const lighthouseBin = path.resolve(repoRoot, 'node_modules/.bin/lighthouse');
  if (!fs.existsSync(lighthouseBin)) {
    throw new Error(`Missing lighthouse binary at ${lighthouseBin}`);
  }

  const baseArgs = [
    url,
    `--chrome-path=${chromePath}`,
    '--only-categories=performance,accessibility,best-practices,seo',
    '--throttling-method=simulate',
    '--quiet'
  ];

  if (mode === 'desktop') {
    baseArgs.push('--preset=desktop', '--form-factor=desktop');
  } else {
    baseArgs.push('--form-factor=mobile');
  }

  const htmlArgs = [...baseArgs, '--output=html', `--output-path=${outputHtml}`];
  const jsonArgs = [...baseArgs, '--output=json', `--output-path=${outputJson}`];

  const htmlResult = spawnSync(lighthouseBin, htmlArgs, { stdio: 'inherit' });
  if (htmlResult.status !== 0) {
    throw new Error(`Lighthouse HTML run failed for ${url} (${mode})`);
  }

  const jsonResult = spawnSync(lighthouseBin, jsonArgs, { stdio: 'inherit' });
  if (jsonResult.status !== 0) {
    throw new Error(`Lighthouse JSON run failed for ${url} (${mode})`);
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

if (process.argv[1] === __filename) {
  const baseUrl = getArgValue('--base-url', 'http://localhost:4321');
  const routesFile = getArgValue(
    '--routes-file',
    path.resolve(repoRoot, 'lighthouse-reports/routes.txt')
  );

  const chromePath = process.env.CHROME_PATH || chromium.executablePath();
  if (!chromePath) {
    throw new Error('Unable to resolve CHROME_PATH');
  }

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
      const outputHtml = `${outputBase}.html`;
      const outputJson = `${outputBase}.json`;

      runLighthouse({
        url,
        mode,
        chromePath,
        outputHtml,
        outputJson
      });

      const lhr = JSON.parse(fs.readFileSync(outputJson, 'utf8'));
      summary.results[mode][route] = extractMetrics(lhr);
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
        row.lcp,
        row.cls,
        row.tbt,
        row.inp,
        row.networkRequests
      ].join(','));
    }
  }
  fs.writeFileSync(path.join(reportsRoot, 'summary.csv'), `${csvLines.join('\n')}\n`);
}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `node --test frontend/scripts/lighthouse-sweep.test.mjs`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add frontend/scripts/lighthouse-sweep.mjs frontend/scripts/lighthouse-sweep.test.mjs
git commit -m "chore: add lighthouse sweep runner"
```

---

### Task 3: Run initial sweep

**Files:**
- Create: `frontend/lighthouse-reports/routes.txt`
- Create: `frontend/lighthouse-reports/*`

- [ ] **Step 1: Build the site**

Run (from `frontend/`): `yarn build`

Expected: `✔ Completed` and all pages built.

- [ ] **Step 2: Start preview server**

Run (from `frontend/`): `yarn preview --host 0.0.0.0 --port 4321`

Expected: `Local: http://localhost:4321/` and process stays running.

- [ ] **Step 3: Generate routes list**

Run (from repo root):

```bash
node frontend/scripts/collect-routes.mjs --pages frontend/src/pages --out frontend/lighthouse-reports/routes.txt
```

Expected: `frontend/lighthouse-reports/routes.txt` populated with routes.

- [ ] **Step 4: Run Lighthouse sweep**

Run (from repo root):

```bash
node frontend/scripts/lighthouse-sweep.mjs --base-url http://localhost:4321 --routes-file frontend/lighthouse-reports/routes.txt
```

Expected: HTML + JSON reports in `frontend/lighthouse-reports/mobile` and `frontend/lighthouse-reports/desktop`, plus `summary.json` and `summary.csv`.

- [ ] **Step 5: Stop preview server**

Action: Stop the preview process (Ctrl+C).

---

### Task 4: Review summary and identify shared bottlenecks

**Files:**
- Read: `frontend/lighthouse-reports/summary.json`

- [ ] **Step 1: Print lowest-performing routes (mobile)**

Run:

```bash
node -e "const s=require('./frontend/lighthouse-reports/summary.json'); const rows=Object.entries(s.results.mobile).map(([route,v])=>({route,perf:v.performance,lcp:v.lcp,tbt:v.tbt,cls:v.cls,reqs:v.networkRequests})); rows.sort((a,b)=>a.perf-b.perf); console.table(rows.slice(0,10));"
```

Expected: table of lowest mobile performance routes.

- [ ] **Step 2: Print lowest-performing routes (desktop)**

Run:

```bash
node -e "const s=require('./frontend/lighthouse-reports/summary.json'); const rows=Object.entries(s.results.desktop).map(([route,v])=>({route,perf:v.performance,lcp:v.lcp,tbt:v.tbt,cls:v.cls,reqs:v.networkRequests})); rows.sort((a,b)=>a.perf-b.perf); console.table(rows.slice(0,10));"
```

Expected: table of lowest desktop performance routes.

---

### Task 5: Add shared JS guards in Layout (if TBT/INP are elevated)

**Files:**
- Modify: `frontend/src/layouts/Layout.astro`

- [ ] **Step 1: Apply JS guards for scroll-reveal and parallax**

Replace the current scroll-reveal/parallax setup in `frontend/src/layouts/Layout.astro` with the guarded version below (keep the rest of the file unchanged):

```js
// Scroll reveal — subtle fade-up when elements enter viewport
const revealTargets = document.querySelectorAll('.scroll-reveal');
if (revealTargets.length) {
  const srObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-in', 'fade-in', 'slide-in-from-bottom-4');
        entry.target.style.opacity = '1';
        srObserver.unobserve(entry.target);
      }
    });
  }, { rootMargin: '80px', threshold: 0.05 });

  revealTargets.forEach(el => {
    el.style.opacity = '0';
    srObserver.observe(el);
  });

  if ('requestIdleCallback' in window) {
    requestIdleCallback(() => {
      const srMo = new MutationObserver(() => {
        document.querySelectorAll('.scroll-reveal:not(.animate-in)').forEach(el => {
          el.style.opacity = '0';
          srObserver.observe(el);
        });
      });
      srMo.observe(document.body, { childList: true, subtree: true });
    }, { timeout: 2000 });
  }
}

// Defer non-critical work until idle
if ('requestIdleCallback' in window) {
  requestIdleCallback(() => {
    const parallaxTargets = document.querySelectorAll('.hero-gradient');
    const hasParallaxLayer = document.querySelector('.parallax-layer');
    if (!parallaxTargets.length || !hasParallaxLayer) return;

    let parallaxTicking = false;
    window.addEventListener('scroll', () => {
      if (!parallaxTicking) {
        requestAnimationFrame(() => {
          parallaxTargets.forEach(section => {
            const speed = 0.15;
            const y = section.getBoundingClientRect().top;
            const shapes = section.querySelectorAll('.parallax-bg-shape');
            const dots = section.querySelectorAll('.parallax-dot-grid');
            shapes.forEach(s => { s.style.transform = `translateY(${y * speed}px)`; });
            dots.forEach(d => { d.style.transform = `translateY(${y * speed * 0.5}px)`; });
          });
          parallaxTicking = false;
        });
        parallaxTicking = true;
      }
    }, { passive: true });
  });
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/layouts/Layout.astro
git commit -m "perf: guard scroll reveal and parallax setup"
```

---

### Task 6: Add mobile-only animation reductions (if mobile perf < 90 on most pages)

**Files:**
- Modify: `frontend/src/styles/global.css`

- [ ] **Step 1: Add mobile-only reduction block**

Append near the reduced-motion section in `frontend/src/styles/global.css`:

```css
@media (max-width: 640px) {
  .bubble {
    display: none !important;
  }

  .parallax-layer {
    display: none !important;
  }

  .hero-gradient {
    animation-duration: 18s;
  }
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/styles/global.css
git commit -m "perf: reduce ambient animations on mobile"
```

---

### Task 7: Simplify hero carousel on mobile (if LCP remains high)

**Files:**
- Modify: `frontend/src/styles/global.css`

- [ ] **Step 1: Add mobile carousel simplification**

Append in `frontend/src/styles/global.css` after the hero carousel rules:

```css
@media (max-width: 640px) {
  .hero-carousel-slide {
    animation: none;
    opacity: 0;
  }

  .hero-img-1 {
    opacity: 1;
  }

  .hero-img-2,
  .hero-img-3,
  .hero-img-4,
  .hero-img-5 {
    display: none;
  }
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/styles/global.css
git commit -m "perf: simplify hero carousel on mobile"
```

---

### Task 8: Conditionally inject speculation rules (if network requests are excessive)

**Files:**
- Modify: `frontend/src/layouts/Layout.astro`

- [ ] **Step 1: Replace static speculation rules with desktop-only injection**

Replace the current `<script type="speculationrules">` block with:

```html
<script is:inline>
  (function() {
    if (window.matchMedia('(max-width: 768px)').matches) return;
    if (navigator.connection && navigator.connection.saveData) return;
    const spec = {
      prerender: [{
        where: { href_matches: '/*' },
        eagerness: 'moderate'
      }]
    };
    const el = document.createElement('script');
    el.type = 'speculationrules';
    el.textContent = JSON.stringify(spec);
    document.head.appendChild(el);
  })();
</script>
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/layouts/Layout.astro
git commit -m "perf: inject speculation rules only on desktop"
```

---

### Task 9: Re-run Lighthouse sweep and compare

**Files:**
- Update: `frontend/lighthouse-reports/*`

- [ ] **Step 1: Re-run preview server**

Run (from `frontend/`): `yarn preview --host 0.0.0.0 --port 4321`

- [ ] **Step 2: Re-run sweep**

Run (from repo root):

```bash
node frontend/scripts/lighthouse-sweep.mjs --base-url http://localhost:4321 --routes-file frontend/lighthouse-reports/routes.txt
```

- [ ] **Step 3: Stop preview server**

Action: Stop the preview process (Ctrl+C).

- [ ] **Step 4: Compare summary**

Run:

```bash
node -e "const s=require('./frontend/lighthouse-reports/summary.json'); const rows=Object.entries(s.results.mobile).map(([route,v])=>({route,perf:v.performance,lcp:v.lcp,tbt:v.tbt,cls:v.cls})); rows.sort((a,b)=>a.perf-b.perf); console.table(rows.slice(0,10));"
```

Expected: higher mobile performance scores than the first sweep.

---

### Task 10: Document results

**Files:**
- Update: `docs/superpowers/specs/2026-05-14-lighthouse-sweep-design.md`

- [ ] **Step 1: Add a short results section**

Append the following block at the end of the spec:

```md
## Results
- Sweep date: <YYYY-MM-DD>
- Mobile performance range: <min>-<max>
- Desktop performance range: <min>-<max>
- Shared fixes applied: <list>
```

- [ ] **Step 2: Commit**

```bash
git add docs/superpowers/specs/2026-05-14-lighthouse-sweep-design.md
git commit -m "docs: record lighthouse sweep results"
```

---

## Spec Coverage Check
- Route collection + Lighthouse sweep across all pages: Tasks 1–3
- Cluster findings: Task 4
- Shared fixes: Tasks 5–8
- Re-sweep validation: Task 9
- Document results: Task 10

## Placeholder Scan
- No TODO/TBD text.
- All commands and code blocks are explicit.

## Type Consistency
- `routeToSlug` is exported and tested.
- Summary keys match `performance`, `accessibility`, `bestPractices`, `seo`, `lcp`, `cls`, `tbt`, `inp`, `networkRequests`.
