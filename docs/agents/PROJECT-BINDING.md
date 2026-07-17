# Project v2 Binding — Manual UI Recipe

This document captures the binding layer between **peace_league_website** and the
GitHub Projects v2 board `peace_league_website Roadmap` (PVT `PVT_kwDOC-C3-s4AkgS_zgA0WkU`).

## What we have (text-architectural + label-level bind)

| Layer | How it binds | Where it lives |
|-------|---|---|
| README pointer | `## Project Board` section links the project's URL | `README.md` on `main` |
| Issue cross-link label | `wayfinder:task-sync` mirrors a ticket's plan-repo counterpart | `peace_league_website` label inventory |
| State mirror row | Each UI-skill batch run appends one row keyed by `slur_sha` | `STATE.md` § Recent loop outcomes |
| Run-log ledger | Machine-written JSONL is the canonical, the markdown is the human copy | `loop-run-log.jsonl` |

A future agent can grep for `rAGPeaceleagueAfricaVisionRoadmap` (read README) or
`PVT_kwDOC-C3` and reconstruct the binding from any of these layers.

## What we LACK — GitHub Projects V2 README / description

GitHub Projects (V2) does **not** currently expose its rich-text README or
description through the GraphQL or REST API:

- `ProjectV2` has no `description` field.
- `updateProjectV2(input)` accepts only `title`, `shortDescription`, and `public`.
- `gh project edit` exposes only `--title` / `--public` / `--private`.
- No public `updateProjectV2Readme` mutation exists (verified against the
  schema on 2026-07-17 per `docs/reference/projectsv2-schema.md` notes).

Therefore the **human-readable bind** on the Projects board itself must be set
manually through the GitHub UI. The repo + labels + STATE + run-log form the
text-architectural bind that an agent can scrape; the Projects board README is
the human-facing bind that only the owner can edit.

## Manual bind recipe — 4 steps, one-time, ~3 minutes

1. Open the board:
   `https://github.com/users/IsaacMorzy/projects/PVT_kwDOC-C3-s4AkgS_zgA0WkU`
2. Click the `...` (menu) icon in the top right of the project page.
3. Select **Edit README**.
4. Paste the block below into the README editor and click **Save**.

```markdown
## Bound repos
- Primary: `IsaacMorzy/peace_league_website` — code, AGENTS.md, DESIGN.md, loop log.
- Plan-repo: `IsaacMorzy/peace-league-website-plan` — canonical wayfinder map,
  ADRs, and decision ledger per `docs/wayfinder/decisions/`.

## Sync convention
- Issues on `peace_league_website` carry `wayfinder:task-sync` when they
  mirror a plan-repo ticket.
- Run-log: every batch run on the worktree branch appends one row to
  `loop-run-log.jsonl` on that branch + mirrors it into `STATE.md` on merge.
- See `docs/plan-substrate/MAP-DRIFT-RULE.md` for cross-repo drift handling.

## Audit trail
- `STATE.md` § Closed this period mirrors PRs that closed real chapters.
- `loop-run-log.jsonl` is the machine truth; `STATE.md` is the human copy.
```

## Why this lives in `docs/agents/`

So the agent can grep `docs/agents/PROJECT-BINDING.md` and re-derive the
shortcuts the human must run. If a future GitHub release exposes
`updateProjectV2Readme`, this doc will be amended to include the mutation
recipe and the manual steps become a no-op fallback only.
