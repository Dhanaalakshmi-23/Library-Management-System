import frappe

def execute():
    frappe.db.auto_commit_on_many_writes = True

    transactions = frappe.get_all(
        "Library Transaction",
        filters={
            "article": ["is", "set"]
        },
        fields=["name", "article", "date", "type", "docstatus"]
    )

    for txn in transactions:

        # safety check: skip if child rows already exist
        child_exists = frappe.db.exists(
            "Library Transaction Books",
            {
                "parent": txn.name,
                "parenttype": "Library Transaction",
                "parentfield": "articles"
            }
        )

        if child_exists:
            continue

        doc = frappe.get_doc("Library Transaction", txn.name)

        # 🔑 VERY IMPORTANT FLAGS
        doc.flags.ignore_permissions = True
        doc.flags.ignore_validate_update_after_submit = True

        row = doc.append("articles", {})
        row.article_name = txn.article

        if txn.type == "Issue":
            row.status = "Issue"
        else:
            row.status = "Return"

        # save WITHOUT changing docstatus
        doc.save()

    frappe.db.commit()
