import secrets
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.instagram_account import InstagramAccount
from app.models.oauth_state import OAuthState
from app.models.user import User
from app.security.deps import get_current_user
from app.security.tokens import encrypt_secret
from app.services.account_data import latest_snapshot, refresh_account
from app.services.instagram_service import InstagramService
from app.settings import settings

router = APIRouter(prefix="/instagram", tags=["instagram"])


def _frontend(path: str, **query: str) -> str:
    base = settings.public_frontend_origin() or ""
    qs = urlencode({k: v for k, v in query.items() if v})
    url = f"{base}{path}" if base else path
    return f"{url}?{qs}" if qs else url


@router.get("/status")
def status(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    public = InstagramService().public_status()
    acc = (
        db.query(InstagramAccount)
        .filter(InstagramAccount.user_id == user.id)
        .order_by(InstagramAccount.created_at.desc())
        .first()
    )
    snap = latest_snapshot(db, user.id)
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
    public["latest_snapshot"] = (
        {
            "status": "REAL",
            "followers_count": snap.followers_count,
            "media_count": snap.media_count,
            "source": snap.source,
            "collected_at": snap.collected_at.isoformat(),
        }
        if snap
        else {"status": "NO DATA"}
    )
    return public


@router.post("/refresh")
def refresh(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    acc = (
        db.query(InstagramAccount)
        .filter(InstagramAccount.user_id == user.id)
        .order_by(InstagramAccount.created_at.desc())
        .first()
    )
    if acc is None or not acc.token_encrypted:
        raise HTTPException(status_code=409, detail="INSTAGRAM_NOT_CONNECTED")
    try:
        return refresh_account(db, acc)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"REFRESH_FAILED:{exc}") from exc


@router.get("/connect")
def connect(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    svc = InstagramService()
    if not settings.meta_configured():
        raise HTTPException(status_code=503, detail="META_NOT_CONFIGURED")
    state = secrets.token_urlsafe(24)
    db.add(
        OAuthState(
            state=state,
            user_id=user.id,
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=15),
        )
    )
    db.commit()
    return {"authorization_url": svc.provider.authorization_url(state)}


@router.get("/callback")
def callback(request: Request, db: Session = Depends(get_db)):
    if not settings.meta_configured():
        raise HTTPException(status_code=503, detail="META_NOT_CONFIGURED")
    error = request.query_params.get("error")
    if error:
        return RedirectResponse(_frontend("/instagram", error=error), status_code=302)
    code = request.query_params.get("code")
    state = request.query_params.get("state")
    row = (
        db.query(OAuthState).filter(OAuthState.state == state).first() if state else None
    )
    if not code or row is None:
        return RedirectResponse(
            _frontend("/instagram", error="OAUTH_INVALID_STATE"), status_code=302
        )
    exp = row.expires_at
    if exp.tzinfo is None:
        exp = exp.replace(tzinfo=timezone.utc)
    if exp < datetime.now(timezone.utc):
        db.delete(row)
        db.commit()
        return RedirectResponse(
            _frontend("/instagram", error="OAUTH_STATE_EXPIRED"), status_code=302
        )
    user_id = row.user_id
    db.delete(row)
    db.commit()

    svc = InstagramService()
    try:
        token_payload = svc.provider.exchange_code(code)
    except Exception:
        return RedirectResponse(
            _frontend("/instagram", error="OAUTH_EXCHANGE_FAILED"), status_code=302
        )
    access = token_payload.get("access_token")
    if not access:
        return RedirectResponse(
            _frontend("/instagram", error="OAUTH_NO_ACCESS_TOKEN"), status_code=302
        )
    try:
        profile = svc.provider.get_profile(access)
    except Exception:
        return RedirectResponse(
            _frontend("/instagram", error="PROFILE_FETCH_FAILED"), status_code=302
        )

    try:
        encrypted = encrypt_secret(access)
    except RuntimeError:
        return RedirectResponse(
            _frontend("/instagram", error="TOKEN_ENCRYPTION_KEY_NOT_CONFIGURED"),
            status_code=302,
        )

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
    acc.scopes = str(token_payload.get("permissions") or "")
    acc.connected_at = now
    acc.last_validated_at = now
    db.commit()
    try:
        refresh_account(db, acc)
    except Exception:
        pass
    return RedirectResponse(_frontend("/instagram", connected="1"), status_code=302)


@router.get("/media")
def list_ig_media(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    acc = (
        db.query(InstagramAccount)
        .filter(InstagramAccount.user_id == user.id)
        .order_by(InstagramAccount.created_at.desc())
        .first()
    )
    if acc is None or not acc.token_encrypted or not acc.ig_user_id:
        return {"status": "NOT_CONFIGURED", "items": []}
    if not settings.token_encryption_key:
        return {"status": "NOT_CONFIGURED", "items": [], "reason": "TOKEN_ENCRYPTION_KEY"}
    from app.security.tokens import decrypt_secret

    try:
        token = decrypt_secret(acc.token_encrypted)
        items = InstagramService().provider.get_media(token, acc.ig_user_id)
    except Exception as exc:
        return {"status": "NOT AVAILABLE", "items": [], "reason": str(exc)[:200]}
    return {
        "status": "REAL" if items else "NO DATA",
        "source": "Instagram Graph API media",
        "items": items,
    }
