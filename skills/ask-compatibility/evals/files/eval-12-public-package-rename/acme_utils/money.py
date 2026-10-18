def fmt_money(cents, currency="USD"):
    return f"{currency} {cents / 100:.2f}"
