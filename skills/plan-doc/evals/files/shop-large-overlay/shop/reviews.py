REVIEWS = []


def add_review(user_id, sku, stars, text):
    REVIEWS.append((user_id, sku, stars, text))


def average(sku):
    xs = [r[2] for r in REVIEWS if r[1] == sku]
    return sum(xs) / len(xs) if xs else None
