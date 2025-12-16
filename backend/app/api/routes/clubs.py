from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select

from app.api.deps import CurrentUser, DbSession, require_roles
from app.models.clubs import Club, ClubMembership
from app.models.user import UserRole
from app.schemas.clubs import ClubCreate, ClubMembershipPublic, ClubPublic


router = APIRouter()


@router.get("/", response_model=list[ClubPublic])
def list_clubs(db: DbSession) -> list[ClubPublic]:
    rows = db.exec(select(Club).order_by(Club.created_at.desc())).all()
    return [ClubPublic.model_validate(r.model_dump()) for r in rows]


@router.post(
    "/",
    response_model=ClubPublic,
    dependencies=[Depends(require_roles({UserRole.staff, UserRole.admin}))],
)
def create_club(payload: ClubCreate, db: DbSession, user: CurrentUser) -> ClubPublic:
    row = Club(
        name=payload.name,
        description=payload.description,
        is_public=payload.is_public,
        created_by_user_id=user.id,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return ClubPublic.model_validate(row.model_dump())


@router.post("/{club_id}/join", response_model=ClubMembershipPublic)
def join_club(club_id: int, db: DbSession, user: CurrentUser) -> ClubMembershipPublic:
    club = db.exec(select(Club).where(Club.id == club_id)).one_or_none()
    if not club:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Club not found")
    existing = db.exec(
        select(ClubMembership).where(ClubMembership.club_id == club_id, ClubMembership.user_id == user.id)
    ).one_or_none()
    if existing:
        return ClubMembershipPublic.model_validate(existing.model_dump())

    row = ClubMembership(club_id=club_id, user_id=user.id)
    db.add(row)
    db.commit()
    db.refresh(row)
    return ClubMembershipPublic.model_validate(row.model_dump())


@router.post("/{club_id}/leave")
def leave_club(club_id: int, db: DbSession, user: CurrentUser) -> dict:
    existing = db.exec(
        select(ClubMembership).where(ClubMembership.club_id == club_id, ClubMembership.user_id == user.id)
    ).one_or_none()
    if not existing:
        return {"ok": True}
    db.delete(existing)
    db.commit()
    return {"ok": True}
