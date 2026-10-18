class CarrierClient:
    def __init__(self, session, base_url):
        self._session = session
        self._base_url = base_url

    def create_shipment(self, order):
        response = self._session.post(
            f"{self._base_url}/shipments", json=order.to_payload(), timeout=10
        )
        response.raise_for_status()
        return response.json()
