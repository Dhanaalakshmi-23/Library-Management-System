import frappe
from frappe.utils import today

def auto_expire_memberships():
    memberships = frappe.get_all(
        "Library Membership",
        filters={
            "to_date": ["<", today()],
            "status": "Active"
        },
        fields=["name"]
    )

    for m in memberships:
        frappe.db.set_value(
            "Library Membership",
            m.name,
            "status",
            "Expired"
        )

    frappe.db.commit()

from frappe.utils import today, add_days

def send_membership_expiry_reminder():
    tomorrow = add_days(today(), 1)

    memberships = frappe.get_all(
        "Library Membership",
        filters={
            "to_date": tomorrow,
            "status": "Active"
        },
        fields=[
            "name",
            "library_member",
            "full_name"
        ]
    )

    for m in memberships:
        if not m.library_member:
            continue

        # Fetch email from Library Member doctype
        member_email = frappe.db.get_value(
            "Library Member",
            m.library_member,
            "email_address"
        )

        if member_email:
            frappe.sendmail(
                recipients=member_email,
                subject="Library Membership Expiry Reminder",
                message=f"""
                Dear {m.full_name or 'Member'},<br><br>
                Your library membership will expire tomorrow.<br>
                Please renew to continue using library services.<br><br>
                Regards,<br>
                Library Management
                """
            )

    frappe.db.commit()
