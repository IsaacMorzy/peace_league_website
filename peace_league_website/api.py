import frappe
from frappe import _
from frappe.utils import getdate, now_datetime, get_request_site_address
import json
import re
from peace_league_website.utils.seed_data import seed_causes as _seed_causes, generate_test_data as _generate_test_data
from payments.payment_gateways.doctype.mpesa_settings.mpesa_connector import MpesaConnector
from payments.payment_gateways.doctype.mpesa_settings.mpesa_settings import sanitize_mobile_number

# Import Turnstile verification from awards module (no circular import since api_awards doesn't import from api)
from peace_league_website.api_awards import verify_turnstile

logger = frappe.logger("peace_league", allow_site=True, file_count=5)


def _validate_email(email):
    """Basic email format validation."""
    if not email or not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return False
    return True


def _validate_phone(phone):
    """Validate phone number is in a reasonable format."""
    if not phone:
        return True  # phone is optional
    digits = re.sub(r"\D", "", phone)
    return len(digits) >= 7


def _validate_amount(amount):
    """Validate donation amount is positive and within limits."""
    try:
        amt = float(amount)
        return amt > 0 and amt <= 10000000
    except (TypeError, ValueError):
        return False


@frappe.whitelist(allow_guest=True)
def get_causes():
    """
    GET /api/method/peace_league_website.api.get_causes

    Returns active causes/campaigns for the public website.
    Called by: frontend/src/pages/causes.astro, frontend/src/pages/index.astro
    Graph edges: reads_from: Cause, returns_to: Astro frontend pages
    """
    try:
        frappe.flags.ignore_permissions = True

        causes_list = frappe.get_list(
            "Cause",
            filters={"show_on_website": 1, "is_active": 1},
            fields=["name", "title", "description", "image", "category", "goal_amount", "raised_amount", "status", "is_active", "show_on_website", "start_date", "end_date", "donors_count"],
            order_by="start_date desc",
            ignore_permissions=True
        )

        return {"status": "success", "data": causes_list}

    except Exception as e:
        logger.error(f"Error fetching causes: {e}", exc_info=True)
        return {"status": "success", "data": []}


@frappe.whitelist(allow_guest=True)
def seed_causes(force=0):
    """Create sample Cause records for development. Use force=1 to delete existing first."""
    return _seed_causes(force=bool(int(force)))


