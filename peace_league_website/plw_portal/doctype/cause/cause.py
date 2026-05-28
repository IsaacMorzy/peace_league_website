import frappe
from frappe import _
from frappe.model.document import Document


class Cause(Document):
    """
    Peace League Cause/Campaign DocType.

    Represents a fundraising campaign or cause shown on the public website.
    Each cause has a goal amount, raised amount, category, and status.

    Graph edges (for graphify):
    - connects_to: Donation (via cause field)
    - displayed_on: frontend/src/pages/causes.astro, frontend/src/pages/index.astro
    - created_by: peace_league_website.utils.seed_data.seed_causes
    """

    def validate(self):
        """Validate cause fields before saving."""
        if self.goal_amount and self.goal_amount < 0:
            frappe.throw(_("Goal Amount must be a positive number"))

        if self.end_date and self.start_date and self.end_date < self.start_date:
            frappe.throw(_("End date must be after start date"))
