from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlmodel import select

from app.api.deps import CurrentUser, DbSession, require_roles
from app.models.content import Announcement, Event
from app.models.user import UserRole
from app.schemas.content import (
    AnnouncementCreate,
    AnnouncementPublic,
    EventCreate,
    EventPublic,
)


router = APIRouter()


@router.get("/announcements", response_model=list[AnnouncementPublic])
def list_announcements(db: DbSession) -> list[AnnouncementPublic]:
    rows = db.exec(select(Announcement).order_by(Announcement.created_at.desc())).all()
    return [AnnouncementPublic.model_validate(r.model_dump()) for r in rows]


@router.post(
    "/announcements",
    response_model=AnnouncementPublic,
    dependencies=[Depends(require_roles({UserRole.staff, UserRole.admin}))],
)
def create_announcement(payload: AnnouncementCreate, db: DbSession, user: CurrentUser):
    row = Announcement(title=payload.title, body=payload.body, created_by_user_id=user.id)
    db.add(row)
    db.commit()
    db.refresh(row)
    return AnnouncementPublic.model_validate(row.model_dump())


@router.get("/events", response_model=list[EventPublic])
def list_events(db: DbSession) -> list[EventPublic]:
    rows = db.exec(select(Event).order_by(Event.starts_at.asc())).all()
    return [EventPublic.model_validate(r.model_dump()) for r in rows]


@router.post(
    "/events",
    response_model=EventPublic,
    dependencies=[Depends(require_roles({UserRole.staff, UserRole.admin}))],
)
def create_event(payload: EventCreate, db: DbSession, user: CurrentUser):
    row = Event(
        title=payload.title,
        description=payload.description,
        starts_at=payload.starts_at,
        ends_at=payload.ends_at,
        location=payload.location,
        created_by_user_id=user.id,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return EventPublic.model_validate(row.model_dump())

