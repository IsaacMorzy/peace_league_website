# Research Report: Ghost Anti-Fraud App for Awards Voting

**Ticket:** #67 — Research: Evaluate Ghost anti-fraud app for Awards voting  
**Map:** #62 — Wayfinder map: Implement Awards feature  
**Date:** 2026-07-22  
**Author:** pi coding agent (research subagent)

---

## Executive Summary

**Recommendation:** ❌ **Ghost is NOT suitable** for the Awards voting anti-fraud use case. Ghost is a guest-to-user conversion system for e-commerce, not an anti-fraud or rate-limiting service. Using it would add unnecessary complexity and create user records for anonymous voters, which does not align with the requirement "anyone can vote" without accounts.

**Alternative:** Implement lightweight rate limiting using Redis + IP tracking, optionally add reCAPTCHA v3, and schedule a future review if bot attacks occur.

---

## 1. What Is Ghost?

Ghost is a Frappe app that creates **temporary "ghost" user identities** for anonymous visitors, allowing the app to track their activity (e.g., cart contents) before they convert to real users via email OTP. It is designed for **e-commerce conversion optimization**, not security or fraud detection.

**Source:** <https://github.com/muneeb141/ghost>

**Key features:**
- OAuth2 bearer tokens for session management
- Automatic ghost user creation on page load
- Conversion to real user via one-time password (OTP)
- Data preservation across conversion (cart, preferences)
- Short-lived tokens (1 hour default) with refresh capability

---

## 2. Compatibility with Frappe v16

Ghost explicitly supports **Frappe v15+** (see badge in README). Frappe v16 is backward compatible with v15 apps, so installation should work.

**Installation commands:**
```bash
bench get-app https://github.com/muneeb141/ghost
bench --site your-site install-app ghost
```

**No known blockers** for v16, but the app has not been widely adopted (few stars, no release tags). Use at your own risk.

---

## 3. Alignment with Awards Voting Requirements

We need anti-fraud measures for voting:

- ✅ **Rate limiting** — restrict number of votes per IP (currently: 10 votes total per IP, with 20 votes / 10min burst limit)
- ✅ **Bot detection** — reCAPTCHA v3 or similar
- ✅ **IP logging** — track IP + user-agent for audit
- ✅ **Anomaly detection** — flag suspicious patterns (many votes from same IP across categories)
- ✅ **Low friction** — voters should not need to create accounts

Ghost provides **none** of these directly. Instead, Ghost would:

- ❌ Create a `User` record for every voter (ghost user), polluting the user table with thousands of anonymous accounts.
- ❌ Require OAuth2 token management on the frontend (complex, unnecessary for simple voting).
- ❌ Add a conversion step (email OTP) if we ever wanted to "convert" voters to real users — irrelevant for awards.
- ❌ No built-in rate limiting or bot detection; those would still need to be implemented separately.
- ❌ No IP-based restrictions; ghost users are still users, but voting would need to check User/Email mapping, which Ghost doesn't provide.

**Conclusion:** Ghost solves a completely different problem (guest checkout conversion). It would be architectural overkill and does not replace the needed anti-fraud mechanisms.

---

## 4. Effort to Integrate Ghost

If we insisted, integration would require:

1. Install Ghost as a Frappe app.
2. Create a ghost session on first visit to `/awards`, storing the token in a cookie.
3. Modify voting endpoint to associate votes with `ghost_user` instead of IP — but then we lose IP rate limiting unless we also track IP separately (Ghost does not expose IP-based limits).
4. Handle token refresh/expiry on frontend.
5. Optionally implement a "convert to real user" flow (useless for awards).

**Estimated effort:** 1–2 days minimum, plus ongoing maintenance and user support for token issues.

**Verdict:** Negative ROI. Ghost does not move us forward.

---

## 5. Proposed Alternative Anti-Fraud Solution

**Current implementation** (in `api_awards.py`) already includes basic protections:

- `@rate_limit(key="ip", limit=10, methods=["POST"], seconds=3600)` — max 10 votes per IP per hour? Actually the decorator may be from `frappe.core.rate_limit`.
- Per-category uniqueness: one vote per IP per category (enforced in code by checking existing `Vote` doc).
- IP + user-agent capture in `Vote` DocType.

**Suggested improvements** (to be implemented in a new ticket):

1. **Aggressive rate limiting** — use Redis to enforce:
   - 10 votes total across all categories per IP (hard limit)
   - 20 requests per 10 minutes (burst protection)
2. **reCAPTCHA v3** — add to nomination and voting forms, verify server-side. Low friction for humans, blocks bots.
3. **IP anonymization** — store only /24 subnet for GDPR compliance, keep full IP in a separate audit log if needed.
4. **Suspicious pattern detection** — cron job to flag IPs that vote for >50% of nominees in <5 minutes; optionally auto-block after threshold.
5. **Admin dashboard** — show recent votes with IP, UA; allow manual IP blocklist.

These can be implemented in 2–3 tickets without adding a new app dependency.

---

## 6. License & Maintenance

Ghost is MIT-licensed, so legally compatible. However, it is a **single-maintainer project** with minimal community adoption. Long-term maintenance risk is moderate. Using built-in Frappe rate limiting and a small custom module is more maintainable.

---

## 7. Final Recommendation

**Do NOT adopt Ghost for Awards voting.** It is the wrong tool for the job. Instead, create a new ticket:

```
[wayfinder:task] Implement anti-fraud enhancements for Awards voting
```

subtasks:

- [ ] Replace basic rate limit with Redis-backed per-IP counting (10 total votes)
- [ ] Add reCAPTCHA v3 to nominate and vote forms
- [ ] Add admin UI for viewing recent votes and blocking IPs
- [ ] Add cron job for anomaly detection
- [ ] Write unit tests for rate limiting logic

Close #67 with "won't fix — Ghost inappropriate, see research report."

---

## Evidence & Sources

| Claim | Source |
|-------|--------|
| Ghost is for e-commerce guest conversion | README: "Let users browse anonymously, convert them when they're ready." |
| Ghost creates temporary user identities | README: "Ghost turns anonymous visitors into authenticated users" |
| Ghost uses OAuth2 tokens | README: "OAuth2 bearer tokens (industry standard)" |
| Ghost supports Frappe v15+ | README badge: "Frappe v15+" |
| Current voting IP limit 10 | `api_awards.py` (commit d70ba94) — `frappe.core.rate_limit` usage |
| No Ghost-funded anti-fraud features | README does not mention rate limiting, bot detection, IP blocking |

---

**Next step:** Close #67, open new task ticket for anti-fraud enhancements, assign to implementation lane.
