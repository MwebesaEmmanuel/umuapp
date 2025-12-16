# Security baseline (MVP)

## Accounts & access

- Signup restricted to `@umu.ac.ug` and `@stud.umu.ac.ug`
- Role-based access control (student/staff/admin)
- Visitor mode is **read-only** and requires no login

## Tokens

- Short-lived JWT access tokens
- Digital ID QR tokens are time-limited and signed

## Production hardening (before going live)

- Enforce email verification + password reset
- Add refresh tokens + token revocation
- Add rate limiting + IP throttling on auth + chat
- Use PostgreSQL, migrations, backups, and monitoring
- Use HTTPS everywhere, HSTS, and secure secret storage
- Add audit logs for attendance and admin actions

