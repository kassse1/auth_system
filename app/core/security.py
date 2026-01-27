import hashlib
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

# ===== JWT CONFIG (ЕДИНСТВЕННОЕ МЕСТО) =====
SECRET_KEY = "AUTH_SYSTEM_SECRET_KEY_123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
# ==========================================

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _pre_hash(password: str) -> bytes:
    return hashlib.sha256(password.encode("utf-8")).digest()


def hash_password(password: str) -> str:
    return pwd.hash(_pre_hash(password))


def verify_password(password: str, hashed: str) -> bool:
    return pwd.verify(_pre_hash(password), hashed)


def create_token(user_id: int) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
