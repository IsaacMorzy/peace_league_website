# loop-run-log

Per-session ledger written by `loop-budget` (gate 3) at run end. **One JSON line per closure**.

The **authoritative content** lives in `STATE.md` § "Recent loop outcomes" — this sibling file exists so:

1. `AGENTS.md` § Loop Dial Pipeline and `docs/adr/0001-loop-pipeline.md` can reference a real path when they mention `loop-run-log.md` (vs. the header inside `STATE.md`).
2. `loop-budget` can `>>` append a JSON line per closure into this file without mutating `STATE.md` directly, keeping `STATE.md` human-curated and `loop-run-log.md` machine-written.

## Format

```json
{"run_id":"<iso>","pattern":"daily","outcome":"no-op","actions_taken":0,"slur_sha":"<git>","scope":"<ticket-id or none>"}
```

Fields:

| Field | Type | Notes |
|-------|------|-------|
| `run_id` | ISO-8601 timestamp | `2026-07-17T20:30Z`-shaped; matches the loop-budget closure time. |
| `pattern` | enum | One of: `daily`, `adhoc`, `scratch-auto`, `feature-pr`, `human-handoff`. |
| `outcome` | enum | `no-op` (early exit), `closed` (ticket merged/closed), `rejected` (verifier rejected), `escalated` (human handoff required). |
| `actions_taken` | int | The number of file mutations performed this run (not commits — file edits). |
| `slur_sha` | string | First 12 chars of the `git rev-parse HEAD` at run end. Empty when no commit landed this run. |
| `scope` | string | The ticket id this run worked on, or "none". |

## Read pattern

```
tail -n 100 loop-run-log.md | jq -r '.run_id + "\t" + .pattern + "\t" + .outcome'
```

Aggregates cleanly into a daily cycle report without touching git log or `gh` again.
