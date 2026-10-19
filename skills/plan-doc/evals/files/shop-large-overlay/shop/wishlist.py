LISTS = {}


def add(user_id, sku):
    LISTS.setdefault(user_id, set()).add(sku)


def items(user_id):
    return sorted(LISTS.get(user_id, ()))
