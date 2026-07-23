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
import re
from urllib.parse import urljoin

import frappe
from frappe import _
from frappe.utils import now, nowdate, get_request_site_address
from frappe.utils.file_manager import save_file
from payments.payment_gateways.doctype.mpesa_settings.mpesa_connector import MpesaConnector
from payments.payment_gateways.doctype.mpesa_settings.mpesa_settings import sanitize_mobile_number

logger = frappe.logger("awards", allow_site=True, file_count=5)

# Anti-fraud settings
VOTE_LIMIT_PER_IP = 10  # max categories an IP can vote in
TURNSTILE_SECRET_KEY = frappe.conf.get("turnstile_secret_key") or ""  # set in site config


def verify_turnstile(token):
    """Verify a Cloudflare Turnstile token with Cloudflare's API.

    Returns True if the token is valid.
    Falls back to allowing the request if TURNSTILE_SECRET_KEY is not configured,
    so the site works in dev/CI without Turnstile keys.
    """
    if not TURNSTILE_SECRET_KEY:
        logger.info("Turnstile not configured — skipping verification.")
        return True
    if not token:
        logger.warning("Turnstile token missing.")
        return False

    try:
        import requests as http
        resp = http.post(
            "https://challenges.cloudflare.com/turnstile/v0/siteverify",
            data={
                "secret": TURNSTILE_SECRET_KEY,
                "response": token,
                "remoteip": frappe.request.remote_addr if frappe.request else "",
            },
            timeout=10,
        )
        result = resp.json()
        success = result.get("success", False)
        if not success:
            error_codes = result.get("error-codes", [])
            logger.warning(f"Turnstile verification failed: {error_codes}")
            return False
        return True
    except Exception as e:
        logger.error(f"Turnstile request error: {e}")
        # Fallback: allow on network error (don't block legitimate users for transient issues)
        return True


# ── Public endpoints ──

@frappe.whitelist(allow_guest=True)
def get_categories():
    """Return all active award categories with nominee counts, ordered by sort_order or name."""
    try:
        categories = frappe.get_list(
            "Award Category",
            filters={"is_active": 1},
            fields=["name", "category_name", "slug", "description", "sort_order"],
            order_by="sort_order asc, category_name asc",
            ignore_permissions=True
        )
        # ponytail: single SQL query for all nominee counts, avoid N+1
        cat_names = [c.name for c in categories]
        if cat_names:
            counts = frappe.db.sql(
                """
                SELECT category, COUNT(*) as cnt
                FROM `tabAward Nominee`
                WHERE category IN %s AND status = 'Active'
                GROUP BY category
                """,
                [cat_names],
                as_dict=True
            )
            count_map = {c.category: c.cnt for c in counts}
            for cat in categories:
                cat["nominee_count"] = count_map.get(cat.name, 0)
        else:
            for cat in categories:
                cat["nominee_count"] = 0

        return {"status": "success", "data": categories}
    except Exception as e:
        logger.error(f"Error fetching categories: {e}", exc_info=True)
        return {"status": "error", "message": _("Unable to fetch categories")}


