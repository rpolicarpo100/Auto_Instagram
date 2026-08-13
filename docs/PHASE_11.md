# Phase 11 — Video engine + Instagram media list

## Status

COMPLETE for capability detection. FFmpeg is NOT assumed present.

## Implemented

- `media-engine` probe + thumbnail
- `GET /api/v1/video/status`
- Optional static ffmpeg install on Render build
- Instagram Login token exchange via `api.instagram.com` + long-lived token
- `GET /api/v1/instagram/media` (REAL items or NO DATA)
- CORS parser ignores accidental comments in env values

## Live production check (2026-08-13)

`https://auto-instagram-1aci.onrender.com/api/v1/config` still reported:

- database NOT_CONFIGURED
- meta_oauth NOT_CONFIGURED

Meta Business setup alone does not activate the API until Render env vars exist.

## Next

Wire FFmpeg trim/crop once binary is on the host; user must add DATABASE_URL + META_* on Render.
