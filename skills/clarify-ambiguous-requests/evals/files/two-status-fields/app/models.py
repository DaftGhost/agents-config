from dataclasses import dataclass


@dataclass
class Order:
    id: int
    customer_id: int
    status: str = "pending"  # pending, shipped, delivered, cancelled


@dataclass
class Payment:
    id: int
    order_id: int
    amount: float
    status: str = "authorized"  # authorized, captured, refunded
