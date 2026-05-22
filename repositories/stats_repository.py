from database.connection import get_connection

class StatsRepository:
    def dashboard(self):
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) AS count FROM bookings")
            total_bookings = dict(cur.fetchone())["count"]
            cur.execute("SELECT COALESCE(SUM(total_price), 0) AS revenue FROM bookings WHERE status != 'cancelled'")
            revenue = dict(cur.fetchone())["revenue"]
            cur.execute("SELECT COUNT(*) AS count FROM properties")
            total_properties = dict(cur.fetchone())["count"]
            cur.execute("SELECT COUNT(*) AS count FROM properties WHERE status = 'maintenance'")
            maintenance_units = dict(cur.fetchone())["count"]
        return {
            "total_bookings": int(total_bookings or 0),
            "revenue": int(revenue or 0),
            "total_properties": int(total_properties or 0),
            "maintenance_units": int(maintenance_units or 0),
        }
