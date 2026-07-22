"""
Awards API endpoints for Peace League Website.

Public endpoints:
- get_categories(): list all active award categories
- get_category(slug): get category details and nominees
- create_nomination(...): submit a nomination (with file upload)
- cast_vote(nominee_id, category_slug, email=None): record a vote
- get_results(): get winners after announcement

All endpoints are whitelisted for guest access except the admin ones (if any).
"""

import datetime
import json
from urllib.parse import urljoin

import frappe
from frappe import _
from frappe.utils import now, nowdate
from frappe.utils.file_manager import save_file

logger = frappe.logger("awards", allow_site=True, file_count=5)

# Anti-fraud settings
VOTE_LIMIT_PER_IP = 10  # max categories an IP can vote in
RECAPTCHA_SECRET = frappe.conf.get("recaptcha_secret_key") or ""  # set in site config


# ── Public endpoints ──

@frappe.whitelist(allow_guest=True)
def get_categories():
    """Return all active award categories, ordered by sort_order or name."""
    try:
        categories = frappe.get_list(
            "Award Category",
            filters={"is_active": 1},
            fields=["name", "category_name", "slug", "description", "sort_order"],
            order_by="sort_order asc, category_name asc",
            ignore_permissions=True
        )
        return {"status": "success", "data": categories}
    except Exception as e:
        logger.error(f"Error fetching categories: {e}", exc_info=True)
        return {"status": "error", "message": _("Unable to fetch categories")}


@frappe.whitelist(allow_guest=True)
def get_category(slug):
    """Return category details and list of active nominees."""
    # Find category by slug
    category = frappe.db.get_value(
        "Award Category",
        {"slug": slug, "is_active": 1},
        ["name", "category_name", "slug", "description", "sort_order"],
        as_dict=True
    )
    if not category:
        return {"status": "error", "message": _("Category not found")}

    category_name = category["name"]

    # Fetch nominees for this category
    nominees = frappe.get_list(
        "Award Nominee",
        filters={"category": category_name, "status": "Active"},
        fields=["name", "nominee_name", "description", "photo", "nominee_email", "nominee_phone", "submission_date"],
        order_by="submission_date asc",
        ignore_permissions=True
    )

    # Count votes per nominee via frappe.db.count (safer than raw SQL)
    for n in nominees:
        n["votes"] = frappe.db.count("Award Vote", {"nominee": n.name})
        n["photo_url"] = urljoin(frappe.utils.get_url(), n.photo) if n.photo else None

    return {
        "status": "success",
        "data": {
            "category": category,
            "nominees": nominees
        }
    }


