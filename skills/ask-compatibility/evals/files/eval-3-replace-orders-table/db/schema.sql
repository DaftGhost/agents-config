CREATE TABLE orders_legacy (
  id INTEGER PRIMARY KEY,
  customer TEXT,
  total_cents INTEGER,
  created_at TEXT
);

CREATE TABLE orders (
  id INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL,
  total_cents INTEGER NOT NULL,
  created_at TEXT NOT NULL
);
