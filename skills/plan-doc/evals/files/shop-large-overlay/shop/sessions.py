import time

SESSIONS = {}


def start(user_id):
    SESSIONS[user_id] = int(time.time())


def purge_expired(db, ttl=86400):
    now = int(time.time())
    for uid in [u for u, t in SESSIONS.items() if now - t > ttl]:
        del SESSIONS[uid]
