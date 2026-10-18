from time import monotonic

CACHE = {}
TTL_SECONDS = 60


def get(key: str):
    entry = CACHE.get(key)
    if entry is None:
        return None
    value, expires_at = entry
    if monotonic() > expires_at:
        del CACHE[key]
        return None
    return value


def set(key: str, value) -> None:
    CACHE[key] = (value, monotonic() + TTL_SECONDS)


def invalidate(prefix: str) -> None:
    for key in [k for k in CACHE if k.startswith(prefix)]:
        del CACHE[key]
