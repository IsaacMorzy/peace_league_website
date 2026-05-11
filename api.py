import frappe
from frappe import _
from frappe.utils import getdate, now_datetime
import json


@frappe.whitelist(allow_guest=True)
def get_programs():
    """Get list of active programs for the website."""
    try:
        programs = frappe.get_list(
            "Program",
            filters={"is_active": 1, "show_on_website": 1},
            fields=["name", "title", "description", "image", "start_date", "end_date", "goal_amount", "raised_amount"],
            order_by="creation desc"
        )
        return {"status": "success", "data": programs}
    except Exception as e:
        frappe.log_error(f"Error fetching programs: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=True)
def get_program_details(name):
    """Get detailed program information."""
    try:
        if not frappe.db.exists("Program", name):
            return {"status": "error", "message": "Program not found"}
        
        program = frappe.get_doc("Program", name)
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
                "is_active": program.is_active,
            }
        }
    except Exception as e:
        frappe.log_error(f"Error fetching program details: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=True)
def create_volunteer(data):
    """Create a new volunteer application."""
    try:
        if isinstance(data, str):
            data = json.loads(data)
        
        required_fields = ["first_name", "last_name", "email", "phone", "volunteer_type"]
        for field in required_fields:
            if not data.get(field):
                return {"status": "error", "message": f"Missing required field: {field}"}
        
        volunteer = frappe.get_doc({
            "doctype": "Volunteer",
            "first_name": data.get("first_name"),
            "last_name": data.get("last_name"),
            "email": data.get("email"),
            "phone": data.get("phone"),
            "volunteer_type": data.get("volunteer_type"),
            "availability": data.get("availability"),
            "skills": data.get("skills"),
            "experience": data.get("experience"),
            "motivation": data.get("motivation"),
            "status": "Applied",
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
def create_donation(data):
    """Create a new donation."""
    try:
        if isinstance(data, str):
            data = json.loads(data)
        
        required_fields = ["donor_name", "email", "amount", "payment_method"]
        for field in required_fields:
            if not data.get(field):
                return {"status": "error", "message": f"Missing required field: {field}"}
        
        donation = frappe.get_doc({
            "doctype": "Donation",
            "donor_name": data.get("donor_name"),
            "email": data.get("email"),
            "phone": data.get("phone"),
            "amount": float(data.get("amount", 0)),
            "payment_method": data.get("payment_method"),
            "currency": data.get("currency", "USD"),
            "program": data.get("program"),
            "anonymous": data.get("anonymous", 0),
            "message": data.get("message"),
            "status": "Pending",
        })
        donation.insert(ignore_permissions=True)
        
        frappe.db.commit()
        
        return {
            "status": "success",
            "message": "Donation recorded successfully",
            "data": {"name": donation.name}
        }
    except Exception as e:
        frappe.log_error(f"Error creating donation: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=True)
def submit_contact_form(data):
    """Submit contact form and create a Lead or Communication."""
    try:
        if isinstance(data, str):
            data = json.loads(data)
        
        required_fields = ["name", "email", "subject", "message"]
        for field in required_fields:
            if not data.get(field):
                return {"status": "error", "message": f"Missing required field: {field}"}
        
        contact = frappe.get_doc({
            "doctype": "Contact",
            "first_name": data.get("name").split()[0] if data.get("name") else "",
            "last_name": " ".join(data.get("name").split()[1:]) if data.get("name") else "",
            "email_id": data.get("email"),
            "phone": data.get("phone"),
        })
        contact.insert(ignore_permissions=True)
        
        communication = frappe.get_doc({
            "doctype": "Communication",
            "communication_type": "Communication",
            "subject": data.get("subject"),
            "content": data.get("message"),
            "sender": data.get("email"),
            "recipients": "info@peaceleagueafrica.org",
            "contact": contact.name,
        })
        communication.insert(ignore_permissions=True)
        
        frappe.db.commit()
        
        return {
            "status": "success",
            "message": "Your message has been sent. We'll get back to you soon!",
            "data": {"contact_id": contact.name}
        }
    except Exception as e:
        frappe.log_error(f"Error submitting contact form: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=True)
def get_chapters():
    """Get list of active chapters."""
    try:
        chapters = frappe.get_list(
            "Chapter",
            filters={"is_active": 1},
            fields=["name", "chapter_name", "description", "location", "image"],
            order_by="chapter_name"
        )
        return {"status": "success", "data": chapters}
    except Exception as e:
        frappe.log_error(f"Error fetching chapters: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=True)
def get_homepage_data():
    """Get data for homepage."""
    try:
        programs = frappe.get_list(
            "Program",
            filters={"is_active": 1, "show_on_website": 1},
            fields=["name", "title", "description", "image", "goal_amount", "raised_amount"],
            limit=3
        )
        
        chapters = frappe.get_list(
            "Chapter",
            filters={"is_active": 1},
            fields=["name", "chapter_name", "location"],
            limit=5
        )
        
        total_donations = frappe.db.get_value(
            "Donation",
            {"status": "Received"},
            "sum(amount)",
            cache=True
        ) or 0
        
        total_volunteers = frappe.db.count("Volunteer", {"status": "Active"}) or 0
        
        return {
            "status": "success",
            "data": {
                "programs": programs,
                "chapters": chapters,
                "stats": {
                    "total_donations": total_donations,
                    "total_volunteers": total_volunteers,
                }
            }
        }
    except Exception as e:
        frappe.log_error(f"Error fetching homepage data: {str(e)}")
        return {"status": "error", "message": str(e)}


def get_boot_data():
    """Add custom data to boot."""
    return {
        "peace_league_website": {
            "settings": {
                "organization_name": "Peace League Africa",
                "currency": "USD",
            }
        }
    }