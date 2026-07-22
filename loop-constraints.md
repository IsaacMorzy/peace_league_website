# Loop Constraints — peace_league_website

Read at the start of every loop run. Rules are binding.

## Execution

- Check `loop-pause-all`. If true → exit immediately. On exit, append a one-line note to `STATE.md` (create on first run if absent).
- One fix per run. Never bundle unrelated edits.
- Stop and escalate after **3 failed fix attempts** on the same issue.

## Push & Merge

- **Agent-initiated merges to `main` are permitted** when all three hold:
  1. `loop-verifier` passes independently (tests + scope check).
  2. One reviewer approval (`code-reviewer-minimax-m3` / `code-reviewer-glm` or human).
  3. No item in the automerge veto list below was tripped.
- The agent may merge a PR to `main` via `gh pr merge --merge`, then sync the local main checkout.
- No force-push except in private, isolated scratch branches already named `scratch/*`.

### Scratch Lane (`scratch/*`)

- **Auto-commit**: commits to a scratch branch happen directly (no PR required *on the branch itself*).
- **Auto-merge to main via PR**: allowed **only** if all three hold:
  1. `loop-verifier` passes independently (tests + scope check).
  2. One reviewer approval (`code-reviewer-minimax-m3` or human).
  3. No item in the automerge veto list was tripped.

**Automerge veto (always forces human escalation):**

- Any denylist path read, modified, or staged.
- Any test bypass added (`.skip`, `xfail`, `only`, commented asserts).
- `payments/**` touched (treated READ-ONLY by the org rule).
- Three failed fix attempts on the same ticket.
- Branch is `main` itself — `main` never bypasses human merge approval.
- **Any `*.key` / `*.crt` / `*.pem` / `*.env*` / `secrets.*` file read, modified, or staged** — certs and secrets are never auto-mergeable. (This repo currently carries `vmi3416692.tailc65d30.ts.net.key` and `*.crt` at root; agents must never stage them.)
- **Any DocType schema delta** — `apps/*/doctype/**/*.json` field add/remove/rename under the Frappe app. Schema changes must flow through `migrations/`, never direct DocType JSON writes.

- No `git reset --hard`, `git clean -fd`, `git push --force` to a shared branch — escalate.

## Denylist Paths — read/edit/commit forbidden

- `.env`, `.env.*`
- `secrets/`, `credentials/`, `keys/`
- `*.pem`, `*.key`, `*.crt`
- `peace_league_website/public/files/` (user uploads)
- Any `private/` directory under `sites/`
- `payments/**` is READ-ONLY. Never edit `payments.payment_gateways.*`, `mpesa_settings.json`, or any third-party payment integration files; escalate writes to upstream.
- `auth/` and any `*auth.py` are READ-ONLY (when present). This project imports `payments.payment_gateways.doctype.mpesa_settings.mpesa_connector`; the import is allowed, edits under `payments/` are not.

Escalate if a task seems to require touching any of these.

## Test Discipline

- Tests must run before any fix is proposed. Verifier runs them independently.
- Never `skip`, `xfail`, `only`, `.skip`, comment out asserts, or delete failing tests to ship.
- Never loosen linters, type checks, or constraints to make CI green.
- A non-trivial branch/loop/parser/money path leaves **one runnable check** (assert-based self-check or one `test_*.py`). No frameworks unless the project already uses them.

## Code Rules

- Read `DESIGN.md` before UI changes. Read `ARCHITECTURE.md` before infra or API contract changes.
- Read the full file before editing any named function. Trace every caller. One guard at the shared function beats a guard per caller.
- Mark deliberate simplifications `# ponytail: <ceiling>, <upgrade path>` — the upgrade path is required, missing trigger = rot risk.
- Reuse before write. Helpers in `peace_league_website/utils/` and `frontend/src/lib/` beat new code.

## Escalation

- 3 failed fix attempts on the same issue → escalate to human.
- Any hit on the denylist → escalate, do not proceed.
- Any change that requires disabling a safety measure → escalate.
