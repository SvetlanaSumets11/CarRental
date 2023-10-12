from databases import Database
from sqlalchemy.ext.declarative import declarative_base

from app.config import settings

Base = declarative_base()

db = Database(settings.DATABASE_URL)
