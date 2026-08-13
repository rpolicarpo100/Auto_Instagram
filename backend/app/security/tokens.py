import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from cryptography.fernet import Fernet, InvalidToken

from app.settings import settings


def new_session_token() -> str:
    return secrets.token_urlsafe(32)


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def session_expiry() -> datetime:
    return datetime.now(timezone.utc) + timedelta(hours=settings.session_ttl_hours)


def _fernet() -> Fernet | None:
    key = settings.token_encryption_key.strip()
    if not key:
        return None
    return Fernet(key.encode() if isinstance(key, str) else key)


def encrypt_secret(value: str) -> str:
    f = _fernet()
    if f is None:
        raise RuntimeError("TOKEN_ENCRYPTION_KEY_NOT_CONFIGURED")
    return f.encrypt(value.encode()).decode()


def decrypt_secret(value: str) -> str:
    f = _fernet()
    if f is None:
        raise RuntimeError("TOKEN_ENCRYPTION_KEY_NOT_CONFIGURED")
    try:
        return f.decrypt(value.encode()).decode()
    except InvalidToken as exc:
        raise RuntimeError("TOKEN_DECRYPT_FAILED") from exc
