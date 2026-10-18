CREATE TABLE orders_legacy (id INT, customer_id INT, total NUMERIC, created DATE);  -- 2018..2024, ~9M rows
CREATE TABLE orders        (id INT, customer_id INT, total NUMERIC, created DATE);  -- 2024-03 onward only
