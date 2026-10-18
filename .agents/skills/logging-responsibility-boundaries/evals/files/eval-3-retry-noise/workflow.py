import logging

logger = logging.getLogger(__name__)


def run(order, gateway):
    try:
        result = submit_with_retry(gateway, order)
        logger.info("submit done order_id=%s", order.id)
        return result
    except TimeoutError:
        logger.exception("submit failed order_id=%s", order.id)
        return None
