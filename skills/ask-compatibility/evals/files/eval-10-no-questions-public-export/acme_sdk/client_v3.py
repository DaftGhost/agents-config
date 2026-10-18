class ClientV3:
    def get(self, key):
        return {"key": key, "via": "v3"}
