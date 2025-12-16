from __future__ import annotations

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError
from sqlmodel import select

from app.api.deps import CurrentUser, DbSession, require_roles
from app.core.security import create_access_token, decode_token
from app.models.attendance import AttendanceCheckin, AttendanceSession
from app.models.user import User, UserRole
from app.schemas.attendance import (
    AttendanceCheckinPublic,
    AttendanceCheckinRequest,
    AttendanceSessionCreate,
    AttendanceSessionPublic,
    QRTokenResponse,
)


router = APIRouter()


@router.get("/id/qr", response_model=QRTokenResponse)
def get_digital_id_qr(user: CurrentUser) -> QRTokenResponse:
    expires_in = 60
    token = create_access_token(
        subject=f"user:{user.id}",
        expires_minutes=1,
        extra={"typ": "umu_digital_id"},
    )
    return QRTokenResponse(token=token, expires_in_seconds=expires_in)


@router.post(
    "/sessions",
    response_model=AttendanceSessionPublic,
    dependencies=[Depends(require_roles({UserRole.staff, UserRole.admin}))],
)
def create_session(payload: AttendanceSessionCreate, db: DbSession, user: CurrentUser):
    row = AttendanceSession(
        name=payload.name,
        kind=payload.kind,
        starts_at=payload.starts_at,
        ends_at=payload.ends_at,
        created_by_user_id=user.id,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return AttendanceSessionPublic.model_validate(row.model_dump())


@router.get(
    "/sessions",
    response_model=list[AttendanceSessionPublic],
    dependencies=[Depends(require_roles({UserRole.staff, UserRole.admin}))],
)
def list_sessions(db: DbSession):
    rows = db.exec(select(AttendanceSession).order_by(AttendanceSession.starts_at.desc())).all()
    return [AttendanceSessionPublic.model_validate(r.model_dump()) for r in rows]


def _verify_qr_token(attendee_qr_token: str) -> int:
    try:
        payload = decode_token(attendee_qr_token)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid QR token")

    if payload.get("typ") != "umu_digital_id":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid QR token type")

    sub = payload.get("sub", "")
    if not isinstance(sub, str) or not sub.startswith("user:"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid QR token subject")
    try:
        user_id = int(sub.split("user:", 1)[1])
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid QR token subject")
    return user_id


@router.post(
    "/checkin",
    response_model=AttendanceCheckinPublic,
    dependencies=[Depends(require_roles({UserRole.staff, UserRole.admin}))],
)
def checkin(payload: AttendanceCheckinRequest, db: DbSession, user: CurrentUser):
    session = db.exec(
        select(AttendanceSession).where(AttendanceSession.id == payload.session_id)
    ).one_or_none()
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    now = datetime.now(timezone.utc).replace(tzinfo=None)
    if now < session.starts_at - timedelta(hours=6) or now > session.ends_at + timedelta(hours=6):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Session not active")

    attendee_user_id = _verify_qr_token(payload.attendee_qr_token)
    attendee = db.exec(select(User).where(User.id == attendee_user_id)).one_or_none()
    if not attendee or not attendee.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attendee not found")

    existing = db.exec(
        select(AttendanceCheckin).where(
            AttendanceCheckin.session_id == session.id,
            AttendanceCheckin.attendee_user_id == attendee.id,
        )
    ).one_or_none()
    if existing:
        return AttendanceCheckinPublic.model_validate(existing.model_dump())

    row = AttendanceCheckin(
        session_id=session.id,
        attendee_user_id=attendee.id,
        scanner_user_id=user.id,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return AttendanceCheckinPublic.model_validate(row.model_dump())

