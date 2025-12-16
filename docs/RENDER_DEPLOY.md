# Deploy backend to Render (FastAPI)

## 0) Put the project on GitHub

Render deploys from GitHub. If you haven’t:

- Create a GitHub repo
- Push `C:\umuapp` to it

## 0b) Pick an Android package id (Play Store)

Play Store requires a unique package id like `ug.ac.umu.umuapp` (not just `umuapp`).

## 1) Create PostgreSQL on Render

- Render Dashboard → New → **PostgreSQL**
- Copy the **Internal Database URL**

## 2) Create Web Service (API)

- Render Dashboard → New → **Web Service**
- Connect your GitHub repo
- Root directory: repo root
- Build command:
  - `cd backend && pip install -r requirements.txt`
- Start command:
  - `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## 3) Set environment variables (API)

- `SECRET_KEY` = long random string
- `DATABASE_URL` = your Render Postgres URL (use `postgresql+psycopg://...`)
- `ALLOWED_EMAIL_DOMAINS` = `umu.ac.ug,stud.umu.ac.ug`
- `CORS_ORIGINS` = your web app domain(s), e.g. `https://umuapp.onrender.com`

## 4) WebSockets (chat)

Render Web Service supports WebSockets, but on free tiers services can sleep; chat will drop when sleeping.

## 4) Verify

- Open `https://YOUR_API.onrender.com/docs`
- Register/login
- Test `/api/v1/public/news`
- Test chat rooms list `/api/v1/chat/rooms`
