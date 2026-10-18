import pytest

from shop import db as dbmod, inventory, orders


@pytest.fixture
def db():
    conn = dbmod.connect(":memory:")
    conn.execute("INSERT INTO stock VALUES ('sku1', 5)")
    return conn


def test_create_order_deducts_stock(db):
    orders.create_order(db, 1, "sku1", 2)
    assert db.execute("SELECT qty FROM stock WHERE sku='sku1'").fetchone()[0] == 3


def test_out_of_stock(db):
    with pytest.raises(inventory.OutOfStock):
        orders.create_order(db, 1, "sku1", 9)
