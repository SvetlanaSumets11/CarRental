from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = 'CarService'

    POSTGRES_ENGINE: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_DATABASE: str

    class Config:
        case_sensitive = True
        frozen = True
        env_file = '../.env'


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