@frappe.whitelist(allow_guest=True)
def create_nomination():
    """
    POST form-data with fields:
    - nominee_name (str, required)
    - category (link to Award Category, required)
    - description (text, required, <=500 chars)
    - photo (file, required, image)
    - nominee_email (str, optional)
    - nominee_phone (str, optional)
    - nominator_name (str, optional)
    - nominator_email (str, optional)
    - recaptcha_token (str) optional for future
    """
    try:
        # Get form fields
        nominee_name = frappe.form_dict.get("nominee_name")
        category_slug = frappe.form_dict.get("category")
        description = frappe.form_dict.get("description")
        photo = frappe.request.files.get("photo")
        nominee_email = frappe.form_dict.get("nominee_email")
        nominee_phone = frappe.form_dict.get("nominee_phone")
        nominator_name = frappe.form_dict.get("nominator_name")
        nominator_email = frappe.form_dict.get("nominator_email")
        # terms acceptance (checkbox)
        terms = frappe.form_dict.get("terms")
        public_consent = frappe.form_dict.get("public_consent")

        # Validate required fields
        if not nominee_name:
            return {"status": "error", "message": _("Nominee name is required")}
        if not category_slug:
            return {"status": "error", "message": _("Category is required")}
        if not description:
            return {"status": "error", "message": _("Description is required")}
        if len(description) > 500:
            return {"status": "error", "message": _("Description must be 500 characters or less")}
        if not photo:
            return {"status": "error", "message": _("Photo is required")}
        if not terms or not public_consent:
            return {"status": "error", "message": _("You must accept the terms and public visibility consent")}

        # Validate category exists
        category_name = frappe.db.get_value("Award Category", {"slug": category_slug, "is_active": 1}, "name")
        if not category_name:
            return {"status": "error", "message": _("Selected category is not active or does not exist")}

        # Optional: reCAPTCHA verification later

        # Create Award Nominee document first; attach photo after insert
        # (save_file needs a docname, so the doc must exist first)
        nominee = frappe.get_doc({
            "doctype": "Award Nominee",
            "nominee_name": nominee_name,
            "category": category_name,
            "description": description,
            "nominee_email": nominee_email,
            "nominee_phone": nominee_phone,
            "nominator_name": nominator_name,
            "nominator_email": nominator_email,
            "status": "Active",
            "submission_date": nowdate(),
            # IP and UA will be set in before_insert if request present
        })
        nominee.insert(ignore_permissions=True)

        # Attach photo to the nominee document
        file_doc = save_file(
            photo.filename, photo.read(),
            "Award Nominee", nominee.name,
            is_private=0,
        )
        nominee.photo = file_doc.file_url
        nominee.save(ignore_permissions=True)
        frappe.db.commit()

        logger.info(f"Award nomination created: {nominee.name} for category {category_name}")

        return {
            "status": "success",
            "message": _("Nomination submitted successfully"),
            "data": {"nominee": nominee.name}
        }
    except Exception as e:
        logger.error(f"Nomination error: {e}", exc_info=True)
        return {"status": "error", "message": _("Failed to submit nomination. Please try again.")}


@frappe.whitelist(allow_guest=True)
def cast_vote(**kwargs):
    """
    Cast a vote for a nominee in a category.
    - nominee_id: name of Award Nominee document
    - category_slug: slug of the category
    - email: optional email for verification (string)

    Enforces:
    - One vote per IP per category (new vote replaces old in same category)
    - Max VOTE_LIMIT_PER_IP total categories voted by this IP
    - Rate limiting via decorator (e.g., 5 votes per minute per IP)
    """
    nominee_id = kwargs.get('nominee_id')
    category_slug = kwargs.get('category_slug')
    email = kwargs.get('email')
    try:
        # Rate limit: max 5 vote attempts per minute per IP
        # We'll wrap the core logic in a rate_limited call (later)
        # For now, we'll manually check using Redis key: rate_limit:vote:<ip>
        ip = frappe.request.remote_addr if frappe.request else "0.0.0.0"
        now_ts = int(now().timestamp())
        # Simple rate limiting: 20 requests per 10 minutes
        rate_key = f"vote_rate:{ip}"
        count = frappe.cache.get(rate_key) or 0
        if count >= 20:
            return {"status": "error", "message": _("Too many vote attempts. Please try again later.")}
        frappe.cache.setex(rate_key, 600, count + 1)  # 10 min TTL

        # Validate nominee exists and is Active
        nominee = frappe.get_doc("Award Nominee", nominee_id)
        if nominee.status != "Active":
            return {"status": "error", "message": _("This nominee is no longer active")}

        # Verify category slug matches nominee's category
        category_doc = frappe.get_doc("Award Category", nominee.category)
        if category_doc.slug != category_slug:
            return {"status": "error", "message": _("Category mismatch")}

        # Check if this IP already voted in this category
        existing_vote = frappe.db.exists(
            "Award Vote",
            {"ip_address": ip, "category": category_doc.name}
        )
        if existing_vote:
            # Update existing vote: change nominee
            vote_doc = frappe.get_doc("Award Vote", existing_vote)
            vote_doc.nominee = nominee_id
            vote_doc.vote_datetime = now()
            vote_doc.user_agent = frappe.request.headers.get('User-Agent') if frappe.request else None
            vote_doc.save(ignore_permissions=True)
            frappe.db.commit()
            return {"status": "success", "message": _("Your vote has been updated")}
        else:
            # Check total distinct categories voted by this IP
            total_votes = frappe.db.count("Award Vote", {"ip_address": ip})
            if total_votes >= VOTE_LIMIT_PER_IP:
                return {"status": "error", "message": _("You have reached the maximum number of categories you can vote in (10).")}

            # Create new vote
            vote = frappe.get_doc({
                "doctype": "Award Vote",
                "nominee": nominee_id,
                "category": category_doc.name,
                "ip_address": ip,
                "email_verified": 0,
                "vote_datetime": now(),
                "user_agent": frappe.request.headers.get('User-Agent') if frappe.request else None,
            })
            vote.insert(ignore_permissions=True)
            frappe.db.commit()

            # Optional: send verification email if email provided
            # (future: use background job)
            if email:
                send_vote_verification_email(email, vote.name)

            logger.info(f"Vote cast: nominee={nominee_id} category={category_doc.name} ip={ip}")
            return {"status": "success", "message": _("Your vote has been recorded")}
    except Exception as e:
        logger.error(f"Vote error: {e}", exc_info=True)
        return {"status": "error", "message": _("Failed to record vote")}


