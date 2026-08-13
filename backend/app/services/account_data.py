import json
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.account_snapshot import AccountSnapshot
from app.models.instagram_account import InstagramAccount
from app.security.tokens import decrypt_secret
from app.services.instagram_service import InstagramService
from app.settings import settings


def latest_snapshot(db: Session, user_id: str) -> AccountSnapshot | None:
    return (
        db.query(AccountSnapshot)
        .filter(AccountSnapshot.user_id == user_id)
        .order_by(AccountSnapshot.collected_at.desc())
        .first()
    )


def refresh_account(db: Session, acc: InstagramAccount) -> dict:
    if not acc.token_encrypted:
        return {"status": "NOT_CONFIGURED", "reason": "no_token"}
    if not settings.token_encryption_key:
        return {"status": "NOT_CONFIGURED", "reason": "TOKEN_ENCRYPTION_KEY"}
    token = decrypt_secret(acc.token_encrypted)
    profile = InstagramService().provider.get_profile(token)
    snap = AccountSnapshot(
        user_id=acc.user_id,
        instagram_account_id=acc.id,
        source="Instagram Graph API /me",
        followers_count=profile.get("followers_count"),
        follows_count=profile.get("follows_count"),
        media_count=profile.get("media_count"),
        raw_json=json.dumps(profile, default=str),
        collected_at=datetime.now(timezone.utc),
    )
    db.add(snap)
    acc.username = profile.get("username") or acc.username
    acc.account_type = profile.get("account_type") or acc.account_type
    acc.ig_user_id = str(profile.get("user_id") or profile.get("id") or acc.ig_user_id)
    acc.last_validated_at = snap.collected_at
    db.commit()
    db.refresh(snap)
    return {
        "status": "REAL",
        "snapshot_id": snap.id,
        "followers_count": snap.followers_count,
        "follows_count": snap.follows_count,
        "media_count": snap.media_count,
        "collected_at": snap.collected_at.isoformat(),
        "source": snap.source,
    }
