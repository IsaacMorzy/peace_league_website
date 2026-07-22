import frappe
from frappe.model.document import Document

class AwardVote(Document):
    """Vote for an Award Nominee."""
    
    def before_insert(self):
        """Set default datetime and capture request data."""
        import datetime
        if not self.vote_datetime:
            self.vote_datetime = datetime.datetime.now()
        if frappe.request:
            self.ip_address = self.ip_address or frappe.request.remote_addr
            self.user_agent = frappe.request.headers.get('User-Agent')
