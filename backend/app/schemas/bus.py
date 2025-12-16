from datetime import datetime

from pydantic import BaseModel, Field

from app.models.bus import BusTripStatus


class BusRouteCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    origin: str = Field(default="", max_length=120)
    destination: str = Field(default="", max_length=120)


class BusRoutePublic(BaseModel):
    id: int
    name: str
    origin: str
    destination: str
    created_at: datetime


class BusTripCreate(BaseModel):
    route_id: int
    departure_time: datetime
    capacity: int = Field(default=50, ge=1, le=200)


class BusTripPublic(BaseModel):
    id: int
    route_id: int
    departure_time: datetime
    status: BusTripStatus
    capacity: int
    created_at: datetime


class BusBookingCreate(BaseModel):
    trip_id: int
    seats: int = Field(default=1, ge=1, le=10)


class BusBookingPublic(BaseModel):
    id: int
    trip_id: int
    user_id: int
    seats: int
    booked_at: datetime


class BusLocationPublic(BaseModel):
    trip_id: int
    latitude: float
    longitude: float
    reported_at: datetime

