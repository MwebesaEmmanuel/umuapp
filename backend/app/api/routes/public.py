from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import feedparser
import httpx
from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.api.deps import DbSession
from app.core.settings import get_settings
from app.models.appconfig import ExternalLink
from app.schemas.appconfig import (
    ExternalLinkPublic,
    MotivationVideo,
    NewsItem,
    PublicHomeResponse,
    WeatherNow,
)


router = APIRouter()


@router.get("/home", response_model=PublicHomeResponse)
def public_home(db: DbSession) -> PublicHomeResponse:
    links = db.exec(select(ExternalLink).order_by(ExternalLink.sort_order.asc())).all()
    return PublicHomeResponse(links=[ExternalLinkPublic.model_validate(r.model_dump()) for r in links])


@router.get("/links", response_model=list[ExternalLinkPublic])
def list_links(db: DbSession) -> list[ExternalLinkPublic]:
    links = db.exec(select(ExternalLink).order_by(ExternalLink.sort_order.asc())).all()
    return [ExternalLinkPublic.model_validate(r.model_dump()) for r in links]


@router.get("/news", response_model=list[NewsItem])
async def global_news(limit: int = 30) -> list[NewsItem]:
    settings = get_settings()
    limit = max(1, min(80, limit))

    def _pick_image(entry) -> str | None:
        try:
            for key in ("media_thumbnail", "media_content"):
                media = getattr(entry, key, None) or entry.get(key)
                if isinstance(media, list) and media:
                    url = media[0].get("url") or media[0].get("href")
                    if url:
                        return str(url)
            links = getattr(entry, "links", None) or entry.get("links") or []
            for l in links:
                if (l.get("type") or "").startswith("image/") and (l.get("href") or ""):
                    return str(l["href"])
        except Exception:
            return None
        return None

    async with httpx.AsyncClient(timeout=6.0, follow_redirects=True) as client:
        items: list[NewsItem] = []
        for url in settings.news_rss_urls:
            try:
                resp = await client.get(url, headers={"User-Agent": "UMUApp/0.1"})
                resp.raise_for_status()
            except Exception:
                continue

            feed = feedparser.parse(resp.text)
            source = (feed.feed.get("title") or url).strip()
            for entry in feed.entries[:limit]:
                link = entry.get("link")
                title = entry.get("title")
                if not link or not title:
                    continue
                published = entry.get("published") or entry.get("updated")
                image_url = _pick_image(entry)
                items.append(
                    NewsItem(
                        source=source,
                        title=str(title),
                        url=str(link),
                        published_at=str(published) if published else None,
                        image_url=image_url,
                    )
                )
                if len(items) >= limit:
                    return items
        return items


@router.get("/motivation", response_model=list[MotivationVideo])
def motivation() -> list[MotivationVideo]:
    settings = get_settings()
    return [MotivationVideo(title=v["title"], url=v["url"], source="youtube") for v in settings.motivation_videos]


@router.get("/weather", response_model=WeatherNow)
async def weather(lat: float, lon: float) -> WeatherNow:
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        raise HTTPException(status_code=400, detail="Invalid coordinates")

    url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude": lat, "longitude": lon, "current_weather": "true"}
    async with httpx.AsyncClient(timeout=6.0, follow_redirects=True) as client:
        resp = await client.get(url, params=params, headers={"User-Agent": "UMUApp/0.1"})
        resp.raise_for_status()
        data: dict[str, Any] = resp.json()

    current = data.get("current_weather") or {}
    observed_at = None
    if current.get("time"):
        observed_at = str(current.get("time"))
    else:
        observed_at = datetime.now(timezone.utc).isoformat()

    return WeatherNow(
        latitude=float(data.get("latitude", lat)),
        longitude=float(data.get("longitude", lon)),
        temperature_c=current.get("temperature"),
        wind_speed_kmh=current.get("windspeed"),
        weather_code=current.get("weathercode"),
        observed_at=observed_at,
    )
