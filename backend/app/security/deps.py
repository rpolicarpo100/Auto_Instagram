from datetime import datetime, timezone

from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db.session import SessionLocal, get_db
from app.models.session import UserSession
from app.models.user import User
from app.security.tokens import hash_token
from app.settings import settings


def require_database() -> None:
    if SessionLocal is None:
        raise HTTPException(status_code=503, detail="DATABASE_NOT_CONFIGURED")


def get_current_user(
    request: Request, db: Session = Depends(get_db)
) -> User:
    require_database()
    raw = request.cookies.get(settings.session_cookie_name)
    if not raw:
        raise HTTPException(status_code=401, detail="NOT_AUTHENTICATED")
    session = (
        db.query(UserSession)
        .filter(UserSession.token_hash == hash_token(raw))
        .first()
    )
    if session is None:
        raise HTTPException(status_code=401, detail="NOT_AUTHENTICATED")
    exp = session.expires_at
    if exp.tzinfo is None:
        exp = exp.replace(tzinfo=timezone.utc)
    if exp < datetime.now(timezone.utc):
        db.delete(session)
        db.commit()
        raise HTTPException(status_code=401, detail="SESSION_EXPIRED")
    user = db.get(User, session.user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="NOT_AUTHENTICATED")
    return user
