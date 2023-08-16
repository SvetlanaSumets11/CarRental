from databases import Database
from sqlalchemy.ext.declarative import declarative_base

from app.config import settings

Base = declarative_base()

db = Database(
    f'{settings.POSTGRES_ENGINE}://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}'
    f'@{settings.POSTGRES_HOST}/{settings.POSTGRES_DATABASE}'
)
