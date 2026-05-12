app_name = "peace_league_website"
app_title = "Peace League Website"
app_publisher = "Peace League Africa"
app_description = "Astro-powered web portal for Peace League Africa"
app_email = "info@peaceleagueafrica.org"
app_license = "AGPL-3.0"

required_apps = ["frappe_npo"]

website_route_rules = [
	{"from_route": "/api/<path:api_path>", "to_route": "api"},
]

website_context = {
	"base_template": "web.html",
}

scheduler_events = {}

fixtures = []

permission_query_conditions = {}

has_permission = {}
