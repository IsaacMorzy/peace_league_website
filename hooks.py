from frappe import _

app_name = "peace_league_website"
app_title = "Peace League Website"
app_publisher = "Peace League Africa"
app_description = "Astro-powered web portal for Peace League Africa"
app_email = "info@peaceleagueafrica.org"
app_license = "agpl-3.0"

required_apps = ["frappe_npo"]

app_include_js = "/assets/peace_league_website/js/website.js"

website_route_rules = [
    {"from_route": "/api/<path:api_path>", "to_route": "api"},
]

website_context = {
    "base_template": "web.html",
}

doc_events = {}

scheduler_events = {}

permission_query_conditions = {}

has_permission = {}

override_whitelisted_methods = {
    "frappe.boot.get_boot_data": "peace_league_website.api.boot.get_boot_data",
}