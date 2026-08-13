import secrets
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.instagram_account import InstagramAccount
from app.models.user import User
from app.security.deps import get_current_user
from app.security.tokens import encrypt_secret
from app.services.instagram_service import InstagramService
from app.settings import settings

router = APIRouter(prefix="/instagram", tags=["instagram"])

_oauth_states: dict[str, str] = {}


@router.get("/status")
def status(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    public = InstagramService().public_status()
    acc = (
        db.query(InstagramAccount)
        .filter(InstagramAccount.user_id == user.id)
        .order_by(InstagramAccount.created_at.desc())
        .first()
    )
    if acc is None or not acc.ig_user_id:
        public["account"] = {
            "status": "NOT_CONFIGURED",
            "username": None,
            "ig_user_id": None,
        }
    else:
        public["account"] = {
            "status": "CONNECTED",
            "username": acc.username,
            "ig_user_id": acc.ig_user_id,
            "account_type": acc.account_type,
            "connected_at": acc.connected_at.isoformat() if acc.connected_at else None,
        }
        public["connection"] = "CONNECTED"
    return public


@router.get("/connect")
def connect(user: User = Depends(get_current_user)):
    svc = InstagramService()
    if not settings.meta_configured():
        raise HTTPException(status_code=503, detail="META_NOT_CONFIGURED")
    state = secrets.token_urlsafe(24)
    _oauth_states[state] = user.id
    return {"authorization_url": svc.provider.authorization_url(state)}


@router.get("/callback")
def callback(request: Request, db: Session = Depends(get_db)):
    if not settings.meta_configured():
        raise HTTPException(status_code=503, detail="META_NOT_CONFIGURED")
    error = request.query_params.get("error")
    if error:
        raise HTTPException(status_code=400, detail=f"OAUTH_DENIED:{error}")
    code = request.query_params.get("code")
    state = request.query_params.get("state")
    if not code or not state or state not in _oauth_states:
        raise HTTPException(status_code=400, detail="OAUTH_INVALID_STATE")
    user_id = _oauth_states.pop(state)
    svc = InstagramService()
    try:
        token_payload = svc.provider.exchange_code(code)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"OAUTH_EXCHANGE_FAILED:{exc}") from exc
    access = token_payload.get("access_token")
    if not access:
        raise HTTPException(status_code=502, detail="OAUTH_NO_ACCESS_TOKEN")
    try:
        profile = svc.provider.get_profile(access)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"PROFILE_FETCH_FAILED:{exc}") from exc

    try:
        encrypted = encrypt_secret(access)
    except RuntimeError:
        raise HTTPException(status_code=503, detail="TOKEN_ENCRYPTION_KEY_NOT_CONFIGURED")

    acc = (
        db.query(InstagramAccount)
        .filter(InstagramAccount.user_id == user_id)
        .first()
    )
    now = datetime.now(timezone.utc)
    if acc is None:
        acc = InstagramAccount(user_id=user_id)
        db.add(acc)
    acc.ig_user_id = str(profile.get("user_id") or profile.get("id") or "")
    acc.username = profile.get("username")
    acc.account_type = profile.get("account_type")
    acc.token_encrypted = encrypted
    acc.scopes = token_payload.get("permissions")
    acc.connected_at = now
    acc.last_validated_at = now
    db.commit()
    return RedirectResponse(url="/instagram?connected=1", status_code=302)
