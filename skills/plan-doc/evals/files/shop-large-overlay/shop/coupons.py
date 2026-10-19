CODES = {"WELCOME10": 10}


def discount_percent(code):
    return CODES.get(code, 0)
