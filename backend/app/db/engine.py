from sqlalchemy.engine.url import make_url
from sqlmodel import create_engine

from app.core.settings import get_settings


def get_engine():
    settings = get_settings()
    database_url = settings.normalized_database_url
    connect_args = {}
    if database_url.startswith("sqlite"):
        connect_args = {"check_same_thread": False}
    # Avoid logging secrets; validate parse early.
    make_url(database_url)
    return create_engine(database_url, echo=False, connect_args=connect_args)
