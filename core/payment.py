from dataclasses import dataclass

@dataclass
class Payment:
    id: int | None
    booking_id: int
    amount: int
    method: str
    status: str = "paid"
