# STATE

Working state for the loop engineering workflow. Append-only between runs. Read at the start of every loop iteration.

## loop-pause-all

`false` — set to `true` to make `loop-constraints` exit immediately. One line note appended below when flipped.

## Active work

| id | slug | branch | worktree | state | commit | opener | closer |
|----|------|--------|----------|-------|--------|--------|--------|
| —  | —    | —      | —        | —     | —      | —      | —      |
| #46 | terms-design | scratch/terms-design | wt-terms-design | in-review | e597324 | agent | — |
| #45 | privacy-design | feature/design-privacy | wt-privacy-design-2026-07-22 | in-review | b645eea | agent | — |
| #44 | sitemap-design | feature/design-sitemap | wt-sitemap-design-2026-07-22 | in-review | 36e642e | agent | — |
| #43 | 404-design | feature/design-404 | wt-404-design-2026-07-22 | in-review | 63fdeb5 | agent | — |
| —  | awards-api-tests | scratch/awards-api-tests | wt-awards-api-tests | in-review | d70ba94 | agent | — |

States: `claimed`, `in-progress`, `in-review`, `closed`. Open a row when a `wayfinder:grilling` / `wayfinder:task` ticket is assigned.

## Closed this period

| id | slug | summary |
|----|------|---------|
| —  | nomination-photo-fix | Astro /awards/nominate was returning "Submission failed: Failed to submit nomination." Root cause: Award Nominee DocType declares `photo` as `reqd: 1` so a doc without a saved file URL fails validation on insert. Fix in commit **b8abaa6**: insert with `nominee.flags.ignore_mandatory=True` inside `try/finally` (global flag never leaks), then `save_file()` to the real generated docname (File referential integrity), then `nominee.db_set("photo", file_url)` (skips full re-validation). Plus 5MB backend size guard and `delete_doc` cleanup if the file attach fails. Added `TestHttpNominationSubmission` (2 HTTP regression-guard tests via urllib against live bench, with `tearDownClass` deleting residual nominees and `BENCH_URL` env var for CI). 17/17 backend tests pass. Mirror migration to drop the workaround tracked in GH #126. |
| #66 | awards-feature | Awards feature: 3 DocTypes (Category/Nominee/Vote) + api_awards.py + 4 frontend pages wired to live API + 55 fixture categories. PR #68 merged. Deployed to production. |
| #61 | privacy-jsonld-drift | Fixed: single source for 'Last updated' by deriving from JSON-LD dateModified; replaced Astro.url.origin with canonical orgUrl. |
| #60 | careers-jsonld-drift | Fixed JobPosting JSON-LD to use https://peaceleagueafrica.org instead of Astro.url.origin. |

Move row here when the worktree closes, the PR merges, or the ticket is `wontfix`.
## Watchlist

Lower-priority items the loop monitors but does not act on without an external signal. Each entry is one line:

`<iso> <surface>: <signal>`.

| since | surface | signal |
|-------|---------|--------|
| 2026-07-23Z | bench | #126 — migrate Award Nominee.photo to `reqd: 0`, then delete the `ignore_mandatory` + `db_set` workaround in `create_nomination()`. Land after one week of production submission traffic. |
| 2026-07-23Z | tests | Add BENCH_BYPASS_TURNSTILE=1 gated happy-path HTTP test for `create_nomination()`. Currently the smoke tests only guard against the historical regression string; full happy-path coverage requires a Turnstile test token or empty site config. |

## Recent loop outcomes

Mirror of `loop-run-log.jsonl`. The machine-written ledger is the authoritative source — this section is the human-curated copy. Append one line per `loop-budget` closure. Schema lives in `loop-run-log.jsonl` (six fields: `run_id` · `pattern` · `outcome` · `actions_taken` · `slur_sha` · `scope`); example:

```
{"run_id":"<iso>","pattern":"daily","outcome":"no-op","actions_taken":0,"slur_sha":"<git>","scope":"<ticket-id or none>"}
```

