from fastapi import Depends
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.car_app.schemas import CarCreatingSchema, CarSchema
from app.core.database import get_session
from app.core.exceptions import CarCreationError, CarGettingError, CarUpdateError
from app.models.cars import Car


class CarRepository:
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self._session = session

    async def get_by_number(self, car_number: str) -> CarSchema:
        query = select(Car).where(Car.number == car_number)
        car = await self._session.scalar(query)
        if car is None:
            raise CarGettingError(f'Car with number {car_number} does not exist', 404)
        return CarSchema.model_validate(car)

    async def get_all(self) -> list[CarSchema]:
        query = select(Car)
        cars = await self._session.execute(query)
        return [CarSchema.model_validate(car) for car in cars]

    async def create(self, **car_data) -> CarCreatingSchema:
        query = insert(Car).values(**car_data).returning(Car)
        try:
            car = await self._session.scalar(query)
        except IntegrityError as ex:
            raise CarCreationError(f'Cannot create car with number {car_data.get("number")}, err={ex}', status_code=409)
        return CarCreatingSchema.model_validate(car)

    async def upgrade(self, car_number: str, **car_data) -> CarSchema:
        query = update(Car).filter(Car.number == car_number).values(**car_data).returning(Car)
        try:
            car = await self._session.scalar(query)
        except IntegrityError as ex:
            raise CarUpdateError(f'Cannot update car with number {car_data.get("number")}, err={ex}', status_code=409)
        return CarSchema.model_validate(car)

    async def remove(self, car_number: str):
        query = delete(Car).where(Car.number == car_number)
        await self._session.scalar(query)
