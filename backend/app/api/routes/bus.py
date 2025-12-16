from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select

from app.api.deps import CurrentUser, DbSession, require_roles
from app.models.bus import BusBooking, BusLocation, BusRoute, BusTrip
from app.models.user import UserRole
from app.schemas.bus import (
    BusBookingCreate,
    BusBookingPublic,
    BusLocationPublic,
    BusRouteCreate,
    BusRoutePublic,
    BusTripCreate,
    BusTripPublic,
)


router = APIRouter()


@router.get("/routes", response_model=list[BusRoutePublic])
def list_routes(db: DbSession) -> list[BusRoutePublic]:
    rows = db.exec(select(BusRoute).order_by(BusRoute.name.asc())).all()
    return [BusRoutePublic.model_validate(r.model_dump()) for r in rows]


@router.post(
    "/routes",
    response_model=BusRoutePublic,
    dependencies=[Depends(require_roles({UserRole.staff, UserRole.admin}))],
)
def create_route(payload: BusRouteCreate, db: DbSession, user: CurrentUser) -> BusRoutePublic:
    row = BusRoute(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return BusRoutePublic.model_validate(row.model_dump())


@router.get("/trips", response_model=list[BusTripPublic])
def list_trips(db: DbSession, route_id: int | None = None) -> list[BusTripPublic]:
    stmt = select(BusTrip).order_by(BusTrip.departure_time.asc())
    if route_id:
        stmt = stmt.where(BusTrip.route_id == route_id)
    rows = db.exec(stmt).all()
    return [BusTripPublic.model_validate(r.model_dump()) for r in rows]


@router.post(
    "/trips",
    response_model=BusTripPublic,
    dependencies=[Depends(require_roles({UserRole.staff, UserRole.admin}))],
)
def create_trip(payload: BusTripCreate, db: DbSession, user: CurrentUser) -> BusTripPublic:
    row = BusTrip(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return BusTripPublic.model_validate(row.model_dump())


@router.post("/bookings", response_model=BusBookingPublic)
def book_trip(payload: BusBookingCreate, db: DbSession, user: CurrentUser) -> BusBookingPublic:
    trip = db.exec(select(BusTrip).where(BusTrip.id == payload.trip_id)).one_or_none()
    if not trip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")

    existing = db.exec(
        select(BusBooking).where(BusBooking.trip_id == trip.id, BusBooking.user_id == user.id)
    ).one_or_none()
    if existing:
        return BusBookingPublic.model_validate(existing.model_dump())

    row = BusBooking(trip_id=trip.id, user_id=user.id, seats=payload.seats)
    db.add(row)
    db.commit()
    db.refresh(row)
    return BusBookingPublic.model_validate(row.model_dump())


@router.get("/trips/{trip_id}/location", response_model=BusLocationPublic | None)
def last_location(trip_id: int, db: DbSession) -> BusLocationPublic | None:
    row = db.exec(
        select(BusLocation).where(BusLocation.trip_id == trip_id).order_by(BusLocation.reported_at.desc())
    ).first()
    if not row:
        return None
    return BusLocationPublic(
        trip_id=row.trip_id,
        latitude=row.latitude,
        longitude=row.longitude,
        reported_at=row.reported_at,
    )


@router.post(
    "/trips/{trip_id}/location",
    response_model=BusLocationPublic,
    dependencies=[Depends(require_roles({UserRole.staff, UserRole.admin}))],
)
def report_location(trip_id: int, lat: float, lon: float, db: DbSession, user: CurrentUser) -> BusLocationPublic:
    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        raise HTTPException(status_code=400, detail="Invalid coordinates")
    trip = db.exec(select(BusTrip).where(BusTrip.id == trip_id)).one_or_none()
    if not trip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
    row = BusLocation(
        trip_id=trip_id,
        latitude=lat,
        longitude=lon,
        reported_at=datetime.utcnow(),
        reported_by_user_id=user.id,
    )
    db.add(row)
    db.commit()
    return BusLocationPublic(trip_id=trip_id, latitude=lat, longitude=lon, reported_at=row.reported_at)

