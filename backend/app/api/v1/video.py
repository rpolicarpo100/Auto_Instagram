from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.media_asset import MediaAsset
from app.models.user import User
from app.security.deps import get_current_user
from app.settings import settings
from app.video_engine import engine_status, probe, thumbnail

router = APIRouter(prefix="/video", tags=["video"])


@router.get("/status")
def video_status():
    return engine_status()


@router.get("/{asset_id}/probe")
def probe_route(
    asset_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    row = (
        db.query(MediaAsset)
        .filter(MediaAsset.id == asset_id, MediaAsset.user_id == user.id)
        .first()
    )
    if row is None:
        raise HTTPException(status_code=404, detail="NOT_FOUND")
    return probe(f"{settings.local_storage_dir}/{row.object_key}")


@router.post("/{asset_id}/thumbnail")
def thumbnail_route(
    asset_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    row = (
        db.query(MediaAsset)
        .filter(MediaAsset.id == asset_id, MediaAsset.user_id == user.id)
        .first()
    )
    if row is None:
        raise HTTPException(status_code=404, detail="NOT_FOUND")
    path = f"{settings.local_storage_dir}/{row.object_key}"
    dest = f"{settings.local_storage_dir}/{row.object_key}.jpg"
    return thumbnail(path, dest)
