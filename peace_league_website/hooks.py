import frappe
from frappe import _

app_title = "Peace League Website"
app_publisher = "Peace League"
app_description = "Peace League Website Portal"
app_icon = "octicon octicon-heart"
app_email = "info@peaceleagueafrica.com"

extend_doctype_class = {
    "Donation": "peace_league_website.doctype.plw_donation.donation.before_insert",
}
