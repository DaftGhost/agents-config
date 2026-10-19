RATE = 0.13


def with_tax(cents):
    return round(cents * (1 + RATE))
