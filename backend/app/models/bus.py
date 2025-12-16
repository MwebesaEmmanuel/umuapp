from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class BusTripStatus(str, Enum):
    scheduled = "scheduled"
    cancelled = "cancelled"
    departed = "departed"
    arrived = "arrived"


class BusRoute(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    origin: str = Field(default="", index=True)
    destination: str = Field(default="", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class BusTrip(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    route_id: int = Field(index=True, foreign_key="busroute.id")
    departure_time: datetime = Field(index=True)
    status: BusTripStatus = Field(default=BusTripStatus.scheduled, index=True)
    capacity: int = Field(default=50)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class BusBooking(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    trip_id: int = Field(index=True, foreign_key="bustrip.id")
    user_id: int = Field(index=True, foreign_key="user.id")
    seats: int = Field(default=1)
    booked_at: datetime = Field(default_factory=datetime.utcnow, index=True)


class BusLocation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    trip_id: int = Field(index=True, foreign_key="bustrip.id")
    latitude: float
    longitude: float
    reported_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    reported_by_user_id: int = Field(index=True, foreign_key="user.id")

