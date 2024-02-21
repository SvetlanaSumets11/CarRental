from datetime import datetime

from pydantic import BaseModel, ConfigDict
from pydantic.v1 import validator

from app.core.enums import Brands, Categories, Colors, FuelTypes, Statuses, Transmissions


class CarSchema(BaseModel):
    id: int
    number: str
    image: str | None
    brand: Brands
    description: str | None
    transmission: Transmissions
    fuel_type: FuelTypes
    color: Colors
    category: Categories
    engine_capacity: str
    year: int
    status: Statuses
    station_id: str
    cost_per_day: float

    model_config = ConfigDict(from_attributes=True)


class CarCreatingSchema(BaseModel):
    id: int
    number: str
    image: str = None
    brand: Brands
    description: str = None
    transmission: Transmissions
    fuel_type: FuelTypes
    color: Colors
    category: Categories
    engine_capacity: float
    year: int
    status: Statuses
    station_id: int
    cost_per_day: float

    @validator('engine_capacity')
    def engine_capacity_must_be_positive(cls, value: float) -> float:
        if value <= 0:
            raise ValueError('Engine capacity must be positive')
        return value

    @validator('year')
    def year_must_be_valid(cls, year: int) -> int:
        current_year = datetime.now().year
        if year < 1900 or year > current_year:
            raise ValueError('Year must be between 1900 and current year')
        return year

    @validator('cost_per_day')
    def cost_per_day_must_be_positive(cls, value: float) -> float:
        if value <= 0:
            raise ValueError('cost_per_day must be positive')
        return value
