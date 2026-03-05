console.log("Bulk Credit Note JS Loaded");

frappe.ui.form.on("Bulk Credit Note", {
    refresh: function(frm) {
        console.log("Parent form loaded");
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