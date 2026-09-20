from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    api_id: int = Field(default=0, alias="API_ID")
    api_hash: str = Field(default="", alias="API_HASH")
    bot_token: str = Field(default="", alias="BOT_TOKEN")
    helper_bot_username: str = Field(default="", alias="HELPER_BOT_USERNAME")
    owner_id: int = Field(default=0, alias="OWNER_ID")
    dry_run: bool = Field(default=True, alias="DRY_RUN")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    db_path: str = Field(default="data/selfbot.db", alias="DB_PATH")
    lang: str = Field(default="fa", alias="LANG")
    log_dir: str = Field(default="logs", alias="LOG_DIR")
    max_log_size_mb: int = Field(default=10, alias="MAX_LOG_SIZE_MB")
    admin_chats: str = Field(default="", alias="ADMIN_CHATS")
    session_path: str = Field(default="data/user.session", alias="SESSION_PATH")
    bot_session_path: str = Field(default="data/bot.session", alias="BOT_SESSION_PATH")
    rate_limit_per_minute: float = Field(default=20.0, alias="RATE_LIMIT_PER_MINUTE")
    rate_limit_min_delay: float = Field(default=0.8, alias="RATE_LIMIT_MIN_DELAY")
    watchdog_minutes: int = Field(default=5, alias="WATCHDOG_MINUTES")

    def admin_chat_ids(self) -> list[int]:
        if not self.admin_chats.strip():
            return []
        return [int(x.strip()) for x in self.admin_chats.split(",") if x.strip()]

    def validate_self_check(self) -> list[str]:
        issues: list[str] = []
        if self.lang not in {"fa", "en"}:
            issues.append(f"LANG must be fa|en, got {self.lang}")
        if self.max_log_size_mb < 1:
            issues.append("MAX_LOG_SIZE_MB must be >= 1")
        return issues


def load_settings() -> Settings:
    return Settings()
