import hashlib
import hmac

from shop import orders

SECRET = b"gateway-secret"


def verify_signature(payload, signature):
    expected = hmac.new(SECRET, payload["order_id"].encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def handle_payment_callback(db, payload, signature):
    """Gateway callback; the same payment may be delivered several times."""
    if not verify_signature(payload, signature):
        raise PermissionError("bad signature")
    if payload["status"] == "success":
        orders.mark_paid(db, int(payload["order_id"]))
