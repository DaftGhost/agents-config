from shop import orders


def mark_paid_by_transfer(db, order_id):
    """Support confirmed a bank transfer outside the gateway, so mark the order paid."""
    orders.mark_paid(db, order_id)
