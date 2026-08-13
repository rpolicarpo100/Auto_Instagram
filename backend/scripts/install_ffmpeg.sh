#!/bin/sh
set -eu
DEST="${1:-/opt/render/project/src/backend/bin}"
mkdir -p "$DEST"
if command -v ffmpeg >/dev/null 2>&1; then
  echo "ffmpeg already on PATH"
  exit 0
fi
if [ -x "$DEST/ffmpeg" ]; then
  echo "ffmpeg already in $DEST"
  exit 0
fi
URL="https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz"
TMP="$(mktemp -d)"
echo "Downloading static ffmpeg…"
if ! wget -q -O "$TMP/ffmpeg.tar.xz" "$URL"; then
  echo "ffmpeg download failed — video engine will report NOT AVAILABLE"
  exit 0
fi
tar -xJf "$TMP/ffmpeg.tar.xz" -C "$TMP"
FF="$(find "$TMP" -type f -name ffmpeg | head -n1)"
FP="$(find "$TMP" -type f -name ffprobe | head -n1)"
if [ -n "$FF" ]; then
  cp "$FF" "$DEST/ffmpeg"
  chmod +x "$DEST/ffmpeg"
fi
if [ -n "$FP" ]; then
  cp "$FP" "$DEST/ffprobe"
  chmod +x "$DEST/ffprobe"
fi
echo "installed to $DEST"
