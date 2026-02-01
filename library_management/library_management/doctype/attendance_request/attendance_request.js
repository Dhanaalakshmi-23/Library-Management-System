// Copyright (c) 2026, Dhanaa Lakshmi and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Attendance Request", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on("Attendance Request", {
    on_submit: function(frm) {
        if (!frm.doc.reason) {
            frappe.msgprint("Reason is mandatory");
            frappe.validated = false;
        }
    }
});
