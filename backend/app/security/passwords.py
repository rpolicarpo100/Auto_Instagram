from passlib.context import CryptContext

_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _prep(password: str) -> str:
    # bcrypt only uses 72 bytes
    return password.encode("utf-8")[:72].decode("utf-8", errors="ignore")


def hash_password(password: str) -> str:
    return _ctx.hash(_prep(password))


def verify_password(password: str, password_hash: str) -> bool:
    return _ctx.verify(_prep(password), password_hash)
