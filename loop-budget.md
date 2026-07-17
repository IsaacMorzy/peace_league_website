# Loop Budget — peace_league_website

Daily caps read at the start of every loop run. Numbers here are placeholders; tune after the first week of real telemetry.

## Per-pattern caps (tokens / day)

| pattern | daily_cap | max_subagent_spawns | early_exit_below_actions |
|---------|-----------|--------------------|--------------------------|
| daily   | 800_000   | 8                  | 2                        |
| ci      | 200_000   | 4                  | 1                        |
| pr      | 200_000   | 4                  | 1                        |

`early_exit_below_actions` = the loop exits in <5k tokens (no sub-agents) when prior actions in the last 24h ≤ this number.

## Kill switches

- `loop-pause-all` — read from `STATE.md`. Mirrors the same flag name so the loop-constraints skill can short-circuit regardless.
- `loop-no-commit` — when set, the loop may stage and review but never commits. Default: unset.
- `loop-no-fix` — when set, the loop runs in report-only mode (findings only, no auto-fix). Default: unset.

## Alerts This Period

Append one line per self-throttle event: `<iso> <pattern> spend <X>% of cap, switched to report-only.`
