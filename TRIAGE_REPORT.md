# Loop Triage Report — 2026-07-22

**Scope**: Post‑awards‑enhancement follow‑ups, design tickets, testing gaps, security review.

## High Priority (Act Now)

### 1. Add unit tests for awards API
- **Why**: Ensure reliability of core voting and nomination flows; prevent regressions.
- **How**: Use pytest/frappe test framework. Test get_categories, get_category (including vote aggregation), cast_vote duplicate handling, create_nomination validation.
- **Effort**: medium
- **Tickets**: new

### 2. Install Playwright and write E2E tests
- **Why**: Verify pages render correctly in both light/dark modes and all CTA buttons present/clickable.
- **How**: Install Playwright, configure, write tests for each page (awards, donate, contact, etc).
- **Effort**: medium‑high
- **Tickets**: new

### 3. Add Cypress tests for frontend (if required by stack)
- **Why**: Provide alternative test suite; satisfy requirement “frontend should have cypress passing tests”.
- **How**: Install Cypress, write smoke tests for key user journeys (view awards, vote, nomination).
- **Effort**: medium‑high
- **Tickets**: new

### 4. Security review of image uploads
- **Why**: Uploaded images are stored publicly via Frappe file manager; potential for malicious uploads (SVG XSS, oversized files).
- **How**: Review current validation; add server‑side checks (mime type, size limit, maybe re‑encode to JPEG). Consider removing image field if risk too high, but images are core to awards; keep with validation.
- **Effort**: medium
- **Tickets**: new

### 5. Add LinkedIn field to Award Nominee
- **Why**: Enrich nominee profiles with professional link.
- **How**: Extend Award Nominee DocType (custom field or patch), API to accept/return, frontend form and display.
- **Effort**: medium‑high (includes DB migration, frontend changes)
- **Tickets**: new

### 6. Implement design improvements for many pages (tickets #46, #45, #44, #43, #42, #41, #40, #39, #38, #37, #36, #35, #34, #33, #32, #31, #30, #29)
- **Why**: These tickets explicitly request “design + improvements” for each page; must resolve via UI skill set (baseline‑ui, fixing‑accessibility, fixing‑metadata).
- **How**: Process each page in isolated worktrees; apply consistent spacing, typography, contrast, remove fluff (excessive ornaments). Verify light/dark contrast.
- **Effort**: high (many pages, but parallelizable)
- **Tickets**: existing GitHub issues

### 7. Close resolved tickets
- **Why**: Keep backlog clean.
- **How**: Close #60, #61 (already merged), and any others after verification.
- **Effort**: trivial

## Watch (Lower Urgency)

- Update AGENTS.md with new patterns discovered (e.g., combining design sweeps into batch runs, testing strategy).
- Explore running frontend build as part of PR automation.

## Noise / Out of Scope

- None at this time.

## Proposed Next Actions

1. Immediately close #60 and #61 (done above).
2. Open separate worktrees for:
   - API tests (unit)
   - Playwright setup & initial tests
   - Cypress setup & smoke tests (if mandated)
   - Security hardening of image uploads
   - LinkedIn field implementation
   - Each design‑improvement page (group by page type: legal, form, listing)
3. Run each change through the loop pipeline (constraints → budget → tdd (where applicable) → verifier → reviews).
4. Build and deploy after each batch merges.
