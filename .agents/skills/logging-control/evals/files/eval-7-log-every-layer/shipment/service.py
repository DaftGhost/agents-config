class ShipmentService:
    def __init__(self, client, repo):
        self._client = client
        self._repo = repo

    def ship(self, order):
        result = self._client.create_shipment(order)
        self._repo.mark_shipped(order.id, result["tracking_number"])
        return result["tracking_number"]
