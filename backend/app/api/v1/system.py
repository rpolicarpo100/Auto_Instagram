from fastapi import APIRouter, Request

from app import __version__
from app.db.session import SessionLocal
from app.services.instagram_service import InstagramService
from app.settings import settings

router = APIRouter()


@router.get("/health")
def v1_health():
    return {"status": "ok", "service": settings.app_name}


@router.get("/version")
def version():
    return {"service": settings.app_name, "version": __version__, "phase": "10"}


@router.get("/config")
def config(request: Request):
    ig = InstagramService().public_status()
    return {
        "app_env": settings.app_env,
        "request_id": getattr(request.state, "request_id", ""),
        "database": "CONFIGURED" if SessionLocal is not None else "NOT_CONFIGURED",
        "meta_oauth": "CONFIGURED" if settings.meta_configured() else "NOT_CONFIGURED",
        "frontend_origin": settings.public_frontend_origin() or "NOT_CONFIGURED",
        "instagram": ig,
        "note": "No secrets are included in this payload.",
    }