@frappe.whitelist(allow_guest=True)
def get_category(slug):
    """Return category details and list of active nominees."""
    try:
        # Use get_list — same pattern as working get_categories
        cats = frappe.get_list(
            "Award Category",
            filters={"slug": slug, "is_active": 1},
            fields=["name", "slug", "description", "sort_order"],
            limit=1,
            ignore_permissions=True
        )
        if not cats:
            return {"status": "error", "message": _("Category not found")}

        cat = cats[0]
        # autoname is field:category_name, so cat.name == category_name value
        cat["category_name"] = cat.name

        # Fetch nominees
        nominees = frappe.get_list(
            "Award Nominee",
            filters={"category": cat.name, "status": "Active"},
            fields=["name", "nominee_name", "description", "photo", "submission_date"],
            order_by="submission_date asc",
            ignore_permissions=True
        )

        # Aggregate vote counts in a single query to avoid N+1
        nominee_names = [n.name for n in nominees]
        vote_counts = {}
        if nominee_names:
            counts = frappe.db.sql(
                """
                SELECT nominee, COUNT(*) as cnt
                FROM `tabAward Vote`
                WHERE nominee IN %s
                GROUP BY nominee
                """,
                [nominee_names],
                as_dict=True
            )
            vote_counts = {vc.nominee: vc.cnt for vc in counts}

        for n in nominees:
            n["votes"] = vote_counts.get(n.name, 0)
            n["photo_url"] = urljoin(frappe.utils.get_url(), n.photo) if n.photo else None

        return {
            "status": "success",
            "data": {
                "category": cat,
                "nominees": nominees
            }
        }
    except Exception as e:
        logger.error(f"Error fetching category {slug}: {e}", exc_info=True)
        return {"status": "error", "message": _("Unable to fetch category")}


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
    - cf-turnstile-response (str) Cloudflare Turnstile token
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
        # ponytail: enforce the frontend's 5MB cap on the backend too (clients can lie)
        # ponytail: shrink, upgrade by using Content-Length header to avoid reading 5MB twice
        photo_max = 5 * 1024 * 1024
        try:
            photo_size = len(photo.read()) if photo and photo.filename else 0
            # Reset stream position so the subsequent save_file can read it again
            if hasattr(photo, "stream") and hasattr(photo.stream, "seek"):
                photo.stream.seek(0)
        except Exception:
            photo_size = 0
        if photo_size > photo_max:
            return {"status": "error", "message": _("Photo is too large. Maximum size is 5MB.")}

        if not terms or not public_consent:
            return {"status": "error", "message": _("You must accept the terms and public visibility consent")}

        # Validate category exists
        category_name = frappe.db.get_value("Award Category", {"slug": category_slug, "is_active": 1}, "name")
        if not category_name:
            return {"status": "error", "message": _("Selected category is not active or does not exist")}

        # Cloudflare Turnstile verification
        turnstile_token = frappe.form_dict.get("cf-turnstile-response")
        if not verify_turnstile(turnstile_token):
            return {"status": "error", "message": _("Verification failed. Please refresh and try again.")}

        # ── Create Award Nominee document ──
        # Photo is non-mandatory at DocType level (GH #126 migration).
        # Insert the doc first, then attach the photo to its generated docname
        # so the File doc gets proper referential integrity.

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
        })
        nominee.insert(ignore_permissions=True)
        frappe.db.commit()

        # ── Attach photo to the real docname (proper File link) ──
        try:
            file_doc = save_file(
                photo.filename, photo.read(),
                "Award Nominee", nominee.name,
                is_private=0,
            )
            # Photo non-mandatory (PR #127); save(ignore_permissions=True) mirrors
            # db_set's permission + hook bypass for the public-guest endpoint.
            # Commit restores the original db_set path's transactional boundary.
            nominee.photo = file_doc.file_url
            nominee.save(ignore_permissions=True)
            frappe.db.commit()
        except Exception as file_err:
            logger.error(f"Photo attach failed for nominee {nominee.name}: {file_err}")
            try:
                frappe.delete_doc("Award Nominee", nominee.name, ignore_permissions=True, force=True)
                frappe.db.commit()
            except Exception as cleanup_err:
                logger.error(f"Failed to cleanup orphan nominee {nominee.name}: {cleanup_err}")
            return {"status": "error", "message": _("Photo upload failed. Please try again.")}

        logger.info(f"Award nomination created: {nominee.name} for category {category_name}")

        return {
            "status": "success",
            "message": _("Nomination submitted successfully"),
            "data": {"nominee": nominee.name, "photo": file_doc.file_url}
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
    - cf_turnstile_response: Cloudflare Turnstile token (required when configured)

    Enforces:
    - Turnstile bot check (when configured)
    - One vote per IP per category (new vote replaces old in same category)
    - Max VOTE_LIMIT_PER_IP total categories voted by this IP
    - Rate limiting via decorator (e.g., 5 votes per minute per IP)
    """
    nominee_id = kwargs.get('nominee_id')
    category_slug = kwargs.get('category_slug')
    email = kwargs.get('email')
    turnstile_token = kwargs.get('cf_turnstile_response', '')
    try:
        # Cloudflare Turnstile verification
        if not verify_turnstile(turnstile_token):
            return {"status": "error", "message": _("Verification failed. Please refresh and try again.")}

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
    Before announcement (Dec 17 10:00 AM EAT), possibly hide or return empty?
    We'll return data only after announced flag is set in a site config or based on datetime.
    """
    try:
        # Check if results are published: could use a Site Config flag or datetime comparison
        # For simplicity, check if current datetime >= 2026-12-17 10:00 AM EAT (UTC+3)
        # Convert to UTC: 2026-12-17 07:00 UTC
        announce_utc = datetime.datetime(2026, 12, 17, 7, 0, 0)
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


@frappe.whitelist(allow_guest=True)
def purchase_ticket(**kwargs):
    """
    Purchase a ticket for the Awards Gala. For M-Pesa, initiates STK Push.
    
    Expected kwargs:
    - ticket_tier: 'premium', 'standard', 'early_bird'
    - quantity: int
    - attendee_name: str
    - attendee_email: str
    - attendee_phone: str
    - special_requests: str (optional)
    - payment_method: 'mpesa', 'card', 'bank'
    - amount: float
    """
    try:
        frappe.flags.ignore_permissions = True
        # Cloudflare Turnstile verification
        turnstile_token = kwargs.get('cf_turnstile_response', '')
        if not verify_turnstile(turnstile_token):
            return {"status": "error", "message": _("Verification failed. Please refresh and try again.")}

        ticket_tier = kwargs.get('ticket_tier')
        quantity = int(kwargs.get('quantity', 1))
        attendee_name = kwargs.get('attendee_name')
        attendee_email = kwargs.get('attendee_email')
        attendee_phone = kwargs.get('attendee_phone')
        special_requests = kwargs.get('special_requests', '')
        payment_method = kwargs.get('payment_method', 'mpesa')
        amount = float(kwargs.get('amount', 0))
        # ponytail: map frontend values to DocType select options
        payment_method = {'mpesa': 'M-Pesa', 'card': 'Card', 'bank': 'Bank Transfer'}.get(payment_method, payment_method)
        is_mpesa = payment_method == 'M-Pesa'

        name_map = {'premium': 'Premium Seat', 'standard': 'Standard Seat', 'early_bird': 'Early Bird Standard Seat'}

        # Validate required fields
        if not attendee_name:
            return {"status": "error", "message": _("Attendee name is required")}
        if not attendee_email:
            return {"status": "error", "message": _("Email is required")}
        if not attendee_phone:
            return {"status": "error", "message": _("Phone number is required")}
        if ticket_tier not in ('premium', 'standard', 'early_bird'):
            return {"status": "error", "message": _("Invalid ticket tier")}
        if quantity < 1 or quantity > 10:
            return {"status": "error", "message": _("Quantity must be between 1 and 10")}
        # All tiers are available for purchase
        # ponytail: remove sold-out restriction — all tiers selectable

        # ── Store ticket purchase in a simple log table ──
        # ponytail: use SQL INSERT into a lightweight log; upgrade to proper doctype later
        checkout_id = None
        if is_mpesa:
            checkout_id = _initiate_mpesa_ticket_stk(attendee_phone, amount, attendee_name)
            if not checkout_id:
                return {"status": "error", "message": _("M-Pesa payment initiation failed. Please try again.")}

        frappe.db.sql(
            """
            INSERT INTO `tabAward Ticket Purchase` (name, ticket_tier, quantity, attendee_name,
                attendee_email, attendee_phone, special_requests, payment_method, amount,
                status, checkout_request_id, creation, modified)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
            """,
            [
                frappe.generate_hash(length=15),
                ticket_tier,
                quantity,
                attendee_name,
                attendee_email,
                attendee_phone,
                special_requests,
                payment_method,
                amount,
                "Pending Payment" if is_mpesa else "Confirmed",
                checkout_id or "",
            ],
        )
        frappe.db.commit()

        logger.info(f"Ticket purchase: {attendee_name} — {quantity}x {ticket_tier} — {payment_method}")

        # ── Send confirmation email (non-blocking) ──
        try:
            payment_note = "Complete payment on your phone to confirm." if is_mpesa else "Payment confirmed."
            frappe.sendmail(
                recipients=[attendee_email],
                subject="Peace League Awards Gala — Ticket Confirmation",
                message=f"""Dear {attendee_name},

Thank you for purchasing {quantity}x {name_map[ticket_tier]} ticket(s) to the Peace League Africa Awards Gala 2026!

Event: Peace League Africa Awards Gala
Date: December 17, 2026
Time: 10:00 AM EAT
Venue: August 7th Memorial Park (next to Cooperative Bank), Nairobi
Ticket: {name_map[ticket_tier]}
Quantity: {quantity}
Amount: KES {amount:,.0f}
Payment Method: {payment_method.upper()}
Status: {payment_note}

{f'Special requests: {special_requests}' if special_requests else ''}

If you have any questions, reply to this email or contact us at info@peaceleagueafrica.org.

See you at the gala!

— The Peace League Africa Team
"""
            )
        except Exception as mail_err:
            logger.warning(f"Ticket confirmation email failed for {attendee_email}: {mail_err}")

        if is_mpesa:
            return {
                "status": "success",
                "message": _("M-Pesa prompt sent to your phone. Complete payment on your phone."),
                "data": {
                    "ticket_tier": ticket_tier,
                    "quantity": quantity,
                    "amount": amount,
                    "checkout_request_id": checkout_id,
                    "mpesa_pending": True,
                }
            }

        return {
            "status": "success",
            "message": _("Your ticket order has been confirmed!"),
            "data": {"ticket_tier": ticket_tier, "quantity": quantity, "amount": amount}
        }
    except Exception as e:
        logger.error(f"Ticket purchase error: {e}", exc_info=True)
        return {"status": "error", "message": _("Failed to process ticket order")}


def _initiate_mpesa_ticket_stk(phone, amount, customer_name):
    """Initiate M-Pesa STK Push for a ticket purchase. Returns checkout_request_id or None."""
    try:
        mpesa_settings_name = frappe.db.get_value("Mpesa Settings", {}, "name")
        if not mpesa_settings_name:
            logger.error("M-Pesa not configured for ticket purchase")
            return None

        mpesa_settings = frappe.get_doc("Mpesa Settings", mpesa_settings_name)
        env = "production" if not mpesa_settings.sandbox else "sandbox"
        business_shortcode = (
            mpesa_settings.business_shortcode if env == "production" else mpesa_settings.till_number
        )

        callback_url = (
            get_request_site_address(True)
            + "/api/method/peace_league_website.api_awards.mpesa_ticket_callback"
        )

        connector = MpesaConnector(
            env=env,
            app_key=mpesa_settings.consumer_key,
            app_secret=mpesa_settings.get_password("consumer_secret"),
        )

        mobile_number = sanitize_mobile_number(phone)

        response = connector.stk_push(
            business_shortcode=business_shortcode,
            amount=int(amount),
            passcode=mpesa_settings.get_password("online_passkey"),
            callback_url=callback_url,
            reference_code=mpesa_settings.till_number,
            phone_number=mobile_number,
            description="Awards Gala Ticket",
        )

        if response.get("ResponseCode") == "0":
            return response["CheckoutRequestID"]
        else:
            logger.error(f"M-Pesa STK Push failed for ticket: {response.get('ResponseDescription')}")
            return None
    except Exception as e:
        logger.error(f"M-Pesa ticket STK error: {e}", exc_info=True)
        return None


@frappe.whitelist(allow_guest=True)
def ticket_payment_status(checkout_request_id):
    """
    GET /api/method/peace_league_website.api_awards.ticket_payment_status
    Poll the status of an M-Pesa ticket payment.
    """
    try:
        frappe.flags.ignore_permissions = True
        if not checkout_request_id:
            return {"status": "error", "message": _("Missing checkout request ID")}

        row = frappe.db.sql(
            """
            SELECT status, amount FROM `tabAward Ticket Purchase`
            WHERE checkout_request_id = %s LIMIT 1
            """,
            [checkout_request_id],
            as_dict=True,
        )
        if not row:
            return {"status": "error", "message": _("Ticket purchase not found")}

        purchase = row[0]
        return {
            "status": "success",
            "data": {
                "paid": purchase.status == "Paid",
                "status": purchase.status,
                "amount": float(purchase.amount),
            }
        }
    except Exception as e:
        logger.error(f"Ticket payment status error: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=True, methods=["POST"])
def mpesa_ticket_callback(**kwargs):
    """
    POST callback from Safaricom M-Pesa STK Push for ticket purchases.
    Updates the Award Ticket Purchase status to Paid or Failed.
    """
    try:
        frappe.flags.ignore_permissions = True
        raw = frappe.get_json()
        body = frappe._dict(raw.get("Body", {}))
        stk_callback = frappe._dict(body.get("stkCallback", {}))

        checkout_request_id = stk_callback.get("CheckoutRequestID")
        result_code = stk_callback.get("ResultCode", 1)

        if not checkout_request_id:
            return {"ResultCode": 1, "ResultDesc": "Missing CheckoutRequestID"}

        if result_code == 0:
            metadata = stk_callback.get("CallbackMetadata", {}).get("Item", [])
            mpesa_receipt = None
            for item in metadata:
                if item.get("Name") == "MpesaReceiptNumber":
                    mpesa_receipt = item.get("Value")
                    break

            frappe.db.sql(
                """
                UPDATE `tabAward Ticket Purchase`
                SET status = 'Paid', mpesa_receipt = %s, modified = NOW()
                WHERE checkout_request_id = %s
                """,
                [mpesa_receipt or "", checkout_request_id],
            )
            frappe.db.commit()
            logger.info(f"M-Pesa ticket payment completed: {checkout_request_id} receipt={mpesa_receipt}")
        else:
            result_desc = stk_callback.get("ResultDesc", "Payment failed")
            frappe.db.sql(
                """
                UPDATE `tabAward Ticket Purchase`
                SET status = 'Failed', modified = NOW()
                WHERE checkout_request_id = %s
                """,
                [checkout_request_id],
            )
            frappe.db.commit()
            logger.warning(f"M-Pesa ticket payment failed: {checkout_request_id} — {result_desc}")

        return {"ResultCode": 0, "ResultDesc": "Success"}
    except Exception as e:
        logger.error(f"M-Pesa ticket callback error: {e}", exc_info=True)
        return {"ResultCode": 1, "ResultDesc": "Internal error"}


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
