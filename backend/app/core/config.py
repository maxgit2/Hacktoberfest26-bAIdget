from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    google_cloud_project: str = "demo-baidget"
    firestore_emulator_host: str | None = None
    firebase_auth_emulator_host: str | None = None
    gemini_api_key: str | None = None
    gemini_model: str | None = None  # set via env; verified against docs in slice 06
    scan_rate_limit_per_hour: int = 30
    max_image_bytes: int = 10_485_760
    tz_name: str = "Europe/Rome"


@lru_cache
def get_settings() -> Settings:
    return Settings()
