from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlmodel import select

from app.api.deps import CurrentUser, DbSession, require_roles
from app.models.campus import OfficeLocation
from app.models.user import UserRole
from app.schemas.campus import OfficeCreate, OfficePublic


router = APIRouter()


@router.get("/offices", response_model=list[OfficePublic])
def list_offices(db: DbSession, q: str | None = None) -> list[OfficePublic]:
    stmt = select(OfficeLocation).order_by(OfficeLocation.name.asc())
    if q:
        q_like = f"%{q.strip()}%"
        stmt = stmt.where(OfficeLocation.name.like(q_like) | OfficeLocation.category.like(q_like))
    rows = db.exec(stmt).all()
    return [OfficePublic.model_validate(r.model_dump()) for r in rows]


@router.post(
    "/offices",
    response_model=OfficePublic,
    dependencies=[Depends(require_roles({UserRole.staff, UserRole.admin}))],
)
def create_office(payload: OfficeCreate, db: DbSession, user: CurrentUser) -> OfficePublic:
    row = OfficeLocation(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return OfficePublic.model_validate(row.model_dump())

