from shop import orders, payments, admin


def post_order(db, body):
    return {"id": orders.create_order(db, body["user_id"], body["sku"], body["qty"])}


def post_cancel(db, order_id):
    orders.cancel_order(db, order_id)
    return {"ok": True}


def post_gateway_callback(db, payload, signature):
    payments.handle_payment_callback(db, payload, signature)
    return {"ok": True}


def post_admin_mark_paid(db, order_id):
    admin.mark_paid_by_transfer(db, order_id)
    return {"ok": True}
