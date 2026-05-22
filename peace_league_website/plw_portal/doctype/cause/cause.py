import frappe
from frappe.model.document import Document


class Cause(Document):
    def validate(self):
        if self.goal_amount and self.goal_amount < 0:
            frappe.throw("Goal Amount must be a positive number")

    def on_update(self):
        pass
