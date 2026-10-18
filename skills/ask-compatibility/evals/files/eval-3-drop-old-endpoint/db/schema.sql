CREATE TABLE login_history (user_id INT, ts TIMESTAMP, ip TEXT, quarter TEXT);  -- ~40M rows, since 2019
CREATE TABLE auth_events  (user_id INT, ts TIMESTAMP, kind TEXT, ip TEXT);      -- since 2025-06, no backfill
