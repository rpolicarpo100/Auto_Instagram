# Phases 09–10 + audit

## Status

COMPLETE for what can run without a live Meta token.

## Audit fixes

- Render `postgres://` URLs normalized to `postgresql+psycopg://`
- OAuth `state` persisted (survives process restart)
- OAuth callback redirects to `FRONTEND_ORIGIN`, not the API host
- Logout cookie flags match Set-Cookie (SameSite/Secure)
- Insights blob no longer shown as a reach number
- Frontend JSON parse errors handled
- Auth rate limited
- Security headers
- bcrypt 72-byte clamp

## Implemented

- Account snapshots from Graph `/me` after connect/refresh
- Dashboard reads last snapshot only (REAL or NO DATA)
- Media library: upload, list, delete, magic-byte validation

## Real data sources

- Health, sessions, media_assets, account_snapshots
- Instagram Graph only after OAuth

## Tests

Health, auth, empty dashboard, media reject/accept, security headers

## Next

Video engine (FFmpeg) when the runtime has ffmpeg installed
