def apply_member_discount(amount, is_member):
    return amount * 0.95 if is_member else amount


def apply_coupon(amount, coupon):
    return max(amount - coupon, 0) if coupon else amount


def checkout_total(subtotal, is_member=False, coupon=0):
    taxed = subtotal * (1 + 0.08)
    total = apply_member_discount(taxed, is_member)
    total = apply_coupon(total, coupon)
    return round(total, 2)
