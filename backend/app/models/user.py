from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class UserRole(str, Enum):
    student = "student"
    staff = "staff"
    admin = "admin"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str

    role: UserRole = Field(default=UserRole.student)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=True)

    created_at: datetime = Field(default_factory=datetime.utcnow)

