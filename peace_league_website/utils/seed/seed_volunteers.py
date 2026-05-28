"""
Seed volunteer records for development.

Graph edges: creates: Volunteer, Volunteer Type
"""

import frappe

logger = frappe.logger("peace_league", allow_site=True, file_count=5)

VOLUNTEERS_DATA = [
    {"volunteer_name": "Emily Chen", "email": "emily.chen@email.com", "phone_number": "+1-555-0301", "volunteer_type": "Event Volunteer"},
    {"volunteer_name": "David Martinez", "email": "david.martinez@email.com", "phone_number": "+1-555-0302", "volunteer_type": "Community Outreach"},
    {"volunteer_name": "Jennifer White", "email": "jennifer.white@email.com", "phone_number": "+1-555-0303", "volunteer_type": "Event Volunteer"},
    {"volunteer_name": "Christopher Taylor", "email": "chris.taylor@email.com", "phone_number": "+1-555-0304", "volunteer_type": "Community Outreach"},
    {"volunteer_name": "Amanda Anderson", "email": "amanda.anderson@email.com", "phone_number": "+1-555-0305", "volunteer_type": "Event Volunteer"},
]


def seed_volunteers():
    """Create sample Volunteer records and Volunteer Types.

    Graph edges: creates: Volunteer, Volunteer Type
    """
    created_counts = {}

    for vt_title in ["Event Volunteer", "Community Outreach"]:
        if not frappe.db.exists("Volunteer Type", vt_title):
            vt = frappe.get_doc({"doctype": "Volunteer Type", "title": vt_title})
            vt.insert(ignore_permissions=True)
            created_counts["volunteer_types"] = created_counts.get("volunteer_types", 0) + 1

    for v in VOLUNTEERS_DATA:
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

    return created_counts
