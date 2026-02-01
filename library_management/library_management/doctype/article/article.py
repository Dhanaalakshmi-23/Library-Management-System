# Copyright (c) 2026, Dhanaa Lakshmi and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Article(Document):
    def calculate_availability(self):
        frappe.msgprint("AAAAAAAAA")
        self.available_quantity = (self.total_quantity or 0) - (self.issued_quantity or 0)

        if self.available_quantity <= 0:
            self.status = "Issued"
        else:
            self.status = "Available"