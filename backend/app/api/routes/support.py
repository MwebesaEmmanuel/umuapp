from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select

from app.api.deps import CurrentUser, DbSession, require_roles
from app.models.support import HelpdeskTicket, HostelIssue
from app.models.user import UserRole
from app.schemas.support import (
    HostelIssueCreate,
    HostelIssuePublic,
    TicketCreate,
    TicketPublic,
)


router = APIRouter()


@router.post("/tickets", response_model=TicketPublic)
def create_ticket(payload: TicketCreate, db: DbSession, user: CurrentUser) -> TicketPublic:
    row = HelpdeskTicket(
        created_by_user_id=user.id,
        category=payload.category,
        subject=payload.subject,
        description=payload.description,
        updated_at=datetime.utcnow(),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return TicketPublic.model_validate(row.model_dump())


@router.get("/tickets", response_model=list[TicketPublic])
def list_tickets(db: DbSession, user: CurrentUser) -> list[TicketPublic]:
    if user.role in {UserRole.staff, UserRole.admin}:
        rows = db.exec(select(HelpdeskTicket).order_by(HelpdeskTicket.created_at.desc())).all()
    else:
        rows = db.exec(
            select(HelpdeskTicket)
            .where(HelpdeskTicket.created_by_user_id == user.id)
            .order_by(HelpdeskTicket.created_at.desc())
        ).all()
    return [TicketPublic.model_validate(r.model_dump()) for r in rows]


@router.post("/hostel/issues", response_model=HostelIssuePublic)
def create_hostel_issue(payload: HostelIssueCreate, db: DbSession, user: CurrentUser) -> HostelIssuePublic:
    row = HostelIssue(
        reporter_user_id=user.id,
        hostel=payload.hostel,
        room=payload.room,
        issue_type=payload.issue_type,
        description=payload.description,
        updated_at=datetime.utcnow(),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return HostelIssuePublic.model_validate(row.model_dump())


@router.get("/hostel/issues", response_model=list[HostelIssuePublic])
def list_hostel_issues(db: DbSession, user: CurrentUser) -> list[HostelIssuePublic]:
    if user.role in {UserRole.staff, UserRole.admin}:
        rows = db.exec(select(HostelIssue).order_by(HostelIssue.created_at.desc())).all()
    else:
        rows = db.exec(
            select(HostelIssue)
            .where(HostelIssue.reporter_user_id == user.id)
            .order_by(HostelIssue.created_at.desc())
        ).all()
    return [HostelIssuePublic.model_validate(r.model_dump()) for r in rows]


@router.post(
    "/tickets/{ticket_id}/assign/{assignee_user_id}",
    response_model=TicketPublic,
    dependencies=[Depends(require_roles({UserRole.staff, UserRole.admin}))],
)
def assign_ticket(ticket_id: int, assignee_user_id: int, db: DbSession, user: CurrentUser) -> TicketPublic:
    row = db.exec(select(HelpdeskTicket).where(HelpdeskTicket.id == ticket_id)).one_or_none()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")
    row.assigned_to_user_id = assignee_user_id
    row.updated_at = datetime.utcnow()
    db.add(row)
    db.commit()
    db.refresh(row)
    return TicketPublic.model_validate(row.model_dump())

