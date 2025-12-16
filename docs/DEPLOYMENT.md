# Deployment (practical checklist)

## Backend (API)

- Pick hosting: Render / Fly.io / AWS / Azure (needs HTTPS + Postgres)
- Provision PostgreSQL + backups
- Set env vars:
  - `SECRET_KEY` (strong, rotated, not committed)
  - `DATABASE_URL`
  - `ALLOWED_EMAIL_DOMAINS`
  - `ADMIN_EMAILS`
  - `REQUIRE_EMAIL_VERIFICATION=true` (recommended)
- Put API behind HTTPS and enable monitoring + logs

## Mobile (stores)

- Google Play:
  - Create a developer account
  - Configure app signing keys + package name
  - Add privacy policy + data safety form
- Apple App Store:
  - Requires Apple Developer account + macOS/Xcode for builds

## Security before “anyone can download”

- Email verification + password reset
- Rate limiting on auth/chat
- Audit logging for attendance + admin actions
- Pen test / security review (especially around QR attendance)

