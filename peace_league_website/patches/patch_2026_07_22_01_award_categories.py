"""
Patch: Insert 55 Award Category fixtures.

This patch loads categories from fixtures/award_categories.json and creates
Award Category documents if they do not already exist.
"""

import json
import os
import frappe

def execute():
    # Path to the fixture file relative to the app directory
    fixture_path = os.path.join(os.path.dirname(__file__), '..', 'fixtures', 'award_categories.json')
    fixture_path = os.path.normpath(fixture_path)

    if not os.path.exists(fixture_path):
        frappe.log_error(f"Award categories fixture not found at {fixture_path}", "Patch failed")
        return

    with open(fixture_path, 'r') as f:
        categories = json.load(f)

    created = 0
    skipped = 0
    for cat in categories:
        # Check if category with this slug already exists
        if frappe.db.exists("Award Category", cat.get("slug")):
            skipped += 1
            continue

        doc = frappe.get_doc({
            "doctype": "Award Category",
            "category_name": cat.get("category_name"),
            "slug": cat.get("slug"),
            "description": cat.get("description", ""),
            "is_active": 1,
            "sort_order": 0
        })
        doc.insert(ignore_permissions=True)
        created += 1

    frappe.db.commit()
    frappe.logger().info(f"Award categories patch: created {created}, skipped {skipped}")
