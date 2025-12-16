from fastapi import APIRouter

from app.api.deps import CurrentUser
from app.schemas.user import UserPublic


router = APIRouter()


@router.get("/me", response_model=UserPublic)
def me(user: CurrentUser) -> UserPublic:
    return UserPublic.model_validate(user.model_dump())

