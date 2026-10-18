class SubmitService:
    def __init__(self, client):
        self._client = client

    def submit(self, order):
        response = self._client.post(
            "/orders", json=order.to_payload(), timeout=10
        )
        response.raise_for_status()
        return response.json()
