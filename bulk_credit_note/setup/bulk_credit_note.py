import frappe
import logging

logger = logging.getLogger(__name__)

MODULE = "Bulk Credit Note"


def apply():
    """
    Apply setup logic for Bulk Credit Note.
    Safe to run multiple times.
    """

    logger.info("Applying Bulk Credit Note setup")

    # Ensure Module Def exists
    if not frappe.db.exists("Module Def", MODULE):
        frappe.get_doc({
            "doctype": "Module Def",
            "module_name": MODULE,
            "app_name": "bulk_credit_note"
        }).insert(ignore_permissions=True)

    # Future:
    # - Create workspace
    # - Create roles
    # - Create permissions
    # - Add custom fields
    # - Add reports

    frappe.clear_cache()