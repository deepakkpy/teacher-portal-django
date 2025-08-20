
import secrets, hashlib, time
from datetime import timedelta, datetime, timezone as dtz

PBKDF2_ITERATIONS = 260_000

def hash_password(plain: str, salt: str = None):
    if salt is None:
        salt = secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac('sha256', plain.encode(), bytes.fromhex(salt), PBKDF2_ITERATIONS)
    return salt, dk.hex()

def verify_password(plain: str, salt: str, stored_hash: str) -> bool:
    dk = hashlib.pbkdf2_hmac('sha256', plain.encode(), bytes.fromhex(salt), PBKDF2_ITERATIONS)
    return secrets.compare_digest(dk.hex(), stored_hash)

def new_session_token() -> str:
    return secrets.token_hex(32)

def user_agent_fingerprint(ua: str) -> str:
    return hashlib.sha256((ua or '').encode()).hexdigest()

def calculate_new_marks(existing: int, new: int) -> int:
    # naive sum; caller will reject if > 100
    return existing + new

def expiry(hours: int = 12):
    return datetime.now(dtz.utc) + timedelta(hours=hours)
