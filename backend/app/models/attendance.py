from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class AttendanceKind(str, Enum):
    lecture = "lecture"
    exam = "exam"
    event = "event"
    gate = "gate"
    hostel = "hostel"


class AttendanceSession(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    kind: AttendanceKind = Field(default=AttendanceKind.lecture)
    starts_at: datetime = Field(index=True)
    ends_at: datetime = Field(index=True)
    created_by_user_id: int = Field(index=True, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class AttendanceCheckin(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: int = Field(index=True, foreign_key="attendancesession.id")
    attendee_user_id: int = Field(index=True, foreign_key="user.id")
    scanner_user_id: int = Field(index=True, foreign_key="user.id")
    checked_in_at: datetime = Field(default_factory=datetime.utcnow, index=True)

