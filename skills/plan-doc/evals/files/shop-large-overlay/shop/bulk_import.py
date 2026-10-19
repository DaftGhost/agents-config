"""Partner CSV import: partners prepay offline, so orders are created already paid."""
import csv
import time

from shop import inventory


def import_partner_orders(db, path):
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            qty = int(row["qty"])
            inventory.deduct(db, row["sku"], qty)
            db.execute(
                "INSERT INTO orders (user_id, sku, qty, status, created_at) VALUES (?, ?, ?, 'paid', ?)",
                (int(row["user_id"]), row["sku"], qty, int(time.time())),
            )
    db.commit()
