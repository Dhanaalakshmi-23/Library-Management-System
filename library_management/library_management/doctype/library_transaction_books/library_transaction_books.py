# Copyright (c) 2026, Dhanaa Lakshmi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import add_days

class LibraryTransactionBooks(Document):

    def validate(self):
        if self.issue_date and not self.expected_return_date:
            settings = frappe.get_single("Library Settings")
            self.expected_return_date = add_days(
                self.issue_date,
                settings.loan_period
            )

