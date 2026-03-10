import frappe
from erpnext.controllers.sales_and_purchase_return import make_return_doc


@frappe.whitelist()
def get_sales_invoice_data(invoice_no):
    """
    Fetch Sales Invoice details for child table autofill.
    """

    if not invoice_no:
        return {}

    if not frappe.db.exists("Sales Invoice", invoice_no):
        frappe.throw("Sales Invoice not found")

    si = frappe.get_doc("Sales Invoice", invoice_no)

    return {
        "customer": si.customer,
        "posting_date": si.posting_date,
        "grand_total": si.grand_total,
        "outstanding_amount": si.outstanding_amount,
        "update_stock": si.update_stock
    }


def create_credit_notes_on_submit(doc, method=None):
    """
    Trigger background job for bulk credit note creation
    """

    frappe.enqueue(
        "bulk_credit_note.api.bulk_credit_note.process_bulk_credit_notes",
        docname=doc.name,
        queue="long",
        timeout=600
    )

    frappe.msgprint("Bulk Credit Note processing started in background.")


def process_bulk_credit_notes(docname):
    """
    Background job to generate credit notes
    """

    doc = frappe.get_doc("Bulk Credit Note", docname)

    created_credit_notes = []

    for row in doc.items:

        if not row.sales_invoice:
            continue

        if not frappe.db.exists("Sales Invoice", row.sales_invoice):
            frappe.log_error(f"Sales Invoice {row.sales_invoice} not found")
            continue

        si = frappe.get_doc("Sales Invoice", row.sales_invoice)

        existing = frappe.db.exists(
            "Sales Invoice",
            {
                "return_against": si.name,
                "is_return": 1,
                "docstatus": 1
            }
        )

        if existing:
            frappe.log_error(f"Credit Note already exists for {si.name}")
            continue

        # credit_note = make_return_doc("Sales Invoice", si.name)

        credit_note_data = make_return_doc("Sales Invoice", si.name)
        credit_note = frappe.get_doc(credit_note_data)

        credit_note.is_return = 1
        credit_note.return_against = si.name

        credit_note.posting_date = frappe.utils.today()
        credit_note.posting_time = frappe.utils.nowtime()

        credit_note.company = doc.company
        credit_note.update_stock = row.update_stock

        # Only invoice-level warehouse
        if row.update_stock:

            if not si.set_warehouse:
                frappe.log_error(
                    f"Sales Invoice {si.name} missing Source Warehouse"
                )
                continue

            credit_note.set_warehouse = si.set_warehouse

        credit_note.insert(ignore_permissions=True)
        credit_note.submit()

        created_credit_notes.append(credit_note.name)

    if created_credit_notes:
        frappe.publish_realtime(
            "msgprint",
            {
                "message": f"Credit Notes Created: {', '.join(created_credit_notes)}"
            }
        )


# @frappe.whitelist()
# def create_credit_notes_on_submit(doc, method=None):
#     """
#     Triggered when Bulk Credit Note is submitted.
#     Creates Credit Notes for each Sales Invoice.
#     """

#     created_credit_notes = []

#     for row in doc.items:

#         if not row.sales_invoice:
#             continue

#         if not frappe.db.exists("Sales Invoice", row.sales_invoice):
#             frappe.throw(f"Sales Invoice {row.sales_invoice} not found")

#         si = frappe.get_cached_doc("Sales Invoice", row.sales_invoice)

#         # prevent duplicate return
#         existing = frappe.db.exists(
#             "Sales Invoice",
#             {
#                 "return_against": si.name,
#                 "is_return": 1,
#                 "docstatus": 1
#             }
#         )

#         if existing:
#             frappe.throw(f"Credit Note already exists for {si.name}")

#         # Create return INVOICE using ERPNext core
#         credit_note = make_return_doc("Sales Invoice", si.name)

#         credit_note.is_return = 1
#         credit_note.return_against = si.name
#         credit_note.posting_date = doc.posting_date
#         credit_note.company = doc.company
#         credit_note.update_stock = row.update_stock

#         # Use ONLY invoice-level warehouse
#         if row.update_stock:

#             if not si.set_warehouse:
#                 frappe.throw(
#                     f"Sales Invoice {si.name} does not have Source Warehouse"
#                 )

#             credit_note.set_warehouse = si.set_warehouse

#         credit_note.insert(ignore_permissions=True)
#         credit_note.submit()

#         created_credit_notes.append(credit_note.name)
    
#     frappe.msgprint(
#         f"Created Credit Notes: {', '.join(created_credit_notes)}"
#     )
