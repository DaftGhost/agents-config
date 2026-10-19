def ship(db, order_id):
    status = db.execute("SELECT status FROM orders WHERE id = ?", (order_id,)).fetchone()[0]
    if status != "paid":
        raise ValueError("only paid orders ship")
    return {"order_id": order_id, "carrier": "std"}
