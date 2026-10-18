class LegacyClient:
    def fetch(self, key):
        return {"key": key, "via": "legacy"}
