import logging

logger = logging.getLogger(__name__)


class PaymentGateway:
    def __init__(self, client):
        self._client = client

    def submit(self, order):
        try:
            response = self._client.post(
                "/payments", json=order.to_payload(), timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception:
            logger.exception("payment submit failed order_id=%s", order.id)
            raise
