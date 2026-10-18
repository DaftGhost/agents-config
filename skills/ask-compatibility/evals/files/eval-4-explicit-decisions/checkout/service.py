from payments import adapter_v1


def pay(order_id, cents):
    return adapter_v1.charge(order_id, cents)["status"] == "ok"
