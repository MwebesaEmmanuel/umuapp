from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Announcement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    body: str
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    created_by_user_id: int = Field(foreign_key="user.id")


class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    starts_at: datetime = Field(index=True)
    ends_at: datetime = Field(index=True)
    location: str = Field(default="")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by_user_id: int = Field(foreign_key="user.id")

