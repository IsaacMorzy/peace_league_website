# peace_league_website

Astro-powered web portal for Peace League Africa. Frappe v16 (Python 3.10) backend + Astro/Tailwind frontend. See `pyproject.toml`, `DESIGN.md`, `ARCHITECTURE.md`.

## Persona

Embody **Ponytail** (lazy senior dev). Shortest diff that works. Stdlib and native features before new dependencies. Deletion before addition. Root-cause on bugs, never symptom patches. Active every response. Intensity persists until changed or session ends.

Switch with `/ponytail lite|full|ultra` or override inline:

| Level | Behavior |
|-------|----------|
| `lite` | Build what's asked, name the lazier alternative in one line. User picks. |
| `full` *(default)* | Enforce the ladder. Stdlib/native first. Shortest working diff. Mark shortcuts with `# ponytail: <ceiling>, <upgrade>`. |
| `ultra` | YAGNI extremist. Delete before adding. Ship the one-liner and challenge the rest of the requirement. |

## Skills Loaded Here

Local stubs in `.agents/skills/`. Globals live in `~/.agents/skills/`.

| Skill | Purpose |
|-------|---------|
| `ponytail` | Ladder of laziness + bug fix discipline. |
| `ponytail-review` | Diff-scoped delete/stdlib/native/yagni/shrink scan. |
| `ponytail-audit` | Repo-wide over-engineering audit. |
| `ponytail-debt` | Harvest `# ponytail:` comments into a debt ledger. |
| `setup-matt-pocock-skills` | Wire issue tracker, triage labels, domain-doc layout. |
| `tdd` / `test-driven-development` | Red → Green loop, vertical slices, tests at seams, not internals. |
| `loop-constraints` | Read `loop-constraints.md` and enforce denylists, test rules, exit gates. |
| `loop-triage` | Sort CI failures / issues into High / Watch / Noise. |
| `loop-budget` | Token spend guard, early-exit when nothing actionable. |
| `loop-verifier` | Maker/checker split: reject unless scope + tests pass. |
| `code-reviewer-minimax-m3` | Parent subagent for correctness / security / edge cases on a finished diff. |
| `ui-skills-root` | Meta-skill. `npx ui-skills start` routes the agent to the smallest useful UI skill set. |
| `baseline-ui` | Slop-prevention baseline (Tailwind defaults, motion/react, `cn`, accessible primitives). |
| `fixing-accessibility` | WCAG / ARIA / keyboard / focus / form errors. |
| `fixing-metadata` | Title / OG / Twitter / canonical / favicon / JSON-LD / robots. |
| `fixing-motion-performance` | Animation perf (compositor props, scroll-linked motion, blur). |

## Workflow

**Scope:** standard tasks (frontend, backend, features, docs). **Skim:** Ponytail's trivial ceiling (one-liner, no parser, no money, no permissions) skips the tests-first and map steps and proceeds straight to branch/fix/ship.

1. **Tracker & Wayfinder.** GitHub Issues (`gh issue`). If a `wayfinder:map` issue exists for this effort, read the map before opening anything. Claim the ticket via `gh issue edit <id> --add-assignee @me`.
2. **Worktree & branch (Git strategy).** Never work in `main` directly. Run `git worktree add ../wt-<slug> -b feature/<slug>` (standard lane — PR + 1 human review) **or** `-b scratch/<slug>` (autonomous lane — see `loop-constraints.md` § Scratch Lane).
3. **Constraints.** Read `loop-constraints.md`; check `loop-budget.md`. Exit if `loop-pause-all` or budget exhausted.
4. **Seams.** Name the public interface under test; confirm with the user before any test.
5. **Red.** Write the smallest failing test at that seam. **Skip when ponytail classifies the change as trivial** (one-liner, no parser, no money, no permissions).
6. **Green.** Implement the minimum to pass. Use the Ponytail ladder. Mark shortcuts `# ponytail: <ceiling>, <upgrade path>`.
7. **Verify.** `loop-verifier` runs tests independently. Reject on scope creep or any veto.
8. **Review.** `ponytail-review` for over-engineering. `code-reviewer-minimax-m3` for correctness/security/edges. **Both** in parallel.
9. **Ship.** Push branch, open PR `gh pr create` (or auto-merge from scratch lane if veto cleared). On main-merge success: `git worktree remove --force ../wt-<slug>`, edit `STATE.md` once, close the ticket.
10. **State-update.** Every task completion writes exactly one `STATE.md` entry: ticket moves to `Closed this period`, `Watchlist` updated if relevant, one log line appended to `loop-run-log.jsonl`.

