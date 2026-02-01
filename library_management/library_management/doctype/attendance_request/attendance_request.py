# Copyright (c) 2026, Dhanaa Lakshmi and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
from frappe.utils import nowdate

class AttendanceRequest(Document):

    def on_update(self):
        if self.status == "Approved":
            self.approved_by = frappe.session.user
            self.approval_date = nowdate()
