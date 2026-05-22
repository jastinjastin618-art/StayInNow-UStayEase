import hashlib
import secrets


def generate_password_hash(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.sha256((salt + (password or "")).encode("utf-8")).hexdigest()
    return f"sha256${salt}${digest}"


def check_password_hash(stored: str, password: str) -> bool:
    try:
        method, salt, digest = stored.split("$", 2)
        if method != "sha256":
            return False
        candidate = hashlib.sha256((salt + (password or "")).encode("utf-8")).hexdigest()
        return secrets.compare_digest(candidate, digest)
    except Exception:
        return False
