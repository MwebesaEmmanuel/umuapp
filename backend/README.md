# Backend (FastAPI)

## Run locally (Windows / PowerShell)

1. Create a venv:
   - `python -m venv .venv`
   - `.\.venv\Scripts\Activate.ps1`
2. Install deps:
   - `pip install -r requirements.txt`
3. Configure env (optional):
   - Copy `.env.example` to `.env` and edit
4. Start API:
   - `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

API docs:
- Swagger UI: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

## Useful endpoints (MVP)

- Auth: `POST /api/v1/auth/register`, `POST /api/v1/auth/login`
- Me: `GET /api/v1/users/me`
- Public: `GET /api/v1/public/links`, `GET /api/v1/public/news`, `GET /api/v1/public/weather`
- Campus: `GET /api/v1/campus/offices`
- Chat: `GET /api/v1/chat/rooms`, `GET /api/v1/chat/rooms/{room_id}/messages`, WS `GET /api/v1/chat/ws/rooms/{room_id}`
- Digital ID: `GET /api/v1/attendance/id/qr`

## Database

Default uses SQLite for quick start. For PostgreSQL set `DATABASE_URL`, e.g.:

`postgresql+psycopg://umu:password@localhost:5432/umuapp`

If you use PostgreSQL you also need `psycopg` (already included in `requirements.txt`).

## Docker (optional)

From repo root:

- `docker compose up --build`

## Security notes (baseline)

- Passwords are hashed (`bcrypt`)
- JWT access tokens (short-lived)
- University email domain allowlist for signup
- Role-based access control for staff/admin routes
