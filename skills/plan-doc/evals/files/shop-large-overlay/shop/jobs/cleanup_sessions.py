from shop import db as dbmod, sessions

if __name__ == "__main__":
    sessions.purge_expired(dbmod.connect())
