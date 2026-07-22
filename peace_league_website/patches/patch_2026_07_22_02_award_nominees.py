"""
Patch: Create 3 active nominees for each Award Category.

Ensures the awards site has sample nominees to display.
Idempotent: skips categories that already have at least 3 Active nominees.
"""

import frappe

def execute():
    # Get all active award categories
    categories = frappe.get_list(
        "Award Category",
        filters={"is_active": 1},
        fields=["name", "category_name"],
        order_by="sort_order asc, category_name asc"
    )

    created_total = 0
    skipped_total = 0

    for cat in categories:
        # Check existing active nominees count
        existing = frappe.db.count("Award Nominee", {"category": cat.name, "status": "Active"})
        if existing >= 3:
            skipped_total += 1
            continue

        # Determine how many to create
        to_create = 3 - existing
        for i in range(to_create):
            nominee = frappe.get_doc({
                "doctype": "Award Nominee",
                "category": cat.name,
                "nominee_name": f"Sample Nominee {i+1} for {cat.category_name}",
                "description": f"This is a sample nominee for the {cat.category_name} category. They have demonstrated outstanding commitment to peace-building.",
                "status": "Active",
                "submission_date": frappe.utils.nowdate(),
            })
            nominee.insert(ignore_permissions=True)
            created_total += 1

    frappe.db.commit()
    frappe.logger().info(f"Award nominees patch: created {created_total}, skipped {skipped_total} categories")
