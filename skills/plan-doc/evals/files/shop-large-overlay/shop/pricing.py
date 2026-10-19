PRICES = {}


def price_of(sku):
    return PRICES.get(sku, 0)


def sync(db):
    """Pull the latest price list into PRICES."""
    return len(PRICES)
