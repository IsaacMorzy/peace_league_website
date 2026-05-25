# Copyright (c) 2021, Peace League and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe_npo.non_profit.doctype.donation.donation import Donation as BaseDonation


class Donation(BaseDonation):
    def validate(self):
        super().validate()
        # Validate cause if provided
        if self.cause and not frappe.db.exists("Cause", self.cause):
            frappe.throw(_("Cause {0} not found").format(self.cause))

    def before_update_after_submit(self):
        super().before_update_after_submit()
        # Ensure cause is valid if provided
        if self.cause and not frappe.db.exists("Cause", self.cause):
            frappe.throw(_("Cause {0} not found").format(self.cause))