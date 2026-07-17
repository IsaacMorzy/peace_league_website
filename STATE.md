# STATE

Working state for the loop engineering workflow. Append-only between runs. Read at the start of every loop iteration.

## loop-pause-all

`false` — set to `true` to make `loop-constraints` exit immediately. One line note appended below when flipped.

## Active work

| id | surface | status | opened | last_touched |
|----|---------|--------|--------|--------------|
| — | — | — | — | — |

No active work yet. The loop opens an entry here when `loop-triage` flags a high-priority item.

## Watchlist

Lower-priority items the loop monitors but does not act on without an external signal. Each entry is one line:

`<iso> <surface>: <signal>`.

| since | surface | signal |
|-------|---------|--------|
| —     | —       | —      |

## Recent loop outcomes

Append one JSON line per `loop-budget` closure. Mirror into `loop-run-log.md`:

```
{"run_id":"<iso>","pattern":"daily","outcome":"no-op","actions_taken":0}
```

## Notes / kill-switch log

Append a single line when:
- `loop-pause-all` flips,
- a denylist path was touched (or an attempt was blocked),
- escalation to a human was required,
- a safety measure was disabled (should be never).
