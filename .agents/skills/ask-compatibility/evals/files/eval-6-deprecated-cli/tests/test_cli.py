from cli import export


def test_limit_zero_means_all():
    assert len(export(0)) == 100
