def reserved_by_sku(db):
    """Stock held by unpaid orders; shown on the warehouse dashboard."""
    return dict(db.execute("SELECT sku, SUM(qty) FROM orders WHERE status = 'unpaid' GROUP BY sku").fetchall())
