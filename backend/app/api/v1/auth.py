from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.session import UserSession
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, UserOut
from app.security.deps import get_current_user, require_database
from app.security.passwords import hash_password, verify_password
from app.security.tokens import hash_token, new_session_token, session_expiry
from app.settings import settings

router = APIRouter(prefix="/auth", tags=["auth"])


def _set_cookie(response: Response, token: str) -> None:
    secure = settings.cookie_secure()
    response.set_cookie(
        key=settings.session_cookie_name,
        value=token,
        httponly=True,
        secure=secure,
        samesite="none" if secure else "lax",
        max_age=settings.session_ttl_hours * 3600,
        path="/",
    )


@router.post("/register", response_model=UserOut)
def register(
    payload: RegisterRequest, response: Response, db: Session = Depends(get_db)
):
    require_database()
    email = payload.email.lower()
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=409, detail="EMAIL_ALREADY_REGISTERED")
    user = User(email=email, password_hash=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    token = new_session_token()
    db.add(
        UserSession(
            user_id=user.id, token_hash=hash_token(token), expires_at=session_expiry()
        )
    )
    db.commit()
    _set_cookie(response, token)
    return UserOut(id=user.id, email=user.email)


@router.post("/login", response_model=UserOut)
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)):
    require_database()
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="INVALID_CREDENTIALS")
    token = new_session_token()
    db.add(
        UserSession(
            user_id=user.id, token_hash=hash_token(token), expires_at=session_expiry()
        )
    )
    db.commit()
    _set_cookie(response, token)
    return UserOut(id=user.id, email=user.email)


@router.post("/logout")
def logout(
    response: Response,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    db.query(UserSession).filter(UserSession.user_id == user.id).delete()
    db.commit()
    response.delete_cookie(settings.session_cookie_name, path="/")
    return {"ok": True}


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return UserOut(id=user.id, email=user.email)
