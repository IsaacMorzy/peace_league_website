# Lighthouse Baseline — 2026-07-27

## What shipped in the infra-fixes commit

- `frontend/scripts/routes.txt` — 10 top routes that **actually exist** in `peace_league_website/public/astro_pages/`. No phantom 404 routes.
- `frontend/scripts/serve-dist.mjs` — fixed the stale `distDir = path.resolve(__dirname, '..', 'dist')` (which resolved to a nonexistent `frontend/dist/`) to default to the canonical Frappe-bench outDir `peace_league_website/public/astro_pages`. `LIGHTHOUSE_DIST=...` env override preserved.
- `frontend/scripts/install-chromium.sh` — one-time chromium installer that runs `pnpm exec playwright install chromium` (~150MB).
- `frontend/package.json` — three new hooks: `audit:lighthouse`, `audit:playwright`, `audit:aria-closures`.

## Run sequence (any developer / CI)

```
# Once per machine:
bash frontend/scripts/install-chromium.sh

# In one terminal — serves the actual Frappe-bench outDir on 4321:
node frontend/scripts/serve-dist.mjs 4321

# In another terminal:
cd frontend
pnpm audit:lighthouse
# -> writes frontend/lighthouse-reports/{mobile,desktop}/*.report.html + summary.csv + summary.json
# -> exits 0 (clean) or non-zero (any route perf <95 or accessibility <90)
```

## Where Chrome comes from

`lighthouse-sweep.mjs` uses spawnSync against the `lighthouse` CLI binary. Lighthouse auto-discovers Chrome via `CHROME_PATH` env or by launching a fresh headless instance.

Playwright's bundled Chromium lives at `~/.cache/ms-playwright/chromium-1223/` (per `pnpm exec playwright install --dry-run chromium`). Set `CHROME_PATH` to the binary inside that directory when running the sweep:

```
export CHROME_PATH="$HOME/.cache/ms-playwright/chromium-1223/chrome-linux/chrome"
pnpm audit:lighthouse
```

## Host-vs-repo MCP split (be honest)

The user asked for "install Lighthouse MCP + activate". MCP servers run inside the host CLI (Claude Code / Cursor / Codex), not in this repo. What shipped in the repo:

- `lighthouse@13.3.0` + `playwright@1.60.0` in `package.json` devDeps.
- The wrapper scripts (`lighthouse-sweep.mjs`, `lh-sweep.mjs`, `playwright-sweep.mjs`) so the user can drive Lighthouse + Playwright from CLI.
- `install-chromium.sh` so chromium lands once on the host.

What the user activates in their host CLI (NOT in this repo):

```
# Playwright MCP — Microsoft official:
claude mcp add playwright npx @playwright/mcp@latest

# Lighthouse MCP — there's no canonical @lighthouse/mcp server.
# Best alternative is `lhci` (web dashboard) or drive Lighthouse through `--port` from Playwright MCP once chromium is up.
```

If the user wants a real Lighthouse MCP, today's options are:
1. Use Lighthouse via Playwright MCP (drive the lighthouse CLI from a Playwright session).
2. Use `lhci` (Lighthouse CI) with a small server in front.

Both require the host to wire them — they're not repo-installable.

## Honest expectations for the first sweep

The 95% Lighthouse target on all 10 routes is **unlikely on the first sweep**. Realistic baseline numbers:

| Category | Expected first-sweep | Why |
|----------|---------------------|-----|
| Performance | 60-80% | Hero image is from images.unsplash.com (third-party CDN); Inter font may be Google Fonts; `lighthouse` uses `simulate` throttling which still penalises external resources. |
| Accessibility | 95-100% | JSON-LD + aria-labelledby (7/8 on /index) + min-h-[44px] buttons + role=progressbar already present. |
| Best Practices | 85-95% | HTTPS-only via nginx enforce; HSTS preload; CSP needs review. |
| SEO | 95-100% | JSON-LD NGO schema on /index; canonical URLs; robots; OG tags. |

To reach 95% on every route, the browser/network frontier needs:
1. Self-host the hero image (one-time copy + responsive srcset).
2. Self-host Inter font + `font-display: swap` + preload `<link rel=preload as=font>`.
3. Code-split below-fold JS (currently single bundle in `<script type=module">`).
4. Remove `images.unsplash.com` and any other third-party CDN references.

These are 4 separate workstreams and each is a half-day minimum. The path to 95% performance is real but not instant.

## Audit gates in place

- `pnpm audit:aria-closures` — checks that every content page has `<main`, `</main>`, `<Layout`, `</Layout>` matched. ✓ exits clean.
- `pnpm audit:lighthouse` — runs Lighthouse + parses the summary.csv + exits non-zero on any `performance < 95` or `accessibility < 90`.
- `pnpm audit:playwright` — runs the smoke checks (HTTP 200 across 17 routes + mobile-menu + desktop-nav assertions).
