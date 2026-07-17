# ADR 0002 — Cross-repo Plan-Substrate Sync on peace_league_website

**Status:** Accepted · 2026-07-17 · mirrors plan-repo canonical
**Deciders:** agent (per `AGENTS.md` § Persona) + repo owner
**Relates:** plan-repo `IsaacMorzy/peace-league-website-plan` (CANONICAL); main repo `IsaacMorzy/peace_league_website` (BENCH substrate); AGENTS.md ADR 0001 (`docs/adr/0001-loop-pipeline.md`).

## Context

The owner maintains the planning substrate in a separate, **private** repo at `IsaacMorzy/peace-league-website-plan`. The plan repo's own `AGENTS.md` declares it **canonical** for peace_league_website planning; GitHub issues filed on the plan repo mirror the local decision files under `docs/wayfinder/decisions/<NN>-*.md`.

The bench repo (`peace_league_website`) previously had:
- its own `AGENTS.md` (Workflow v2 + Loop Dial Pipeline + Commit-Message Convention),
- its own wayfinder map (issue #1) + 3 child tickets,
- no awareness of the plan-repo's 7 tickets / 5 Standing Orders / 4 Stage 4 benchmarks.

Without a sync step, an agent loading `peace_league_website/AGENTS.md` would not recover:
- the **bench pre-merge gate** (plan-repo Stage 4: `bash -n deploy.sh`, `sudo nginx -t`, `scripts/smoke-bench.sh`, `peaceleagueafrica.com` grep gate, sudoers mode 0440 root:root check),
- the **8 Standing Orders** (`peaceleagueafrica.org` canonical, `.com` forbidden, `peace_league-<feature>` scoped sudoers rule, etc.),
- the **ticket-numbering scheme** on the plan-repo side,
- the **drift rule** linking `docs/wayfinder/decisions/` files to plan-repo issue bodies.

## Decision

Promote this turn's sync to **3 handoffs**, two of which live in `peace_league_website/docs/plan-substrate/`, None of which are allowed to mutate the canonical plan repo (the agent only READS from the plan repo; a human mutates it):

1. **`docs/plan-substrate/STANDING-ORDERS.md`** — verbatim mirror of plan-repo § Standing orders 1-8. Read-only, pointer-stamped, say-the-source at the top.
2. **`docs/plan-substrate/STAGE-4-GATE.md`** — bench pre-merge gate as a checklist, with a layered-control table positioning the gate against the in-process dial (ADR 0001) and the loop-engineering control layer (plan-repo `LOOP.md`).
3. **`docs/plan-substrate/MAP-DRIFT-RULE.md`** — the `gh issue edit <N> --body-file` pattern, extended to the main repo with a "cross-link" methodology for tickets that exist on both trackers.

Plus, the GitHub-side counterpart on `peace_league_website`:
- **Project v2** named `peace_league_website Roadmap` (bound to the main repo, owner: IsaacMorzy) — populated from all open issues on the main repo at sync time.
- **7 cross-link issues** labelled `wayfinder:task-sync` mirroring the plan-repo tickets #2-#8 (`Rebuild Astro Dist for .org Domain`, `Preflight checks in deploy.sh`, `CSP Headers on apex-443`, `Archive Tailnet Paths (/admin, sensitive /api)`, `Smoke Test via Peer Node`, `Real MCP Server & libredesk wiring`, `M-Pesa Webhook hardening + fail2ban rules`).
- **Update of wayfinder map #1** on the main repo: body appended with the dual-tracker methodology pointer.

## Consequences

**Positive**

- An agent loading `peace_league_website/AGENTS.md` now recovers Stage 4 + Standing Orders + drift rule via a single `docs/plan-substrate/` directory pointer.
- The main repo's GitHub Project gives the owner a single pane-of-glass: open issues here + cross-links to plan-repo + the closed loop history.
- The dual-tracker methodology is **non-destructive**: the plan repo remains canonical, this is a read-only mirror on the bench side.

**Negative / risks**

- **Mirrors can drift.** Stage 5 of the loop's sync discipline applies to the dual tracker too. The drift rule in `docs/plan-substrate/MAP-DRIFT-RULE.md` documents the `gh issue edit` pattern; manual sync is required when a plan-repo decision file changes.
- **Two sources of truth.** Local agents must remember "plan repo is canonical for the 7 tickets; main repo is canonical for the dial + workflow + ui-skills tickets". Confusion risk on cross-tracker tickets; the dual-tracker methodology in MAP-DRIFT-RULE.md is the antidote.
- **Working-tree state.** This commit lands via a worktree under `scratch/plan-sync-2026-07-17` per `AGENTS.md` § Worktree Convention (one worktree per ticket). Dial step 2 instructions hold: never work in `main` directly.

## Alternatives considered

- **Replace the local `AGENTS.md` with the plan-repo's `AGENTS.md` verbatim.** Rejected — the locally-built dial (ADR 0001, workflow v2) is more developed than the plan-repo's; the plan repo's § Standing orders is the missing piece locally, not the converse.
- **Hardlink / symlink the plan repo's files into the bench repo.** Rejected — the plan repo is private, the bench repo is public; a hardlink leaks plan-repo content into the public commit history. A copy-with-pointer is the right move.
- **Skip the Project v2 step.** Rejected — the owner's explicit ask was "create issues and project". Project v2 + cross-link issues are the smallest-pieces answer.

## Forward work

- After roughly 7 working sessions, review whether the dual-tracker methodology was tolerated by the bench workflow or whether tickets consistently drift to one side. If drift becomes the norm, propose moving the canonical ticket tracker from the plan repo to the main repo (decision would land in ADR 0003).
- If `npx @cobusgreyling/loop-{sync,audit}` are installed locally, replace the manual `gh issue edit <N> --body-file` pattern with a Stage 5 hook that runs `loop-sync` automatically.
