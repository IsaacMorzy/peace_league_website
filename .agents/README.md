# .agents/

Per-repo AI agent configuration and audit trail for `peace_league_website`.

## Where things live

| File | Loaded by | Purpose |
|------|-----------|---------|
| `../AGENTS.md` | the agent (start of every session) | the per-repo contract — persona, workflow, project rules, do/don't. |
| `../loop-constraints.md` | `loop-constraints` skill | binding rules: denylist paths, push/merge policy, test discipline, escalation. |
| `../STATE.md` | `loop-triage`, `loop-budget` | loop state — kill switches, active work, watchlist, recent outcomes. |
| `../loop-budget.md` | `loop-budget` skill | daily token caps per pattern, kill switches. |
| `../loop-run-log.md` | `loop-budget` skill | append-only log of loop outcomes. |
| `../docs/adr/README.md` | human reviewers | ADR convention. Open one when a non-trivial decision lands. |
| `../docs/audit-YYYY-MM-DD.md` | `ponytail-audit` skill output | one-shot audit reports. Most recent: `../docs/audit-2026-07-17.md`. |

## Skills (stubs)

Byte-identical copies of `~/.agents/skills/<name>/SKILL.md`. Pick whichever is in scope at skill-load time.

- `ponytail` — lazy senior dev persona + ladder of laziness.
- `ponytail-review` — diff-scoped over-engineering scan (tags: `delete:` / `stdlib:` / `native:` / `yagni:` / `shrink:`).
- `ponytail-audit` — repo-wide over-engineering audit (one-shot, lists findings, applies nothing). Output lands in `../docs/audit-YYYY-MM-DD.md`.
- `ponytail-debt` — harvest `# ponytail:` comments into a debt ledger.
- `setup-matt-pocock-skills` — wire issue tracker, triage labels, domain docs.
- `tdd` / `test-driven-development` — red → green vertical-slice loop, behavior-not-implementation tests, agreed seams before any test.
- `loop-constraints` — enforce `../loop-constraints.md` at startup.
- `loop-triage` — rank CI failures / issues.
- `loop-budget` — token-spend guard, early exit when nothing actionable.
- `loop-verifier` — independent maker/checker split: reject unless scope + tests pass.

## Audit trail

`ponytail-audit` outputs land here:

- `docs/audit-2026-07-17.md` — initial whole-repo scan. Found 2 candidates (`utils/seed_data.py` passthrough, `api.py::generate_test_data` wrapper); both deferred because both require either a multi-file refactor or an API rename, neither of which was provably safe within the run.

Re-run after the next 5+ commits land; the report naming convention is `docs/audit-YYYY-MM-DD.md`.


## UI Skills (external family)

From `npx ui-skills@0.2.3` (ibelick / motion-primitives.com). Installed in this project under `.agents/skills/<slug>/SKILL.md` and globally at `~/.agents/skills/<slug>/SKILL.md`. Byte-equivalent to upstream.

- `ui-skills-root` — meta-skill: `npx ui-skills start` routes the agent to the smallest useful UI skill set.
- `baseline-ui` — slop-prevention baseline (Tailwind defaults, motion/react, `cn` utility, accessibility primitives).
- `fixing-accessibility` — WCAG / ARIA / keyboard / focus / form errors; trigger when adding interactive controls.
- `fixing-metadata` — title / OG / Twitter / canonical / favicon / JSON-LD / robots; trigger on new pages or metadata changes.
- `fixing-motion-performance` — animation perf (layout thrashing, compositor props, scroll-linked motion, blur); trigger on jank.

Project-specific overrides (no React islands assumed; use Astro-native HTML + Tailwind for `baseline-ui`) live in `../DESIGN.md` § “Design Skills Routing”. When the upstream skill prescribes `motion/react`, Base UI, or React Aria, the override is “use Astro-native HTML + native CSS first; install only when migration is justified” (Ponytail ladder).

## Conventions

- `# ponytail: <ceiling>, <upgrade path>` — mandatory comment on deliberate simplifications. Missing upgrade path = rot risk; flagged by `ponytail-debt`.
- Walk every change through `ponytail-review`. Then `code-reviewer-minimax-m3` in parallel. Both runs are mandatory before asking to ship.
- One focused diff per run. Multiple steps produce one PR, not multiple PRs.
