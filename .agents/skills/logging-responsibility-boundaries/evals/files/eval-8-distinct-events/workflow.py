import logging

logger = logging.getLogger(__name__)


def run(order, gateway):
    try:
        result = charge_with_retry(gateway, order)
        logger.info(
            "charge accepted order_id=%s payment_id=%s",
            order.id,
            result["payment_id"],
        )
        return result["payment_id"]
    except RateLimited:
        logger.exception("charge failed order_id=%s", order.id)
        return None
