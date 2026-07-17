# Stage 4 Bench Pre-Merge Gate

> Source: IsaacMorzy/peace-league-website-plan/AGENTS.md § Stage 4 - Gate. Mirror for bench-root-relative ops. **CANONICAL** on the plan-repo; this file documents the local operational checklist.

This gate must pass (paths are bench-root-relative, `$BENCH = /home/crowd/Documents/backend/frappe-bench/`):

* `bash -n apps/peace_league_website/frontend/deploy.sh` parses.
* `sudo nginx -t` passes.
* `scripts/smoke-bench.sh` reports `RESULT: OK`.
* `grep -rn 'peaceleagueafrica\.com' apps/peace_league_website/frontend/src` is empty.
* `grep -n crowduser apps/peace_league_website/frontend/deploy.sh` is empty.
* `stat -c '%a %U:%G' /etc/sudoers.d/peace-league-deploy` reports `0440 root:root` and `sudo visudo -c -f /etc/sudoers.d/peace-league-deploy` is clean.

## Distinct from the agent dial

This is the **bench pre-merge gate** (Stage 4 of the Matt Pocock x Loop-engineering hybrid). Distinct from Cobus Greyling's `loop-gate check` (a per-iteration control signal in `$PLAN/LOOP.md` running at the loop-engineering control layer) — they share a name, but operate at different layers. Both run, at different layers.

The agent dial in `AGENTS.md` § Loop Dial Pipeline is the **third, smallest** control layer (the in-process make/check loop inside one ticket). The three layers compose:

| Layer | Skill | Lives in | Run when |
|------|-------|----------|----------|
| In-process dial  | `loop-constraints` · `loop-triage` · `loop-budget` · `tdd` · `loop-verifier` · reviews | bench repo (`AGENTS.md`, `loop-constraints.md`) | every run / every diff |
| Loop-engineering control  | `loop-gate` / `loop-context` / `loop-audit` | plan repo (`$PLAN/LOOP.md`) | per-daily triage cycle |
| Bench pre-merge  | scripts (`smoke-bench.sh`, `bash -n deploy.sh`), `sudo nginx -t` | bench infra | each ticket pre-merge |
