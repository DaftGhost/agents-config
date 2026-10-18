import logging
import time

logger = logging.getLogger(__name__)


def charge_with_retry(gateway, order, attempts=4):
    for attempt in range(1, attempts + 1):
        try:
            return gateway.charge(order)
        except RateLimited as exc:
            logger.warning(
                "rate limited order_id=%s attempt=%s retry_after=%s",
                order.id,
                attempt,
                exc.retry_after,
            )
            if attempt == attempts:
                logger.exception(
                    "charge retries exhausted order_id=%s attempts=%s",
                    order.id,
                    attempts,
                )
                raise
            time.sleep(exc.retry_after)
