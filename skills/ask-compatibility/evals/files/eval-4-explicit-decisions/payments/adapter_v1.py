def charge(order_id, cents):
    return {"status": "ok", "table": "payments_v1", "order": order_id, "cents": cents}
