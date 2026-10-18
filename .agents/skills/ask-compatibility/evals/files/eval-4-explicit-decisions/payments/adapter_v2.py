def charge(order_id, cents, currency="USD"):
    return {"status": "ok", "order": order_id, "amount": cents, "currency": currency}
