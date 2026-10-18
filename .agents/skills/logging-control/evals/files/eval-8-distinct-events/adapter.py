import logging

logger = logging.getLogger(__name__)


class RateLimited(Exception):
    def __init__(self, retry_after):
        self.retry_after = retry_after


class Gateway:
    def __init__(self, client):
        self._client = client

    def charge(self, order):
        try:
            response = self._client.post(
                "/charges", json={"order_id": order.id, "amount": order.total}
            )
            if response.status_code == 429:
                raise RateLimited(int(response.headers.get("Retry-After", "1")))
            response.raise_for_status()
            return response.json()
        except Exception:
            logger.exception(
                "gateway charge failed order_id=%s endpoint=%s",
                order.id,
                "/charges",
            )
            raise
