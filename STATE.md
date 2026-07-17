# STATE

Working state for the loop engineering workflow. Append-only between runs. Read at the start of every loop iteration.

## loop-pause-all

`false` — set to `true` to make `loop-constraints` exit immediately. One line note appended below when flipped.

## Active work

| id | slug | branch | worktree | state | commit | opener | closer |
|----|------|--------|----------|-------|--------|--------|--------|
| —  | —    | —      | —        | —     | —      | —      | —      |

States: `claimed`, `in-progress`, `in-review`, `closed`. Open a row when a `wayfinder:grilling` / `wayfinder:task` ticket is assigned.

## Closed this period

| id | slug | summary |
|----|------|---------|
| —  | —    | —       |

Move row here when the worktree closes, the PR merges, or the ticket is `wontfix`.
## Watchlist

Lower-priority items the loop monitors but does not act on without an external signal. Each entry is one line:

`<iso> <surface>: <signal>`.

| since | surface | signal |
|-------|---------|--------|
| —     | —       | —      |

## Recent loop outcomes

Mirror of `loop-run-log.md`. The machine-written ledger is the authoritative source — this section is the human-curated copy. Append one line per `loop-budget` closure. Schema lives in `loop-run-log.md` (six fields: `run_id` · `pattern` · `outcome` · `actions_taken` · `slur_sha` · `scope`); example:

```
{"run_id":"<iso>","pattern":"daily","outcome":"no-op","actions_taken":0,"slur_sha":"<git>","scope":"<ticket-id or none>"}
```

## Entries

```
{"run_id":"2026-07-17T20:35Z","pattern":"adhoc","outcome":"closed","actions_taken":2,"slur_sha":"32a19a1","scope":"none"}
```
[ mirror of `loop-run-log.md` first entry — corresponds to commit 32a19a1 · "docs(agents): tighten dial gate-skip rule + loop-run-log sibling" — actions_taken: 2 reflects *that single run's* file mutations: AGENTS.md skip-rule clarification + `loop-run-log.md` creation. ]

## Notes / kill-switch log

Append a single line when:
- `loop-pause-all` flips,
- a denylist path was touched (or an attempt was blocked),
- escalation to a human was required,
- a safety measure was disabled (should be never).
