RATES = {
    ("USD", "EUR"): 0.92,
    ("EUR", "USD"): 1.08,
    ("USD", "JPY"): 150.0,
    ("JPY", "USD"): 1 / 150.0,
}


def convert(amount, source, target):
    if source == target:
        return amount
    try:
        rate = RATES[(source, target)]
    except KeyError:
        raise ValueError(f"unsupported currency pair: {source}->{target}") from None
    return amount * rate
