from db import query


def list_orders_v1(customer_id):  # GET /v1/orders
    return query("SELECT * FROM orders_legacy WHERE customer_id = ?", customer_id)
