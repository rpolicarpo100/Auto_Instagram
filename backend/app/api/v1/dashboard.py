from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal, get_db
from app.models.content import Content
from app.models.instagram_account import InstagramAccount
from app.models.user import User
from app.security.deps import get_current_user
from app.security.tokens import decrypt_secret
from app.services.instagram_service import InstagramService
from app.settings import settings

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def _metric(status: str, value=None, source=None, extra=None):
    payload = {
        "status": status,
        "value": value,
        "source": source,
        "collected_at": datetime.now(timezone.utc).isoformat() if value is not None else None,
    }
    if extra:
        payload.update(extra)
    return payload


@router.get("")
def dashboard(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if SessionLocal is None:
        return {"status": "DATABASE_NOT_CONFIGURED"}

    acc = (
        db.query(InstagramAccount)
        .filter(InstagramAccount.user_id == user.id)
        .order_by(InstagramAccount.created_at.desc())
        .first()
    )
    content_count = (
        db.query(Content).filter(Content.user_id == user.id).count()
        if acc
        else 0
    )

    base = {
        "account_status": _metric(
            "NOT_CONFIGURED" if acc is None or not acc.ig_user_id else "CONNECTED",
            acc.username if acc else None,
            "instagram_accounts" if acc else None,
        ),
        "followers": _metric("NO DATA", None, "Instagram Graph API"),
        "content": _metric(
            "CALCULATED" if acc else "NO DATA",
            content_count if acc else None,
            "local content table" if acc else None,
        ),
        "reach": _metric("NO DATA", None, "Instagram Insights"),
        "engagement": _metric("NO DATA", None, "Instagram Insights"),
        "recent_activity": {"status": "NO DATA", "items": []},
    }

    if acc is None or not acc.token_encrypted:
        return base

    if not settings.token_encryption_key:
        base["followers"] = _metric(
            "NOT_CONFIGURED", None, "TOKEN_ENCRYPTION_KEY"
        )
        return base

    try:
        token = decrypt_secret(acc.token_encrypted)
    except Exception:
        base["followers"] = _metric("NOT AVAILABLE", None, "token decrypt")
        return base

    svc = InstagramService()
    try:
        profile = svc.provider.get_profile(token)
    except Exception:
        base["followers"] = _metric("NOT AVAILABLE", None, "Instagram Graph API")
        return base

    followers = profile.get("followers_count")
    media = profile.get("media_count")
    if followers is None:
        base["followers"] = _metric("NOT AVAILABLE", None, "Instagram Graph API /me")
    else:
        base["followers"] = _metric("REAL", followers, "Instagram Graph API /me")
    if media is None:
        base["content"] = _metric("NOT AVAILABLE", None, "Instagram Graph API /me")
    else:
        base["content"] = _metric("REAL", media, "Instagram Graph API /me")

    if acc.ig_user_id:
        insights = svc.provider.get_insights(token, acc.ig_user_id)
        if insights.get("status") == "NOT_AVAILABLE":
            base["reach"] = _metric("NOT AVAILABLE", None, "Instagram Insights")
        else:
            base["reach"] = {
                "status": "REAL",
                "value": insights,
                "source": "Instagram Graph API insights",
                "collected_at": datetime.now(timezone.utc).isoformat(),
            }

    return base
