from src.cache import CACHE, get, invalidate, set


def test_set_then_get_returns_value():
    CACHE.clear()
    set("user:1", {"name": "Ada"})
    assert get("user:1") == {"name": "Ada"}


def test_invalidate_removes_matching_keys():
    CACHE.clear()
    set("user:1", {"name": "Ada"})
    set("user:2", {"name": "Grace"})
    invalidate("user:1")
    assert get("user:1") is None
    assert get("user:2") == {"name": "Grace"}
