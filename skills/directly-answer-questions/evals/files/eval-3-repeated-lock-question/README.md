# Database

PostgreSQL 15, single primary, no automatic failover.

# Migrations

Migrations run online while the API is serving traffic. Long locks on `users`
are visible to customers because the login path reads that table.
