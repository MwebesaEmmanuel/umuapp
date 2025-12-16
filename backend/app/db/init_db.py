from sqlmodel import Session, SQLModel, select

from app.db.engine import get_engine
from app.models import appconfig, attendance, bus, campus, chat, clubs, content, support, user  # noqa: F401
from app.models.chat import ChatRoom
from app.models.appconfig import ExternalLink
from app.models.campus import OfficeLocation


def init_db() -> None:
    engine = get_engine()
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        existing = session.exec(select(ChatRoom).where(ChatRoom.name == "UMU Community")).one_or_none()
        if not existing:
            session.add(ChatRoom(name="UMU Community", is_public=True))
            session.commit()

        if not session.exec(select(ExternalLink)).first():
            session.add_all(
                [
                    ExternalLink(
                        title="Uganda Martyrs University",
                        url="https://www.umu.ac.ug/",
                        icon="school",
                        sort_order=10,
                    ),
                    ExternalLink(
                        title="Online Applications",
                        url="https://applications.umu.ac.ug/",
                        icon="assignment",
                        sort_order=20,
                    ),
                    ExternalLink(
                        title="Library",
                        url="https://www.umu.ac.ug/",
                        icon="local_library",
                        sort_order=30,
                    ),
                ]
            )
            session.commit()

        if not session.exec(select(OfficeLocation)).first():
            session.add(
                OfficeLocation(
                    name="UMU Campus (sample)",
                    category="Campus",
                    building="Main",
                    description="Sample marker. Replace with real campus offices + coordinates.",
                    latitude=0.103,
                    longitude=32.0,
                    phone="",
                    email="",
                    opening_hours="",
                )
            )
            session.commit()
