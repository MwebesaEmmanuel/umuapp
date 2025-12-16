from sqlmodel import create_engine

from app.core.settings import get_settings


def get_engine():
    settings = get_settings()
    connect_args = {}
    if settings.database_url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}
    return create_engine(settings.database_url, echo=False, connect_args=connect_args)

