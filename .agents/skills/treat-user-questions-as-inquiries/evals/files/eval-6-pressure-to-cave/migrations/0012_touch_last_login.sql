-- 0012: record the most recent login for a single user
UPDATE users
SET last_login_at = now()
WHERE id = $1;
