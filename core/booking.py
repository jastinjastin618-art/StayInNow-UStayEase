from dataclasses import dataclass
from datetime import date
from .enums import BookingStatus

@dataclass
class Booking:
    id: int | None
    customer_id: int
    property_id: int
    check_in: date
    check_out: date
    guests: int
    total_price: int
    status: str = BookingStatus.PENDING.value
