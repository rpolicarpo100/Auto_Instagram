# Phase 01 — Deploy Foundation

## Status

COMPLETE

## Implemented

- Repository layout
- FastAPI app with `GET /api/health` and `GET /health`
- React + Vite + TypeScript landing page
- `.env.example`, `.gitignore`, `LICENSE`, `README.md`
- `render.yaml` for API + static web
- `docker-compose.yml` for local API
- GitHub Actions: backend health import + frontend typecheck/build

## Real data sources

None in this phase. Health response is process status only, not Instagram data.

## Tests

- `pytest` backend: health payload
- Frontend `npm run build` (typecheck via `tsc`)

## Known limitations

- No database
- No authentication
- No Instagram connection
- Landing CTA does not claim later features work

## Security notes

- No secrets in repo
- CORS limited via `CORS_ORIGINS`

## Next phase

PHASE 02 — UI Foundation (sidebar shells). Do not start until this phase is accepted.
