import frappe
from frappe.utils import getdate


def _log(level, msg):
    """Debug logging to frappe's error log."""
    try:
        with open("/tmp/gt_debug.log", "a") as f:
            f.write(f"[{level}] {msg}\n")
    except Exception:
        pass


def seed_programs():
    """Create sample Email Campaign records for programs."""
    try:
        frappe.flags.ignore_permissions = True
        created_counts = {}

        sample_programs = [
            {"campaign_name": "Peace Education Program", "email_campaign_for": "Comprehensive peace education workshops for schools and communities, teaching conflict resolution and peaceful communication skills.", "status": "Active", "start_date": "2025-01-15", "end_date": "2025-12-31"},
            {"campaign_name": "Youth Empowerment Initiative", "email_campaign_for": "Empowering young leaders through mentorship programs, skills training, and community service opportunities.", "status": "Active", "start_date": "2025-03-01", "end_date": "2025-11-30"},
            {"campaign_name": "Community Reconciliation", "email_campaign_for": "Facilitating dialogue and reconciliation processes in communities affected by conflict and division.", "status": "Active", "start_date": "2025-02-01", "end_date": "2025-10-31"},
            {"campaign_name": "Peace Leader Training", "email_campaign_for": "Intensive leadership development program for emerging peace leaders and community organizers.", "status": "Active", "start_date": "2025-04-15", "end_date": "2025-08-15"},
            {"campaign_name": "Global Peace Summit 2025", "email_campaign_for": "Annual international conference bringing together peace advocates, leaders, and organizations from around the world.", "status": "Active", "start_date": "2025-09-20", "end_date": "2025-09-25"},
        ]

        for p in sample_programs:
            if not frappe.db.exists("Email Campaign", {"campaign_name": p["campaign_name"]}):
                campaign = frappe.get_doc({
                    "doctype": "Email Campaign",
                    "campaign_name": p["campaign_name"],
                    "email_campaign_for": p["email_campaign_for"],
                    "status": p["status"],
                    "start_date": p["start_date"],
                    "end_date": p["end_date"],
                })
                campaign.insert(ignore_permissions=True)
                created_counts["programs"] = created_counts.get("programs", 0) + 1

        frappe.db.commit()
        return {"status": "success", "message": f"Created {created_counts.get('programs', 0)} programs", "data": created_counts}
    except Exception as e:
        frappe.log_error(f"Error seeding programs: {str(e)}")
        return {"status": "error", "message": str(e)}


