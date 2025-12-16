from datetime import datetime

from pydantic import BaseModel, Field


class ClubCreate(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    description: str = Field(default="", max_length=4000)
    is_public: bool = True


class ClubPublic(BaseModel):
    id: int
    name: str
    description: str
    is_public: bool
    created_by_user_id: int
    created_at: datetime


class ClubMembershipPublic(BaseModel):
    id: int
    club_id: int
    user_id: int
    joined_at: datetime