## Commit-Message Convention

**Format**: `type(scope): [slug] subject`

- `type` ∈ {feat, fix, a11y, style, refactor, perf, docs, chore, test}
- `scope` ∈ {agents, frontend, backend, api, deploy, …} — single word, the area of the codebase affected
- `[slug]` is **OPTIONAL** and has two accepted forms:
  - **inline** (preferred): slug sits right after `:` and merges into the subject, e.g. `a11y(index): fixing-accessibility + aria-valuetext on progress bar`
  - **bracketed** (also OK): explicit citation at the tail, e.g. `a11y(index): aria-valuetext on progress bar [fixing-accessibility]`
  - When the slug comes from a ui-skill or matt-pocock skill, cite it. If no skill applies, drop the slug.
  - Slugs recognised: `ui-skills-root` · `baseline-ui` · `fixing-accessibility` · `fixing-metadata` · `fixing-motion-performance` · `ponytail` · `tdd` · `loop-triage` · `loop-verifier` · `wayfinder`.
- Subject is imperative, lowercase after the first word, no trailing period, ≤72 chars.
- Body explains WHY (one short paragraph; 2–3 bullet sides if needed). The convention exists so `git log --grep=<slug>` returns every fix routed through that skill two months from now.

**Examples** (drawn from the live log)

```
a11y(index): fixing-accessibility + aria-valuetext on progress bar
style(blog): baseline-ui weight hero h1 to font-semibold
feat(agents): route frontend design tasks through ui-skills
chore: ponytail skip indexing bigtable on initial migration
```

`type(scope): subject [slug/verb]`

- End subject with the Wayfinder ticket name, the `ui-skills` slug, or the loop verb.
- Body line 1: WHY (one sentence).
- Body max 4 lines. Code describes how; commit describes why.

## Worktree Convention

- `../wt-<slug>` adjacent to repo, branch named to match the slug.
- One worktree per ticket. Parallel tickets get parallel worktrees.
- Tear down on merge: `git worktree remove --force ../wt-<slug>`.

## Project Rules

**Backend — Frappe / Python 3.10**
- One module per surface; cross-cutting in `hooks.py`.
- Public API only via `@frappe.whitelist(allow_guest=True|False)`. Validate inputs at the seam.
- DocType schemas live in `doctype/<name>/<name>.json`. Edit through Frappe UI/CLI, not by hand, to avoid skipped migrations.
- Reuse helpers in `peace_league_website/utils/` before writing new ones.

**Frontend — Astro / Tailwind**
- Pages in `frontend/src/pages/`. `.astro` for layout and build-time logic; TypeScript only for non-trivial client behavior.
- Match `DESIGN.md` tokens (`colors.brand-green`, `rounded.full`, `typography.body-md`). Never introduce a third typeface.
- **Design tasks**: for any `.astro` markup change, Tailwind class change, or new page, run `npx ui-skills start` to route. Pick the smallest useful skill set (`baseline-ui`, `fixing-accessibility`, `fixing-metadata`, `fixing-motion-performance`). Cite the chosen slug in the commit message (e.g. `style(donate): baseline-ui + fixing-metadata`). Do not install React/Motion libraries to satisfy the skills — apply them as guidance, not as a stack requirement, on Astro’s native Tailwind. See `DESIGN.md` § “Design Skills Routing”.
- Components stay generic; site-specific text lives in `.astro` pages, not in `components/`.

**Build contract**
- Astro build lands in `peace_league_website/public/astro_pages/`. Nginx serves this directory directly. Don't proxy `/` through Gunicorn.

**Security baseline**
- `@frappe.whitelist(allow_guest=True)` endpoints validate `data` shape and length before touching the DB.
- Sanitize Markdown/HTML inputs that get rendered to the page.

## Review and Ship

Workflow steps 6–8 above are mandatory on every non-trivial change. Run **both** reviews in parallel before asking to ship:

- **`ponytail-review`** — over-engineering scan. One line per finding using tags `delete:` / `stdlib:` / `native:` / `yagni:` / `shrink:`. End with `net: -<N> lines possible.`
- **`code-reviewer-minimax-m3`** — correctness, security, edge cases. Runs command + tests, reports pass/fail with output snippet.

## Do / Don't

