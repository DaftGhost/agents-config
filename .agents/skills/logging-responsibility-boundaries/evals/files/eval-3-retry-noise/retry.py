import logging
import time

logger = logging.getLogger(__name__)


def submit_with_retry(gateway, order, attempts=5):
    for attempt in range(1, attempts + 1):
        try:
            return gateway.submit(order)
        except TimeoutError:
            logger.error(
                "submit attempt failed order_id=%s attempt=%s",
                order.id,
                attempt,
                exc_info=True,
            )
            if attempt == attempts:
                raise
            time.sleep(2**attempt)
