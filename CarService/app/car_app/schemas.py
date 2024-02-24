from datetime import datetime

from fastapi import Form
from pydantic import BaseModel, ConfigDict, field_validator, PositiveFloat

from app.core.enums import Brands, Categories, Colors, FuelTypes, Statuses, Transmissions


class BaseCarSchema(BaseModel):
    number: str
    brand: Brands
    year: int
    status: Statuses
    description: str | None = None
    transmission: Transmissions
    fuel_type: FuelTypes
    color: Colors
    category: Categories
    engine_capacity: PositiveFloat
    station_id: int
    cost_per_hour: PositiveFloat

    @field_validator('year')
    def over_the_current_year(cls, year: int) -> int:
        current_year = datetime.now().year
        if year < 1900 or year > current_year:
            raise ValueError('Year must be between 1900 and current year')
        return year

    @classmethod
    def as_form(
        cls,
        number: str = Form(),
        brand: Brands = Form(),
        year: int = Form(),
        status: Statuses = Form(),
        description: str | None = Form(None),
        transmission: Transmissions = Form(),
        fuel_type: FuelTypes = Form(),
        color: Colors = Form(),
        category: Categories = Form(),
        engine_capacity: PositiveFloat = Form(),
        station_id: int = Form(),
        cost_per_hour: PositiveFloat = Form(),
    ) -> 'BaseCarSchema':
        return cls(
            description=description,
            status=status,
            color=color,
            engine_capacity=engine_capacity,
            fuel_type=fuel_type,
            cost_per_hour=cost_per_hour,
            station_id=station_id,
            transmission=transmission,
            number=number,
            year=year,
            brand=brand,
            category=category,
        )


class CarSchema(BaseCarSchema):
    id: int
    image: str | None = None

    model_config = ConfigDict(from_attributes=True)


class CarCreatingSchema(BaseCarSchema):
    pass


class CarUpdatingSchema(BaseCarSchema):
    pass
