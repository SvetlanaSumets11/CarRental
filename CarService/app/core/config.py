from functools import lru_cache

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = 'CarService'

    DATABASE_URL: PostgresDsn

    model_config = SettingsConfigDict(
        case_sensitive=True,
        frozen=True,
        env_file='.env',
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
