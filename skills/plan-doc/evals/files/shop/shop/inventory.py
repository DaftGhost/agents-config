class OutOfStock(Exception):
    pass


def deduct(db, sku, qty):
    cur = db.execute("UPDATE stock SET qty = qty - ? WHERE sku = ? AND qty >= ?", (qty, sku, qty))
    if cur.rowcount == 0:
        raise OutOfStock(sku)


def restore(db, sku, qty):
    db.execute("UPDATE stock SET qty = qty + ? WHERE sku = ?", (qty, sku))
