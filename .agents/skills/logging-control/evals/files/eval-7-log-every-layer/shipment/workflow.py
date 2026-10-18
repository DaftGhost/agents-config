def ship_orders(orders, service):
    shipped = []
    failed = []
    for order in orders:
        try:
            shipped.append(service.ship(order))
        except Exception:
            failed.append(order.id)
    return {"shipped": shipped, "failed": failed}
