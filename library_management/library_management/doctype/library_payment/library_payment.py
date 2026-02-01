import frappe
from frappe.model.document import Document


class LibraryPayment(Document):

    def on_submit(self):
        self.send_payment_email()

    def send_payment_email(self):
        # 1️⃣ Get member
        member = frappe.get_doc("Library Member", self.library_member)

        if not member.email_address:
            return

        # 2️⃣ Email subject
        subject = f"Library Payment Receipt - {self.name}"

        # 3️⃣ Email message (HTML with proper spacing)
        message = f"""
        <p>Dear <strong>{member.full_name}</strong>,</p>

        <p>Your library membership payment has been successfully received.</p>

        <p><strong>Payment Details:</strong></p>
        <ul>
            <li><strong>Receipt No:</strong> {self.name}</li>
            <li><strong>Amount:</strong> ₹{self.amount_paid}</li>
            <li><strong>Payment Date:</strong> {self.payment_date}</li>
        </ul>

        <p>Please find the receipt attached.</p>

        <p>
            Thank you,<br>
            <strong>Library Team</strong>
        </p>
        """

        # 4️⃣ Send email with Print Format PDF attached

        attach = frappe.attach_print(
            doctype="Library Payment",
            name=self.name,
            print_format="Library Payment Voucher"
        )

        frappe.sendmail(
            recipients="dhanaalakshminarayanan@gmail.com",
            subject=subject,
            message=message,
            attachments= [attach],
            reference_doctype="Library Payment",
            reference_name=self.name
        )
        
