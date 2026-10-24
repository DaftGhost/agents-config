# tinyserve 2.0
- `.ini` config files are no longer read. Use `config.toml`.
- `[server] host` and `port` are merged into `[server] listen = "host:port"`.
- `[limits]` is now `[server.limits]`, and `max_conn` is now `max_connections`.
