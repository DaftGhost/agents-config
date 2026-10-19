HITS = {}


def allow(key, limit=60):
    HITS[key] = HITS.get(key, 0) + 1
    return HITS[key] <= limit
