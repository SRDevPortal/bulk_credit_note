import frappe
import logging

from . import masters

logger = logging.getLogger(__name__)


def _should_skip():
    if getattr(frappe.flags, "in_test", False):
        return True
    if getattr(frappe.flags, "in_patch", False):
        return True
    return False


def setup_all():
    """
    Main setup orchestrator.
    Safe & idempotent.
    """

    if _should_skip():
        logger.info("Skipping Bulk Credit Note setup (test/patch context)")
        return

    logger.info("🚀 Bulk Credit Note setup started")

    try:
        masters.apply()

        frappe.clear_cache()
        frappe.db.commit()

        logger.info("✅ Bulk Credit Note setup completed")

    except Exception as e:
        frappe.db.rollback()
        logger.error(f"❌ Bulk Credit Note setup failed: {e}")
        raise