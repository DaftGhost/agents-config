def on_order_created(order_id, user_id):
    return f"Order {order_id} placed; your items are reserved for you."


def on_order_cancelled(order_id, user_id):
    return f"Order {order_id} cancelled; reserved stock was returned."
