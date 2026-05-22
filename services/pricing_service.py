from datetime import date, timedelta
from core.property import Villa, Apartment, HotelRoom, Property

class PricingService:
    def _make_property_object(self, row: dict) -> Property:
        cls = {"Villa": Villa, "Apartment": Apartment, "HotelRoom": HotelRoom}.get(row["type"], Property)
        facilities = row.get("facilities") or ""
        return cls(
            id=row["id"], name=row["name"], location=row["location"],
            weekday_price=int(row["weekday_price"]), weekend_price=int(row["weekend_price"]),
            status=row["status"], rating=float(row.get("rating") or 4.8),
            facilities=[x.strip() for x in facilities.split(",") if x.strip()],
            max_guests=int(row.get("max_guests") or 2),
        )

    def calculate_total(self, property_row: dict, check_in: date, check_out: date) -> dict:
        prop = self._make_property_object(property_row)
        total = 0
        weekday = 0
        weekend = 0
        current = check_in
        while current < check_out:
            is_weekend = current.weekday() >= 5
            if is_weekend: weekend += 1
            else: weekday += 1
            total += prop.calculate_night_price(is_weekend)
            current += timedelta(days=1)
        return {"total_price": total, "weekday_nights": weekday, "weekend_nights": weekend}
