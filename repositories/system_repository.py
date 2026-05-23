from database.db import get_connection, sql_placeholder

class SystemRepository:
    KEY = "system_maintenance"

    def get_maintenance(self):
        ph = sql_placeholder()
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT value FROM app_settings WHERE key = {ph}", (self.KEY,))
            row = cur.fetchone()
            value = dict(row)["value"] if row else "off"
            return {"maintenance": value == "on"}

    def set_maintenance(self, enabled: bool):
        ph = sql_placeholder()
        value = "on" if enabled else "off"
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(f"UPDATE app_settings SET value = {ph}, updated_at = CURRENT_TIMESTAMP WHERE key = {ph}", (value, self.KEY))
            if cur.rowcount == 0:
                cur.execute(f"INSERT INTO app_settings (key, value) VALUES ({ph},{ph})", (self.KEY, value))
        return {"maintenance": enabled}
