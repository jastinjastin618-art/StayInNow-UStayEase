from database.connection import get_connection, rows_to_dicts, sql_placeholder

class PropertyRepository:
    def all(self):
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM properties ORDER BY id")
            return rows_to_dicts(cur.fetchall())

    def find(self, property_id):
        ph = sql_placeholder()
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM properties WHERE id = {ph}", (property_id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def update_status(self, property_id, status):
        ph = sql_placeholder()
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT status FROM properties WHERE id = {ph}", (property_id,))
            row = cur.fetchone()
            if not row:
                raise ValueError("Property tidak ditemukan")
            old_status = dict(row)["status"]
            cur.execute(f"UPDATE properties SET status = {ph} WHERE id = {ph}", (status, property_id))
            cur.execute(f"INSERT INTO maintenance_logs (property_id, old_status, new_status, note) VALUES ({ph},{ph},{ph},{ph})", (property_id, old_status, status, "Updated by admin dashboard"))
            return self.find(property_id)

    def create(self, payload):
        ph = sql_placeholder()
        fields = ["name", "type", "location", "weekday_price", "weekend_price", "status", "rating", "facilities", "max_guests", "image_url"]
        values = [
            payload.get("name"),
            payload.get("type", "Villa"),
            payload.get("location"),
            int(payload.get("weekday_price", 0)),
            int(payload.get("weekend_price", 0)),
            payload.get("status", "available"),
            float(payload.get("rating", 4.8)),
            payload.get("facilities", ""),
            int(payload.get("max_guests", 2)),
            payload.get("image_url", ""),
        ]
        if not values[0] or not values[2] or values[3] <= 0 or values[4] <= 0:
            raise ValueError("Nama, lokasi, harga weekday, dan harga weekend wajib valid")
        if values[5] not in ["available", "maintenance"]:
            raise ValueError("Status harus available atau maintenance")
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                f"INSERT INTO properties ({','.join(fields)}) VALUES ({','.join([ph]*len(fields))})",
                tuple(values)
            )
            try:
                new_id = cur.lastrowid
            except AttributeError:
                cur.execute("SELECT MAX(id) AS id FROM properties")
                new_id = dict(cur.fetchone())["id"]
            return self.find(new_id)

