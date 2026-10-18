from pricing import quote, quote_with_coupon

ITEMS = [{"price": 60, "qty": 2}]


def test_quote():
    assert quote(ITEMS, False) == 114.0


def test_coupon():
    assert quote_with_coupon(ITEMS, True, 10) == 92.34
