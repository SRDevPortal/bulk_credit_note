import frappe
import logging

from .utils import MODULE_DEF_NAME, APP_PY_MODULE, ensure_module_def

logger = logging.getLogger(__name__)


def apply():
    """
    Apply master setup for Bulk Credit Note.
    Safe to run multiple times.
    """

    logger.info("Applying Bulk Credit Note masters setup")

    ensure_module_def(MODULE_DEF_NAME, APP_PY_MODULE)

    create_bulk_credit_note_doctype()
    create_bulk_credit_note_item_doctype()

    frappe.clear_cache()
    frappe.db.commit()

    logger.info("Bulk Credit Note masters setup completed")


# ---------------------------------------------------------
# DocType Creators
# ---------------------------------------------------------

def create_bulk_credit_note_doctype():
    """Create Bulk Credit Note parent DocType if missing."""

    doctype = "Bulk Credit Note"

    if frappe.db.exists("DocType", doctype):
        return

    logger.info(f"Creating DocType: {doctype}")

    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": doctype,
        "module": MODULE_DEF_NAME,
        "custom": 0,
        "autoname": "naming_series:",
        "track_changes": 1,
        "is_submittable": 1,
        "fields": [

            {
                "fieldname": "naming_series",
                "label": "Series",
                "fieldtype": "Select",
                "options": "BCN-.YYYY.-.#####",
                "default": "BCN-.YYYY.-.#####",
                "reqd": 1
            },

            {
                "fieldname": "company",
                "label": "Company",
                "fieldtype": "Link",
                "options": "Company",
                "reqd": 1,
                "default": frappe.defaults.get_user_default("Company"),
            },

            {
                "fieldname": "posting_date",
                "label": "Posting Date",
                "fieldtype": "Date",
                "reqd": 1,
                "default": "Today",
            },

            {
                "fieldname": "items_section",
                "label": "Invoices",
                "fieldtype": "Section Break"
            },

            {
                "fieldname": "items",
                "label": "Invoices",
                "fieldtype": "Table",
                "options": "Bulk Credit Note Item",
                "reqd": 1,
            }
        ],
        "permissions": [
            {
                "role": "System Manager",
                "read": 1,
                "write": 1,
                "create": 1,
                "delete": 1,
                "submit": 1,
                "cancel": 1,
                "amend": 1
            },
            {
                "role": "Accounts Manager",
                "read": 1,
                "write": 1,
                "create": 1,
                "submit": 1,
                "cancel": 1
            }
        ]
    })

    doc.insert(ignore_permissions=True)
    frappe.db.commit()


def create_bulk_credit_note_item_doctype():
    """Create Bulk Credit Note Item child table if missing."""

    doctype = "Bulk Credit Note Item"

    if frappe.db.exists("DocType", doctype):
        return

    logger.info(f"Creating DocType: {doctype}")

    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": doctype,
        "module": MODULE_DEF_NAME,
        "custom": 0,
        "istable": 1,
        "editable_grid": 1,
        "fields": [

            {
                "fieldname": "sales_invoice",
                "label": "Sales Invoice",
                "fieldtype": "Link",
                "options": "Sales Invoice",
                "reqd": 1,
                "in_list_view": 1,
                "columns": 2
            },

            {
                "fieldname": "customer",
                "label": "Customer",
                "fieldtype": "Link",
                "options": "Customer",
                "in_list_view": 1,
                "read_only": 1,
                "columns": 2
            },

            {
                "fieldname": "posting_date",
                "label": "Invoice Posting Date",
                "fieldtype": "Date",
                "read_only": 1,
                "in_list_view": 1,
                "columns": 1
            },

            {
                "fieldname": "grand_total",
                "label": "Grand Total",
                "fieldtype": "Currency",
                "read_only": 1,
                "in_list_view": 1,
                "columns": 2
            },

            {
                "fieldname": "outstanding_amount",
                "label": "Outstanding",
                "fieldtype": "Currency",
                "read_only": 1,
                "in_list_view": 1,
                "columns": 2
            },

            {
                "fieldname": "update_stock",
                "label": "Update Stock",
                "fieldtype": "Check",
                "default": 0,
                "read_only": 1,
                "in_list_view": 1,
                "columns": 1
            },
        ],
        "permissions": []
    })

    doc.insert(ignore_permissions=True)
    frappe.db.commit()