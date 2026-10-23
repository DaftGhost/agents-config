import sqlite3

db = sqlite3.connect("shop.db")


def create_order(customer_id, total_cents, created_at):
    db.execute(
        "INSERT INTO orders (customer_id, total_cents, created_at) VALUES (?, ?, ?)",
        (customer_id, total_cents, created_at),
    )


def revenue_report():
    # still reads the old table; finance uses this report for yearly totals
    return db.execute("SELECT SUM(total_cents) FROM orders_legacy").fetchone()[0]
