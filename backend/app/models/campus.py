from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class OfficeLocation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    category: str = Field(default="", index=True)
    building: str = Field(default="", index=True)
    description: str = Field(default="")
    latitude: float
    longitude: float
    phone: str = Field(default="")
    email: str = Field(default="")
    opening_hours: str = Field(default="")
    created_at: datetime = Field(default_factory=datetime.utcnow)

