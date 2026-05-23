from database.db import get_connection, rows_to_dicts, sql_placeholder

class BookingRepository:
    def all(self):
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT b.*, p.name AS property_name, c.name AS customer_name, c.email AS customer_email
                FROM bookings b
                JOIN properties p ON p.id = b.property_id
                JOIN customers c ON c.id = b.customer_id
                ORDER BY b.id DESC
            """)
            return rows_to_dicts(cur.fetchall())

    def has_overlap(self, property_id, check_in, check_out):
        ph = sql_placeholder()
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(f"""
                SELECT COUNT(*) AS count FROM bookings
                WHERE property_id = {ph}
                AND status != 'cancelled'
                AND check_in < {ph}
                AND check_out > {ph}
            """, (property_id, check_out, check_in))
            return dict(cur.fetchone())["count"] > 0


    def find_detail(self, booking_id):
        ph = sql_placeholder()
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(f"""
                SELECT b.*, p.name AS property_name, p.location AS property_location,
                       c.name AS customer_name, c.email AS customer_email, c.phone AS customer_phone,
                       pay.method AS payment_method, pay.status AS payment_status
                FROM bookings b
                JOIN properties p ON p.id = b.property_id
                JOIN customers c ON c.id = b.customer_id
                LEFT JOIN payments pay ON pay.booking_id = b.id
                WHERE b.id = {ph}
            """, (booking_id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def create_atomic(self, customer, booking, payment):
        ph = sql_placeholder()
        with get_connection() as conn:
            cur = conn.cursor()
            if ph == "%s":
                cur.execute("INSERT INTO customers (name,email,phone) VALUES (%s,%s,%s) RETURNING id", (customer["name"], customer["email"], customer["phone"]))
                customer_id = cur.fetchone()["id"]
                cur.execute("""
                    INSERT INTO bookings (customer_id,property_id,check_in,check_out,guests,total_price,status)
                    VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id
                """, (customer_id, booking["property_id"], booking["check_in"], booking["check_out"], booking["guests"], booking["total_price"], booking["status"]))
                booking_id = cur.fetchone()["id"]
                cur.execute("INSERT INTO payments (booking_id,amount,method,status) VALUES (%s,%s,%s,%s) RETURNING id", (booking_id, payment["amount"], payment["method"], payment["status"]))
            else:
                cur.execute("INSERT INTO customers (name,email,phone) VALUES (?,?,?)", (customer["name"], customer["email"], customer["phone"]))
                customer_id = cur.lastrowid
                cur.execute("""
                    INSERT INTO bookings (customer_id,property_id,check_in,check_out,guests,total_price,status)
                    VALUES (?,?,?,?,?,?,?)
                """, (customer_id, booking["property_id"], booking["check_in"], booking["check_out"], booking["guests"], booking["total_price"], booking["status"]))
                booking_id = cur.lastrowid
                cur.execute("INSERT INTO payments (booking_id,amount,method,status) VALUES (?,?,?,?)", (booking_id, payment["amount"], payment["method"], payment["status"]))
            return {"booking_id": booking_id, "customer_id": customer_id}
