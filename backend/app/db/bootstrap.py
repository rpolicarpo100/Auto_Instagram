from app.db.base import Base
from app.db.session import engine
from app.models import Content, InstagramAccount, Job, MediaAsset, User, UserSession  # noqa: F401


def create_schema() -> None:
    if engine is None:
        return
    Base.metadata.create_all(bind=engine)
