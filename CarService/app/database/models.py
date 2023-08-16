from sqlalchemy import CheckConstraint, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.database.db import Base


class Car(Base):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    brand_id = Column(Integer, ForeignKey('brands.id'), nullable=False)
    transmission_id = Column(Integer, ForeignKey('transmissions.id'), nullable=False)
    fuel_type_id = Column(Integer, ForeignKey('fuel_types.id'), nullable=False)
    color_id = Column(Integer, ForeignKey('colors.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    engine_capacity = Column(Float, CheckConstraint('engine_capacity > 0'), nullable=False)
    year = Column(Integer, CheckConstraint('year >= 1900 AND year <= EXTRACT(YEAR FROM NOW())'), nullable=False)
    cost_per_day = Column(Float, CheckConstraint('cost_per_day > 0'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Brand(Base):
    __tablename__ = 'brands'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(128), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Transmission(Base):
    __tablename__ = 'transmissions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(128), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class FuelType(Base):
    __tablename__ = 'fuel_types'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(128), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Color(Base):
    __tablename__ = 'colors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(64), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(128), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
