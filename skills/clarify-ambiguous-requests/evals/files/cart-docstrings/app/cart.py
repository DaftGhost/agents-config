def add_item(cart, sku, qty=1):
    cart[sku] = cart.get(sku, 0) + qty
    return cart


def remove_item(cart, sku):
    cart.pop(sku, None)
    return cart


def total(cart, prices):
    return sum(prices[sku] * qty for sku, qty in cart.items())
