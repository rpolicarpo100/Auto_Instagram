from fastapi import APIRouter

from app.api.v1 import auth, dashboard, instagram, media, system

api_router = APIRouter()
api_router.include_router(system.router)
api_router.include_router(auth.router)
api_router.include_router(instagram.router)
api_router.include_router(dashboard.router)
api_router.include_router(media.router)
