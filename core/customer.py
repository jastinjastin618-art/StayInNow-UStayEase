from dataclasses import dataclass

@dataclass
class Customer:
    id: int | None
    name: str
    email: str
    phone: str
