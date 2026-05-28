"""
Seed donor records for development.

Graph edges: creates: Donor, Donor Type, Custom Field
"""

import frappe

logger = frappe.logger("peace_league", allow_site=True, file_count=5)

DONORS_DATA = [
    {"donor_name": "William Thompson", "email": "william.thompson@charity.org", "phone_number": "+1-555-0201", "donor_type": "Individual"},
    {"donor_name": "Elizabeth Davis", "email": "elizabeth.davis@charity.org", "phone_number": "+1-555-0202", "donor_type": "Individual"},
    {"donor_name": "Peace Foundation", "email": "donations@peacefdn.org", "phone_number": "+1-555-0203", "donor_type": "Organization"},
    {"donor_name": "Michael Lee", "email": "michael.lee@email.com", "phone_number": "+1-555-0204", "donor_type": "Individual"},
    {"donor_name": "Global Aid Trust", "email": "giving@globalaid.org", "phone_number": "+1-555-0205", "donor_type": "Organization"},
]


def seed_donors():
    """Create sample Donor records and ensure Donor Type exists.

    Graph edges: creates: Donor, Donor Type
    """
    created_counts = {}

    for dt in ["Individual", "Organization"]:
        if not frappe.db.exists("Donor Type", dt):
            dt_doc = frappe.get_doc({"doctype": "Donor Type", "donor_type": dt})
            dt_doc.insert(ignore_permissions=True)
            created_counts["donor_types"] = created_counts.get("donor_types", 0) + 1

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
        created_counts["custom_fields"] = 1
    frappe.db.sql("UPDATE `tabDocType` SET `autoname`='naming_series:' WHERE `name`='Donor'")

    for d in DONORS_DATA:
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

    return created_counts
