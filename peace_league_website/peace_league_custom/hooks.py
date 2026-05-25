# Copyright (c) 2021, Peace League and contributors
# For license information, please see license.txt

app_include_js = "assets/js/peace_league_custom.min.js"
app_include_css = "assets/css/peace_league_custom.min.css"

# Custom Fields
custom_fields = [
    {"doctype": "Donation", "fieldname": "cause", "label": "Campaign/Cause", "fieldtype": "Link", "options": "Cause", "insert_after": "project", "in_list_view": 1, "in_standard_filter": 1, "search_index": 1}
]

# Custom Scripts
custom_scripts = {
    "Donation": "donation_custom.js"
}

# Override Controllers
override_whitelisted_methods = {
    "frappe_npo.non_profit.doctype.donation.donation.validate": "peace_league_custom.doctype.donation.donation.validate",
    "frappe_npo.non_profit.doctype.donation.donation.before_update_after_submit": "peace_league_custom.doctype.donation.donation.before_update_after_submit"
}