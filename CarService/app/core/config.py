from functools import lru_cache

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = 'CarService'
    ROOT_PATH: str = '/car_service/'
    SESSION_SECRET_KEY: str

    DATABASE_URL: PostgresDsn

    AWS_S3_CARS_BUCKET_NAME: str
    AWS_S3_ENDPOINT_URL: str | None = None

    model_config = SettingsConfigDict(
        case_sensitive=True,
        frozen=True,
        env_file='.env',
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
