# Graph Report - /home/crowd/frappe-bench/apps/peace_league_website  (2026-05-12)

## Corpus Check
- Corpus is ~15,836 words - fits in a single context window. You may not need a graph.

## Summary
- 247 nodes · 354 edges · 28 communities (24 shown, 4 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 1% AMBIGUOUS · INFERRED: 34 edges (avg confidence: 0.86)
- Token cost: 18,414 input · 8,832 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Frontend Pages & Architecture|Frontend Pages & Architecture]]
- [[_COMMUNITY_API Endpoints (Backend)|API Endpoints (Backend)]]
- [[_COMMUNITY_API Endpoints (AST)|API Endpoints (AST)]]
- [[_COMMUNITY_Minified Build JS (donate)|Minified Build JS (donate)]]
- [[_COMMUNITY_Minified Build JS (volunteer)|Minified Build JS (volunteer)]]
- [[_COMMUNITY_Minified Build JS (contact)|Minified Build JS (contact)]]
- [[_COMMUNITY_Components & Layout|Components & Layout]]
- [[_COMMUNITY_DocType Definitions|DocType Definitions]]
- [[_COMMUNITY_API Client Library|API Client Library]]
- [[_COMMUNITY_Seed Data Generation|Seed Data Generation]]
- [[_COMMUNITY_App Metadata|App Metadata]]
- [[_COMMUNITY_Website Context Config|Website Context Config]]
- [[_COMMUNITY_Utils __init__ (empty)|Utils __init__ (empty)]]
- [[_COMMUNITY_Frontend README|Frontend README]]

## God Nodes (most connected - your core abstractions)
1. `Architecture Documentation` - 42 edges
2. `frappe_npo app (external dependency)` - 12 edges
3. `generate_test_data() all DocTypes seeder` - 11 edges
4. `Backend API Module (api.py)` - 11 edges
5. `API Client Module` - 10 edges
6. `apiCall()` - 9 edges
7. `website_route_rules for /api/ proxy` - 9 edges
8. `apiCall Helper` - 9 edges
9. `Volunteer DocType` - 8 edges
10. `Chapter DocType` - 8 edges

## Surprising Connections (you probably didn't know these)
- `Donate Page` --calls--> `Submit Donation API Endpoint`  [INFERRED]
  frontend/src/pages/donate.astro → peace_league_website/api.py
- `Volunteer Page` --calls--> `Submit Volunteer API Endpoint`  [INFERRED]
  frontend/src/pages/volunteer.astro → peace_league_website/api.py
- `Contact Page` --calls--> `Submit Contact API Endpoint`  [INFERRED]
  frontend/src/pages/contact.astro → peace_league_website/api.py
- `Architecture Documentation` --references--> `Program DocType`  [EXTRACTED]
  ARCHITECTURE.md → peace_league_website/api.py
- `GET get_programs API` --references--> `Program DocType`  [EXTRACTED]
  ARCHITECTURE.md → peace_league_website/api.py

## Communities (28 total, 4 thin omitted)

### Community 0 - "Frontend Pages & Architecture"
Cohesion: 0.1
Nodes (43): About Page (/about), apiCall Helper, Backend API Module (api.py), Architecture Documentation, Astro Configuration, Astro Framework, Contact Page (/contact), POST create_donation API (+35 more)

### Community 1 - "API Endpoints (Backend)"
Cohesion: 0.1
Nodes (34): create_chapter() API endpoint, create_donation() API endpoint, create_volunteer() API endpoint, generate_test_data() wrapper, get_chapters() API endpoint, get_homepage_data() aggregated API, get_program_details() API endpoint, get_programs() API endpoint (+26 more)

### Community 2 - "API Endpoints (AST)"
Cohesion: 0.08
Nodes (26): create_chapter(), create_donation(), create_volunteer(), generate_test_data(), get_chapters(), get_homepage_data(), get_program_details(), get_programs() (+18 more)

### Community 3 - "Minified Build JS (donate)"
Cohesion: 0.09
Nodes (21): a(), c(), d(), u(), e, n, o, r (+13 more)

### Community 4 - "Minified Build JS (volunteer)"
Cohesion: 0.09
Nodes (21): a(), d(), p(), u(), e, n, o, r (+13 more)

### Community 5 - "Minified Build JS (contact)"
Cohesion: 0.09
Nodes (21): a(), d(), p(), u(), e, n, o, r (+13 more)

### Community 6 - "Components & Layout"
Cohesion: 0.26
Nodes (18): Footer Component, Layout Component, Navigation Component, About Page, API Client Library, Contact Page, Donate Page, Chapters API Endpoint (+10 more)

### Community 7 - "DocType Definitions"
Cohesion: 0.17
Nodes (9): Chapter DocType, Donation DocType, Peace League Website module, Program DocType, Volunteer DocType, execute(), Frappe Framework Library, frappe_npo dependency (+1 more)

### Community 8 - "API Client Library"
Cohesion: 0.38
Nodes (9): apiCall(), getChapters(), getHomepageData(), getProgramDetails(), getPrograms(), getVolunteers(), submitContact(), submitDonation() (+1 more)

### Community 9 - "Seed Data Generation"
Cohesion: 0.33
Nodes (6): generate_test_data(), _log(), Create sample Email Campaign records for programs., Generate sample test data for frappe_npo doctypes: Members, Donors, Chapters, Vo, Debug logging to frappe's error log., seed_programs()

## Ambiguous Edges - Review These
- `API Client Library` → `Submit Donation API Endpoint`  [AMBIGUOUS]
  None · relation: references
- `API Client Library` → `Submit Volunteer API Endpoint`  [AMBIGUOUS]
  None · relation: references
- `API Client Library` → `Submit Contact API Endpoint`  [AMBIGUOUS]
  None · relation: references

## Knowledge Gaps
- **92 isolated node(s):** `Debug logging to frappe's error log.`, `Get list of active programs for the website using Program DocType.`, `Return sample program data for frontend demo.`, `Create sample Email Campaign records for programs.`, `Get detailed program information.` (+87 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `API Client Library` and `Submit Donation API Endpoint`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `API Client Library` and `Submit Volunteer API Endpoint`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `API Client Library` and `Submit Contact API Endpoint`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **Why does `Architecture Documentation` connect `Frontend Pages & Architecture` to `API Endpoints (Backend)`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `frappe_npo app (external dependency)` (e.g. with `Program DocType` and `Volunteer DocType`) actually correct?**
  _`frappe_npo app (external dependency)` has 11 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Debug logging to frappe's error log.`, `Get list of active programs for the website using Program DocType.`, `Return sample program data for frontend demo.` to the rest of the system?**
  _92 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Frontend Pages & Architecture` be split into smaller, more focused modules?**
  _Cohesion score 0.1 - nodes in this community are weakly interconnected._