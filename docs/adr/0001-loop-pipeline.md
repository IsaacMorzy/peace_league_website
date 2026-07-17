# ADR 0001 — Loop + Matt Pocock Dial on peace_league_website

**Status:** Accepted · 2026-07-17 · IRC `IsaacMorzy/peace_league_website`
**Deciders:** agent (per `AGENTS.md` § Persona) + repo owner
**Relates:** AGENTS.md Workflow contract v2 (commit `6ac39e5`); wayfinder map issue #1.

## Context

peace_league_website now carries an `AGENTS.md` Workflow v2 contract that maps every task to:

  Wayfinder ticket → worktree isolation (`feature/*` or `scratch/*`) → constraints check → seam → red → green → verify → reviews (parallel) → ship → state-update.

Until this ADR the contract referenced the loop + matt-pocock skills by name only, with no ordered rubric and no audit trail of which gate ran when. Two failure modes had already been observed:

1. Drift between sessions — the agent re-derived the order from memory and got it wrong (commit `8e56001 fix(loops): repair malformed JSON schema in loop-run-log.md` reflects one such self-correction).
2. Difficulty for a fresh-context agent loading `AGENTS.md` to recover the intended invocation order without probing the skill folders one by one.

## Decision

Make the dial **explicit and ordered**, six gates total. Wire it both:

- into `AGENTS.md` § "Loop Dial Pipeline — invocation contract" (verbatim); and
- as an ADR record (`docs/adr/0001-loop-pipeline.md`) so the design choice survives the contract text even if that section gets reworded later.

The dial:

| # | Gate | Skill | When |
|---|------|-------|------|
| 1 | Block bad paths / pause signals | `loop-constraints` | top of every run |
| 2 | Pick the right ticket | `loop-triage` | before opening a worktree |
| 3 | Spend guard + run-log | `loop-budget` | every run start + end |
| 4 | Test at the seam | `tdd` | before any non-trivial change |
| 5 | Independent make/check | `loop-verifier` | after every diff, before push |
| 6 | Two reviews, in parallel | `ponytail-review` + `code-reviewer-minimax-m3` | after every diff |

Plus two cross-cutting skills that wire to the gates:

| When | Skill |
|------|-------|
| Before multi-session work | `wayfinder` (already mapped to issue #1) |
| Once per repo | `setup-matt-pocock-skills` |
| Before any `.astro` / Tailwind change | `ui-skills-root` (meta) → routed child slug |

## Consequences

**Positive**

- **Less drift.** A fresh-context agent loading `AGENTS.md` knows the order verbatim; no need to retread the prior commit log.
- **Audit trail.** `STATE.md` § "Recent loop outcomes" + `loop-run-log.md` become the timestamped log of what each session ran.
- **Gate failure is observable.** A `REJECT` from `loop-verifier` is now an explicit event in STATE, not a silent retry.
- **Less gate, bounded blast radius.** `scratch/*` lanes can auto-merge when verifier+approval+veto all clear (see `loop-constraints.md` § Scratch Lane); `feature/*` keeps PR + 1 human review; `main` stays human-only. This was previously implicit, now codified.

**Negative / risks**

- **Process overhead.** Six gates per task add latency on trivial work; the § Workflow "Skim" line exists to allow skipping gates 4–6 on Ponytail-classified trivial changes.
- **Coupling to skill versions.** If `loop-constraints.md` is renamed or moved, `loop-pause-all` no longer exists, etc., the dial entry points break. Mitigation: `loop-constraints` runs first and emits a fail-loud exit if any referenced path is missing.
- **Auto-merge blast radius.** `scratch/*` auto-merge is a real relaxation of the prior "human approves every merge" rule. The veto list (certs/keys/secrets, DocType deltas, denylist paths, payments/**, force-push) exists to bound the relaxation.

## Alternatives considered

- **One mega-script wrapping all gates.** Rejected — would hide which gate tripped and make `ponytail-review`-style over-engineering review harder.
- **Implicit / remembered order.** Rejected — the prior commit log proves drift.
- **External workflow tool (GitHub Actions, Act).** Rejected — adds a dependency; the agent contract is meant to be portable across machines.
- **Per-skill SKILL.md frontmatter as the authority.** Considered — but `SKILL.md` is what each skill SAYS about itself, not what the repo DECIDES about their order. The repo's contract lives in `AGENTS.md`; ADR captures why.

## Forward work

- After roughly 10 runs through this dial, re-evaluate ordering and trim if gates 4–6 are routinely redundant on trivial fixes.
- Promote `loop-run-log.md` JSON schema into a typed contract once the run count makes manual parsing fragile.
- When payments/** integration or other veto-sensitive surfaces mature, harden the veto list and consider promoting it into a dedicated `veto-list.md` rather than a sub-section of `loop-constraints.md`.
