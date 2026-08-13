import json
import os
import shutil
import subprocess
from pathlib import Path


def _local(name: str) -> Path:
    return Path(__file__).resolve().parents[1] / "bin" / name


def ffmpeg_bin() -> str | None:
    env = os.environ.get("FFMPEG_PATH")
    if env and Path(env).exists():
        return env
    found = shutil.which("ffmpeg")
    if found:
        return found
    p = _local("ffmpeg")
    return str(p) if p.exists() else None


def ffprobe_bin() -> str | None:
    env = os.environ.get("FFPROBE_PATH")
    if env and Path(env).exists():
        return env
    found = shutil.which("ffprobe")
    if found:
        return found
    p = _local("ffprobe")
    return str(p) if p.exists() else None


def available() -> bool:
    return ffmpeg_bin() is not None and ffprobe_bin() is not None


def engine_status() -> dict:
    return {
        "ffmpeg": "AVAILABLE" if available() else "NOT AVAILABLE",
        "source": "local ffmpeg/ffprobe binary",
    }


def probe(path: str) -> dict:
    binary = ffprobe_bin()
    if binary is None:
        return {"status": "NOT AVAILABLE", "reason": "ffmpeg_not_installed"}
    cmd = [
        binary,
        "-v",
        "error",
        "-show_format",
        "-show_streams",
        "-print_format",
        "json",
        path,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        return {"status": "FAILED", "reason": (proc.stderr or "")[:500] or "ffprobe_error"}
    data = json.loads(proc.stdout)
    fmt = data.get("format") or {}
    streams = data.get("streams") or []
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    return {
        "status": "REAL",
        "source": "ffprobe",
        "duration": float(fmt["duration"]) if fmt.get("duration") else None,
        "size": int(fmt["size"]) if fmt.get("size") else None,
        "format_name": fmt.get("format_name"),
        "video_codec": video.get("codec_name") if video else None,
        "width": video.get("width") if video else None,
        "height": video.get("height") if video else None,
        "fps": video.get("r_frame_rate") if video else None,
        "audio_codec": audio.get("codec_name") if audio else None,
    }


def thumbnail(src: str, dest: str, at_seconds: float = 1.0) -> dict:
    binary = ffmpeg_bin()
    if binary is None:
        return {"status": "NOT AVAILABLE", "reason": "ffmpeg_not_installed"}
    proc = subprocess.run(
        [binary, "-y", "-ss", str(at_seconds), "-i", src, "-frames:v", "1", dest],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0 or not Path(dest).exists():
        return {"status": "FAILED", "reason": (proc.stderr or "")[-400:]}
    return {"status": "REAL", "path": dest, "source": "ffmpeg"}
