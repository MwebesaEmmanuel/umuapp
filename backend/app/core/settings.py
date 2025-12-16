from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    secret_key: str = Field(default="change-me", alias="SECRET_KEY")
    database_url: str = Field(default="sqlite:///./umuapp.db", alias="DATABASE_URL")

    allowed_email_domains: str = Field(
        default="umu.ac.ug,stud.umu.ac.ug", alias="ALLOWED_EMAIL_DOMAINS"
    )
    admin_emails: str = Field(default="", alias="ADMIN_EMAILS")
    require_email_verification: bool = Field(
        default=False, alias="REQUIRE_EMAIL_VERIFICATION"
    )

    # For local Flutter web, the port changes often, so we default to regex-based localhost allow.
    # In production, set `CORS_ORIGINS` explicitly and leave `CORS_ORIGIN_REGEX` empty.
    cors_origins_raw: str = Field(default="", alias="CORS_ORIGINS")
    cors_origin_regex: str = Field(
        # Avoid backslash escaping issues in `.env` by using `[0-9]` and `[.]`.
        default=r"^http://localhost(:[0-9]+)?$|^http://127[.]0[.]0[.]1(:[0-9]+)?$",
        alias="CORS_ORIGIN_REGEX",
    )
    news_rss_urls_raw: str = Field(
        default="https://news.google.com/rss?hl=en&gl=US&ceid=US:en,https://feeds.bbci.co.uk/news/rss.xml",
        alias="NEWS_RSS_URLS",
    )
    motivation_videos_raw: str = Field(
        default=(
            "TED: The power of believing you can improve|https://www.youtube.com/watch?v=_X0mgOOSpLU,"
            "TED: Grit - The power of passion and perseverance|https://www.youtube.com/watch?v=H14bBuluwB8,"
            "TED: Your body language may shape who you are|https://www.youtube.com/watch?v=Ks-_Mh1QhMc"
        ),
        alias="MOTIVATION_VIDEOS",
    )

    @property
    def cors_origins(self) -> List[str]:
        return [o.strip() for o in self.cors_origins_raw.split(",") if o.strip()]

    @property
    def allowed_domains(self) -> List[str]:
        return [d.strip().lower() for d in self.allowed_email_domains.split(",") if d.strip()]

    @property
    def admin_email_list(self) -> List[str]:
        return [e.strip().lower() for e in self.admin_emails.split(",") if e.strip()]

    @property
    def news_rss_urls(self) -> List[str]:
        return [u.strip() for u in self.news_rss_urls_raw.split(",") if u.strip()]

    @property
    def motivation_videos(self) -> List[dict]:
        videos: List[dict] = []
        for raw in self.motivation_videos_raw.split(","):
            item = raw.strip()
            if not item:
                continue
            if "|" not in item:
                continue
            title, url = item.split("|", 1)
            videos.append({"title": title.strip(), "url": url.strip()})
        return videos


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
