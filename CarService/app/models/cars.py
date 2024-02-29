from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Enum, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base
from app.core.enums import Brands, Categories, Colors, FuelTypes, Statuses, Transmissions


class Car(Base):
    __tablename__ = 'cars'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    number: Mapped[str] = mapped_column(String(length=16), unique=True, nullable=False)
    image: Mapped[str] = mapped_column(String(length=256), unique=True, nullable=True)
    brand: Mapped[str] = mapped_column(Enum(Brands), nullable=False)
    description: Mapped[str] = mapped_column(String(length=256), nullable=True)
    transmission: Mapped[str] = mapped_column(Enum(Transmissions), nullable=False)
    fuel_type: Mapped[str] = mapped_column(Enum(FuelTypes), nullable=False)
    color: Mapped[str] = mapped_column(Enum(Colors), nullable=False)
    category: Mapped[str] = mapped_column(Enum(Categories), nullable=False)
    engine_capacity: Mapped[float] = mapped_column(Float, CheckConstraint('engine_capacity > 0'), nullable=False)
    year: Mapped[int] = mapped_column(
        Integer, CheckConstraint('year >= 1900 AND year <= EXTRACT(YEAR FROM NOW())'), nullable=False
    )
    status: Mapped[str] = mapped_column(Enum(Statuses), nullable=False, default=Statuses.free)
    station_id: Mapped[int] = mapped_column(Integer, nullable=False)
    cost_per_hour: Mapped[float] = mapped_column(Float, CheckConstraint('cost_per_hour > 0'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
