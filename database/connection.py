import os
import sqlite3
from contextlib import contextmanager
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    psycopg2 = None
    RealDictCursor = None
from security import generate_password_hash
from config import Config

IS_POSTGRES = Config.DATABASE_URL.startswith("postgres")

@contextmanager
def get_connection():
    if IS_POSTGRES:
        if psycopg2 is None:
            raise RuntimeError("psycopg2-binary belum terinstall. Jalankan: pip install -r requirements.txt")
        conn = psycopg2.connect(Config.DATABASE_URL, cursor_factory=RealDictCursor)
    else:
        db_path = Config.DATABASE_URL.replace("sqlite:///", "")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def rows_to_dicts(rows):
    return [dict(row) for row in rows]

def sql_placeholder() -> str:
    return "%s" if IS_POSTGRES else "?"

def init_db():
    with get_connection() as conn:
        cur = conn.cursor()
        if IS_POSTGRES:
            with open(os.path.join(os.path.dirname(__file__), "schema.sql"), encoding="utf-8") as f:
                cur.execute(f.read())
            try:
                cur.execute("ALTER TABLE properties ADD COLUMN image_url TEXT")
            except Exception:
                pass
        else:
            sqlite_schema = """
            CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, phone TEXT, password_hash TEXT, role TEXT NOT NULL DEFAULT 'user', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
            CREATE TABLE IF NOT EXISTS app_settings (key TEXT PRIMARY KEY, value TEXT NOT NULL, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
            CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT NOT NULL, phone TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
            CREATE TABLE IF NOT EXISTS properties (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, type TEXT NOT NULL, location TEXT NOT NULL, weekday_price INTEGER NOT NULL, weekend_price INTEGER NOT NULL, status TEXT NOT NULL DEFAULT 'available', rating REAL DEFAULT 4.8, facilities TEXT, max_guests INTEGER DEFAULT 2, image_url TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
            CREATE TABLE IF NOT EXISTS bookings (id INTEGER PRIMARY KEY AUTOINCREMENT, customer_id INTEGER NOT NULL REFERENCES customers(id), property_id INTEGER NOT NULL REFERENCES properties(id), check_in DATE NOT NULL, check_out DATE NOT NULL, guests INTEGER NOT NULL, total_price INTEGER NOT NULL, status TEXT NOT NULL DEFAULT 'pending', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
            CREATE TABLE IF NOT EXISTS payments (id INTEGER PRIMARY KEY AUTOINCREMENT, booking_id INTEGER NOT NULL REFERENCES bookings(id), amount INTEGER NOT NULL, method TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'paid', created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
            CREATE TABLE IF NOT EXISTS maintenance_logs (id INTEGER PRIMARY KEY AUTOINCREMENT, property_id INTEGER NOT NULL REFERENCES properties(id), old_status TEXT, new_status TEXT NOT NULL, note TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
            """
            cur.executescript(sqlite_schema)
            try:
                cur.execute("ALTER TABLE properties ADD COLUMN image_url TEXT")
            except Exception:
                pass
        seed_db(conn)

def seed_db(conn):
    cur = conn.cursor()
    ph = "%s" if IS_POSTGRES else "?"
    admin_hash = generate_password_hash("admin123")
    if IS_POSTGRES:
        cur.execute("INSERT INTO app_settings (key,value) VALUES (%s,%s) ON CONFLICT (key) DO NOTHING", ("system_maintenance", "off"))
        cur.execute("INSERT INTO users (name,email,phone,password_hash,role) VALUES (%s,%s,%s,%s,%s) ON CONFLICT (email) DO NOTHING", ("Admin S", "admin@gmail.com.com", "", admin_hash, "admin"))
    else:
        cur.execute("INSERT OR IGNORE INTO app_settings (key,value) VALUES (?,?)", ("system_maintenance", "off"))
        cur.execute("INSERT OR IGNORE INTO users (name,email,phone,password_hash,role) VALUES (?,?,?,?,?)", ("Admin STAYINOW", "admin@gmail.com", "", admin_hash, "admin"))
    cur.execute("SELECT COUNT(*) AS count FROM properties")
    count = cur.fetchone()["count"]
    if count:
        return
    data = [
        ("Modern Villa Bali Paradise", "Villa", "Seminyak, Bali", 1200000, 1800000, "available", 4.8, "Private Pool,WiFi,AC,Kitchen,Parking", 6, ""),
        ("Downtown Luxury Apartment", "Apartment", "Jakarta Selatan", 800000, 1200000, "available", 4.9, "WiFi,Gym,Pool,Security,AC", 4, ""),
        ("Cozy Mountain Cabin", "Villa", "Puncak, Jawa Barat", 650000, 950000, "maintenance", 4.7, "Mountain View,Fireplace,WiFi,Kitchen", 5, ""),
        ("Sunrise Hotel Room", "HotelRoom", "Batam Center", 550000, 850000, "available", 4.6, "Breakfast,WiFi,AC,Reception", 2, ""),
    ]
    cur.executemany(
        f"INSERT INTO properties (name,type,location,weekday_price,weekend_price,status,rating,facilities,max_guests,image_url) VALUES ({','.join([ph]*10)})",
        data
    )
