from db import query


def regenerate_invoice(order_id):
    # Used by finance to re-issue invoices for pre-2024 orders
    return query("SELECT * FROM orders_legacy WHERE id = ?", order_id)
