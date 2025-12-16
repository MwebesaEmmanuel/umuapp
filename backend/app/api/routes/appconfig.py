from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlmodel import select

from app.api.deps import CurrentUser, DbSession, require_roles
from app.models.appconfig import ExternalLink
from app.models.user import UserRole
from app.schemas.appconfig import ExternalLinkCreate, ExternalLinkPublic


router = APIRouter()


@router.get(
    "/links",
    response_model=list[ExternalLinkPublic],
    dependencies=[Depends(require_roles({UserRole.staff, UserRole.admin}))],
)
def admin_list_links(db: DbSession, user: CurrentUser) -> list[ExternalLinkPublic]:
    rows = db.exec(select(ExternalLink).order_by(ExternalLink.sort_order.asc())).all()
    return [ExternalLinkPublic.model_validate(r.model_dump()) for r in rows]


@router.post(
    "/links",
    response_model=ExternalLinkPublic,
    dependencies=[Depends(require_roles({UserRole.staff, UserRole.admin}))],
)
def create_link(payload: ExternalLinkCreate, db: DbSession, user: CurrentUser) -> ExternalLinkPublic:
    row = ExternalLink(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return ExternalLinkPublic.model_validate(row.model_dump())
