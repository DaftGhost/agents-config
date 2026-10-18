import logging

logger = logging.getLogger(__name__)


def submit_order(order, gateway):
    logger.info("submitting order order_id=%s", order.id)
    try:
        response = gateway.submit(order)
    except TimeoutError:
        logger.warning("submit timeout order_id=%s", order.id)
        return None

    logger.info(
        "order submitted successfully order_id=%s payment_id=%s",
        order.id,
        response["payment_id"],
    )
    return response["payment_id"]
