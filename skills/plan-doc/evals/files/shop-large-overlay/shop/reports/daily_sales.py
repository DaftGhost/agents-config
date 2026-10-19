def daily_sales(db, day_start, day_end):
    return db.execute(
        "SELECT sku, SUM(qty) FROM orders WHERE status = 'paid' AND created_at >= ? AND created_at < ? GROUP BY sku",
        (day_start, day_end),
    ).fetchall()
