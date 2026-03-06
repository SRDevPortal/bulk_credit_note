# bulk_credit_note/install.py
import frappe
import logging

from .setup.runner import setup_all
from .setup.utils import MODULE_DEF_NAME, APP_PY_MODULE, ensure_module_def

logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# Utilities
# ---------------------------------------------------------

def _ensure_module():
    """Ensure Module Def exists (safety for partial installs)."""
    ensure_module_def(MODULE_DEF_NAME, APP_PY_MODULE)


def _clear_cache():
    frappe.clear_cache()


# ---------------------------------------------------------
# Lifecycle Hooks
# ---------------------------------------------------------

def before_install():
    """Runs before app installation."""
    logger.info("===== Bulk Credit Note: Before Install =====")
    frappe.clear_cache()


def after_install():
    """Runs once after app installation."""
    logger.info("===== Bulk Credit Note: After Install Started =====")

    try:
        _ensure_module()

        # Run full setup
        setup_all()

        _clear_cache()
        frappe.db.commit()

        logger.info("===== Bulk Credit Note: After Install Completed =====")

    except Exception as e:
        frappe.db.rollback()
        logger.error(f"❌ Bulk Credit Note install failed: {e}")
        raise


def after_migrate():
    """
    Runs after migrations.
    Must be idempotent.
    """
    logger.info("===== Bulk Credit Note: After Migrate Started =====")

    try:
        _ensure_module()

        # Re-run setup safely
        setup_all()

        _clear_cache()
        frappe.db.commit()

        logger.info("===== Bulk Credit Note: After Migrate Completed =====")

    except Exception as e:
        frappe.db.rollback()
        logger.error(f"❌ Bulk Credit Note migrate setup failed: {e}")
        raise
