from collections.abc import Generator

from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.settings import settings

engine = None
SessionLocal = None


def init_engine() -> None:
    global engine, SessionLocal
    if not settings.database_configured():
        engine = None
        SessionLocal = None
        return
    url = settings.database_url
    kwargs: dict = {"pool_pre_ping": True}
    if url.startswith("sqlite"):
        kwargs["connect_args"] = {"check_same_thread": False}
        if ":memory:" in url:
            kwargs["poolclass"] = StaticPool
            kwargs["pool_pre_ping"] = False
    engine = create_engine(url, **kwargs)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session, None, None]:
    if SessionLocal is None:
        raise HTTPException(status_code=503, detail="DATABASE_NOT_CONFIGURED")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


init_engine()
