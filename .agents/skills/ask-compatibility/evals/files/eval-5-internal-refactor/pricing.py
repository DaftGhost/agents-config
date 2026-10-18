def quote(items, member):
    t = 0
    for i in items:
        p = i["price"] * i["qty"]
        if member:
            p = p - p * 0.1
        t = t + p
    d = 0
    if t > 100:
        d = t * 0.05
    return round(t - d, 2)


def quote_with_coupon(items, member, pct):
    t = 0
    for i in items:
        p = i["price"] * i["qty"]
        if member:
            p = p - p * 0.1
        t = t + p
    d = 0
    if t > 100:
        d = t * 0.05
    return round((t - d) * (1 - pct / 100), 2)
