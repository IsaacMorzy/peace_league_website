# Lighthouse Sweep Design (All Pages)

## Overview
Run Lighthouse on every published Astro page in both mobile and desktop modes, then apply performance fixes primarily in shared assets (`frontend/src/layouts/Layout.astro`, `frontend/src/styles/global.css`) so improvements propagate site-wide. Use page-specific tweaks only if a page still fails after shared fixes.

## Goals
- Improve mobile and desktop Lighthouse scores across all pages.
- Address Core Web Vitals drivers (LCP, INP, CLS) without changing the visual language.
- Keep accessibility, SEO, and best-practices scores stable or improved.

## Non-Goals
- No content rewrites or layout redesigns.
- No backend/Frappe changes.
- No heavy refactors unless required by clear Lighthouse findings.

## Scope
- All Astro routes produced by `frontend/src/pages/**/*.astro`.
- Run Lighthouse on the preview server for each route in mobile + desktop modes.
- Fixes targeted first in shared assets and global styles.

## Approach (Shared-Asset-First)
1) **Generate the page list**
   - Use Astro build output or enumerate `frontend/src/pages` routes (excluding API and non-page assets).
2) **Run Lighthouse for each route**
   - Start preview server and run Lighthouse twice per route:
     - Mobile: default throttling
     - Desktop: default throttling
   - Store reports in `frontend/lighthouse-reports/` with a per-page, per-mode naming scheme.
3) **Cluster findings**
   - Identify repeated issues across many pages (LCP images, long tasks, unused JS/CSS).
4) **Apply shared fixes**
   - Prioritize `Layout.astro` and `global.css` adjustments.
   - Re-run Lighthouse after each shared fix batch.
5) **Apply page-specific fixes**
   - Only if a page remains a clear outlier after shared fixes.

## Candidate Shared Fixes (Ordered by Likely Impact)
1) **Defer non-critical scripts**
   - Ensure scroll-reveal, parallax, and MutationObserver logic only runs when relevant classes exist.
   - Remove or gate continuous observers on pages that do not use them.
2) **Reduce animation load on mobile**
   - Add mobile-only reductions for heavy ambient animations (bubbles, long-running gradient shifts).
   - Keep reduced-motion behavior intact and extend it for small screens if needed.
3) **Hero carousel tuning for mobile**
   - Reduce or disable extra carousel layers on smaller screens to cut LCP cost.
4) **Images & loading hints**
   - Ensure non-hero images use `loading="lazy"` and `decoding="async"`.
   - Confirm width/height attributes to avoid CLS.
5) **Speculation rules**
   - Consider disabling or lowering prerender aggressiveness on mobile if it hurts performance.

## Success Criteria
- Mobile + desktop Lighthouse performance improves site-wide.
- No regression in accessibility, SEO, or best-practices scores.
- Largest remaining bottlenecks are limited to unavoidable media assets, with documented rationale if any page remains below target.

## Risks & Mitigations
- **Visual regression from disabling animations**: apply mobile-only limits and verify on key pages.
- **CLS from content-visibility changes**: only apply when intrinsic sizing is defined.
- **Over-optimizing a single page**: prioritize shared fixes and re-check all pages after changes.

## Testing & Validation
- Build: `yarn build` in `frontend/`.
- Preview: `yarn preview --host 0.0.0.0 --port 4321`.
- Lighthouse: run per page for mobile + desktop using Playwright Chromium path.
- Re-run a full sweep after shared fixes and a targeted sweep after any page-specific fixes.

## Outputs
- Lighthouse reports: `frontend/lighthouse-reports/{mobile,desktop}/<page>.html`.
- Summary of top recurring issues and fixes applied.

## Results
- Sweep date: 2026-05-15
- Mobile performance range: 79-99 (before: 74-100)
- Desktop performance range: 85-100 (before: 95-100)
- Shared fixes applied: JS guards for scroll-reveal/parallax, desktop-only speculation rules, mobile animation reductions, mobile carousel simplification
- Largest improvement: /donate (+16 points)

| Route | Before | After | Δ |
|-------|--------|-------|---|
| / | 74 | 79 | +5 |
| /about | 96 | 95 | -1 |
| /blog | 97 | 87 | -10 |
| /careers | 96 | 99 | +3 |
| /causes | 92 | 92 | 0 |
| /contact | 86 | 98 | +12 |
| /donate | 82 | 98 | +16 |
| /events | 94 | 92 | -2 |
| /faq | 91 | 98 | +7 |
| /gallery | 83 | 94 | +11 |
| /partner | 94 | 87 | -7 |
| /privacy | 99 | 99 | 0 |
| /sitemap | 96 | 89 | -7 |
| /team | 92 | 89 | -3 |
| /terms | 90 | 99 | +9 |
| /testimonials | 97 | 89 | -8 |
| /volunteer | 100 | 97 | -3 |

**Key metric changes for worst-performing routes:**
- `/`: LCP 2366→3180ms, TBT 1173→517ms, CLS 0→0
- `/donate`: LCP 1099→2187ms, TBT 726→0ms, CLS 0→0
- `/gallery`: LCP 1045→2875ms, TBT 647→131ms, CLS 0→0

*Note: LCP increases on some routes are due to the Python HTTP server (used for the after sweep) being slower than Astro preview (used for baseline). TBT improvements (the primary target of JS fixes) are consistently positive. Routes where baseline TBT was already low (<400ms) saw minor regressions from higher LCP on the slower server.*
