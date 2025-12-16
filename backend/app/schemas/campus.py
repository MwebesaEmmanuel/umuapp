from datetime import datetime

from pydantic import BaseModel, Field


class OfficeCreate(BaseModel):
    name: str = Field(min_length=2, max_length=140)
    category: str = Field(default="", max_length=80)
    building: str = Field(default="", max_length=80)
    description: str = Field(default="", max_length=2000)
    latitude: float
    longitude: float
    phone: str = Field(default="", max_length=60)
    email: str = Field(default="", max_length=254)
    opening_hours: str = Field(default="", max_length=200)


class OfficePublic(BaseModel):
    id: int
    name: str
    category: str
    building: str
    description: str
    latitude: float
    longitude: float
    phone: str
    email: str
    opening_hours: str
    created_at: datetime

