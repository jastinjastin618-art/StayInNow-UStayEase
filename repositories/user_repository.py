from security import generate_password_hash, check_password_hash
from database.connection import get_connection, sql_placeholder

class UserRepository:
    def find_by_email(self, email: str):
        ph = sql_placeholder()
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM users WHERE LOWER(email) = LOWER({ph})", (email,))
            row = cur.fetchone()
            return dict(row) if row else None

    def create_user(self, payload: dict):
        name = (payload.get("name") or "").strip()
        email = (payload.get("email") or "").strip().lower()
        phone = (payload.get("phone") or "").strip()
        password = payload.get("password") or "user123"
        if not name or not email:
            raise ValueError("Nama dan email wajib diisi")
        if self.find_by_email(email):
            raise ValueError("Email sudah terdaftar, silakan login")
        ph = sql_placeholder()
        password_hash = generate_password_hash(password)
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                f"INSERT INTO users (name,email,phone,password_hash,role) VALUES ({ph},{ph},{ph},{ph},{ph})",
                (name, email, phone, password_hash, "user")
            )
        return self.public_user(self.find_by_email(email))

    def login(self, email: str, password: str = ""):
        user = self.find_by_email(email)
        if not user:
            raise ValueError("Akun belum terdaftar")
        if user.get("role") == "admin":
            if not password or not check_password_hash(user.get("password_hash") or "", password):
                raise ValueError("Password admin salah")
        return self.public_user(user)

    def public_user(self, user: dict):
        return {
            "id": user.get("id"),
            "name": user.get("name"),
            "email": user.get("email"),
            "phone": user.get("phone") or "",
            "role": user.get("role", "user"),
        }
