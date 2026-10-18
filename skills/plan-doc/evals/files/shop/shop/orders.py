import time

from shop import inventory


def create_order(db, user_id, sku, qty):
    """Create an unpaid order and deduct stock immediately (raises OutOfStock)."""
    inventory.deduct(db, sku, qty)
    cur = db.execute(
        "INSERT INTO orders (user_id, sku, qty, status, created_at) VALUES (?, ?, ?, 'unpaid', ?)",
        (user_id, sku, qty, int(time.time())),
    )
    db.commit()
    return cur.lastrowid


def mark_paid(db, order_id):
    db.execute("UPDATE orders SET status = 'paid' WHERE id = ?", (order_id,))
    db.commit()


def cancel_order(db, order_id):
    """User-initiated cancel. Restores the stock that was deducted at order time."""
    sku, qty = db.execute("SELECT sku, qty FROM orders WHERE id = ?", (order_id,)).fetchone()
    db.execute("UPDATE orders SET status = 'cancelled' WHERE id = ?", (order_id,))
    inventory.restore(db, sku, qty)
    db.commit()
