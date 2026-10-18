import logging
import sqlite3

logger = logging.getLogger(__name__)


class OrderRepository:
    def __init__(self, conn):
        self._conn = conn

    def save(self, order) -> bool:
        try:
            self._conn.execute(
                "INSERT INTO orders (id, customer_id, total) VALUES (?, ?, ?)",
                (order.id, order.customer_id, order.total),
            )
            self._conn.commit()
            return True
        except sqlite3.IntegrityError:
            logger.warning("order conflict order_id=%s", order.id)
            return False
        except sqlite3.OperationalError:
            logger.error("database unavailable order_id=%s", order.id)
            return False
