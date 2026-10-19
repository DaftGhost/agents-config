from shop import db as dbmod, pricing

if __name__ == "__main__":
    pricing.sync(dbmod.connect())
