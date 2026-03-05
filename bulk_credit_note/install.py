import frappe
import logging

from .setup.runner import setup_all

logger = logging.getLogger(__name__)


def before_install():
    frappe.clear_cache()


def after_install():
    try:
        setup_all()
        frappe.clear_cache()
        frappe.db.commit()
    except Exception:
        frappe.db.rollback()
        raise


def after_migrate():
    try:
        setup_all()
        frappe.clear_cache()
        frappe.db.commit()
    except Exception:
        frappe.db.rollback()
        raise