@frappe.whitelist(allow_guest=True)
def create_volunteer(**kwargs):
    """
    POST /api/method/peace_league_website.api.create_volunteer

    Create a new volunteer application using frappe_npo Volunteer DocType.
    Called by: frontend/src/pages/volunteer.astro
    Graph edges: creates: Volunteer, Volunteer Type
    """
    try:
        frappe.flags.ignore_permissions = True
        data = {k: v for k, v in kwargs.items()}

        # Cloudflare Turnstile verification
        turnstile_token = data.get('cf_turnstile_response', '')
        if not verify_turnstile(turnstile_token):
            return {"status": "error", "message": _("Verification failed. Please refresh and try again.")}

        # ── Input validation ──
        email = (data.get("email") or "").strip()
        if not email or not _validate_email(email):
            return {"status": "error", "message": _("A valid email is required")}

        full_name = data.get("volunteer_name") or ""
        if not full_name:
            first_name = (data.get("first_name") or "").strip()
            last_name = (data.get("last_name") or "").strip()
            full_name = f"{first_name} {last_name}".strip() or "Anonymous"

        phone = (data.get("phone") or data.get("phone_number") or "").strip()
        if phone and not _validate_phone(phone):
            return {"status": "error", "message": _("Invalid phone number format")}

        volunteer_type_value = data.get("volunteer_type")
        if not volunteer_type_value:
            return {"status": "error", "message": _("Volunteer type is required")}

        # Auto-create Volunteer Type if it doesn't exist
        if not frappe.db.exists("Volunteer Type", volunteer_type_value):
            try:
                vt = frappe.get_doc({
                    "doctype": "Volunteer Type",
                    "title": volunteer_type_value,
                })
                vt.insert(ignore_permissions=True)
            except Exception as e:
                logger.warning(f"Could not auto-create Volunteer Type {volunteer_type_value}: {e}")

        volunteer = frappe.get_doc({
            "doctype": "Volunteer",
            "volunteer_name": full_name,
            "email": email,
            "phone_number": phone,
            "volunteer_type": volunteer_type_value,
            "availability": (data.get("availability") or "").strip(),
            "note": (data.get("note") or data.get("motivation") or "").strip(),
        })
        volunteer.insert(ignore_permissions=True)

        frappe.db.commit()

        return {
            "status": "success",
            "message": _("Volunteer application submitted successfully"),
            "data": {"name": volunteer.name}
        }
    except Exception as e:
        logger.error(f"Error creating volunteer: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=True)
def get_volunteers():
    """
    GET /api/method/peace_league_website.api.get_volunteers

    Get list of all volunteers.
    Called by: admin dashboard
    Graph edges: reads_from: Volunteer
    """
    try:
        frappe.flags.ignore_permissions = True
        volunteers = frappe.get_list(
            "Volunteer",
            filters={},
            fields=["name", "volunteer_name", "email", "phone_number", "volunteer_type", "availability"],
            order_by="creation desc",
            ignore_permissions=True
        )
        return {"status": "success", "data": volunteers}
    except Exception as e:
        logger.error(f"Error fetching volunteers: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=True)
def create_donation(**kwargs):
    """
    POST /api/method/peace_league_website.api.create_donation

    Create a new donation. For M-Pesa, initiates STK Push and returns checkout_request_id.
    Called by: frontend/src/pages/donate.astro
    Graph edges: creates: Donation, Donor, Mode of Payment
    Graph edges: calls: initiate_mpesa_payment, Mpesa Settings, MpesaConnector
    """
    try:
        frappe.flags.ignore_permissions = True
        data = {k: v for k, v in kwargs.items()}

        # Cloudflare Turnstile verification
        turnstile_token = data.get('cf_turnstile_response', '')
        if not verify_turnstile(turnstile_token):
            return {"status": "error", "message": _("Verification failed. Please refresh and try again.")}

        # ── Input validation ──
        donor_name = (data.get("donor_name") or "").strip()
        if not donor_name:
            return {"status": "error", "message": _("Donor name is required")}

        email = (data.get("email") or "").strip()
        if not email or not _validate_email(email):
            return {"status": "error", "message": _("A valid email is required")}

        amount_raw = data.get("amount", 0)
        if not _validate_amount(amount_raw):
            return {"status": "error", "message": _("Amount must be positive and within limits")}
        amount = float(amount_raw)

        phone = (data.get("phone") or "").strip()
        payment_method = (data.get("payment_method") or "Cash").strip()
        cause = data.get("cause") or ""
        is_mpesa = payment_method in ("MPesa", "Mobile Money")

        if is_mpesa and not phone:
            return {"status": "error", "message": _("Phone number is required for M-Pesa payments")}
        if is_mpesa and not _validate_phone(phone):
            return {"status": "error", "message": _("Invalid phone number format for M-Pesa")}

        # ── Find or create Donor ──
        existing_donor = frappe.db.get_value("Donor", {"email": email}, "name")
        if not existing_donor:
            donor = frappe.get_doc({
                "doctype": "Donor",
                "donor_name": donor_name,
                "email": email,
                "phone_number": phone,
                "donor_type": "Individual",
            })
            donor.insert(ignore_permissions=True)
            donor_doc_name = donor.name
        else:
            donor_doc_name = existing_donor

        # ── Find or create Mode of Payment ──
        mop_value = "MPesa" if is_mpesa else payment_method
        if mop_value and not frappe.db.exists("Mode of Payment", mop_value):
            try:
                mop = frappe.get_doc({"doctype": "Mode of Payment", "mode_of_payment": mop_value, "type": "General"})
                mop.insert(ignore_permissions=True)
            except Exception:
                mop_value = "Cash"

        # ── Create Donation ──
        donation = frappe.get_doc({
            "doctype": "Donation",
            "donor": donor_doc_name,
            "donor_name": donor_name,
            "email": email,
            "phone": phone,
            "amount": amount,
            "currency": data.get("currency", "USD"),
            "mode_of_payment": mop_value,
            "payment_method": "MPesa" if is_mpesa else payment_method,
            "date": getdate(),
            "paid": 0 if is_mpesa else 1,
            "status": "Pending" if is_mpesa else "Received",
            "message": (data.get("message") or "").strip(),
            "anonymous": 1 if str(data.get("anonymous", "0")) == "1" else 0,
            "cause": cause,
        })
        donation.insert(ignore_permissions=True)

        # ── M-Pesa STK Push ──
        if is_mpesa:
            result = initiate_mpesa_payment(donation, phone, amount)
            if result.get("error"):
                frappe.db.commit()
                return {"status": "error", "message": result["error"]}

            donation.checkout_request_id = result["checkout_request_id"]
            donation.save(ignore_permissions=True)
            frappe.db.commit()

            return {
                "status": "success",
                "message": _("M-Pesa prompt sent to your phone. Complete payment on your phone."),
                "data": {
                    "name": donation.name,
                    "donor": donor_name,
                    "checkout_request_id": result["checkout_request_id"],
                    "mpesa_pending": True,
                }
            }

        frappe.db.commit()

        return {
            "status": "success",
            "message": _("Donation recorded successfully"),
            "data": {"name": donation.name, "donor": donor_name}
        }
    except Exception as e:
        logger.error(f"Error creating donation: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=True)
def submit_contact_form(**kwargs):
    """
    POST /api/method/peace_league_website.api.submit_contact_form

    Submit contact form and create a Lead.
    Called by: frontend/src/pages/contact.astro
    Graph edges: creates: Lead
    """
    try:
        frappe.flags.ignore_permissions = True
        data = {k: v for k, v in kwargs.items()}

        # Cloudflare Turnstile verification
        turnstile_token = data.get('cf_turnstile_response', '')
        if not verify_turnstile(turnstile_token):
            return {"status": "error", "message": _("Verification failed. Please refresh and try again.")}

        # ── Input validation ──
        name = (data.get("name") or "").strip()
        if not name:
            return {"status": "error", "message": _("Name is required")}

        email = (data.get("email") or "").strip()
        if not email or not _validate_email(email):
            return {"status": "error", "message": _("A valid email is required")}

        subject = (data.get("subject") or "").strip()
        if not subject:
            return {"status": "error", "message": _("Subject is required")}

        phone = (data.get("phone") or "").strip()
        if phone and not _validate_phone(phone):
            return {"status": "error", "message": _("Invalid phone number format")}

        lead = frappe.get_doc({
            "doctype": "Lead",
            "lead_name": name,
            "email_id": email,
            "phone": phone,
            "company_name": (data.get("company") or "").strip(),
            "status": "Open",
            "type": "Client",
            "lead_owner": "Administrator",
        })
        lead.insert(ignore_permissions=True)

        frappe.db.commit()

        return {
            "status": "success",
            "message": _("Your message has been sent. We'll get back to you soon!"),
            "data": {"lead_id": lead.name}
        }
    except Exception as e:
        logger.error(f"Error submitting contact form: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=True)
def get_chapters():
    """
    GET /api/method/peace_league_website.api.get_chapters

    Get list of active chapters using Chapter DocType.
    Called by: frontend/src/pages/about.astro
    Graph edges: reads_from: Chapter
    """
    try:
        frappe.flags.ignore_permissions = True
        chapters = frappe.get_list(
            "Chapter",
            filters={"published": 1},
            fields=["name", "introduction", "region", "address"],
            order_by="region",
            ignore_permissions=True
        )
        return {"status": "success", "data": chapters}
    except Exception as e:
        logger.error(f"Error fetching chapters: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=True)
def create_chapter(**kwargs):
    """
    POST /api/method/peace_league_website.api.create_chapter

    Create a new chapter using Chapter DocType.
    Called by: admin dashboard
    Graph edges: creates: Chapter, references: Member
    """
    try:
        frappe.flags.ignore_permissions = True
        data = {k: v for k, v in kwargs.items()}

        # ── Input validation ──
        introduction = (data.get("introduction") or "").strip()
        region = (data.get("region") or "").strip()
        address = (data.get("address") or "").strip()

        if not introduction:
            return {"status": "error", "message": _("Chapter introduction is required")}
        if not region:
            return {"status": "error", "message": _("Region is required")}
        if not address:
            return {"status": "error", "message": _("Address is required")}

        chapter_head = data.get("chapter_head")
        if not chapter_head:
            members = frappe.get_all("Member", fields=["name"], order_by="creation asc", limit=1, ignore_permissions=True)
            if members:
                chapter_head = members[0].name

        chapter_name = (data.get("chapter_name") or introduction).strip()

        chapter = frappe.get_doc({
            "doctype": "Chapter",
            "naming_series": "NPO-CHAP-.YYYY.-",
            "introduction": introduction,
            "chapter_name": chapter_name,
            "chapter_head": chapter_head,
            "region": region,
            "city": (data.get("city") or "").strip(),
            "address": address,
            "published": data.get("published", 1),
        })
        chapter.insert(ignore_permissions=True)

        frappe.db.commit()

        return {
            "status": "success",
            "message": _("Chapter created successfully"),
            "data": {"name": chapter.name, "introduction": chapter.introduction, "region": chapter.region}
        }
    except Exception as e:
        logger.error(f"Error creating chapter: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=True)
def get_homepage_data():
    """
    GET /api/method/peace_league_website.api.get_homepage_data

    Aggregate homepage data from multiple DocTypes.
    Called by: frontend/src/pages/index.astro
    Graph edges: reads_from: Cause, Chapter, Donation, Volunteer
    """
    try:
        frappe.flags.ignore_permissions = True

        causes = get_causes()["data"] if get_causes()["status"] == "success" else []

        chapters = frappe.get_list(
            "Chapter",
            filters={"published": 1},
            fields=["name", "introduction", "region"],
            limit=5,
            ignore_permissions=True
        )

        total_donations = frappe.db.sql(
            "SELECT COALESCE(SUM(amount), 0) FROM `tabDonation` WHERE paid = 1"
        )[0][0] or 0

        total_volunteers = frappe.db.count("Volunteer") or 0

        return {
            "status": "success",
            "data": {
                "causes": causes,
                "chapters": chapters,
                "stats": {
                    "total_donations": float(total_donations) if total_donations else 0,
                    "total_volunteers": total_volunteers,
                }
            }
        }
    except Exception as e:
        logger.error(f"Error fetching homepage data: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}


def initiate_mpesa_payment(donation, phone, amount):
    """
    Initiate M-Pesa STK Push for a donation.

    Graph edges: calls: Mpesa Settings, MpesaConnector.stk_push
    Graph edges: callback_to: peace_league_website.api.mpesa_donation_callback
    """
    try:
        mpesa_settings_name = frappe.db.get_value("Mpesa Settings", {}, "name")
        if not mpesa_settings_name:
            return {"error": "M-Pesa is not configured. Please contact the site administrator."}

        mpesa_settings = frappe.get_doc("Mpesa Settings", mpesa_settings_name)
        env = "production" if not mpesa_settings.sandbox else "sandbox"
        business_shortcode = (
            mpesa_settings.business_shortcode if env == "production" else mpesa_settings.till_number
        )

        callback_url = (
            get_request_site_address(True)
            + "/api/method/peace_league_website.api.mpesa_donation_callback"
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
            description="Donation",
        )

        if response.get("ResponseCode") == "0":
            return {"checkout_request_id": response["CheckoutRequestID"]}
        else:
            error_msg = response.get("ResponseDescription", "M-Pesa request failed")
            logger.error(f"M-Pesa STK Push failed: {error_msg}")
            return {"error": error_msg}

    except Exception as e:
        logger.error(f"M-Pesa initiation error: {e}", exc_info=True)
        return {"error": str(e)}


@frappe.whitelist(allow_guest=True)
def mpesa_donation_callback(**kwargs):
    """
    POST callback from Safaricom M-Pesa STK Push results.

    Called by: Safaricom M-Pesa API (external)
    Graph edges: updates: Donation (paid, status, mpesa_receipt)
    Graph edges: called_by: Safaricom M-Pesa
    """
    try:
        frappe.flags.ignore_permissions = True
        raw = frappe.get_json()
        body = frappe._dict(raw.get("Body", {}))
        stk_callback = frappe._dict(body.get("stkCallback", {}))

        checkout_request_id = stk_callback.get("CheckoutRequestID")
        result_code = stk_callback.get("ResultCode", 1)

        if not checkout_request_id:
            logger.error("M-Pesa callback missing CheckoutRequestID")
            return {"ResultCode": 1, "ResultDesc": "Missing CheckoutRequestID"}

        donation_name = frappe.db.get_value("Donation", {"checkout_request_id": checkout_request_id}, "name")
        if not donation_name:
            logger.error(f"No donation found for CheckoutRequestID: {checkout_request_id}")
            return {"ResultCode": 1, "ResultDesc": "Donation not found"}

        donation = frappe.get_doc("Donation", donation_name)

        if result_code == 0:
            metadata = stk_callback.get("CallbackMetadata", {}).get("Item", [])
            mpesa_receipt = None
            for item in metadata:
                if item.get("Name") == "MpesaReceiptNumber":
                    mpesa_receipt = item.get("Value")
                    break

            donation.paid = 1
            donation.status = "Received"
            if mpesa_receipt:
                donation.mpesa_receipt = mpesa_receipt
            donation.save(ignore_permissions=True)
            frappe.db.commit()

            logger.info(f"M-Pesa donation {donation_name} completed. Receipt: {mpesa_receipt}")
        else:
            result_desc = stk_callback.get("ResultDesc", "Payment failed")
            donation.status = "Failed"
            donation.save(ignore_permissions=True)
            frappe.db.commit()

            logger.warning(f"M-Pesa donation {donation_name} failed: {result_desc}")

        return {"ResultCode": 0, "ResultDesc": "Success"}

    except Exception as e:
        logger.error(f"M-Pesa callback error: {e}", exc_info=True)
        return {"ResultCode": 1, "ResultDesc": "Internal error"}


@frappe.whitelist(allow_guest=True)
def donation_status(checkout_request_id):
    """
    GET /api/method/peace_league_website.api.donation_status

    Check the status of an M-Pesa donation by checkout_request_id.
    Called by: frontend/src/pages/donate.astro (polling after M-Pesa)
    Graph edges: reads_from: Donation
    """
    try:
        frappe.flags.ignore_permissions = True

        if not checkout_request_id:
            return {"status": "error", "message": _("Missing checkout request ID")}

        donation_name = frappe.db.get_value(
            "Donation",
            {"checkout_request_id": checkout_request_id},
            "name"
        )
        if not donation_name:
            return {"status": "error", "message": _("Donation not found")}

        donation = frappe.get_doc("Donation", donation_name)

        return {
            "status": "success",
            "data": {
                "paid": bool(donation.paid),
                "status": donation.status,
                "receipt": donation.mpesa_receipt or "",
                "donor_name": donation.donor_name,
                "amount": donation.amount,
            }
        }
    except Exception as e:
        logger.error(f"Donation status error: {e}", exc_info=True)
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def generate_test_data():
    """
    POST /api/method/peace_league_website.api.generate_test_data

    Generate sample test data for all DocTypes.
    Graph edges: creates: Member, Donor, Chapter, Volunteer, Donation, Volunteer Type
    """
    return _generate_test_data()
