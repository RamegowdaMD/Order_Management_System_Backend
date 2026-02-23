from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class PaymentData:
    order_id: int
    amount: Decimal
    payment_method: str
    transaction_id: Optional[str] = None
    payment_status: str = "PENDING"
