# Peace League Africa — Architecture Documentation

## Table of Contents

1. [High-Level Architecture](#1-high-level-architecture)
2. [Directory Structure](#2-directory-structure)
3. [Request Flow](#3-request-flow)
4. [API Endpoints](#4-api-endpoints)
5. [Frontend Pages](#5-frontend-pages)
6. [Database Schema](#6-database-schema)
7. [Deployment Architecture](#7-deployment-architecture)
8. [Security](#8-security)
9. [Development Workflow](#9-development-workflow)

---

## 1. High-Level Architecture

```
┌──────────────────────────────────────────────────────────┐
│                     Browser (User)                        │
│              https://peaceleagueafrica.com                │
└────────────────────────┬─────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────┐
│                    Nginx (port 443)                       │
│                                                          │
│  ┌──────────────────┐     ┌──────────────────────────┐   │
│  │  /               │     │  /api/method/*            │   │
│  │  Static Astro    │     │  Proxy → Gunicorn:8001    │   │
│  │  Frontend (HTML) │     │  + CORS headers           │   │
│  └────────┬─────────┘     └────────────┬──────────────┘   │
└───────────┼────────────────────────────┼──────────────────┘
            │                            │
            ▼                            ▼
┌───────────────────────┐   ┌──────────────────────────┐
│  Astro Static Files   │   │  Gunicorn (port 8001)     │
│  public/astro_pages/  │   │  9 workers, preloaded     │
│                       │   │  frappe.app:application   │
│  Served directly by   │   │                           │
│  nginx, no Python     │   │  Runs Frappe WSGI app     │
└───────────────────────┘   └───────────┬──────────────┘
                                        │
                                        ▼
                            ┌──────────────────────────┐
                            │     Frappe v16.17.5      │
                            │  peace_league_website    │
                            │  Custom App              │
                            │                          │
                            │  ┌──────────────────┐   │
                            │  │ api.py           │   │
                            │  │ @frappe.whitelist│   │
                            │  └──────────────────┘   │
                            │  ┌──────────────────┐   │
                            │  │ frappe_npo       │   │
                            │  │ DocTypes         │   │
                            │  └──────────────────┘   │
                            └───────────┬──────────────┘
                                        │
                    ┌───────────────────┼───────────────────┐
                    ▼                   ▼                   ▼
          ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
          │   MariaDB    │   │    Redis     │   │   Workers    │
          │  (port 3306) │   │ (11000/13000)│   │  (RQ queue)  │
          └──────────────┘   └──────────────┘   └──────────────┘
```

### Key Technologies

| Layer | Technology | Version |
|-------|-----------|---------|
| Frontend Framework | Astro | Latest |
| Styling | TailwindCSS | — |
| Backend Framework | Frappe | v16.17.5 |
| ERP Module | frappe_npo | — |
| Database | MariaDB | — |
| Cache/Queue | Redis | 7.0.15 |
| App Server | Gunicorn | — |
| Web Server | Nginx | 1.24.0 |
| Process Manager | Supervisor | — |
| SSL | Let's Encrypt / Certbot | — |

---

## 2. Directory Structure

```
peace_league_website/
├── frontend/                          # Astro frontend source
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navigation.astro       # Top navigation bar
│   │   │   └── Footer.astro           # Site footer
│   │   ├── layouts/
│   │   │   └── Layout.astro           # Base HTML layout (head, meta, fonts)
│   │   ├── lib/
│   │   │   └── api.js                 # API client (fetch wrappers)
│   │   └── pages/
│   │       ├── index.astro            # Homepage (stats, featured programs)
│   │       ├── about.astro            # About + chapters
│   │       ├── programs.astro         # Programs listing
│   │       ├── donate.astro           # Donation form
│   │       ├── volunteer.astro        # Volunteer application form
│   │       └── contact.astro          # Contact form
│   └── package.json
│
├── peace_league_website/              # Frappe app (backend)
│   ├── api.py                         # All REST API endpoints
│   ├── hooks.py                       # Frappe app hooks config
│   ├── utils/
│   │   ├── __init__.py
│   │   └── seed_data.py               # Test data generation utilities
│   ├── public/
│   │   └── astro_pages/               # Built frontend (served by nginx)
│   ├── patches/
│   │   ├── __init__.py
│   │   └── create_doctypes.py         # DocType creation patch
│   ├── doctype/
│   │   └── volunteer/
│   │       └── volunteer.json         # Volunteer DocType definition
│   └── __init__.py
│
├── pyproject.toml                     # Python package config
├── MANIFEST.in                        # Package manifest
└── ARCHITECTURE.md                    # This file
```

---

## 3. Request Flow

### 3.1 Frontend Page Requests

```
Browser ──GET https://peaceleagueafrica.com/──▶ Nginx (443)
                                                    │
                                              ┌─────┴─────┐
                                              │  location  │
                                              │  /         │
                                              └─────┬─────┘
                                                    │
                                                    ▼
                                              astro_pages/
                                              index.html
                                                    │
                                              Served directly
                                              (no Python exec)
                                                    │
                                              ◀── HTML ────
```

### 3.2 API Requests

```
Browser ──GET https://peaceleagueafrica.com/api/method/peace_league_website.api.get_programs──▶
                                                                                              │
                                                                                              ▼
                                                                                          Nginx (443)
                                                                                              │
                                                                                   ┌──────────┴──────────┐
                                                                                   │  location /api/     │
                                                                                   │  + CORS headers     │
                                                                                   └──────────┬──────────┘
                                                                                              │
                                                                                              ▼
                                                                                     Proxy to :8001
                                                                                              │
                                                                                              ▼
                                                                                    ┌─────────────────┐
                                                                                    │    Gunicorn     │
                                                                                    │  9 preloaded    │
                                                                                    │   workers       │
                                                                                    └────────┬────────┘
                                                                                             │
                                                                                             ▼
                                                                                    ┌─────────────────┐
                                                                                    │  Frappe WSGI    │
                                                                                    │  Site:          │
                                                                                    │  peaceleague    │
                                                                                    │  africa.com     │
                                                                                    └────────┬────────┘
                                                                                             │
                                                                                             ▼
                                                                                    ┌─────────────────┐
                                                                                    │  api.py         │
                                                                                    │  @frappe.whitel-│
                                                                                    │  ist(allow_guest│
                                                                                    │  =True)         │
                                                                                    └────────┬────────┘
                                                                                             │
                                                                                             ▼
                                                                                    ┌─────────────────┐
                                                                                    │  frappe.get_list │
                                                                                    │  / get_doc /    │
                                                                                    │  db.sql         │
                                                                                    └────────┬────────┘
                                                                                             │
                                                                                             ▼
                                                                                        MariaDB
                                                                                             │
                                                                                    ◀── JSON ────
```

### 3.3 Form Submission (Donate/Volunteer/Contact)

```
User fills form ──▶ Browser JS collects FormData ──▶ api.js function
                                                          │
                                                   POST /api/method/...create_donation
                                                   Content-Type: application/json
                                                          │
                                                          ▼
                                                     Nginx proxy ──▶ Gunicorn
                                                          │
                                                          ▼
                                                   @frappe.whitelist(allow_guest=True)
                                                   def create_donation(data):
                                                       # Parse JSON
                                                       # Validate required fields
                                                       # Find or create Donor
                                                       # Create Donation record
                                                       # db.commit()
                                                       return {"status": "success"}
                                                          │
                                                          ▼
                                                   Browser shows success/error message
```

### 3.4 Homepage Data Loading

```
Page Load ──▶ window.onload / <script> at end of body
                  │
                  ▼
         fetch(`${API_BASE_URL}/api/method/...get_homepage_data`)
                  │
                  ▼
         if success:
           - Update #stat-donations with total
           - Update #stat-volunteers with count
           - Update #stat-chapters with chapter count
           - Render 3 featured programs into #programs-container
         if error:
           - Show static mock content (graceful degradation)
```

---

## 4. API Endpoints

All endpoints are in `peace_league_website/api.py`. All are `@frappe.whitelist(allow_guest=True)`.

### 4.1 GET Endpoints

| Endpoint | Returns | Example Response |
|----------|---------|-----------------|
| `get_programs()` | List of programs from `Program` DocType, or sample data if none exist | `{"status":"success","data":[...]}` |
| `get_chapters()` | All published chapters from `Chapter` DocType | `{"status":"success","data":[...]}` |
| `get_volunteers()` | All volunteers from `Volunteer` DocType | `{"status":"success","data":[...]}` |
| `get_homepage_data()` | Programs (from Email Campaign), chapters, stats (total donations + volunteers) | `{"status":"success","data":{"programs":[],"chapters":[],"stats":{}}}` |
| `get_program_details(name)` | Single program detail by name | `{"status":"success","data":{...}}` |

### 4.2 POST Endpoints

| Endpoint | Required Fields | Creates | Example |
|----------|----------------|---------|---------|
| `create_donation(data)` | `donor_name`, `email`, `amount` | `Donor` (if new email) + `Donation` | `{"status":"success","message":"...","data":{"name":"DON-0001"}}` |
| `create_volunteer(data)` | `volunteer_name` or `first_name`+`last_name`, `email`, `volunteer_type` | `Volunteer` + auto-creates `Volunteer Type` if missing | `{"status":"success","message":"...","data":{"name":"..."}}` |
| `submit_contact_form(data)` | `name`, `email`, `subject` | `Lead` with type="Website" | `{"status":"success","message":"...","data":{"lead_id":"..."}}` |
| `create_chapter(data)` | `introduction`, `region`, `address` | `Chapter` | `{"status":"success","message":"...","data":{...}}` |

### 4.3 Internal Endpoints (requires auth)

| Endpoint | Purpose |
|----------|---------|
| `seed_programs()` | Create sample Email Campaign records (for testing) |
| `generate_test_data()` | Generate 35 test records across 7 DocTypes (for testing) |

---

## 5. Frontend Pages

### 5.1 Pages Overview

| Page | Route | API Calls | Purpose |
|------|-------|-----------|---------|
| Home | `/` | `get_homepage_data` | Hero section, impact stats (donations, volunteers, chapters), featured programs |
| About | `/about` | `get_chapters` | Mission, history, values, chapters listing |
| Programs | `/programs` | `get_programs` | Full program listing with status and progress bars |
| Donate | `/donate` | `create_donation` (on submit) | Donation form with preset amounts, payment methods |
| Volunteer | `/volunteer` | `create_volunteer` (on submit) | Volunteer application form with type selection |
| Contact | `/contact` | `submit_contact_form` (on submit) | Contact form + organization info |

### 5.2 API Integration Pattern

**GET pages (home, about, programs):** Client-side fetch on page load. Fallback to static mock content if API is unavailable:

```javascript
// Inline script in .astro page
const API_BASE_URL = window.ENV?.PUBLIC_API_URL || '';
async function fetchData() {
  try {
    const res = await fetch(`${API_BASE_URL}/api/method/peace_league_website.api.get_X`);
    const data = await res.json();
    // Update DOM dynamically
  } catch (e) {
    console.log('API not available, using static content');
  }
}
fetchData();
```

**POST pages (donate, volunteer, contact):** Import `api.js` functions, call on form submit:

```javascript
import { submitDonation } from '../lib/api.js';
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(form));
  const response = await submitDonation(data);
  // Show success/error
});
```

### 5.3 API Client (`api.js`)

```javascript
const API_BASE_URL = import.meta.env.PUBLIC_API_URL || '';
// Uses relative URLs so requests go to same origin
// In production: https://peaceleagueafrica.com/api/method/...
// In dev: set PUBLIC_API_URL=http://localhost:8001
```

---

## 6. Database Schema

The app uses DocTypes from `frappe_npo` (no custom DocTypes were created). Key tables:

```
tabMember
  - member_name, email_id, phone, membership_type, membership_expiry_date

tabDonor
  - donor_name, email, phone_number, donor_type

tabDonation
  - donor (link to Donor), donor_name, email, amount, currency
  - mode_of_payment, date, paid, company

tabVolunteer
  - volunteer_name, email, phone_number, volunteer_type, availability, note

tabVolunteer Type
  - title, amount

tabChapter
  - chapter_name, introduction, chapter_head (link to Member)
  - region, city, address, published

tabLead
  - lead_name, email_id, phone, company_name, status, type

tabProgram (frappe built-in)
  - title, description, image, start_date, end_date, goal_amount, raised_amount

tabEmail Campaign (frappe built-in)
  - campaign_name, email_campaign_for, status, start_date, end_date
```

---

## 7. Deployment Architecture

### 7.1 Process Management (Supervisor)

```
supervisord (root, PID 164821)
├── frappe-bench-redis:cache        Redis on 127.0.0.1:13000
├── frappe-bench-redis:queue        Redis on 127.0.0.1:11000
├── frappe-bench-web:frappe-web     Gunicorn on 127.0.0.1:8001 (9 workers)
├── frappe-bench-web:node-socketio  Socket.IO on 127.0.0.1:9000
├── frappe-bench-workers:long       RQ worker (long queue)
├── frappe-bench-workers:short      RQ worker (short queue)
└── frappe-bench-workers:schedule   RQ scheduler
```

### 7.2 Nginx Configuration

```
Port 80 (HTTP)     → 301 redirect → Port 443 (HTTPS)
Port 443 (HTTPS)   →  /               → Astro static files from astro_pages/
                  →  /api/method/*    → Proxy to Gunicorn :8001
                  →  /assets/*        → Frappe static assets
                  →  /socket.io/*     → Proxy to Socket.IO :9000
                  →  /protected/*     → Internal (Frappe file access)
```

### 7.3 CORS Configuration

Configured in two places:
1. **Nginx**: `add_header Access-Control-Allow-Origin "https://peaceleagueafrica.com"` on `/api/` location
2. **Frappe site config**: `cors_allow_origins: ["https://peaceleagueafrica.com"]`

### 7.4 SSL/TLS

- Certificates from Let's Encrypt (Certbot)
- Auto-renewal via Certbot timer
- HSTS enabled: `Strict-Transport-Security: max-age=63072000; includeSubDomains; preload`

---

## 8. Security

### 8.1 API Security

- All public endpoints use `@frappe.whitelist(allow_guest=True)` — accessible without authentication
- Input validation on all POST endpoints (required field checks, type casting)
- No raw SQL injection vectors (parameterized queries via frappe.db)
- `frappe.flags.ignore_permissions = True` + explicit `ignore_permissions=True` on all query calls
- POST endpoints accept JSON only

### 8.2 Frontend Security

- No CSRF issues — frontend is same-origin (no token-based auth needed for public forms)
- Forms use POST with JSON body
- API errors caught and displayed as user-friendly messages (no raw error exposure)

### 8.3 Infrastructure Security

- HTTPS enforced (HTTP → 301 → HTTPS)
- HSTS preload ready
- SSL certificates from trusted CA (Let's Encrypt)
- Nginx security headers: X-Frame-Options, X-Content-Type-Options, X-XSS-Protection

---

## 9. Development Workflow

### 9.1 Local Development

```bash
# Activate Frappe environment
cd /home/crowd/frappe-bench
source env/bin/activate

# Start Frappe services
bench start

# In another terminal, start Astro dev server
cd apps/peace_league_website/frontend
yarn dev

# Set env var for API URL:
export PUBLIC_API_URL=http://localhost:8001
```

### 9.2 Frontend Build

```bash
cd apps/peace_league_website/frontend
yarn build
# Output goes to dist/
cp -r dist/* ../peace_league_website/public/astro_pages/
```

### 9.3 Server Restart

```bash
# After code changes
sudo supervisorctl restart frappe-bench-web:frappe-bench-frappe-web
sudo nginx -s reload
```

### 9.4 Adding a New API Endpoint

1. Add function to `peace_league_website/api.py` with `@frappe.whitelist(allow_guest=True)`
2. Set `frappe.flags.ignore_permissions = True` at start
3. Use `ignore_permissions=True` in all frappe.get_list / get_doc calls
4. Return `{"status": "success", "data": ...}` or `{"status": "error", "message": ...}`
5. Add client function in `frontend/src/lib/api.js`
6. Call from .astro page via import or inline script

### 9.5 Adding a New Frontend Page

1. Create `.astro` file in `frontend/src/pages/`
2. Import Layout, Navigation, Footer
3. Add fetch script for GET data or form handler for POST
4. Import API functions from `../lib/api.js`
5. Rebuild with `yarn build && cp dist/* ../peace_league_website/public/astro_pages/`

---

## Appendix: Key Ports

| Port | Service | Purpose |
|------|---------|---------|
| 80 | Nginx HTTP | Redirect to HTTPS |
| 443 | Nginx HTTPS | Frontend + API proxy |
| 3306 | MariaDB | Database |
| 6379 | System Redis | Frappe cache |
| 8000 | Bench dev server | Development only |
| 8001 | Gunicorn | Frappe WSGI production |
| 9000 | Node Socket.IO | WebSocket for desk |
| 11000 | Redis Queue | RQ job queue |
| 13000 | Redis Cache | Frappe cache |
