from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class TicketStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    closed = "closed"


class HelpdeskTicket(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_by_user_id: int = Field(index=True, foreign_key="user.id")
    category: str = Field(default="", index=True)
    subject: str
    description: str
    status: TicketStatus = Field(default=TicketStatus.open, index=True)
    assigned_to_user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow, index=True)


class HostelIssue(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    reporter_user_id: int = Field(index=True, foreign_key="user.id")
    hostel: str = Field(default="", index=True)
    room: str = Field(default="", index=True)
    issue_type: str = Field(default="", index=True)
    description: str
    status: TicketStatus = Field(default=TicketStatus.open, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow, index=True)

