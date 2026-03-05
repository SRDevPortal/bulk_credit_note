import frappe
import logging

logger = logging.getLogger(__name__)

APP = "bulk_credit_note"
MODULE = "Bulk Credit Note"

# Customizations potentially created by this app
CUSTOMIZATION_DT_LIST = [
    "Custom Field",
    "Property Setter",
    "Client Script",
    "Server Script",
    "Workspace",
    "Workspace Link",
    "Print Format",
    "Report",
    "Dashboard Chart",
    "Notification",
    "Web Template",
    "Form Tour",
    "Form Tour Step",
    "Custom DocPerm",
]


# ---------------------------------------------------------
# Utility Functions
# ---------------------------------------------------------

def _delete_all(dt, filters=None):
    """Delete documents safely."""
    if not frappe.db.exists("DocType", dt):
        return

    filters = filters or {}

    meta = frappe.get_meta(dt)
    valid_filters = {
        k: v for k, v in filters.items()
        if k in meta.get_valid_columns()
    }

    names = frappe.get_all(dt, pluck="name", filters=valid_filters)

    for name in names:
        try:
            frappe.delete_doc(
                dt,
                name,
                force=True,
                ignore_permissions=True,
                delete_permanently=True,
            )
        except Exception:
            logger.warning(f"Could not delete {dt}: {name}")


def _delete_module_doctypes():
    """
    Remove custom DocTypes created under this module.
    (Bench normally removes these automatically,
     but this acts as a safety net.)
    """
    doctypes = frappe.get_all(
        "DocType",
        fields=["name", "module", "custom"],
        filters={"module": MODULE},
    )

    for dt in doctypes:
        if not dt.custom:
            continue

        try:
            logger.info(f"Deleting custom DocType: {dt.name}")
            frappe.delete_doc(
                "DocType",
                dt.name,
                force=True,
                ignore_permissions=True,
                delete_permanently=True,
            )
        except Exception as e:
            logger.warning(f"Could not delete DocType {dt.name}: {e}")


def _delete_module_def():
    """Remove module record."""
    if frappe.db.exists("Module Def", MODULE):
        try:
            frappe.delete_doc(
                "Module Def",
                MODULE,
                force=True,
                ignore_permissions=True,
                delete_permanently=True,
            )
        except Exception as e:
            logger.warning(f"Failed to delete Module Def {MODULE}: {e}")


def _clear_global_search():
    """Clear global search entries to avoid ghost results."""
    try:
        frappe.db.sql(
            "DELETE FROM `__global_search` WHERE module=%s",
            (MODULE,),
        )
    except Exception:
        pass


# ---------------------------------------------------------
# Hooks
# ---------------------------------------------------------

def before_uninstall():
    """
    Runs BEFORE schema removal.
    This is the most important cleanup phase.
    """
    logger.info("===== Bulk Credit Note: Before Uninstall Started =====")

    frappe.clear_cache()

    # 1️⃣ Remove fixtures & customizations
    for dt in CUSTOMIZATION_DT_LIST:
        _delete_all(dt, {"module": MODULE})

    # 2️⃣ Remove custom DocTypes (safety net)
    _delete_module_doctypes()

    # 3️⃣ Clear search index
    _clear_global_search()

    frappe.db.commit()
    logger.info("===== Bulk Credit Note: Before Uninstall Completed =====")


def after_uninstall():
    """
    Runs AFTER app is removed.
    Final cleanup.
    """
    logger.info("===== Bulk Credit Note: After Uninstall Started =====")

    _delete_module_def()

    frappe.clear_cache()
    frappe.db.commit()

    logger.info("===== Bulk Credit Note: After Uninstall Completed =====")