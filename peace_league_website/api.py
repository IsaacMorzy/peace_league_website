import frappe
from frappe import _
from frappe.utils import getdate, now_datetime
import json
from peace_league_website.utils.seed_data import seed_programs as _seed_programs, generate_test_data as _generate_test_data

def _log(level, msg):
    """Debug logging to frappe's error log."""
    try:
        with open("/tmp/gt_debug.log", "a") as f:
            f.write(f"[{level}] {msg}\n")
    except Exception:
        pass


@frappe.whitelist(allow_guest=True)
def get_programs():
    """Get list of active programs for the website using Program DocType."""
    try:
        frappe.flags.ignore_permissions = True

        # First try to get from Program DocType
        programs_list = frappe.get_list(
            "Program",
            filters={"show_on_website": 1, "is_active": 1},
            fields=["name", "title", "description", "image", "start_date", "end_date", "goal_amount", "raised_amount"],
            order_by="start_date desc",
            ignore_permissions=True
        )

        if programs_list:
            return {"status": "success", "data": programs_list}

        # If no programs exist, return sample programs for frontend demo
        return {"status": "success", "data": get_sample_programs()}

    except Exception as e:
        # Return sample data on error for frontend demo
        frappe.log_error(f"Error fetching programs: {str(e)}")
        return {"status": "success", "data": get_sample_programs()}


def get_sample_programs():
    """Return sample program data for frontend demo."""
    return [
        {
            "name": "peace-education-2025",
            "title": "Peace Education Program",
            "description": "Comprehensive peace education workshops for schools and communities, teaching conflict resolution and peaceful communication skills.",
            "start_date": "2025-01-15",
            "end_date": "2025-12-31",
            "category": "Education",
            "image": "/images/programs/peace-education.jpg"
        },
        {
            "name": "youth-empowerment-2025",
            "title": "Youth Empowerment Initiative",
            "description": "Empowering young leaders through mentorship programs, skills training, and community service opportunities.",
            "start_date": "2025-03-01",
            "end_date": "2025-11-30",
            "category": "Youth",
            "image": "/images/programs/youth-empowerment.jpg"
        },
        {
            "name": "community-reconciliation-2025",
            "title": "Community Reconciliation",
            "description": "Facilitating dialogue and reconciliation processes in communities affected by conflict and division.",
            "start_date": "2025-02-01",
            "end_date": "2025-10-31",
            "category": "Community",
            "image": "/images/programs/reconciliation.jpg"
        },
        {
            "name": "leadership-training-2025",
            "title": "Peace Leader Training",
            "description": "Intensive leadership development program for emerging peace leaders and community organizers.",
            "start_date": "2025-04-15",
            "end_date": "2025-08-15",
            "category": "Training",
            "image": "/images/programs/leadership.jpg"
        },
        {
            "name": "global-peace-summit-2025",
            "title": "Global Peace Summit 2025",
            "description": "Annual international conference bringing together peace advocates, leaders, and organizations from around the world.",
            "start_date": "2025-09-20",
            "end_date": "2025-09-25",
            "category": "Event",
            "image": "/images/programs/summit.jpg"
        }
    ]


@frappe.whitelist()
def seed_programs():
    """Create sample Email Campaign records for programs."""
    return _seed_programs()


@frappe.whitelist(allow_guest=True)
def get_program_details(name):
    """Get detailed program information."""
    try:
        frappe.flags.ignore_permissions = True
        if not frappe.db.exists("Program", name):
            return {"status": "error", "message": "Program not found"}

        program = frappe.get_doc("Program", name)
        program.flags.ignore_permissions = True
        return {
            "status": "success",
            "data": {
                "name": program.name,
                "title": program.title,
                "description": program.description,
                "image": program.image,
                "start_date": program.start_date,
                "end_date": program.end_date,
                "goal_amount": program.goal_amount,
                "raised_amount": program.raised_amount,
            }
        }
    except Exception as e:
        frappe.log_error(f"Error fetching program details: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=True)
def create_volunteer(**kwargs):
    """Create a new volunteer application using frappe_npo Volunteer DocType."""
    try:
        frappe.flags.ignore_permissions = True
        data = {k: v for k, v in kwargs.items()}

        # Build full name from first/last or use directly
        full_name = data.get("volunteer_name")
        if not full_name:
            first_name = data.get("first_name", "")
            last_name = data.get("last_name", "")
            full_name = f"{first_name} {last_name}".strip() or "Anonymous"

        # Get phone (use phone or phone_number)
        phone = data.get("phone") or data.get("phone_number") or ""

        # Auto-create Volunteer Type if it doesn't exist (requires 'amount' field)
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
                    pass  # If creation fails, let the LinkValidationError fire naturally

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
    """Create a new donation using frappe_npo Donation DocType."""
    try:
        frappe.flags.ignore_permissions = True
        data = {k: v for k, v in kwargs.items()}

        required_fields = ["donor_name", "email", "amount"]
        for field in required_fields:
            if not data.get(field):
                return {"status": "error", "message": f"Missing required field: {field}"}

        # First try to find or create donor
        donor_name = data.get("donor_name")
        email = data.get("email")
        phone = data.get("phone") or ""

        # Check if donor exists by email
        existing_donor = frappe.db.get_value("Donor", {"email": email}, "name")
        if not existing_donor:
            # Create new donor
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

        donation = frappe.get_doc({
            "doctype": "Donation",
            "donor": donor_doc_name,  # Link field: use donor document name
            "donor_name": donor_name,  # Display name: use original input value
            "email": email,
            "amount": float(data.get("amount", 0)),
            "currency": data.get("currency", "USD"),
            "mode_of_payment": data.get("payment_method") or data.get("mode_of_payment", "Online"),
            "date": getdate(),
            "paid": 1,
        })
        donation.insert(ignore_permissions=True)

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

        # Create lead
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

        # Get chapter_head (Member) if provided, otherwise use first available member
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
        campaigns = frappe.get_list(
            "Email Campaign",
            filters={"status": "Active"},
            fields=["name", "campaign_name", "start_date"],
            limit=3,
            ignore_permissions=True
        )
        programs = []
        for c in campaigns:
            programs.append({
                "name": c.name,
                "title": c.campaign_name,
                "start_date": c.start_date,
            })

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
                "programs": programs,
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


@frappe.whitelist()
def generate_test_data():
    """Generate sample test data for frappe_npo doctypes: Members, Donors, Chapters, Volunteers, Donations."""
    return _generate_test_data()