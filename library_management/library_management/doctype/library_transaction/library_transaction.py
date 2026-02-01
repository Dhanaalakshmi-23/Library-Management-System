import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus
from frappe.utils import date_diff

class LibraryTransaction(Document):

    # -------------------------------------------------
    # VALIDATE (runs on Save + Submit)
    # -------------------------------------------------

    def validate(self):
        self.validate_member_active()
        self.validate_membership()

    # -------------------------------------------------
    # BEFORE SUBMIT (runs only on Submit)
    # -------------------------------------------------

    def before_submit(self):
        for item in self.articles:
            self.process_article(item)

    # -------------------------------------------------
    # ARTICLE PROCESSING
    # -------------------------------------------------

    def process_article(self, item):
        article = frappe.get_doc("Article", item.article_name)

        if item.status == "Issue":
            if article.available_quantity <= 0:
                frappe.throw(f"Article {article.name} is out of stock")

            article.issued_quantity += 1
            item.status = "Issue"

        elif item.status == "Return":
            if article.issued_quantity <= 0:
                frappe.throw(f"Article {article.name} was not issued")

            article.issued_quantity -= 1
            item.status = "Return"

        article.available_quantity = (
            article.total_quantity - article.issued_quantity
        )

        article.save(ignore_permissions=True)

    # -------------------------------------------------
    # VALIDATIONS
    # -------------------------------------------------

    def validate_member_active(self):
        member = frappe.get_doc("Library Member", self.library_member)

        if member.status != "Active":
            frappe.throw(
                f"Library member {member.name} is inactive. Transaction not allowed."
            )

    def validate_membership(self):
        valid_membership = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "from_date": ("<=", self.date),
                "to_date": (">=", self.date),
                "docstatus": DocStatus.submitted(),
            },
        )

        if not valid_membership:
            frappe.throw("The member does not have a valid membership")


    def validate(self):
        self.calculate_fine()
        self.prevent_new_issue_if_fine_pending()

    def calculate_fine(self):
        settings = frappe.get_single("Library Settings")
        self.total_fine = 0

        for row in self.articles:
            if (
                row.status == "Return"
                and row.actual_return_date
                and row.expected_return_date
            ):
                late_days = date_diff(
                    row.actual_return_date,
                    row.expected_return_date
                )

                if late_days > 0:
                    self.total_fine += late_days * settings.amount_per_day

    def prevent_new_issue_if_fine_pending(self):
        if self.total_fine and self.total_fine > 0:
            frappe.throw(
                "Fine payment should be completed before issuing another book."
            )
