from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.content import Content
from app.models.instagram_account import InstagramAccount
from app.models.user import User
from app.security.deps import get_current_user
from app.services.account_data import latest_snapshot
from app.db.session import get_db

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def _metric(status: str, value=None, source=None):
    return {
        "status": status,
        "value": value,
        "source": source,
        "collected_at": datetime.now(timezone.utc).isoformat()
        if value is not None
        else None,
    }


@router.get("")
def dashboard(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    acc = (
        db.query(InstagramAccount)
        .filter(InstagramAccount.user_id == user.id)
        .order_by(InstagramAccount.created_at.desc())
        .first()
    )
    snap = latest_snapshot(db, user.id)
    local_content = db.query(Content).filter(Content.user_id == user.id).count()

    connected = acc is not None and bool(acc.ig_user_id)
    return {
        "account_status": _metric(
            "CONNECTED" if connected else "NOT_CONFIGURED",
            acc.username if connected else None,
            "instagram_accounts" if connected else None,
        ),
        "followers": _metric(
            "REAL" if snap and snap.followers_count is not None else "NO DATA",
            snap.followers_count if snap else None,
            snap.source if snap else "Instagram Graph API",
        ),
        "content": _metric(
            "REAL"
            if snap and snap.media_count is not None
            else ("CALCULATED" if local_content else "NO DATA"),
            snap.media_count if snap and snap.media_count is not None else (
                local_content if local_content else None
            ),
            snap.source
            if snap and snap.media_count is not None
            else ("local content table" if local_content else "Instagram Graph API"),
        ),
        "reach": _metric("NO DATA", None, "Instagram Insights"),
        "engagement": _metric("NO DATA", None, "Instagram Insights"),
        "recent_activity": {"status": "NO DATA", "items": []},
        "snapshot": {
            "status": "REAL" if snap else "NO DATA",
            "collected_at": snap.collected_at.isoformat() if snap else None,
            "source": snap.source if snap else None,
        },
    }