def send_vote_verification_email(email, vote_name):
    """Send an email to verify the voter's email (stub)."""
    # To be implemented: generate token, send email with verification link
    pass


@frappe.whitelist(allow_guest=True)
def get_results():
    """
    Get the results of the awards.
    Before announcement (Dec 5 18:00 EAT), possibly hide or return empty?
    We'll return data only after announced flag is set in a site config or based on datetime.
    """
    try:
        # Check if results are published: could use a Site Config flag or datetime comparison
        # For simplicity, check if current datetime >= 2026-12-05 18:00 EAT (UTC+3)
        # Convert to UTC: 2026-12-05 15:00 UTC
        announce_utc = datetime.datetime(2026, 12, 5, 15, 0, 0)
        now_utc = datetime.datetime.utcnow()
        if now_utc < announce_utc:
            return {"status": "success", "data": {"published": False, "message": "Results not yet published"}}

        # Results published: compute winners per category
        # For each category, find nominee with highest votes
        categories = frappe.get_list("Award Category", fields=["name", "category_name", "slug"])
        results = []
        for cat in categories:
            # Get vote counts per nominee in this category
            vote_counts = frappe.db.sql("""
                SELECT nominee, COUNT(*) as cnt
                FROM `tabAward Vote`
                WHERE category = %s
                GROUP BY nominee
                ORDER BY cnt DESC
                LIMIT 1
            """, cat.name, as_dict=True)
            total = 0
            winner = None
            winner_vote = None
            if vote_counts:
                winner_vote = vote_counts[0]
                winner = frappe.get_doc("Award Nominee", winner_vote.nominee)
                total = frappe.db.count("Award Vote", {"category": cat.name})

            results.append({
                "category": cat.category_name,
                "slug": cat.slug,
                "winner": {
                    "name": winner.nominee_name if winner else None,
                    "photo": urljoin(frappe.utils.get_url(), winner.photo) if winner and winner.photo else None,
                    "votes": winner_vote.cnt if winner_vote else 0,
                    "percentage": (winner_vote.cnt / total * 100) if winner_vote and total else 0
                } if winner else None,
                "total_votes": total
            })

        return {"status": "success", "data": {"published": True, "results": results}}
    except Exception as e:
        logger.error(f"Results error: {e}", exc_info=True)
        return {"status": "error", "message": _("Unable to fetch results")}


# ── Admin endpoints (require login) ──
# We'll use standard Frappe Desk for most admin tasks. These APIs are for custom dashboard only.

