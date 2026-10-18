CREATE TABLE sessions (id TEXT, user_id INT, expires_at TIMESTAMP);
CREATE TABLE payments (id INT, user_id INT, cents INT, created TIMESTAMP);
