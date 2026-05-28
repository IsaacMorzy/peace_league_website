"""
Seed donation records for development.

Graph edges: creates: Donation
Graph edges: references: Donor (via email)
"""

import frappe

logger = frappe.logger("peace_league", allow_site=True, file_count=5)

DONATIONS_DATA = [
    {"donor_email": "william.thompson@charity.org", "amount": 250, "mode_of_payment": "Online"},
    {"donor_email": "elizabeth.davis@charity.org", "amount": 500, "mode_of_payment": "Wire Transfer"},
    {"donor_email": "donations@peacefdn.org", "amount": 1000, "mode_of_payment": "Cheque"},
    {"donor_email": "michael.lee@email.com", "amount": 100, "mode_of_payment": "Online"},
    {"donor_email": "giving@globalaid.org", "amount": 2000, "mode_of_payment": "Wire Transfer"},
]


def seed_donations():
    """Create sample Donation records linked to existing Donors.

    Graph edges: creates: Donation
    Graph edges: references: Donor
    """
    created_counts = {}

    for d in DONATIONS_DATA:
        donor_name = frappe.db.get_value("Donor", {"email": d["donor_email"]}, "name")
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

    return created_counts
