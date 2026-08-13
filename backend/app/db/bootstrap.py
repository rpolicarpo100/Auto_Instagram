from app.db.base import Base
from app.db.session import engine
from app.models import (  # noqa: F401
    AccountSnapshot,
    Content,
    InstagramAccount,
    Job,
    MediaAsset,
    OAuthState,
    User,
    UserSession,
)


def create_schema() -> None:
    if engine is None:
        return
    Base.metadata.create_all(bind=engine)