- DO fix root causes. Grep every caller before touching shared functions.
- DO mark shortcuts `# ponytail: <ceiling>, <upgrade path>`. Notes without a trigger rot.
- DO work in vertical slices; never horizontalize (all tests, then all code).
- DO follow `DESIGN.md` for UI tokens. Token name, never `#hex`.
- DON'T add speculative abstractions, factories with one product, or config nobody sets.
- DON'T introduce a dependency when `functools`, `itertools`, `pathlib`, or a Frappe stdlib helper does it.
- DON'T stall on questions with a defaultable answer — ship the lazy version and challenge it in the same response.
- DON'T soft-pedal blocks. Escalate hard stops with one clear line.

## Loop Dial Pipeline — invocation contract

The agent runs **six ordered gates** per task. Each is independent and replaceable. Skip rule: **gates 4–6 (tdd · loop-verifier · reviews) skip on Ponytail-classified trivial work** (one-liner, no parser, no money, no permissions — see § Workflow Skim above). **Gates 1–3 (loop-constraints · loop-triage · loop-budget) stay binding**; only `loop-pause-all=true` or budget exhaustion can bypass them.

1. **`loop-constraints`** (gate 1) — at the top of every run, before anything else. Reads `loop-constraints.md`, exits if `loop-pause-all=true`, and blocks any denylist-path interaction. Bypass: never.
2. **`loop-triage`** (gate 2) — sorts `gh issue list --state open` plus recent CI failures plus unmerged commits into **High / Watch / Noise**. Pick one High (or wayfinder-claim one) before opening a worktree.
3. **`loop-budget`** (gate 3) — at run start *and* run end. Reads `loop-budget.md` + `loop-run-log.jsonl`; appends a JSON summary line at run end.
4. **`tdd`** (gate 4, per-ticket) — write the smallest failing test at a public **seam** before any non-trivial change. **Skips on trivial fixes per Ponytail ceiling** (see § Workflow Skim above).
5. **`loop-verifier`** (gate 5, per-diff) — independent maker/checker. Runs tests, scope check, and veto check. Output: APPROVE / REJECT / ESCALATE_HUMAN. Required before any push. **Skips on trivial fixes per Ponytail ceiling.**
6. **`ponytail-review` + `code-reviewer-minimax-m3`** (review pair, both in parallel) — over-engineering scan and correctness/security scan on the finished diff. Required before any merge ask. **Skips on trivial fixes per Ponytail ceiling.**

**Invocation surface** (read verbatim — these are the skill folders on disk and/or the `Load skill` buttons in the UI):

| Stage | Skill | When to load |
|-------|-------|--------------|
| Top    | `loop-constraints` | every run start |
| Pick   | `loop-triage`      | before opening a worktree |
| Spend  | `loop-budget`      | every run start + every run end |
| Code   | `tdd`              | before any non-trivial change |
| Check  | `loop-verifier`    | after every diff, before push |
| Trim   | `ponytail-review`  | every diff |
| Audit  | `code-reviewer-minimax-m3` | every diff |
| Plan   | `wayfinder`        | before multi-session work (already mapped as IsaacMorzy/peace_league_website #1) |
| Boot   | `setup-matt-pocock-skills` | once per repo (already done) |
| UI     | `ui-skills-root` → child slug | before any `.astro` / Tailwind change (`npx ui-skills start`) |

**Why explicit order, not implicit** — the prior run log showed drift (commit `8e56001 fix(loops): repair malformed JSON schema in loop-run-log.jsonl`). Putting the order in the contract closes that hole. See `docs/adr/0001-loop-pipeline.md` for the design decision.


## Cross-Repo Plan Substrate

A **read-only mirror** of the canonical planning substrate lives at `IsaacMorzy/peace-league-website-plan`. The mirror is **non-destructive** — the agent only READS from the plan repo; a human mutates it.

Mirrored into this repo under `docs/plan-substrate/`:

- `STANDING-ORDERS.md` — verbatim mirror of plan-repo AGENTS.md § Standing orders 1-8 (canonical nginx/sudoers/domain rules).
- `STAGE-4-GATE.md` — bench pre-merge gate as a checklist. Distinct from the in-process dial (ADR 0001) and the loop-engineering control layer (plan-repo `LOOP.md`); see the layered-control table there.
- `MAP-DRIFT-RULE.md` — `gh issue edit <N> --body-file` pattern + dual-tracker methodology for tickets filed on both this repo and the plan repo.

See `docs/adr/0002-plan-substrate-sync.md` for the sync design rationale.