def generate_test_data():
    """Generate sample test data for frappe_npo doctypes: Members, Donors, Chapters, Volunteers, Donations."""
    try:
        frappe.flags.ignore_permissions = True
        created_counts = {}
        _log("INFO", "=== generate_test_data START ===")

        # First, ensure Membership Type exists
        if not frappe.db.exists("Membership Type", "Individual"):
            membership_type = frappe.get_doc({
                "doctype": "Membership Type",
                "membership_type": "Individual",
                "amount": 50,
            })
            membership_type.insert(ignore_permissions=True)
            created_counts["membership_types"] = 1
            _log("INFO", f"Membership Type created")

        # Members - uses naming_series, member_name, email_id, membership_type
        members_data = [
            {"member_name": "Alice Johnson", "email_id": "alice.johnson@email.com", "phone": "+1-555-0101", "membership_type": "Individual"},
            {"member_name": "Robert Smith", "email_id": "robert.smith@email.com", "phone": "+1-555-0102", "membership_type": "Individual"},
            {"member_name": "Maria Garcia", "email_id": "maria.garcia@email.com", "phone": "+1-555-0103", "membership_type": "Individual"},
            {"member_name": "James Wilson", "email_id": "james.wilson@email.com", "phone": "+1-555-0104", "membership_type": "Individual"},
            {"member_name": "Sarah Brown", "email_id": "sarah.brown@email.com", "phone": "+1-555-0105", "membership_type": "Individual"},
        ]

        for m in members_data:
            if not frappe.db.exists("Member", {"email_id": m["email_id"]}):
                _log("INFO", f"Creating member: {m['member_name']} ({m['email_id']})")
                member = frappe.get_doc({
                    "doctype": "Member",
                    "naming_series": "NPO-MEM-.YYYY.-",
                    "member_name": m["member_name"],
                    "email_id": m["email_id"],
                    "membership_type": m["membership_type"],
                    "membership_expiry_date": "2026-12-31",
                })
                member.insert(ignore_permissions=True)
                created_counts["members"] = created_counts.get("members", 0) + 1
                _log("INFO", f"Member inserted: {member.name}")

        # First ensure Donor Type exists
        for dt in ["Individual", "Organization"]:
            if not frappe.db.exists("Donor Type", dt):
                dt_doc = frappe.get_doc({"doctype": "Donor Type", "donor_type": dt})
                dt_doc.insert(ignore_permissions=True)
                created_counts["donor_types"] = created_counts.get("donor_types", 0) + 1

        # Donor DocType uses autoname=field:email which can't handle @ symbols
        # Change it to naming_series so we can use valid email formats
        # First add naming_series field if it doesn't exist (needed for naming_series autoname)
        if not frappe.db.exists("Custom Field", "Donor-naming_series"):
            cf = frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Donor",
                "fieldname": "naming_series",
                "label": "Series",
                "fieldtype": "Select",
                "options": "NPO-DON-.YYYY.-",
                "insert_after": "donor_name",
                "allow_on_submit": 1,
            })
            cf.insert(ignore_permissions=True)
        frappe.db.sql("UPDATE `tabDocType` SET `autoname`='naming_series:' WHERE `name`='Donor'")

        donors_data = [
            {"donor_name": "William Thompson", "email": "william.thompson@charity.org", "phone_number": "+1-555-0201", "donor_type": "Individual"},
            {"donor_name": "Elizabeth Davis", "email": "elizabeth.davis@charity.org", "phone_number": "+1-555-0202", "donor_type": "Individual"},
            {"donor_name": "Peace Foundation", "email": "donations@peacefdn.org", "phone_number": "+1-555-0203", "donor_type": "Organization"},
            {"donor_name": "Michael Lee", "email": "michael.lee@email.com", "phone_number": "+1-555-0204", "donor_type": "Individual"},
            {"donor_name": "Global Aid Trust", "email": "giving@globalaid.org", "phone_number": "+1-555-0205", "donor_type": "Organization"},
        ]

        for d in donors_data:
            if not frappe.db.exists("Donor", {"email": d["email"]}):
                donor = frappe.get_doc({
                    "doctype": "Donor",
                    "donor_name": d["donor_name"],
                    "email": d["email"],
                    "phone_number": d["phone_number"],
                    "donor_type": d["donor_type"],
                })
                donor.insert(ignore_permissions=True)
                created_counts["donors"] = created_counts.get("donors", 0) + 1

        # Chapters - uses chapter_name, region, city, address (requires chapter_head link to Member)
        chapters_data = [
            {"chapter_name": "Peace Builders New York", "region": "Northeast", "city": "New York", "address": "123 Peace Avenue, NY 10001"},
            {"chapter_name": "California Peace Alliance", "region": "West", "city": "Los Angeles", "address": "456 Harmony Street, CA 90001"},
            {"chapter_name": "Midwest Peace Initiative", "region": "Midwest", "city": "Chicago", "address": "789 Unity Road, IL 60601"},
            {"chapter_name": "Southern Peace Network", "region": "South", "city": "Atlanta", "address": "321 Calm Lane, GA 30301"},
            {"chapter_name": "Peace Council Texas", "region": "South", "city": "Houston", "address": "654 Serenity Blvd, TX 77001"},
        ]

        # Chapter uses autoname=prompt, so we need naming_series + update DocType
        if not frappe.db.exists("Custom Field", "Chapter-naming_series"):
            cf = frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Chapter",
                "fieldname": "naming_series",
                "label": "Series",
                "fieldtype": "Select",
                "options": "NPO-CHAP-.YYYY.-",
                "insert_after": "chapter_head",
                "allow_on_submit": 1,
            })
            cf.insert(ignore_permissions=True)
        frappe.db.sql("UPDATE `tabDocType` SET `autoname`='naming_series:' WHERE `name`='Chapter'")
        frappe.clear_cache(doctype="Chapter")

        # Get first member for chapter_head
        first_member_list = frappe.get_all("Member", fields=["name"], order_by="creation asc", limit=1)
        first_member = first_member_list[0].name if first_member_list else None

        for c in chapters_data:
            if not frappe.db.exists("Chapter", {"introduction": c["chapter_name"]}):
                chapter = frappe.get_doc({
                    "doctype": "Chapter",
                    "naming_series": "NPO-CHAP-.YYYY.-",
                    "introduction": c["chapter_name"],
                    "chapter_head": first_member,
                    "region": c["region"],
                    "city": c["city"],
                    "address": c["address"],
                    "published": 1,
                })
                chapter.insert(ignore_permissions=True)
                created_counts["chapters"] = created_counts.get("chapters", 0) + 1

        # First ensure Volunteer Type exists
        if not frappe.db.exists("Volunteer Type", "Event Volunteer"):
            vt1 = frappe.get_doc({"doctype": "Volunteer Type", "title": "Event Volunteer"})
            vt1.insert(ignore_permissions=True)
            created_counts["volunteer_types"] = created_counts.get("volunteer_types", 0) + 1

        if not frappe.db.exists("Volunteer Type", "Community Outreach"):
            vt2 = frappe.get_doc({"doctype": "Volunteer Type", "title": "Community Outreach"})
            vt2.insert(ignore_permissions=True)
            created_counts["volunteer_types"] = created_counts.get("volunteer_types", 0) + 1

        # Volunteers - uses volunteer_name, email, phone_number, volunteer_type
        volunteers_data = [
            {"volunteer_name": "Emily Chen", "email": "emily.chen@email.com", "phone_number": "+1-555-0301", "volunteer_type": "Event Volunteer"},
            {"volunteer_name": "David Martinez", "email": "david.martinez@email.com", "phone_number": "+1-555-0302", "volunteer_type": "Community Outreach"},
            {"volunteer_name": "Jennifer White", "email": "jennifer.white@email.com", "phone_number": "+1-555-0303", "volunteer_type": "Event Volunteer"},
            {"volunteer_name": "Christopher Taylor", "email": "chris.taylor@email.com", "phone_number": "+1-555-0304", "volunteer_type": "Community Outreach"},
            {"volunteer_name": "Amanda Anderson", "email": "amanda.anderson@email.com", "phone_number": "+1-555-0305", "volunteer_type": "Event Volunteer"},
        ]

        for v in volunteers_data:
            if not frappe.db.exists("Volunteer", {"email": v["email"]}):
                volunteer = frappe.get_doc({
                    "doctype": "Volunteer",
                    "volunteer_name": v["volunteer_name"],
                    "email": v["email"],
                    "phone_number": v["phone_number"],
                    "volunteer_type": v["volunteer_type"],
                })
                volunteer.insert(ignore_permissions=True)
                created_counts["volunteers"] = created_counts.get("volunteers", 0) + 1

        # Donations - uses donor (link), amount, date, mode_of_payment, paid
        donations_data = [
            {"donor": "william.thompson@charity.org", "amount": 250, "mode_of_payment": "Online"},
            {"donor": "elizabeth.davis@charity.org", "amount": 500, "mode_of_payment": "Wire Transfer"},
            {"donor": "donations@peacefdn.org", "amount": 1000, "mode_of_payment": "Cheque"},
            {"donor": "michael.lee@email.com", "amount": 100, "mode_of_payment": "Online"},
            {"donor": "giving@globalaid.org", "amount": 2000, "mode_of_payment": "Wire Transfer"},
        ]

        for d in donations_data:
            donor_name = frappe.db.get_value("Donor", {"email": d["donor"]}, "name")
            if donor_name and not frappe.db.exists("Donation", {"donor": donor_name, "amount": d["amount"]}):
                donation = frappe.get_doc({
                    "doctype": "Donation",
                    "naming_series": "DON-.YYYY.-",
                    "donor": donor_name,
                    "amount": d["amount"],
                    "currency": "USD",
                    "mode_of_payment": d["mode_of_payment"],
                    "date": "2025-06-01",
                    "paid": 1,
                    "company": "Peace League Africa",
                })
                donation.insert(ignore_permissions=True)
                created_counts["donations"] = created_counts.get("donations", 0) + 1

        frappe.db.commit()
        _log("INFO", f"=== SUCCESS: created {created_counts}")

        return {
            "status": "success",
            "message": "Test data generated successfully",
            "data": {
                "records_created": created_counts,
                "total_records": sum(created_counts.values())
            }
        }
    except Exception as e:
        import traceback
        _log("ERROR", f"EXCEPTION: {type(e).__name__}: {e}")
        _log("ERROR", traceback.format_exc())
        frappe.log_error(f"Error generating test data: {str(e)}")
        return {"status": "error", "message": str(e)}