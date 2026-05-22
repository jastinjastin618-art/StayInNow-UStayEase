from dataclasses import dataclass, field
from typing import List
from .enums import PropertyStatus

@dataclass
class Property:
    id: int | None
    name: str
    location: str
    weekday_price: int
    weekend_price: int
    status: str = PropertyStatus.AVAILABLE.value
    rating: float = 4.8
    facilities: List[str] = field(default_factory=list)
    max_guests: int = 2

    @property
    def type(self) -> str:
        return self.__class__.__name__

    def is_available(self) -> bool:
        return self.status == PropertyStatus.AVAILABLE.value

    def set_maintenance(self) -> None:
        self.status = PropertyStatus.MAINTENANCE.value

    def set_available(self) -> None:
        self.status = PropertyStatus.AVAILABLE.value

    def calculate_night_price(self, is_weekend: bool) -> int:
        return self.weekend_price if is_weekend else self.weekday_price

@dataclass
class Villa(Property):
    cleaning_fee: int = 150000

    def calculate_night_price(self, is_weekend: bool) -> int:
        # Polymorphism: Villa punya tambahan fee kecil per malam.
        return super().calculate_night_price(is_weekend) + 50000

@dataclass
class Apartment(Property):
    service_charge: int = 50000

    def calculate_night_price(self, is_weekend: bool) -> int:
        return super().calculate_night_price(is_weekend) + self.service_charge

@dataclass
class HotelRoom(Property):
    tax_percent: float = 0.1

    def calculate_night_price(self, is_weekend: bool) -> int:
        base = super().calculate_night_price(is_weekend)
        return int(base + (base * self.tax_percent))