@frappe.whitelist()
def admin_get_nominations(filters=None):
    """
    Get nominations with filtering for admin dashboard.
    Expects filters as JSON string or dict: {status, category, search}
    """
    if not frappe.has_permission("Award Nominee", "read"):
        frappe.throw(_("Not permitted"), frappe.PermissionError)

    # filters arrives as a JSON string from @frappe.whitelist()
    if isinstance(filters, str) and filters:
        filters = json.loads(filters)
    filters = filters or {}
    # Build filter dict
    db_filters = {}
    if filters.get("status"):
        db_filters["status"] = filters["status"]
    if filters.get("category"):
        # category could be name or slug; resolve
        cat_name = filters["category"]
        if frappe.db.exists("Award Category", {"slug": filters["category"]}):
            cat_doc = frappe.get_doc("Award Category", {"slug": filters["category"]})
            db_filters["category"] = cat_doc.name
        else:
            db_filters["category"] = filters["category"]
    if filters.get("search"):
        search = filters["search"]
        db_filters["nominee_name"] = ["like", f"%{search}%"]

    nominations = frappe.get_list(
        "Award Nominee",
        filters=db_filters,
        fields=["name", "nominee_name", "category", "description", "photo", "nominee_email", "nominee_phone", "status", "submission_date", "ip_address"],
        order_by="submission_date desc",
        limit_page_length=100
    )
    # Resolve category names
    for n in nominations:
        cat = frappe.get_doc("Award Category", n.category)
        n["category_name"] = cat.category_name
        n["category_slug"] = cat.slug
        if n.photo:
            n["photo_url"] = urljoin(frappe.utils.get_url(), n.photo)
    return {"status": "success", "data": nominations}


@frappe.whitelist()
def admin_delete_nomination(nominee_name):
    """Delete a nomination (and its votes will cascade if set in DocType)."""
    if not frappe.has_permission("Award Nominee", "delete"):
        frappe.throw(_("Not permitted"), frappe.PermissionError)

    nominee = frappe.get_doc("Award Nominee", nominee_name)
    nominee.delete(ignore_permissions=True)
    frappe.db.commit()
    return {"status": "success", "message": _("Nomination deleted")}


@frappe.whitelist()
def admin_update_nomination(nominee_name, **kwargs):
    """Update nomination fields (e.g., status)."""
    if not frappe.has_permission("Award Nominee", "write"):
        frappe.throw(_("Not permitted"), frappe.PermissionError)

    nominee = frappe.get_doc("Award Nominee", nominee_name)
    # Allowed fields
    allowed = ["status", "description", "nominee_email", "nominee_phone", "category"]
    for k, v in kwargs.items():
        if k in allowed:
            nominee.set(k, v)
    nominee.save(ignore_permissions=True)
    frappe.db.commit()
    return {"status": "success", "message": _("Nomination updated")}


@frappe.whitelist()
def admin_get_vote_stats():
    """Return vote counts per category and nominee for admin dashboard."""
    if not frappe.has_permission("Award Vote", "read"):
        frappe.throw(_("Not permitted"), frappe.PermissionError)

    # Get totals per category
    totals = frappe.db.sql("""
        SELECT category, COUNT(*) as total_votes
        FROM `tabAward Vote`
        GROUP BY category
    """, as_dict=True)

    # Get top nominee per category
    top_nominees = frappe.db.sql("""
        SELECT category, nominee, COUNT(*) as cnt
        FROM `tabAward Vote`
        GROUP BY category, nominee
        ORDER BY category, cnt DESC
    """, as_dict=True)

    # Organize
    stats = {}
    for t in totals:
        stats[t.category] = {"total_votes": t.total_votes, "top_nominee": None, "top_votes": 0}

    for row in top_nominees:
        if stats.get(row.category) and stats[row.category]["top_nominee"] is None:
            stats[row.category]["top_nominee"] = row.nominee
            stats[row.category]["top_votes"] = row.cnt

    return {"status": "success", "data": stats}
