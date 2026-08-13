# Instagram AI Factory

AI-powered Instagram content operating system.

This repository is built in **30 phases**. Phase 01 is the deploy foundation only.

## What works now (Phase 08)

- FastAPI `/api/health` and `/api/v1/*`
- Register / login / session cookies
- Dashboard and Instagram screens with honest empty states
- Official Meta OAuth **when** `META_*` and `DATABASE_URL` are set

Deployed API: `https://auto-instagram-1aci.onrender.com/api/health`

### Render env (API service)

- `DATABASE_URL` — Render PostgreSQL (required for login)
- `CORS_ORIGINS` — exact Static Site origin, e.g. `https://xxx.onrender.com`
- `SESSION_SECRET`
- `TOKEN_ENCRYPTION_KEY` (Fernet)
- `META_APP_ID` / `META_APP_SECRET` / `META_REDIRECT_URI` = `https://auto-instagram-1aci.onrender.com/api/v1/instagram/callback`

Later phases add auth, Instagram OAuth, media, Reels, analytics, and agents. Those features are **not implemented** yet.

## Requirements

- Python 3.11+
- Node.js 20+
- Git

## Local development

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Health check:

```bash
curl http://localhost:8000/api/health
```

Expected:

```json
{"status":"ok","service":"instagram-ai-factory"}
```

### Frontend

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

Copy `.env.example` to `.env` and set `VITE_API_BASE_URL` if the API is not on `http://localhost:8000`.

## Deploy (Render)

`render.yaml` defines:

- `instagram-ai-factory-api` — FastAPI
- `instagram-ai-factory-web` — static Vite build

Configure environment variables in the Render dashboard. Do not commit secrets.

## Data policy

No fake metrics, followers, revenue, or analytics. If a source is not connected, the UI must show **NO DATA**, **NOT CONFIGURED**, **NOT AVAILABLE**, or **NOT SUPPORTED**.

## License

MIT
