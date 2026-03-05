import frappe

MODULE_DEF_NAME = "Bulk Credit Note"
APP_PY_MODULE = "bulk_credit_note"


def ensure_module_def(module_name, app_name):
    """Ensure Module Def exists."""
    if not frappe.db.exists("Module Def", module_name):
        frappe.get_doc({
            "doctype": "Module Def",
            "module_name": module_name,
            "app_name": app_name
        }).insert(ignore_permissions=True)
        frappe.db.commit()