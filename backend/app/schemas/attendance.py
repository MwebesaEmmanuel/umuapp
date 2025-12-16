from datetime import datetime

from pydantic import BaseModel, Field

from app.models.attendance import AttendanceKind


class QRTokenResponse(BaseModel):
    token: str
    expires_in_seconds: int


class AttendanceSessionCreate(BaseModel):
    name: str = Field(min_length=2, max_length=140)
    kind: AttendanceKind = AttendanceKind.lecture
    starts_at: datetime
    ends_at: datetime


class AttendanceSessionPublic(BaseModel):
    id: int
    name: str
    kind: AttendanceKind
    starts_at: datetime
    ends_at: datetime
    created_by_user_id: int
    created_at: datetime


class AttendanceCheckinRequest(BaseModel):
    session_id: int
    attendee_qr_token: str


class AttendanceCheckinPublic(BaseModel):
    id: int
    session_id: int
    attendee_user_id: int
    scanner_user_id: int
    checked_in_at: datetime

