import frappe
from frappe import _
from frappe.model.document import Document


class Donation(Document):
    """
    Peace League Donation DocType.

    Extends the base Donation with:
    - Automatic status default on creation
    - Cause/campaign validation
    - M-Pesa payment integration fields

    Graph edges (for graphify):
    - connects_to: Cause, Donor, Mode of Payment, Mpesa Settings
    - implements: frappe_npo.non_profit.doctype.donation.donation.Donation
    """

    def before_insert(self):
        if not self.get("status"):
            self.status = "Pending"

    def validate(self):
        """Validate donation before saving."""
        # Validate cause if provided
        if self.cause and not frappe.db.exists("Cause", self.cause):
            frappe.throw(_("Cause {0} not found").format(self.cause))

        # Validate amount
        if self.amount and self.amount <= 0:
            frappe.throw(_("Donation amount must be positive"))

    def before_update_after_submit(self):
        """Re-validate cause on update after submit."""
        if self.cause and not frappe.db.exists("Cause", self.cause):
            frappe.throw(_("Cause {0} not found").format(self.cause))
