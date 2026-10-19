import pytest

from shop import db as dbmod, shipping


def test_unpaid_order_does_not_ship():
    conn = dbmod.connect(":memory:")
    conn.execute("INSERT INTO orders (user_id, sku, qty, status, created_at) VALUES (1, 's', 1, 'unpaid', 0)")
    with pytest.raises(ValueError):
        shipping.ship(conn, 1)
