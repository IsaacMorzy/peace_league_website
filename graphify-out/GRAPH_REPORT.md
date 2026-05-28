# Graph Report - peace_league_website  (2026-05-28)

## Corpus Check
- 94 files · ~450,298 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 771 nodes · 891 edges · 78 communities (71 shown, 7 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 12 edges (avg confidence: 0.78)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e7d39faa`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 54|Community 54]]
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 56|Community 56]]
- [[_COMMUNITY_Community 57|Community 57]]
- [[_COMMUNITY_Community 59|Community 59]]
- [[_COMMUNITY_Community 60|Community 60]]
- [[_COMMUNITY_Community 61|Community 61]]

## God Nodes (most connected - your core abstractions)
1. `../layouts/Layout.astro` - 29 edges
2. `../components/Navigation.astro` - 29 edges
3. `../components/Footer.astro` - 22 edges
4. `../components/Navigation.astro` - 20 edges
5. `Meditative Motion + Persuasive Layout Refinements (Peace League Website)` - 13 edges
6. `Peace League Africa — Architecture Documentation` - 12 edges
7. `Lighthouse Sweep Design (All Pages)` - 12 edges
8. `File Structure` - 11 edges
9. `Components` - 10 edges
10. `Backend API Module (api.py)` - 10 edges

## Surprising Connections (you probably didn't know these)
- `Donation` --uses--> `Donation`  [INFERRED]
  peace_league_website/peace_league_custom/doctype/donation/donation.py → peace_league_website/doctype/plw_donation/donation.py
- `generate_test_data()` --calls--> `seed_chapters()`  [EXTRACTED]
  peace_league_website/utils/seed_data.py → peace_league_website/utils/seed/seed_chapters.py
- `generate_test_data()` --calls--> `seed_donations()`  [EXTRACTED]
  peace_league_website/utils/seed_data.py → peace_league_website/utils/seed/seed_donations.py
- `generate_test_data()` --calls--> `seed_donors()`  [EXTRACTED]
  peace_league_website/utils/seed_data.py → peace_league_website/utils/seed/seed_donors.py
- `generate_test_data()` --calls--> `seed_members()`  [EXTRACTED]
  peace_league_website/utils/seed_data.py → peace_league_website/utils/seed/seed_members.py

## Communities (78 total, 7 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.11
Nodes (32): About Page (/about), Backend API Module (api.py), Astro Framework, Contact Page (/contact), POST create_chapter API, POST create_donation API, POST create_volunteer API, Donate Page (/donate) (+24 more)

### Community 1 - "Community 1"
Cohesion: 0.10
Nodes (23): c(), d(), n(), p(), u(), E(), f(), i (+15 more)

### Community 2 - "Community 2"
Cohesion: 0.08
Nodes (32): create_chapter(), create_donation(), create_volunteer(), donation_status(), generate_test_data(), get_causes(), get_chapters(), get_homepage_data() (+24 more)

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (44): amountField, amountInputs, causeSelect, clearAllErrors(), clearFieldError(), data, fieldChecks, form (+36 more)

### Community 4 - "Community 4"
Cohesion: 0.05
Nodes (40): Badges & Status, Border Radius Scale, Brand & Accent, Breakpoints, Buttons, Cards & Containers, Code, Collapsing Strategy (+32 more)

### Community 5 - "Community 5"
Cohesion: 0.05
Nodes (39): code:css (/* ── Meditative Decorative Motion ── */), code:astro (<h2 class="scroll-reveal text-2xl sm:text-3xl lg:text-4xl fo), code:astro (<div class="absolute inset-0 pointer-events-none" aria-hidde), code:astro (<div class="flex gap-6 whitespace-nowrap items-center opacit), code:astro (<div class="absolute inset-0 pointer-events-none z-[2]" aria), code:bash (git add frontend/src/pages/index.astro), code:astro (<section class="hero-gradient text-white py-16 lg:py-20 rela), code:astro (<section class="py-16 bg-surface section-band">) (+31 more)

### Community 6 - "Community 6"
Cohesion: 0.06
Nodes (42): $, a, Ae(), at(), b(), Be(), D, de (+34 more)

### Community 7 - "Community 7"
Cohesion: 0.40
Nodes (3): Peace League Website module, frappe_npo dependency, peace_league_website app

### Community 8 - "Community 8"
Cohesion: 0.38
Nodes (9): apiCall(), donationStatus(), getCauses(), getChapters(), getHomepageData(), getVolunteers(), submitContact(), submitDonation() (+1 more)

### Community 9 - "Community 9"
Cohesion: 0.08
Nodes (21): Seed causes/campaigns for development.  Graph edges: creates: Cause, references:, Create sample Cause records for development.      Args:         force: If True,, seed_causes(), Seed chapter records for development.  Graph edges: creates: Chapter, Custom Fie, Create sample Chapter records.      Graph edges: creates: Chapter     Graph edge, seed_chapters(), Seed donation records for development.  Graph edges: creates: Donation Graph edg, Create sample Donation records linked to existing Donors.      Graph edges: crea (+13 more)

### Community 11 - "Community 11"
Cohesion: 0.05
Nodes (37): code:js (import { test } from 'node:test';), code:bash (node -e "const s=require('./frontend/lighthouse-reports/summ), code:js (// Scroll reveal — subtle fade-up when elements enter viewpo), code:bash (git add frontend/src/layouts/Layout.astro), code:css (@media (max-width: 640px) {), code:bash (git add frontend/src/styles/global.css), code:css (@media (max-width: 640px) {), code:bash (git add frontend/src/styles/global.css) (+29 more)

### Community 15 - "Community 15"
Cohesion: 0.08
Nodes (25): allow_copy, allow_import, allow_rename, autoname, creation, custom, doctype, document_type (+17 more)

### Community 16 - "Community 16"
Cohesion: 0.08
Nodes (25): actions, autoname, creation, doctype, editable_grid, engine, field_order, fields (+17 more)

### Community 17 - "Community 17"
Cohesion: 0.08
Nodes (23): AllValuesOf, CollectionEntry, CollectionKey, ContentConfig, DataEntryMap, ExtractCollectionFilterType, ExtractEntryFilterType, ExtractErrorType (+15 more)

### Community 18 - "Community 18"
Cohesion: 0.09
Nodes (20): dependencies, astro, @astrojs/sitemap, canvas-confetti, tailwindcss, tailwindcss-animate, @tailwindcss/vite, devDependencies (+12 more)

### Community 22 - "Community 22"
Cohesion: 0.11
Nodes (10): BaseDonation, Cause, Validate cause fields before saving., Peace League Cause/Campaign DocType.      Represents a fundraising campaign or c, Document, Donation, Donation, Validate donation before saving. (+2 more)

### Community 25 - "Community 25"
Cohesion: 0.13
Nodes (11): config, __dirname, m, modes, outputBase, repoRoot, reportsRoot, routes (+3 more)

### Community 26 - "Community 26"
Cohesion: 0.14
Nodes (13): doctype, fieldname, fieldtype, in_list_view, in_standard_filter, insert_after, label, module (+5 more)

### Community 27 - "Community 27"
Cohesion: 0.29
Nodes (6): Astro Starter Kit: Minimal, code:sh (npm create astro@latest -- --template minimal), code:text (/), 🧞 Commands, 🚀 Project Structure, 👀 Want to learn more?

### Community 28 - "Community 28"
Cohesion: 0.14
Nodes (13): Acceptance Criteria, Accessibility and Performance, Design Principles, Goals, Implementation Scope (Planned Files), Layout and Hierarchy, Meditative Motion + Persuasive Layout Refinements (Peace League Website), Motion System (+5 more)

### Community 29 - "Community 29"
Cohesion: 0.19
Nodes (11): collectRoutesFromPages(), __dirname, __filename, isApiRoute(), isDynamicRoute(), outFile, routes, pages (+3 more)

### Community 30 - "Community 30"
Cohesion: 0.15
Nodes (12): Approach (Shared-Asset-First), Candidate Shared Fixes (Ordered by Likely Impact), Goals, Lighthouse Sweep Design (All Pages), Non-Goals, Outputs, Overview, Results (+4 more)

### Community 31 - "Community 31"
Cohesion: 0.15
Nodes (12): chevron, children, d, focusable, group, iconPaths, items, navItems (+4 more)

### Community 32 - "Community 32"
Cohesion: 0.27
Nodes (10): __dirname, ensureDir(), extractMetrics(), __filename, getArgValue(), main(), readRoutesFile(), repoRoot (+2 more)

### Community 33 - "Community 33"
Cohesion: 0.18
Nodes (9): relatedPosts, ../../lib/blog-data.json, ../lib/blog-data.json, allPostsJson, categories, end, pages, start (+1 more)

### Community 34 - "Community 34"
Cohesion: 0.20
Nodes (8): FLAG_COUNTRIES, footerLinks, ../components/Footer.astro, ../components/Navigation.astro, ../lib/api.js, pages, boardMembers, teamMembers

### Community 35 - "Community 35"
Cohesion: 0.18
Nodes (11): 2. Directory Structure, 6. Database Schema, 8.1 API Security, 8.2 Frontend Security, 8.3 Infrastructure Security, 8. Security, Appendix: Key Ports, code:block10 (tabMember) (+3 more)

### Community 36 - "Community 36"
Cohesion: 0.23
Nodes (9): ../lib/causes-data.json, ../components/Footer.astro, ../lib/causes-data.json, goTo(), next(), prev(), startAutoplay(), stopAutoplay() (+1 more)

### Community 38 - "Community 38"
Cohesion: 0.22
Nodes (9): 3.1 Frontend Page Requests, 3.2 API Requests, 3.3 Form Submission (Donate/Volunteer/Contact), 3.4 Homepage Data Loading, 3. Request Flow, code:block3 (Browser ──GET https://peaceleagueafrica.com/──▶ Nginx (443)), code:block4 (Browser ──GET https://peaceleagueafrica.com/api/method/peace), code:block5 (User fills form ──▶ Browser JS collects FormData ──▶ api.js ) (+1 more)

### Community 39 - "Community 39"
Cohesion: 0.22
Nodes (9): 9.1 Local Development, 9.2 Frontend Build, 9.3 Server Restart, 9.4 Adding a New API Endpoint, 9.5 Adding a New Frontend Page, 9. Development Workflow, code:bash (# Activate Frappe environment), code:bash (cd apps/peace_league_website/frontend) (+1 more)

### Community 40 - "Community 40"
Cohesion: 0.25
Nodes (7): answer, chevron, faqs, item, otherAnswer, otherChevron, otherItem

### Community 41 - "Community 41"
Cohesion: 0.29
Nodes (7): 5.1 Pages Overview, 5.2 API Integration Pattern, 5.3 API Client (`api.js`), 5. Frontend Pages, code:javascript (// Inline script in .astro page), code:javascript (import { submitDonation } from '../lib/api.js';), code:javascript (const API_BASE_URL = import.meta.env.PUBLIC_API_URL || '';)

### Community 42 - "Community 42"
Cohesion: 0.29
Nodes (7): 7.1 Process Management (Supervisor), 7.2 Nginx Configuration, 7.3 CORS Configuration, 7.4 SSL/TLS, 7. Deployment Architecture, code:block11 (supervisord (root, PID 164821)), code:block12 (Port 80 (HTTP)     → 301 redirect → Port 443 (HTTPS))

### Community 43 - "Community 43"
Cohesion: 0.33
Nodes (5): __dirname, distDir, MIME, port, server

### Community 44 - "Community 44"
Cohesion: 0.40
Nodes (4): empty, past, pastEvents, upcomingEvents

### Community 45 - "Community 45"
Cohesion: 0.40
Nodes (3): starIcons, stats, testimonials

### Community 46 - "Community 46"
Cohesion: 0.50
Nodes (3): countries, countryDots, lines

### Community 47 - "Community 47"
Cohesion: 0.67
Nodes (3): main(), pageStatus(), ROUTES

### Community 48 - "Community 48"
Cohesion: 0.50
Nodes (3): benefits, jobs, whyStats

### Community 49 - "Community 49"
Cohesion: 0.15
Nodes (12): ../layouts/Layout.astro, ../styles/global.css, canonicalURL, dots, heroSection, mo, rect, shapes (+4 more)

### Community 50 - "Community 50"
Cohesion: 0.50
Nodes (3): exclude, extends, include

### Community 51 - "Community 51"
Cohesion: 0.50
Nodes (4): 4.1 GET Endpoints, 4.2 POST Endpoints, 4.3 Internal Endpoints (requires auth), 4. API Endpoints

### Community 54 - "Community 54"
Cohesion: 0.33
Nodes (5): ../components/CTA.astro, btn, data, ideas, steps

### Community 55 - "Community 55"
Cohesion: 0.50
Nodes (3): error, submitBtn, successMsg

### Community 57 - "Community 57"
Cohesion: 0.67
Nodes (3): 1. High-Level Architecture, code:block1 (┌──────────────────────────────────────────────────────────┐), Key Technologies

## Knowledge Gaps
- **412 isolated node(s):** `canonicalURL`, `srMo`, `sheen`, `rect`, `mo` (+407 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `../layouts/Layout.astro` connect `Community 49` to `Community 33`, `Community 34`, `Community 3`, `Community 36`, `Community 40`, `Community 44`, `Community 45`, `Community 48`, `Community 54`, `Community 55`, `Community 31`?**
  _High betweenness centrality (0.011) - this node is a cross-community bridge._
- **Why does `../components/Navigation.astro` connect `Community 31` to `Community 33`, `Community 34`, `Community 3`, `Community 36`, `Community 40`, `Community 44`, `Community 45`, `Community 48`, `Community 49`, `Community 54`, `Community 55`?**
  _High betweenness centrality (0.011) - this node is a cross-community bridge._
- **What connects `canonicalURL`, `srMo`, `sheen` to the rest of the system?**
  _447 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.10795454545454546 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.09788359788359788 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.07765151515151515 - nodes in this community are weakly interconnected._
- **Should `Community 3` be split into smaller, more focused modules?**
  _Cohesion score 0.05603864734299517 - nodes in this community are weakly interconnected._