"""
Patch: Create Awards Admin role.

This role grants access to manage Awards categories, nominations, and view vote stats.
"""

import frappe

def execute():
    role_name = "Awards Admin"
    if not frappe.db.exists("Role", role_name):
        role = frappe.get_doc({
            "doctype": "Role",
            "role_name": role_name,
            "desk_access": 1,
            "is_default": 0,
            "disabled": 0
        })
        role.insert(ignore_permissions=True)
        frappe.db.commit()
        frappe.logger().info(f"Created role: {role_name}")
    else:
        frappe.logger().info(f"Role {role_name} already exists")
