import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS stock (sku TEXT PRIMARY KEY, qty INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    sku TEXT NOT NULL,
    qty INTEGER NOT NULL,
    status TEXT NOT NULL,          -- unpaid / paid / cancelled
    created_at INTEGER NOT NULL    -- unix seconds
);
"""


def connect(path="shop.db"):
    db = sqlite3.connect(path)
    db.executescript(SCHEMA)
    return db
