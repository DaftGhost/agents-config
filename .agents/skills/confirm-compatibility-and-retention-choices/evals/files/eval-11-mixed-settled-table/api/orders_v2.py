from db import query


def list_orders_v2(customer_id):  # GET /v2/orders
    return query("SELECT * FROM orders WHERE customer_id = ?", customer_id)
