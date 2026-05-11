import frappe
import json
import os

def execute():
    site = frappe.utils.get_site_path()
    app_path = os.path.join(site, "..", "apps", "peace_league_website", "peace_league_website", "doctype")
    app_path = os.path.abspath(app_path)
    
    DOC_TYPES = ["Program", "Chapter", "Volunteer", "Donation"]
    
    for doctype in DOC_TYPES:
        json_path = os.path.join(app_path, doctype.lower(), f"{doctype.lower()}.json")
        if os.path.exists(json_path):
            print(f"Installing {doctype}...")
            with open(json_path) as f:
                doc = json.load(f)
                doc["module"] = "Peace League Website"
                try:
                    dt = frappe.get_doc(doc)
                    dt.insert()
                    print(f"  Created {doctype}")
                except frappe.DuplicateEntryError:
                    print(f"  {doctype} already exists")
                except Exception as e:
                    print(f"  Error: {e}")
    
    frappe.db.commit()