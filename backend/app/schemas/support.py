from datetime import datetime

from pydantic import BaseModel, Field

from app.models.support import TicketStatus


class TicketCreate(BaseModel):
    category: str = Field(default="", max_length=80)
    subject: str = Field(min_length=2, max_length=140)
    description: str = Field(min_length=1, max_length=10_000)


class TicketPublic(BaseModel):
    id: int
    created_by_user_id: int
    category: str
    subject: str
    description: str
    status: TicketStatus
    assigned_to_user_id: int | None
    created_at: datetime
    updated_at: datetime


class HostelIssueCreate(BaseModel):
    hostel: str = Field(default="", max_length=80)
    room: str = Field(default="", max_length=40)
    issue_type: str = Field(default="", max_length=80)
    description: str = Field(min_length=1, max_length=10_000)


class HostelIssuePublic(BaseModel):
    id: int
    reporter_user_id: int
    hostel: str
    room: str
    issue_type: str
    description: str
    status: TicketStatus
    created_at: datetime
    updated_at: datetime

