from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.api.deps import DbSession
from app.core.security import create_access_token, hash_password, verify_password
from app.core.settings import get_settings
from app.models.user import User, UserRole
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse


router = APIRouter()


def _role_from_email(email: str) -> UserRole:
    email = email.lower()
    if email.endswith("@stud.umu.ac.ug"):
        return UserRole.student
    return UserRole.staff


def _validate_email_domain(email: str) -> None:
    settings = get_settings()
    domain = email.split("@")[-1].lower().strip()
    if domain not in settings.allowed_domains:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email domain not allowed",
        )


@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: DbSession) -> TokenResponse:
    email = payload.email.lower().strip()
    _validate_email_domain(email)

    existing = db.exec(select(User).where(User.email == email)).one_or_none()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    settings = get_settings()
    role = _role_from_email(email)
    if email in settings.admin_email_list:
        role = UserRole.admin

    user = User(
        email=email,
        hashed_password=hash_password(payload.password),
        role=role,
        is_verified=not settings.require_email_verification,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(subject=user.email, extra={"role": user.role.value})
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: DbSession) -> TokenResponse:
    email = payload.email.lower().strip()
    user = db.exec(select(User).where(User.email == email)).one_or_none()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    settings = get_settings()
    if settings.require_email_verification and not user.is_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email not verified")

    if not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(subject=user.email, extra={"role": user.role.value})
    return TokenResponse(access_token=token)

