-- 0007: mark users inactive after a year without login
ALTER TABLE users ADD COLUMN is_active boolean NOT NULL DEFAULT true;

UPDATE users
SET is_active = false
WHERE last_login_at < now() - interval '1 year';

CREATE INDEX CONCURRENTLY idx_users_is_active ON users (is_active);
