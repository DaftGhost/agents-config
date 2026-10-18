from api.orders import serialize_order


class O:
    id, status, total = 5, "paid", 30


def test_serialize():
    assert serialize_order(O())["status_code"] == "paid"
