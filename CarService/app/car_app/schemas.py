from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator, model_validator, PositiveFloat

from app.core.enums import Brands, Categories, Colors, FuelTypes, Statuses, Transmissions


class BaseCarSchema(BaseModel):
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
    @classmethod
    def over_the_current_year(cls, year: int) -> int:
        current_year = datetime.now().year
        if year < 1900 or year > current_year:
            raise ValueError('Year must be between 1900 and current year')
        return year


class CarSchema(BaseCarSchema):
    id: int
    number: str
    image: str | None = None

    model_config = ConfigDict(from_attributes=True)


class CarCreatingSchema(BaseCarSchema):
    number: str

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value: Any) -> Any:
        if isinstance(value, str):
            return cls.model_validate_json(value)
        return value


class CarUpdatingSchema(BaseCarSchema):
    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value: Any) -> Any:
        if isinstance(value, str):
            return cls.model_validate_json(value)
        return value


class CarPartialUpdateSchema(BaseModel):
    status: Statuses | None = None
    description: str | None = None
    color: Colors | None = None
    station_id: int | None = None
    cost_per_hour: PositiveFloat | None = None

    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value: Any) -> Any:
        if isinstance(value, str):
            return cls.model_validate_json(value)
        return value
