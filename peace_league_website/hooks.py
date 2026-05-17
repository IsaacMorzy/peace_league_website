import frappe
from frappe import _

extend_doctype_class = {
    "Donation": "peace_league_website.donation.donation.before_insert",
}
