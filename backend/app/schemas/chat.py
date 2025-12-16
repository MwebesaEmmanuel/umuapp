from datetime import datetime

from pydantic import BaseModel, Field


class ChatRoomCreate(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    is_public: bool = True


class ChatRoomPublic(BaseModel):
    id: int
    name: str
    is_public: bool
    created_at: datetime


class ChatMessagePublic(BaseModel):
    id: int
    room_id: int
    sender_user_id: int
    body: str
    sent_at: datetime

