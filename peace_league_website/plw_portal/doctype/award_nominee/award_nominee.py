import frappe
from frappe.model.document import Document

class AwardNominee(Document):
    """Award Nominee for Peace League Awards."""
    
    def before_insert(self):
        """Set defaults on creation."""
        if not self.submission_date:
            self.submission_date = frappe.utils.today()
        # Capture IP and user agent from request if available
        if frappe.request:
            self.ip_address = frappe.request.remote_addr
            self.user_agent = frappe.request.headers.get('User-Agent')
