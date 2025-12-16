from datetime import datetime

from pydantic import BaseModel, Field


class ExternalLinkCreate(BaseModel):
    title: str = Field(min_length=2, max_length=80)
    url: str = Field(min_length=4, max_length=500)
    icon: str = Field(default="", max_length=40)
    requires_login: bool = False
    sort_order: int = 0


class ExternalLinkPublic(BaseModel):
    id: int
    title: str
    url: str
    icon: str
    requires_login: bool
    sort_order: int
    created_at: datetime


class NewsItem(BaseModel):
    source: str
    title: str
    url: str
    published_at: str | None = None
    image_url: str | None = None


class MotivationVideo(BaseModel):
    title: str
    url: str
    source: str | None = None


class WeatherNow(BaseModel):
    latitude: float
    longitude: float
    temperature_c: float | None = None
    wind_speed_kmh: float | None = None
    weather_code: int | None = None
    observed_at: str | None = None


class PublicHomeResponse(BaseModel):
    links: list[ExternalLinkPublic]
