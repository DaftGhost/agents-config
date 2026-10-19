CATALOG = {}


def get_product(sku):
    return CATALOG.get(sku)


def list_products():
    return sorted(CATALOG)
