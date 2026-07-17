# STATE

Working state for the loop engineering workflow. Append-only between runs.

## loop-pause-all

`false` — set to `true` to make `loop-constraints` exit immediately. One line note appended below when flipped.

## Active work

| id | surface | status | opened | last_touched |
|----|---------|--------|--------|--------------|
| — | — | — | — | — |

No active work yet. The loop opens an entry here when `loop-triage` flags a high-priority item.

## Recent loop outcomes

One JSON line per `loop-budget` closure:

```
{"run_id":"<iso>","pattern":"daily","outcome":"no-op","actions_taken":0}
```

## Notes / kill-switch log

Append a single line when `loop-pause-all` flips, when a denylist path was touched, or when escalation was needed.
