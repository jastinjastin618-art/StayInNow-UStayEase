from enum import Enum

class PropertyStatus(str, Enum):
    AVAILABLE = "available"
    MAINTENANCE = "maintenance"

class BookingStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"
