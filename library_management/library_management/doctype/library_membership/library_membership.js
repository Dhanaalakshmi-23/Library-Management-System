// Copyright (c) 2026, Dhanaa Lakshmi and contributors
// For license information, please see license.txt

frappe.ui.form.on("Library Membership", {

    package: function(frm) {
        let days = 0;

        if (frm.doc.package === "100") {
            days = 10;
        } 
        else if (frm.doc.package === "200") {
            days = 20;
        } 
        else if (frm.doc.package === "300") {
            days = 30;
        }

        frm.set_value("membership_days", days);

        // Auto calculate to_date if from_date exists
        if (frm.doc.from_date && days > 0) {
            let to_date = frappe.datetime.add_days(frm.doc.from_date, days);
            frm.set_value("to_date", to_date);
        }
    },

    from_date: function(frm) {
        if (frm.doc.from_date && frm.doc.membership_days > 0) {
            let to_date = frappe.datetime.add_days(
                frm.doc.from_date,
                frm.doc.membership_days
            );
            frm.set_value("to_date", to_date);
        }
    }
});
