from fastapi import APIRouter

from app.api.routes import (
    appconfig,
    attendance,
    auth,
    bus,
    campus,
    chat,
    clubs,
    content,
    public,
    support,
    users,
    ai,
)


api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(content.router, prefix="/content", tags=["content"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(attendance.router, prefix="/attendance", tags=["attendance"])
api_router.include_router(campus.router, prefix="/campus", tags=["campus"])
api_router.include_router(support.router, prefix="/support", tags=["support"])
api_router.include_router(public.router, prefix="/public", tags=["public"])
api_router.include_router(appconfig.router, prefix="/config", tags=["config"])
api_router.include_router(bus.router, prefix="/bus", tags=["bus"])
api_router.include_router(clubs.router, prefix="/clubs", tags=["clubs"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
