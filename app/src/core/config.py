"""Bot settings from environment variables."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Bot settings from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    bot_token: str
    admin_ids: list[int] = Field(default_factory=list)
    admin_chat_id: int
    redis_url: str = "redis://localhost:6379/0"


settings = Settings()  # type: ignore[call-arg]
