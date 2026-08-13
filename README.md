# Instagram AI Factory

AI-powered Instagram content operating system.

This repository is built in **30 phases**. Phase 01 is the deploy foundation only.

## What works now (Phase 02)

- FastAPI backend with a real health endpoint
- App shell: Dashboard, Produção, Biblioteca, Calendário, Analytics, Receita, Instagram, AI Brain, Settings
- Honest empty states (NO DATA / NOT CONFIGURED / NOT IMPLEMENTED)
- Render blueprint
- Environment template (no secrets)

Deployed API (example): `https://auto-instagram-1aci.onrender.com/api/health`

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
