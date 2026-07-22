# Label Bootstrap Recipe

> First-class artifact so future agents don't trip the "label doesn't exist" error on retry.

When running the plan-substrate sync, `gh issue create --label <name>` fails with silent exit code 1 if the label isn't already on the repo. **Bootstrap labels BEFORE filing the issues that need them.**

## Recipe (skip-if-exists, description ≤100 chars)

```bash
gh label create 'wayfinder:task-sync' \
  --color 'D4C5F9' \
  --description 'Cross-link mirror of a ticket on peace-league-website-plan (canonical plan repo).'
```

`description` MUST be ≤100 chars; GitHub rejects longer descriptions with HTTP 422.

## Other wayfinder labels in this repo (per `gh label list`)

| Label | Color | Description (≤100 chars) |
|-------|-------|---------------------------|
| `wayfinder:map` | `0E8A16` | Master plan for a multi-session effort. |
| `wayfinder:research` | `D4C5F9` | Fact-finding without changing system state. |
| `wayfinder:prototype` | `F9D0C4` | Throwaway code to test an approach. |
| `wayfinder:grilling` | `E99695` | Conversation ticket for domain discovery. |
| `wayfinder:task` | `C2E0C6` | Pre-requisite work unblocking a decision. |
| `wayfinder:task-sync` | `D4C5F9` | Cross-link mirror of a ticket on peace-league-website-plan. |

Use `--label wayfinder:<type>` matching the plan-repo's ticket type. Cross-link labels are always `wayfinder:task-sync` regardless of the source ticket type.

## Path forward

When `gh label create` exits non-zero with HTTP 422 about description length, shorten the description. When it exits non-zero saying "already exists" or similar, ignore and proceed.
