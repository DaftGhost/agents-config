from app.models import Order, Payment


def ship(order: Order) -> None:
    order.status = "shipped"


def refund(payment: Payment) -> None:
    payment.status = "refunded"
