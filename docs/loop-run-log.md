# loop-run-log — schema, conventions, parser check

This file is the **schema/docs** companion to the JSONL ledger at `loop-run-log.jsonl`. The JSONL file at the repo root is the **machine-written** authoritative source; this doc explains what each line means, how the file is read, and what the parser check looks like.

For workflow-level context: [`AGENTS.md` § Loop Dial Pipeline](../AGENTS.md) (gate 3 — `loop-budget`); architecture rationale in [`docs/adr/0001-loop-pipeline.md`](adr/0001-loop-pipeline.md); mirror in [`STATE.md` § Recent loop outcomes](../STATE.md).

## Format

One JSON object per line in `loop-run-log.jsonl`. **Strict JSONL — no prose, no comments, no fenced blocks.**

```json
{"run_id":"<iso>","pattern":"daily","outcome":"no-op","actions_taken":0,"slur_sha":"<git>","scope":"<ticket-id or none>"}
```

Fields:

| Field | Type | Notes |
|-------|------|-------|
| `run_id` | ISO-8601 timestamp | `2026-07-17T20:30Z`-shaped; matches the `loop-budget` closure time. |
| `pattern` | enum | One of: `daily`, `adhoc`, `scratch-auto`, `feature-pr`, `human-handoff`. |
| `outcome` | enum | `no-op` (early exit), `closed` (ticket merged/closed), `rejected` (verifier rejected), `escalated` (human handoff required). |
| `actions_taken` | int | The number of **file mutations** performed this **single run** (not commits — file edits). **Per-run, not cumulative** — reset between `loop-budget` closures. Computed by `loop-budget` from `git diff --stat` at run end. |
| `slur_sha` | string | First 12 chars of the `git rev-parse HEAD` at run end. Empty when no commit landed this run. |
| `scope` | string | The ticket id this run worked on, or `"none"`. |

## Append-only conventions

- **Do not** manually edit entries. New entries = append.
- **Do not** reformat. Strict JSONL — one line per closure, no pretty-printing, no trailing commas.
- **Commit separately** with a clear subject (`chore(loop): append run-log`), not bundled with feature or fix work.
- After ~50 lines, rotate older entries to `loop-run-log.archive/YYYY-MM.jsonl` if performance becomes a concern.

## Parser check (gate 5 — `loop-verifier`)

`loop-verifier` (gate 5 of the dial — the **maker/checker** split, not gate 6's review pair) gates the run on JSONL parseability. The mechanical check is:

```bash
jq -c . loop-run-log.jsonl > /dev/null && echo "ledger parses cleanly"
```

If this exits non-zero, the ledger is corrupted and the run is **REJECTED** until repaired.

## Read pattern

```bash
tail -n 100 loop-run-log.jsonl | jq -r '.run_id + "\t" + .pattern + "\t" + .outcome'
```

Aggregates cleanly into a daily cycle report without touching git log or `gh` again.

## Mirror

`STATE.md` § Recent loop outcomes / Entries is the **human-curated mirror**. Per the contract, the JSONL file is the authoritative machine source; STATE.md entries are appended in lockstep with `[corresponds to]` bullets for human searchability — the JSONL line in STATE.md carries the same fields, the [corresponds to] bullet is a human-only attachment.

## Migration note

The JSONL file at this repo's root is `loop-run-log.jsonl`. Earlier contract text referenced `loop-run-log.md` (a prose file containing the schema inline). The split was a fix for review-nits on commit `a4d4f98`: `jq -c .` on the old file failed because it mixed JSON with markdown prose. The split was committed under `refactor(loops): extract loop-run-log schema to docs, migrate ledger to jsonl`.
