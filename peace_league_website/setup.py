import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def add_custom_fields():
    create_custom_fields({
        "Donation": [
            dict(
                fieldname="phone",
                label="Phone",
                fieldtype="Data",
                insert_after="email",
            ),
            dict(
                fieldname="message",
                label="Message",
                fieldtype="Small Text",
                insert_after="phone",
            ),
            dict(
                fieldname="anonymous",
                label="Anonymous Donation",
                fieldtype="Check",
                insert_after="message",
            ),
            dict(
                fieldname="payment_method",
                label="Payment Method",
                fieldtype="Select",
                options="Cash\nCard\nMPesa\nMobile Money\nBank Transfer",
                insert_after="mode_of_payment",
            ),
            dict(
                fieldname="checkout_request_id",
                label="Checkout Request ID",
                fieldtype="Data",
                insert_after="payment_method",
            ),
            dict(
                fieldname="mpesa_receipt",
                label="M-Pesa Receipt",
                fieldtype="Data",
                insert_after="checkout_request_id",
            ),
            dict(
                fieldname="status",
                label="Status",
                fieldtype="Select",
                options="Pending\nReceived\nFailed\nRefunded",
                default="Pending",
                insert_after="paid",
            ),
        ]
    }, update=True)