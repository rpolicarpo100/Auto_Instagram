import hashlib
import uuid
from pathlib import Path

from app.settings import settings

ALLOWED = {
    b"\xff\xd8\xff": "image/jpeg",
    b"\x89PNG\r\n\x1a\n": "image/png",
    b"GIF87a": "image/gif",
    b"GIF89a": "image/gif",
    b"RIFF": "video/mp4",  # may be webp/avi; refined below
}


def detect_mime(data: bytes) -> str | None:
    if data.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if data.startswith(b"GIF87a") or data.startswith(b"GIF89a"):
        return "image/gif"
    if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        return "image/webp"
    if data.startswith(b"RIFF") and data[8:12] == b"AVI ":
        return None
    if len(data) > 12 and data[4:8] == b"ftyp":
        return "video/mp4"
    if data.startswith(b"\x1a\x45\xdf\xa3"):
        return "video/webm"
    return None


def store_bytes(data: bytes, *, declared_mime: str | None) -> dict:
    if len(data) > settings.max_upload_bytes:
        raise ValueError("FILE_TOO_LARGE")
    mime = detect_mime(data)
    if mime is None:
        raise ValueError("UNSUPPORTED_OR_INVALID_FILE")
    if declared_mime and declared_mime.split(";")[0].strip() not in {
        mime,
        "application/octet-stream",
        "video/quicktime",
    }:
        if not (
            mime == "video/mp4" and declared_mime in {"video/mp4", "video/quicktime"}
        ):
            raise ValueError("MIME_MISMATCH")
    root = Path(settings.local_storage_dir)
    root.mkdir(parents=True, exist_ok=True)
    key = f"{uuid.uuid4().hex}"
    path = root / key
    path.write_bytes(data)
    return {
        "storage_provider": "local",
        "object_key": key,
        "mime_type": mime,
        "size": len(data),
        "checksum": hashlib.sha256(data).hexdigest(),
    }
