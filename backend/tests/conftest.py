import os

os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")
os.environ.setdefault("SESSION_SECRET", "test-secret")

from cryptography.fernet import Fernet

os.environ.setdefault("TOKEN_ENCRYPTION_KEY", Fernet.generate_key().decode())

from app.db import session as session_mod
from app.settings import settings

settings.database_url = os.environ["DATABASE_URL"]
settings.app_env = "test"
session_mod.init_engine()

from app.db.base import Base
from app.models import Content, InstagramAccount, Job, MediaAsset, User, UserSession  # noqa: F401

assert session_mod.engine is not None
Base.metadata.create_all(bind=session_mod.engine)
