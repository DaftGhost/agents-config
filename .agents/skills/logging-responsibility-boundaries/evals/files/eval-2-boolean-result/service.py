import logging
import time

logger = logging.getLogger(__name__)


class OrderService:
    def __init__(self, repo):
        self._repo = repo

    def save_with_retry(self, order, attempts=5):
        for attempt in range(1, attempts + 1):
            if self._repo.save(order):
                return True
            logger.warning(
                "save failed, retrying order_id=%s attempt=%s", order.id, attempt
            )
            time.sleep(2**attempt)
        logger.error("save failed permanently order_id=%s", order.id)
        return False
