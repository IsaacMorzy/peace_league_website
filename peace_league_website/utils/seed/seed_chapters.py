"""
Seed chapter records for development.

Graph edges: creates: Chapter, Custom Field
Graph edges: references: Member (as chapter_head)
"""

import frappe

logger = frappe.logger("peace_league", allow_site=True, file_count=5)

CHAPTERS_DATA = [
    {"chapter_name": "Peace Builders New York", "region": "Northeast", "city": "New York", "address": "123 Peace Avenue, NY 10001"},
    {"chapter_name": "California Peace Alliance", "region": "West", "city": "Los Angeles", "address": "456 Harmony Street, CA 90001"},
    {"chapter_name": "Midwest Peace Initiative", "region": "Midwest", "city": "Chicago", "address": "789 Unity Road, IL 60601"},
    {"chapter_name": "Southern Peace Network", "region": "South", "city": "Atlanta", "address": "321 Calm Lane, GA 30301"},
    {"chapter_name": "Peace Council Texas", "region": "South", "city": "Houston", "address": "654 Serenity Blvd, TX 77001"},
]


def seed_chapters():
    """Create sample Chapter records.

    Graph edges: creates: Chapter
    Graph edges: references: Member (chapter_head)
    """
    created_counts = {}

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
        created_counts["custom_fields"] = 1
    frappe.db.sql("UPDATE `tabDocType` SET `autoname`='naming_series:' WHERE `name`='Chapter'")
    frappe.clear_cache(doctype="Chapter")

    first_member_list = frappe.get_all("Member", fields=["name"], order_by="creation asc", limit=1)
    first_member = first_member_list[0].name if first_member_list else None

    for c in CHAPTERS_DATA:
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

    return created_counts
