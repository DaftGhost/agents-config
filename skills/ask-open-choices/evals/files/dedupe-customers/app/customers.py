from dataclasses import dataclass
from datetime import datetime


@dataclass
class Customer:
    id: int
    email: str
    name: str
    phone: str | None
    created_at: datetime
    updated_at: datetime


def load_customers(rows):
    return [Customer(**row) for row in rows]
