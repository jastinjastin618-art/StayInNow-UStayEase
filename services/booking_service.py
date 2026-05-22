from datetime import datetime
from repositories.property_repository import PropertyRepository
from repositories.booking_repository import BookingRepository
from services.pricing_service import PricingService
from repositories.system_repository import SystemRepository

class BookingService:
    def __init__(self):
        self.properties = PropertyRepository()
        self.bookings = BookingRepository()
        self.pricing = PricingService()
        self.system = SystemRepository()

    def create_booking(self, payload: dict) -> dict:
        required = ["property_id", "customer_name", "customer_email", "customer_phone", "check_in", "check_out", "guests"]
        for key in required:
            if not payload.get(key):
                raise ValueError(f"Field {key} wajib diisi")

        if self.system.get_maintenance().get("maintenance"):
            raise ValueError("Sistem sedang maintenance. Booking sementara ditutup.")

        prop = self.properties.find(payload["property_id"])
        if not prop:
            raise ValueError("Property tidak ditemukan")
        if prop["status"] == "maintenance":
            raise ValueError("Property sedang maintenance dan tidak bisa dibooking")

        check_in = datetime.strptime(payload["check_in"], "%Y-%m-%d").date()
        check_out = datetime.strptime(payload["check_out"], "%Y-%m-%d").date()
        if check_out <= check_in:
            raise ValueError("Tanggal check-out harus setelah check-in")
        if int(payload["guests"]) > int(prop.get("max_guests") or 2):
            raise ValueError("Jumlah tamu melebihi kapasitas property")
        if self.bookings.has_overlap(prop["id"], payload["check_in"], payload["check_out"]):
            raise ValueError("Property sudah dibooking pada rentang tanggal tersebut")

        price = self.pricing.calculate_total(prop, check_in, check_out)
        customer = {"name": payload["customer_name"], "email": payload["customer_email"], "phone": payload["customer_phone"]}
        booking = {"property_id": prop["id"], "check_in": payload["check_in"], "check_out": payload["check_out"], "guests": int(payload["guests"]), "total_price": price["total_price"], "status": "paid"}
        payment = {"amount": price["total_price"], "method": payload.get("payment_method", "Cash"), "status": "paid"}
        result = self.bookings.create_atomic(customer, booking, payment)
        return {**result, **booking, **price, "property_name": prop["name"], "customer_name": customer["name"]}
