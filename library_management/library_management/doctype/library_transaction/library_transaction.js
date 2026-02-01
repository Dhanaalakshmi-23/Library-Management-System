// Copyright (c) 2026, Dhanaa Lakshmi and contributors
// For license information, please see license.txt
frappe.ui.form.on("Library Transaction", {
    setup(frm) {
        frm.set_query("article", () => {
            return {
                filters: {
                    status: "Available",
                    available_quantity: [">", 0]
                }
            };
        });
    }
});
frappe.ui.form.on("Library Transaction", {
    onload: function(frm) {
        frm.set_query("library_member", function() {
            return {
                filters: {
                    status: "Active"
                }
            };
        });
    }
});

frappe.ui.form.on("Library Transaction", {
    refresh(frm) {

        if (!frm.is_new()) {

            frm.add_custom_button("Update Books", () => {

                let dialog = new frappe.ui.Dialog({
                    title: "Update Books",
                    size: "large",
                    fields: [
                        {
                            fieldname: "articles_table",
                            fieldtype: "Table",
                            label: "Books",
                            cannot_add_rows: false,
                            in_place_edit: true,
                            fields: [
                                {
                                    fieldtype: "Link",
                                    fieldname: "article_name",
                                    label: "Article",
                                    options: "Article",
                                    in_list_view: 1,
                                    reqd: 1
                                },
                                {
                                    fieldtype: "Select",
                                    fieldname: "status",
                                    label: "Status",
                                    options: "Issue\nReturn",
                                    in_list_view: 1,
                                    reqd: 1
                                }
                            ]
                        }
                    ],

                    primary_action_label: "Update Books",

                    primary_action(values) {

                        // ✅ collect existing articles
                        let existing_articles = new Set();

                        (frm.doc.articles || []).forEach(row => {
                            existing_articles.add(row.article_name);
                        });

                        // ❗ clear and re-add (keeps edit + delete behavior)
                        frm.clear_table("articles");

                        (values.articles_table || []).forEach(row => {
                            let child = frm.add_child("articles");
                            child.article_name = row.article_name;
                            child.status = row.status;
                        });

                        frm.refresh_field("articles");

                        // handle draft + submitted
                        if (frm.doc.docstatus === 1) {
                            frm.save("Update");   // Update After Submit
                        } else {
                            frm.save();
                        }

                        dialog.hide();
                    }
                });

                // ✅ preload existing child table data
                let dialog_data = [];

                (frm.doc.articles || []).forEach(row => {
                    dialog_data.push({
                        article_name: row.article_name,
                        status: row.status
                    });
                });

                dialog.fields_dict.articles_table.df.data = dialog_data;
                dialog.fields_dict.articles_table.grid.refresh();

                dialog.show();
            });
        }
    }
});


