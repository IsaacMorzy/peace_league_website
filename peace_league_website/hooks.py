import frappe
from frappe import _

app_title = "Peace League Website"
app_publisher = "Peace League"
app_description = "Peace League Website Portal"
app_icon = "octicon octicon-heart"
app_email = "info@peaceleagueafrica.org"

# ── DocType connections (for graphify knowledge graph) ──
# These document explicit relationships between DocTypes that
# graphify cannot infer from AST alone.
doc_type_connections = {
    "Donation": ["Cause", "Donor", "Mode of Payment", "Mpesa Settings", "Company"],
    "Cause": ["Donation"],
    "Volunteer": ["Volunteer Type"],
    "Chapter": ["Member"],
    "Lead": [],  # Created via contact form
}

# Extend frappe_npo's Donation with Peace League custom logic
extend_doctype_class = {
    "Donation": "peace_league_website.doctype.plw_donation.donation.Donation",
}

# Custom fields for standard DocTypes
custom_fields = [
    {
        "doctype": "Donation",
        "fieldname": "cause",
        "label": "Campaign/Cause",
        "fieldtype": "Link",
        "options": "Cause",
        "insert_after": "project",
        "in_list_view": 1,
        "in_standard_filter": 1,
        "search_index": 1,
    },
    {
        "doctype": "Donation",
        "fieldname": "checkout_request_id",
        "label": "M-Pesa Checkout Request ID",
        "fieldtype": "Data",
        "insert_after": "donation_payments",
        "read_only": 1,
    },
    {
        "doctype": "Donation",
        "fieldname": "mpesa_receipt",
        "label": "M-Pesa Receipt Number",
        "fieldtype": "Data",
        "insert_after": "checkout_request_id",
        "read_only": 1,
    },
    {
        "doctype": "Donation",
        "fieldname": "phone",
        "label": "Phone",
        "fieldtype": "Data",
        "insert_after": "email",
        "in_list_view": 1,
    },
    {
        "doctype": "Donation",
        "fieldname": "anonymous",
        "label": "Anonymous Donor",
        "fieldtype": "Check",
        "default": "0",
        "insert_after": "phone",
    },
    {
        "doctype": "Donation",
        "fieldname": "message",
        "label": "Message",
        "fieldtype": "Small Text",
        "insert_after": "message_section",
    },
    {
        "doctype": "Donation",
        "fieldname": "payment_method",
        "label": "Payment Method",
        "fieldtype": "Data",
        "insert_after": "mode_of_payment",
        "in_list_view": 1,
        "in_standard_filter": 1,
        "read_only": 1,
        "allow_on_submit": 1,
    },
    {
        "doctype": "Donation",
        "fieldname": "status",
        "label": "Status",
        "fieldtype": "Select",
        "options": "Pending\nReceived\nFailed",
        "default": "Pending",
        "insert_after": "payment_method",
        "in_list_view": 1,
        "in_standard_filter": 1,
        "read_only": 1,
        "allow_on_submit": 1,
    },
]
