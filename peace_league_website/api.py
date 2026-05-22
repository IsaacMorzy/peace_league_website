import frappe
from frappe import _
from frappe.utils import getdate, now_datetime, get_request_site_address
import json
from peace_league_website.utils.seed_data import seed_causes as _seed_causes, generate_test_data as _generate_test_data
from payments.payment_gateways.doctype.mpesa_settings.mpesa_connector import MpesaConnector
from payments.payment_gateways.doctype.mpesa_settings.mpesa_settings import sanitize_mobile_number


def _log(level, msg):
    try:
        with open("/tmp/gt_debug.log", "a") as f:
            f.write(f"[{level}] {msg}\n")
    except Exception:
        pass


@frappe.whitelist(allow_guest=True)
def get_causes():
    """Get list of active causes using Cause DocType."""
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
        frappe.log_error(f"Error fetching causes: {str(e)}")
        return {"status": "success", "data": []}


@frappe.whitelist(allow_guest=True)
def seed_causes(force=0):
    """Create sample Cause records for development. Use force=1 to delete existing first."""
    return _seed_causes(force=bool(int(force)))


@frappe.whitelist(allow_guest=True)
def create_volunteer(**kwargs):
    """Create a new volunteer application using frappe_npo Volunteer DocType."""
    try:
        frappe.flags.ignore_permissions = True
        data = {k: v for k, v in kwargs.items()}

        full_name = data.get("volunteer_name")
        if not full_name:
            first_name = data.get("first_name", "")
            last_name = data.get("last_name", "")
            full_name = f"{first_name} {last_name}".strip() or "Anonymous"

        phone = data.get("phone") or data.get("phone_number") or ""

        volunteer_type_value = data.get("volunteer_type")
        if volunteer_type_value:
            if not frappe.db.exists("Volunteer Type", volunteer_type_value):
                try:
                    vt = frappe.get_doc({
                        "doctype": "Volunteer Type",
                        "name": volunteer_type_value,
                        "amount": 0
                    })
                    vt.insert(ignore_permissions=True)
                except Exception:
                    pass

        required_fields = ["email", "volunteer_type"]
        for field in required_fields:
            if not data.get(field):
                return {"status": "error", "message": f"Missing required field: {field}"}

        volunteer = frappe.get_doc({
            "doctype": "Volunteer",
            "volunteer_name": full_name,
            "email": data.get("email"),
            "phone_number": phone,
            "volunteer_type": data.get("volunteer_type"),
            "availability": data.get("availability", ""),
            "note": data.get("note") or data.get("motivation") or "",
        })
        volunteer.insert(ignore_permissions=True)

        frappe.db.commit()

        return {
            "status": "success",
            "message": "Volunteer application submitted successfully",
            "data": {"name": volunteer.name}
        }
    except Exception as e:
        frappe.log_error(f"Error creating volunteer: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=True)
def get_volunteers():
    """Get list of all volunteers."""
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
        frappe.log_error(f"Error fetching volunteers: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=True)
def create_donation(**kwargs):
    """Create a new donation. For M-Pesa, initiates STK Push and returns checkout_request_id."""
    try:
        frappe.flags.ignore_permissions = True
        data = {k: v for k, v in kwargs.items()}

        required_fields = ["donor_name", "email", "amount"]
        for field in required_fields:
            if not data.get(field):
                return {"status": "error", "message": f"Missing required field: {field}"}

        donor_name = data.get("donor_name")
        email = data.get("email")
        phone = data.get("phone") or ""
        payment_method = data.get("payment_method") or "Cash"
        is_mpesa = payment_method in ("MPesa", "Mobile Money")

        if is_mpesa and not phone:
            return {"status": "error", "message": "Phone number is required for M-Pesa payments"}

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

        mop_value = "MPesa" if is_mpesa else payment_method
        if mop_value and not frappe.db.exists("Mode of Payment", mop_value):
            try:
                mop = frappe.get_doc({"doctype": "Mode of Payment", "mode_of_payment": mop_value, "type": "General"})
                mop.insert(ignore_permissions=True)
            except Exception:
                mop_value = "Cash"

        donation = frappe.get_doc({
            "doctype": "Donation",
            "donor": donor_doc_name,
            "donor_name": donor_name,
            "email": email,
            "phone": phone,
            "amount": float(data.get("amount", 0)),
            "currency": data.get("currency", "USD"),
            "mode_of_payment": mop_value,
            "payment_method": "MPesa" if is_mpesa else payment_method,
            "date": getdate(),
            "paid": 0 if is_mpesa else 1,
            "status": "Pending" if is_mpesa else "Received",
            "message": data.get("message", ""),
            "anonymous": 1 if str(data.get("anonymous", "0")) == "1" else 0,
        })
        donation.insert(ignore_permissions=True)

        if is_mpesa:
            result = initiate_mpesa_payment(donation, phone, float(data.get("amount", 0)))
            if result.get("error"):
                frappe.db.commit()
                return {"status": "error", "message": result["error"]}

            donation.checkout_request_id = result["checkout_request_id"]
            donation.save(ignore_permissions=True)
            frappe.db.commit()

            return {
                "status": "success",
                "message": "M-Pesa prompt sent to your phone. Complete payment on your phone.",
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
            "message": "Donation recorded successfully",
            "data": {"name": donation.name, "donor": donor_name}
        }
    except Exception as e:
        frappe.log_error(f"Error creating donation: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=True)
def submit_contact_form(**kwargs):
    """Submit contact form and create a Lead."""
    try:
        frappe.flags.ignore_permissions = True
        data = {k: v for k, v in kwargs.items()}

        required_fields = ["name", "email", "subject"]
        for field in required_fields:
            if not data.get(field):
                return {"status": "error", "message": f"Missing required field: {field}"}

        lead = frappe.get_doc({
            "doctype": "Lead",
            "lead_name": data.get("name"),
            "email_id": data.get("email"),
            "phone": data.get("phone") or "",
            "company_name": data.get("company", ""),
            "status": "Open",
            "type": "Client",
            "lead_owner": "Administrator",
        })
        lead.insert(ignore_permissions=True)

        frappe.db.commit()

        return {
            "status": "success",
            "message": "Your message has been sent. We'll get back to you soon!",
            "data": {"lead_id": lead.name}
        }
    except Exception as e:
        frappe.log_error(f"Error submitting contact form: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=True)
def get_chapters():
    """Get list of active chapters using Chapter DocType."""
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
        frappe.log_error(f"Error fetching chapters: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=True)
def create_chapter(**kwargs):
    """Create a new chapter using Chapter DocType."""
    try:
        frappe.flags.ignore_permissions = True
        data = {k: v for k, v in kwargs.items()}

        required_fields = ["introduction", "region", "address"]
        for field in required_fields:
            if not data.get(field):
                return {"status": "error", "message": f"Missing required field: {field}"}

        chapter_head = data.get("chapter_head")
        if not chapter_head:
            members = frappe.get_all("Member", fields=["name"], order_by="creation asc", limit=1, ignore_permissions=True)
            if members:
                chapter_head = members[0].name

        chapter_name = data.get("chapter_name") or data.get("introduction")

        chapter = frappe.get_doc({
            "doctype": "Chapter",
            "naming_series": "NPO-CHAP-.YYYY.-",
            "introduction": data.get("introduction"),
            "chapter_name": chapter_name,
            "chapter_head": chapter_head,
            "region": data.get("region"),
            "city": data.get("city", ""),
            "address": data.get("address"),
            "published": data.get("published", 1),
        })
        chapter.insert(ignore_permissions=True)

        frappe.db.commit()

        return {
            "status": "success",
            "message": "Chapter created successfully",
            "data": {"name": chapter.name, "introduction": chapter.introduction, "region": chapter.region}
        }
    except Exception as e:
        frappe.log_error(f"Error creating chapter: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=True)
def get_homepage_data():
    """Get data for homepage using available DocTypes."""
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
        frappe.log_error(f"Error fetching homepage data: {str(e)}")
        return {"status": "error", "message": str(e)}


def initiate_mpesa_payment(donation, phone, amount):
    """Initiate M-Pesa STK Push for a donation."""
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
            frappe.log_error(f"M-Pesa STK Push failed: {error_msg}", "M-Pesa Donation")
            return {"error": error_msg}

    except Exception as e:
        frappe.log_error(f"M-Pesa initiation error: {str(e)}", "M-Pesa Donation")
        return {"error": str(e)}


@frappe.whitelist(allow_guest=True)
def mpesa_donation_callback(**kwargs):
    """Callback endpoint for Safaricom M-Pesa STK Push results."""
    try:
        frappe.flags.ignore_permissions = True
        raw = frappe.get_json()
        body = frappe._dict(raw.get("Body", {}))
        stk_callback = frappe._dict(body.get("stkCallback", {}))

        checkout_request_id = stk_callback.get("CheckoutRequestID")
        result_code = stk_callback.get("ResultCode", 1)

        if not checkout_request_id:
            frappe.log_error("M-Pesa callback missing CheckoutRequestID", "M-Pesa Donation")
            return {"ResultCode": 1, "ResultDesc": "Missing CheckoutRequestID"}

        donation_name = frappe.db.get_value("Donation", {"checkout_request_id": checkout_request_id}, "name")
        if not donation_name:
            frappe.log_error(f"No donation found for CheckoutRequestID: {checkout_request_id}", "M-Pesa Donation")
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

            frappe.log_error(
                f"M-Pesa donation {donation_name} completed. Receipt: {mpesa_receipt}",
                "M-Pesa Donation"
            )
        else:
            result_desc = stk_callback.get("ResultDesc", "Payment failed")
            donation.status = "Failed"
            donation.save(ignore_permissions=True)
            frappe.db.commit()

            frappe.log_error(
                f"M-Pesa donation {donation_name} failed: {result_desc}",
                "M-Pesa Donation"
            )

        return {"ResultCode": 0, "ResultDesc": "Success"}

    except Exception as e:
        frappe.log_error(f"M-Pesa callback error: {str(e)}", "M-Pesa Donation")
        return {"ResultCode": 1, "ResultDesc": "Internal error"}


@frappe.whitelist(allow_guest=True)
def donation_status(checkout_request_id):
    """Check the status of an M-Pesa donation by checkout_request_id."""
    try:
        frappe.flags.ignore_permissions = True

        if not checkout_request_id:
            return {"status": "error", "message": "Missing checkout_request_id"}

        donation_name = frappe.db.get_value(
            "Donation",
            {"checkout_request_id": checkout_request_id},
            "name"
        )
        if not donation_name:
            return {"status": "error", "message": "Donation not found"}

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
        frappe.log_error(f"Donation status error: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
def generate_test_data():
    """Generate sample test data for frappe_npo doctypes: Members, Donors, Chapters, Volunteers, Donations."""
    return _generate_test_data()