## Entries

```
{"run_id":"2026-07-17T20:35Z","pattern":"adhoc","outcome":"closed","actions_taken":2,"slur_sha":"32a19a1","scope":"none"}
{"run_id":"2026-07-23T19:45Z","pattern":"adhoc","outcome":"closed","actions_taken":2,"slur_sha":"b8abaa6","scope":"nomination-photo-fix"}
```
[ mirror of `loop-run-log.jsonl` first entry — corresponds to commit 32a19a1 · "docs(agents): tighten dial gate-skip rule + loop-run-log sibling" — actions_taken: 2 reflects *that single run's* file mutations: AGENTS.md skip-rule clarification + `loop-run-log.jsonl` creation. ]

## Notes / kill-switch log

Append a single line when:
- `loop-pause-all` flips,
- a denylist path was touched (or an attempt was blocked),
- escalation to a human was required,
- a safety measure was disabled (should be never).

- 2026-07-22Z push-blocked: user asked to push 26 unpushed local `main` commits; BLOCKED for 3 reasons — (1) `gh auth status` → “Timeout trying to log in to github.com” (push auth unreliable), (2) `origin` and `upstream` URLs are identical (non-standard setup — pushing either lands in the canonical repo), (3) “26 ahead” is from cached remote refs (no fresh `git fetch` this session); denylist diff scan was clean. Awaiting human verify + fresh fetch before retry.
- 2026-07-22T15:50Z push-closed: after a fresh `git fetch --prune origin upstream`, real divergence collapsed from 26 to 1 — `upstream/main` moved from cached `46ad3b3` → live `3d74a80`. `GIT_TERMINAL_PROMPT=0 git push upstream main` then fast-forwarded `3d74a80..750bb9e` (the `merge: sync with origin/main (1-commit catchup) [loop-budget]` commit). Post-push `rev-parse` shows local HEAD === `upstream/main` = `750bb9e`. Root-cause on the cache: the local checkout had not fetched since upstream moved; the stale tracking ref inflated the ahead-count. Auth path (`/usr/bin/gh auth git-credential`) is functional — the earlier `gh auth status` “Timeout” was a status-check hang, not a credential failure. Note: `origin` and `upstream` URLs are identical (`https://github.com/IsaacMorzy/peace_league_website.git`) — pushing to either alias lands in the canonical repo; consider pruning one remote to break the ambiguity.
- 2026-07-22T16:40Z merge-gate-loosened: loop-constraints.md updated — agent-initiated merges to `main` now permitted when loop-verifier + reviewer pass and no automerge veto tripped. User explicitly requested loosening.
- 2026-07-22T16:45Z awards-deployed: PR #68 merged to main. bench migrate succeeded — Award Category/Nominee/Vote DocTypes created, 55 categories loaded from fixtures. Frontend built (109 pages) + deployed to astro_pages/. Nginx reloaded, gunicorn restarted. API confirmed: get_categories returns 55 active categories. Production pages /awards, /awards/nominate, /awards/results, /awards/category/[slug] all return HTTP 200. 5 post-merge deployment fixes committed directly to main (doctype module path, patches.txt format, fixture name/is_active fields, patch idempotency).
- 2026-07-23T19:45Z nomination-photo-fix: commit b8abaa6 lands on upstream/main. Fix chain: `nominee.flags.ignore_mandatory` inside try/finally → `save_file()` to real docname → `nominee.db_set("photo", file_url)` → orphan `delete_doc` on file failure. 5MB backend guard via `photo.read()` + `seek(0)`. 17/17 backend tests pass (15 unit + 2 HTTP regression guard). Curl proof: error changed from "Value missing for Award Nominee: Photo" to "Verification failed. Please refresh and try again." — the photo bug path is dead. Migration to drop the workaround tracked in #126. Frontend rebuilt (144 pages) + deployed to dev site.
