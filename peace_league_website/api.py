import frappe
from frappe import _
from frappe.utils import getdate, now_datetime
import json


@frappe.whitelist(allow_guest=True)
def get_programs():
    """Get list of active programs for the website using Email Campaign."""
    try:
        frappe.flags.ignore_permissions = True
        campaigns = frappe.get_list(
            "Email Campaign",
            filters={"status": "Active"},
            fields=["name", "campaign_name", "start_date", "end_date", "email_campaign_for"],
            order_by="start_date desc",
            ignore_permissions=True
        )
        programs = []
        for c in campaigns:
            programs.append({
                "name": c.name,
                "title": c.campaign_name,
                "description": c.email_campaign_for or "",
                "start_date": c.start_date,
                "end_date": c.end_date,
            })
        return {"status": "success", "data": programs}
    except Exception as e:
        frappe.log_error(f"Error fetching programs: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=True)
def get_program_details(name):
    """Get detailed program information."""
    try:
        frappe.flags.ignore_permissions = True
        if not frappe.db.exists("Email Campaign", name):
            return {"status": "error", "message": "Program not found"}
        
        program = frappe.get_doc("Email Campaign", name)
        program.flags.ignore_permissions = True
        return {
            "status": "success",
            "data": {
                "name": program.name,
                "title": program.campaign_name,
                "description": program.email_campaign_for,
                "start_date": program.start_date,
                "end_date": program.end_date,
                "status": program.status,
            }
        }
    except Exception as e:
        frappe.log_error(f"Error fetching program details: {str(e)}")
        return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=True)
