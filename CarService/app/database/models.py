from sqlalchemy import CheckConstraint, Column, DateTime, Enum, Float, Integer
from sqlalchemy.sql import func

from app.database.db import Base
from app.enums import Brands, Categories, Colors, FuelTypes, Transmissions


class Car(Base):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    brand = Column(Enum(Brands), nullable=False)
    transmission = Column(Enum(Transmissions), nullable=False)
    fuel_type = Column(Enum(FuelTypes), nullable=False)
    color = Column(Enum(Colors), nullable=False)
    category = Column(Enum(Categories), nullable=False)
    engine_capacity = Column(Float, CheckConstraint('engine_capacity > 0'), nullable=False)
    year = Column(Integer, CheckConstraint('year >= 1900 AND year <= EXTRACT(YEAR FROM NOW())'), nullable=False)
    cost_per_day = Column(Float, CheckConstraint('cost_per_day > 0'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
