from acme_utils import fmt_money


def test_fmt():
    assert fmt_money(1234) == "USD 12.34"
