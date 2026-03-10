console.log("Bulk Credit Note JS Loaded");

frappe.ui.form.on("Bulk Credit Note", {

    onload: function(frm) {

        // Auto set company from Global Defaults if empty
        if (!frm.doc.company) {

            frappe.call({
                method: "frappe.client.get_single_value",
                args: {
                    doctype: "Global Defaults",
                    field: "default_company"
                },
                callback: function(r) {
                    if (r.message) {
                        frm.set_value("company", r.message);
                    }
                }
            });

        }

    },

    refresh: function(frm) {
        console.log("Parent form loaded");
    },

    scan_sales_invoice: function(frm) {

        let invoice = frm.doc.scan_sales_invoice;

        if (!invoice) return;

        // Prevent duplicate invoices
        let exists = (frm.doc.items || []).some(row => row.sales_invoice === invoice);

        if (exists) {
            frappe.msgprint("Sales Invoice already added.");
            frm.set_value("scan_sales_invoice", "");
            return;
        }

        frappe.call({
            method: "bulk_credit_note.api.bulk_credit_note.get_sales_invoice_data",
            args: {
                invoice_no: invoice
            },
            callback: function(r) {

                if (!r.message) {
                    frappe.msgprint("Sales Invoice not found");
                    frm.set_value("scan_sales_invoice", "");
                    return;
                }

                // Add row in child table
                let row = frm.add_child("items");

                row.sales_invoice = invoice;
                row.customer = r.message.customer;
                row.posting_date = r.message.posting_date;
                row.grand_total = r.message.grand_total;
                row.outstanding_amount = r.message.outstanding_amount;
                row.update_stock = r.message.update_stock;

                frm.refresh_field("items");

                // Set parent posting date from first invoice
                if (frm.doc.items.length === 1) {
                    frm.set_value("posting_date", r.message.posting_date);
                }

                // Clear scan field for next scan
                frm.set_value("scan_sales_invoice", "");

                // Focus again for next scan
                frm.fields_dict.scan_sales_invoice.$input.focus();

            }
        });

    }

});


frappe.ui.form.on("Bulk Credit Note Item", {
    sales_invoice: function(frm, cdt, cdn) {

        let row = locals[cdt][cdn];
        if (!row.sales_invoice) return;

        frappe.call({
            method: "bulk_credit_note.api.bulk_credit_note.get_sales_invoice_data",
            args: {
                invoice_no: row.sales_invoice
            },
            callback: function(r) {

                if (!r.message) return;

                frappe.model.set_value(cdt, cdn, "customer", r.message.customer);
                frappe.model.set_value(cdt, cdn, "posting_date", r.message.posting_date);
                frappe.model.set_value(cdt, cdn, "grand_total", r.message.grand_total);
                frappe.model.set_value(cdt, cdn, "outstanding_amount", r.message.outstanding_amount);

                // Set update stock on child row
                frappe.model.set_value(cdt, cdn, "update_stock", r.message.update_stock);

                // Only set posting date on parent
                if (frm.doc.items.length === 1) {
                    frm.set_value("posting_date", r.message.posting_date);
                }
            }
        });
    }
});