# BMRC Inventory — FastAPI Backend

## Quick start (local)

```bash
cd bmrc_backend
pip install -r requirements.txt
cp .env.example .env          # add your ANTHROPIC_API_KEY
python seed.py                # load sample items
uvicorn main:app --reload     # starts on http://localhost:8000
```

## API docs
Open http://localhost:8000/docs for interactive Swagger UI.

## Key endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /api/items/ | All items with status |
| POST | /api/items/ | Add new item |
| GET | /api/items/qr/{code} | QR payload for item |
| POST | /api/transfers/ | Record transfer / STD |
| POST | /api/grn/ | Post GRN (auto-recalcs WAC) |
| GET | /api/returns/ | Open returns with status |
| POST | /api/returns/ | Log returnable item |
| PATCH | /api/returns/{id}/close | Mark returned |
| POST | /api/ai/chat | AI assistant query |

## Deploy to Railway (free tier)
1. Push this folder to a GitHub repo
2. New project on railway.app → Deploy from GitHub
3. Add env vars: DATABASE_URL (PostgreSQL), ANTHROPIC_API_KEY
4. Done — Railway gives you a public URL

## Connect the web app
In the artifact, replace the in-browser state with:
```js
const API = "https://your-railway-url.up.railway.app";
const items = await fetch(`${API}/api/items/`).then(r => r.json());
```
