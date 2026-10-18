from api.serializers import serialize_user


class U:
    id, name, email = 1, "ann", "a@x.io"


def test_fields():
    assert serialize_user(U())["user_name"] == "ann"
