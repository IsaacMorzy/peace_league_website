"""
Seed member records for development.

Graph edges: creates: Member, Membership Type
"""

import frappe

logger = frappe.logger("peace_league", allow_site=True, file_count=5)

MEMBERS_DATA = [
    {"member_name": "Alice Johnson", "email_id": "alice.johnson@email.com", "phone": "+1-555-0101"},
    {"member_name": "Robert Smith", "email_id": "robert.smith@email.com", "phone": "+1-555-0102"},
    {"member_name": "Maria Garcia", "email_id": "maria.garcia@email.com", "phone": "+1-555-0103"},
    {"member_name": "James Wilson", "email_id": "james.wilson@email.com", "phone": "+1-555-0104"},
    {"member_name": "Sarah Brown", "email_id": "sarah.brown@email.com", "phone": "+1-555-0105"},
]


def seed_members():
    """Create sample Member records.

    Graph edges: creates: Member, Membership Type
    """
    created_counts = {}

    if not frappe.db.exists("Membership Type", "Individual"):
        membership_type = frappe.get_doc({
            "doctype": "Membership Type",
            "membership_type": "Individual",
            "amount": 50,
        })
        membership_type.insert(ignore_permissions=True)
        created_counts["membership_types"] = 1
        logger.info("Membership Type created")

    for m in MEMBERS_DATA:
        if not frappe.db.exists("Member", {"email_id": m["email_id"]}):
            logger.info(f"Creating member: {m['member_name']} ({m['email_id']})")
            member = frappe.get_doc({
                "doctype": "Member",
                "naming_series": "NPO-MEM-.YYYY.-",
                "member_name": m["member_name"],
                "email_id": m["email_id"],
                "membership_type": "Individual",
                "membership_expiry_date": "2026-12-31",
            })
            member.insert(ignore_permissions=True)
            created_counts["members"] = created_counts.get("members", 0) + 1
            logger.info(f"Member inserted: {member.name}")

    return created_counts
