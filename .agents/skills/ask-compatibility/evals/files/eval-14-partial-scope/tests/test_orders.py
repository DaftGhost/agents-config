from api.orders import serialize_order


class O:
    id, status, total = 5, "paid", 30


def test_serialize():
    out = serialize_order(O())
    assert out["status_code"] == "paid" and out["total"] == 30
