# Phases 03–08

## Status

COMPLETE (incremental). Instagram OAuth works only when Meta env vars are set.

## Implemented

- `/api/v1/health`, `/version`, `/config` + request IDs + error envelope
- PostgreSQL models: users, sessions, instagram_accounts, content, media_assets, jobs
- Alembic `0001_initial` + `create_all` on boot
- register / login / logout / me (httpOnly session cookie)
- Dashboard API: REAL / NO DATA / NOT AVAILABLE / NOT CONFIGURED
- InstagramProvider + Meta + Mock (tests only)
- Official OAuth connect + callback + encrypted token storage

## Real data sources

- Process health
- Local user session
- Instagram Graph `/me` and insights **only after** successful OAuth

## Tests

Pytest: health/v1, auth cycle, dashboard empty metrics, connect without Meta → 503

## Known limitations

- No Postgres on Render until you add the addon and `DATABASE_URL`
- OAuth `state` is in process memory (lost on restart)
- Publish not implemented
- Cross-origin cookies need `CORS_ORIGINS` = exact frontend origin

## Next phase

PHASE 09 — persist account snapshots and list media from Graph when connected
