# Loop Run Log

Append-only log read by `loop-budget` at the start of every iteration. One JSON object per line; never rewrite. Retention: last 24h read into `loop-budget`'s start-of-run math.

## Schema

```
{"run_id":"<iso>","pattern":"daily|ci|pr","duration_s":<n>,"items_found":<n>,"actions_taken":<n>,"escalations":<n>,"tokens_estimate":<n>,"outcome":"no-op|report-only|fix-proposed|escalated"}
```

Empty on first commit. Entries accumulate from the first loop iteration that closes.

## Field notes

- `run_id` — ISO8601 UTC.
- `pattern` — one of `daily`, `ci`, `pr` (matches the `loop-budget.md` daily-cap table).
- `outcome` — `no-op` (no actionable items, no sub-agent spawns), `report-only` (cap-throttled), `fix-proposed` (minimal-fix landed in worktree, awaiting human review), `escalated` (denylist hit, 3-attempt ceiling, or disabled-constraint request).

## Examples (do not commit — for shape reference only)

```
{"run_id":"2026-07-18T07:00:00Z","pattern":"daily","duration_s":12.4,"items_found":0,"actions_taken":0,"escalations":0,"tokens_estimate":4100,"outcome":"no-op"}
{"run_id":"2026-07-18T09:30:00Z","pattern":"ci","duration_s":8.1,"items_found":1,"actions_taken":0,"escalations":1,"tokens_estimate":22000,"outcome":"report-only"}
```
