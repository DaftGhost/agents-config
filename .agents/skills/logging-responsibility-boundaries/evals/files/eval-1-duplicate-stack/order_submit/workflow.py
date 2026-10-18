import logging

logger = logging.getLogger(__name__)


def submit_orders(orders, service):
    for order in orders:
        try:
            service.submit(order)
        except Exception:
            logger.exception("submit workflow failed order_id=%s", order.id)
            continue
