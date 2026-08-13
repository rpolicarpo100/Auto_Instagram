from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.media_asset import MediaAsset
from app.models.user import User
from app.security.deps import get_current_user
from app.services.media_storage import store_bytes
from app.settings import settings

router = APIRouter(prefix="/media", tags=["media"])


@router.get("")
def list_media(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = (
        db.query(MediaAsset)
        .filter(MediaAsset.user_id == user.id)
        .order_by(MediaAsset.created_at.desc())
        .all()
    )
    return {
        "status": "REAL" if rows else "NO DATA",
        "source": "media_assets",
        "items": [
            {
                "id": r.id,
                "storage_provider": r.storage_provider,
                "object_key": r.object_key,
                "mime_type": r.mime_type,
                "size": r.size,
                "checksum": r.checksum,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in rows
        ],
    }


@router.post("")
async def upload_media(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
):
    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="EMPTY_FILE")
    if len(data) > settings.max_upload_bytes:
        raise HTTPException(status_code=413, detail="FILE_TOO_LARGE")
    try:
        stored = store_bytes(data, declared_mime=file.content_type)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    row = MediaAsset(user_id=user.id, **stored)
    db.add(row)
    db.commit()
    db.refresh(row)
    return {
        "id": row.id,
        "status": "STORED",
        "mime_type": row.mime_type,
        "size": row.size,
        "checksum": row.checksum,
        "storage_provider": row.storage_provider,
    }


@router.delete("/{asset_id}")
def delete_media(
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
    db.delete(row)
    db.commit()
    return {"ok": True, "id": asset_id}