def create_volunteer(data):
    """Create a new volunteer application using Volunteer DocType."""
    try:
        frappe.flags.ignore_permissions = True
        if isinstance(data, str):
            data = json.loads(data)
        
        required_fields = ["volunteer_name", "email"]
        for field in required_fields:
            if not data.get(field):
                return {"status": "error", "message": f"Missing required field: {field}"}
        
        volunteer = frappe.get_doc({
            "doctype": "Volunteer",
            "volunteer_name": data.get("volunteer_name"),
            "email": data.get("email"),
            "phone_number": data.get("phone"),
            "volunteer_type": data.get("volunteer_type"),
            "availability": data.get("availability"),
            "volunteer_skills": data.get("skills"),
            "note": data.get("experience") or "",
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
    """Create a new donation using Donation DocType."""
    try:
        frappe.flags.ignore_permissions = True
        if isinstance(data, str):
            data = json.loads(data)
        
        required_fields = ["donor_name", "email", "amount"]
        for field in required_fields:
            if not data.get(field):
                return {"status": "error", "message": f"Missing required field: {field}"}
        
        donation = frappe.get_doc({
            "doctype": "Donation",
            "donor_name": data.get("donor_name"),
            "email": data.get("email"),
            "amount": float(data.get("amount", 0)),
            "currency": data.get("currency", "USD"),
            "mode_of_payment": data.get("payment_method"),
            "date": getdate(),
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
    """Submit contact form and create a Lead."""
    try:
        frappe.flags.ignore_permissions = True
        if isinstance(data, str):
            data = json.loads(data)
        
        required_fields = ["name", "email", "subject"]
        for field in required_fields:
            if not data.get(field):
                return {"status": "error", "message": f"Missing required field: {field}"}
        
        name_parts = data.get("name", "").split()
        first_name = name_parts[0] if name_parts else ""
        last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
        
        lead = frappe.get_doc({
            "doctype": "Lead",
            "lead_name": data.get("name"),
            "first_name": first_name,
            "last_name": last_name,
            "email_id": data.get("email"),
            "phone": data.get("phone"),
            "mobile_no": data.get("phone"),
            "company_name": data.get("company", ""),
            "status": "Open",
            "type": "Website",
            "lead_owner": "Administrator",
            "notes": f"Subject: {data.get('subject')}\n\n{data.get('message', '')}",
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
            "SELECT COALESCE(SUM(total_amount_paid), 0) as total FROM `tabDonation` WHERE paid = 1"
        )[0][0] if frappe.db.sql("SELECT COUNT(*) FROM `tabDonation` WHERE paid = 1")[0][0] else 0
        
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
    try:
        frappe.flags.ignore_permissions = True
        created_counts = {}

        members_data = [
            {"full_name": "Alice Johnson", "email": "alice.johnson@email.com", "phone": "+1-555-0101", "member_type": "Individual", "membership_status": "Active"},
            {"full_name": "Robert Smith", "email": "robert.smith@email.com", "phone": "+1-555-0102", "member_type": "Individual", "membership_status": "Active"},
            {"full_name": "Maria Garcia", "email": "maria.garcia@email.com", "phone": "+1-555-0103", "member_type": "Individual", "membership_status": "Active"},
            {"full_name": "James Wilson", "email": "james.wilson@email.com", "phone": "+1-555-0104", "member_type": "Individual", "membership_status": "Active"},
            {"full_name": "Sarah Brown", "email": "sarah.brown@email.com", "phone": "+1-555-0105", "member_type": "Individual", "membership_status": "Active"},
        ]

        for m in members_data:
            if not frappe.db.exists("Member", {"email": m["email"]}):
                member = frappe.get_doc({
                    "doctype": "Member",
                    "full_name": m["full_name"],
                    "email": m["email"],
                    "phone": m["phone"],
                    "member_type": m["member_type"],
                    "membership_status": m["membership_status"],
                    "membership_start_date": "2025-01-01",
                    "membership_end_date": "2026-12-31",
                })
                member.insert(ignore_permissions=True)
                created_counts["members"] = created_counts.get("members", 0) + 1

        donors_data = [
            {"donor_name": "William Thompson", "email": "william.t@charity.org", "phone": "+1-555-0201", "donor_type": "Individual"},
            {"donor_name": "Elizabeth Davis", "email": "elizabeth.d@charity.org", "phone": "+1-555-0202", "donor_type": "Individual"},
            {"donor_name": "Peace Foundation", "email": "donations@peacefdn.org", "phone": "+1-555-0203", "donor_type": "Organization"},
            {"donor_name": "Michael Lee", "email": "michael.lee@email.com", "phone": "+1-555-0204", "donor_type": "Individual"},
            {"donor_name": "Global Aid Trust", "email": "giving@globalaid.org", "phone": "+1-555-0205", "donor_type": "Organization"},
        ]

        for d in donors_data:
            if not frappe.db.exists("Donor", {"email": d["email"]}):
                donor = frappe.get_doc({
                    "doctype": "Donor",
                    "donor_name": d["donor_name"],
                    "email": d["email"],
                    "phone": d["phone"],
                    "donor_type": d["donor_type"],
                })
                donor.insert(ignore_permissions=True)
                created_counts["donors"] = created_counts.get("donors", 0) + 1

        chapters_data = [
            {"chapter_name": "Peace Builders New York", "region": "Northeast", "city": "New York", "address": "123 Peace Avenue, NY 10001", "published": 1},
            {"chapter_name": "California Peace Alliance", "region": "West", "city": "Los Angeles", "address": "456 Harmony Street, CA 90001", "published": 1},
            {"chapter_name": "Midwest Peace Initiative", "region": "Midwest", "city": "Chicago", "address": "789 Unity Road, IL 60601", "published": 1},
            {"chapter_name": "Southern Peace Network", "region": "South", "city": "Atlanta", "address": "321 Calm Lane, GA 30301", "published": 1},
            {"chapter_name": "Peace Council Texas", "region": "South", "city": "Houston", "address": "654 Serenity Blvd, TX 77001", "published": 1},
        ]

        for c in chapters_data:
            if not frappe.db.exists("Chapter", {"chapter_name": c["chapter_name"]}):
                chapter = frappe.get_doc({
                    "doctype": "Chapter",
                    "chapter_name": c["chapter_name"],
                    "region": c["region"],
                    "city": c["city"],
                    "address": c["address"],
                    "published": c["published"],
                })
                chapter.insert(ignore_permissions=True)
                created_counts["chapters"] = created_counts.get("chapters", 0) + 1

        volunteers_data = [
            {"volunteer_name": "Emily Chen", "email": "emily.chen@email.com", "phone_number": "+1-555-0301", "volunteer_type": "Event Volunteer", "availability": "Weekends"},
            {"volunteer_name": "David Martinez", "email": "david.martinez@email.com", "phone_number": "+1-555-0302", "volunteer_type": "Fundraising", "availability": "Evenings"},
            {"volunteer_name": "Jennifer White", "email": "jennifer.white@email.com", "phone_number": "+1-555-0303", "volunteer_type": "Community Outreach", "availability": "Flexible"},
            {"volunteer_name": "Christopher Taylor", "email": "chris.taylor@email.com", "phone_number": "+1-555-0304", "volunteer_type": "Event Volunteer", "availability": "Weekends"},
            {"volunteer_name": "Amanda Anderson", "email": "amanda.anderson@email.com", "phone_number": "+1-555-0305", "volunteer_type": "Administrative", "availability": "Mornings"},
        ]

        for v in volunteers_data:
            if not frappe.db.exists("Volunteer", {"email": v["email"]}):
                volunteer = frappe.get_doc({
                    "doctype": "Volunteer",
                    "volunteer_name": v["volunteer_name"],
                    "email": v["email"],
                    "phone_number": v["phone_number"],
                    "volunteer_type": v["volunteer_type"],
                    "availability": v["availability"],
                })
                volunteer.insert(ignore_permissions=True)
                created_counts["volunteers"] = created_counts.get("volunteers", 0) + 1

        donations_data = [
            {"donor_name": "William Thompson", "email": "william.t@charity.org", "amount": 250, "currency": "USD", "mode_of_payment": "Online", "paid": 1},
            {"donor_name": "Elizabeth Davis", "email": "elizabeth.d@charity.org", "amount": 500, "currency": "USD", "mode_of_payment": "Bank Transfer", "paid": 1},
            {"donor_name": "Peace Foundation", "email": "donations@peacefdn.org", "amount": 1000, "currency": "USD", "mode_of_payment": "Cheque", "paid": 1},
            {"donor_name": "Michael Lee", "email": "michael.lee@email.com", "amount": 100, "currency": "USD", "mode_of_payment": "Online", "paid": 1},
            {"donor_name": "Global Aid Trust", "email": "giving@globalaid.org", "amount": 2000, "currency": "USD", "mode_of_payment": "Bank Transfer", "paid": 1},
        ]

        for d in donations_data:
            if not frappe.db.exists("Donation", {"email": d["email"], "amount": d["amount"]}):
                donation = frappe.get_doc({
                    "doctype": "Donation",
                    "donor_name": d["donor_name"],
                    "email": d["email"],
                    "amount": d["amount"],
                    "currency": d["currency"],
                    "mode_of_payment": d["mode_of_payment"],
                    "date": "2025-06-01",
                    "paid": d["paid"],
                    "total_amount_paid": d["amount"] if d["paid"] else 0,
                })
                donation.insert(ignore_permissions=True)
                created_counts["donations"] = created_counts.get("donations", 0) + 1

        frappe.db.commit()

        return {
            "status": "success",
            "message": "Test data generated successfully",
            "data": {
                "records_created": created_counts,
                "total_records": sum(created_counts.values())
            }
        }
    except Exception as e:
        frappe.log_error(f"Error generating test data: {str(e)}")
        return {"status": "error", "message": str(e)}