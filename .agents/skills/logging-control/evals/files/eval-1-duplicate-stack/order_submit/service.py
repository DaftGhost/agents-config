import logging

logger = logging.getLogger(__name__)


class OrderService:
    def __init__(self, gateway, repo):
        self._gateway = gateway
        self._repo = repo

    def submit(self, order):
        try:
            result = self._gateway.submit(order)
            self._repo.mark_submitted(order.id, result["payment_id"])
            return True
        except Exception:
            logger.exception("order submit failed order_id=%s", order.id)
            raise
