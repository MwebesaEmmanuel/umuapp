from datetime import datetime

from pydantic import BaseModel, Field


class AnnouncementCreate(BaseModel):
    title: str = Field(min_length=2, max_length=140)
    body: str = Field(min_length=1, max_length=10_000)


class AnnouncementPublic(BaseModel):
    id: int
    title: str
    body: str
    created_at: datetime
    created_by_user_id: int


class EventCreate(BaseModel):
    title: str = Field(min_length=2, max_length=140)
    description: str = Field(min_length=1, max_length=10_000)
    starts_at: datetime
    ends_at: datetime
    location: str = ""


class EventPublic(BaseModel):
    id: int
    title: str
    description: str
    starts_at: datetime
    ends_at: datetime
    location: str
    created_at: datetime
    created_by_user_id: int

