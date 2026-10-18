from acme_sdk import LegacyClient


def build(key):
    return LegacyClient().fetch(key)
