import frappe


def before_insert(doc):
    if not doc.get("status"):
        doc.status = "Pending"
