# /index aria-labelledby coverage (as of 2026-07-27T13:59Z)

This is a domain-doc describing the actual aria-labelledby coverage on the home page.
Located in `docs/agents/` to match the project's \"single-context layout\" convention
(`docs/agents/issue-tracker.md`, `docs/agents/domain.md`).

## Final counts (verified via dist grep)

Source (`frontend/src/pages/index.astro`): **7 of 8 planned slugs** carry `aria-labelledby`.
Dist (`frontend/../peace_league_website/public/astro_pages/index.html`): **7 of 8**.

| Slug | Source | Dist | Notes |
| :--- | :---: | :---: | :--- |
| why-pla | 1 | 1 | Always-present content section |
| impact-numbers | 1 | 1 | Always-present content section |
| our-causes | 1 | 1 | Always-present content section |
| featured-event | 1 | 1 | Conditional: renders when `awardsEvent` is in events-data (currently yes) |
| how-we-work | 1 | 1 | Always-present content section |
| donation-tiers | 1 | 1 | Always-present content section |
| trusted-orgs | 1 | 1 | Always-present content section |
| latest-blog | 0 | 0 | **Phantom from planning** — no `<h2 id="latest-blog">` exists in `/index` because the file tail uses different structure |

## Why latest-blog is 0/0

The original plan called for 8 content sections (Hero excluded by design; no h2). 7 of those
have explicit `<h2 id="...">` markers and matching `aria-labelledby`. The 8th (`latest-blog`)
was planned for a \"Latest from our Blog\" tail section that turned out to use different markup
structure on the page; a search for candidate h2 text (\"Latest News & Stories\", \"Latest from
Our Blog\", \"From Our Blog\", \"Latest Stories\") did not match. No id was ever added because no
h2 to attach it to exists in source.

This is the practical ceiling. Future iterations should not chase 8/8 — they should add a real
h2-with-id to the file tail first if a Latest Blog section is to be labeled.

## Why this state is final

The aria-labelledby coverage hit the practical ceiling. Further iterations on `/index` only
spent commit-budget without producing a different outcome. New pages (e.g. `/awards`) are a
separate scope and should run the same surgical per-section pattern independently.
