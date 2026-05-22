import frappe
from frappe.model.document import Document


class Donation(Document):
    def before_insert(self):
        if not self.get("status"):
            self.status = "Pending"
