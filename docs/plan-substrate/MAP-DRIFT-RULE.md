# MAP Drift Rule — issue bodies mirror decision files

> Source: IsaacMorzy/peace-league-website-plan/MAP.md. The plan repo IS canonical; **issue bodies are derived**, so any edit to a `docs/wayfinder/decisions/<NN>-*.md` file MUST sync the matching GitHub issue body.

## Pattern

```bash
gh issue edit <N> --body-file docs/wayfinder/decisions/<NN>-<slug>.md -R IsaacMorzy/peace-league-website-plan
```

Drop the leading `## Ticket type / ## Question` header lines via `tail -n +N` so the issue body mirrors only the action sketch + acceptance. Worked example for plan ticket #04 (GitHub #5):

```bash
gh issue edit 5 --body "$(tail -n +3 docs/wayfinder/decisions/04-archive-tailnet-paths.md)" -R IsaacMorzy/peace-league-website-plan
```

## Dual-tracker methodology on peace_league_website

For tickets that ALSO have a discoverable presence on the main repo (`IsaacMorzy/peace_league_website`), the local repo maintains a **cross-link** issue labelled `wayfinder:task-sync` whose body is:

```
Cross-link to plan-repo ticket. Plan repo is canonical; main repo
mirrors the issue for visibility + filter by `is:in-progress`.

Plan-repo URL: https://github.com/IsaacMorzy/peace-league-website-plan/issues/<N>
Plan-repo title: <verbatim>
Main-repo actions: <none — read-only mirror unless you are working
this ticket on the bench>.

Ref: docs/plan-substrate/MAP-DRIFT-RULE.md
```

If you actually work the ticket on the bench side, the main repo issue gets the work-comments, the plan-repo issue is where the canonical decision file lives. Both are kept in sync via the drift rule at the close of Stage 5.
