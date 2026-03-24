import frappe


def apply_credit_note_discount(doc, method=None):
    """
    Apply discount on Grand Total (forced override)
    """

    if doc.is_return and doc.return_against:

        original = frappe.get_doc("Sales Invoice", doc.return_against)

        if original.discount_amount:

            # prevent infinite loop
            if not doc.flags.discount_fixed:

                # doc.flags.discount_fixed = True

                # doc.apply_discount_on = "Net Total"
                # doc.discount_amount = -abs(original.discount_amount)
                # doc.additional_discount_percentage = original.additional_discount_percentage

                # doc.calculate_taxes_and_totals()
                # doc.db_update()

                doc.flags.discount_fixed = True

                # 🔥 Step 1: let ERPNext calculate normally
                doc.calculate_taxes_and_totals()

                # 🔥 Step 2: NOW override with Grand Total logic
                doc.apply_discount_on = "Grand Total"
                doc.discount_amount = -abs(original.discount_amount)
                doc.additional_discount_percentage = (
                    original.additional_discount_percentage
                )

                # 🔥 Step 3: force recalculation again
                doc.calculate_taxes_and_totals()

                # 🔥 Step 4: persist changes
                doc.db_update()