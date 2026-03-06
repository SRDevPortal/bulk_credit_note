import frappe
import logging

logger = logging.getLogger(__name__)

MODULE_DEF_NAME = "Bulk Credit Note"
APP_PY_MODULE = "bulk_credit_note"


# ---------------------------------------------------------
# Module Utilities
# ---------------------------------------------------------

def ensure_module_def(module_name: str, app_name: str):
    """Ensure Module Def exists."""
    if not frappe.db.exists("Module Def", module_name):
        logger.info(f"Creating Module Def: {module_name}")
        frappe.get_doc({
            "doctype": "Module Def",
            "module_name": module_name,
            "app_name": app_name
        }).insert(ignore_permissions=True)
        frappe.db.commit()


def reload_local_json_doctypes(names: list[str]):
    """Reload DocTypes shipped as JSON under doctype/"""
    for dn in names or []:
        try:
            logger.info(f"Reloading JSON DocType: {dn}")
            frappe.reload_doc(APP_PY_MODULE, "doctype", dn)
        except Exception as e:
            logger.warning(f"Failed to reload DocType {dn}: {e}")