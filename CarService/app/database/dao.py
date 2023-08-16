from abc import ABC, abstractmethod

from databases import Database
from databases.backends.postgres import Record
from sqlalchemy import delete, insert, select, update

from app.database.models import Brand, Car, Category, Color, FuelType, Transmission


class BaseDAO(ABC):
    @property
    @abstractmethod
    def model(self):
        pass

    @classmethod
    async def get(cls, id_: int, db: Database) -> Record:
        query = select([cls.model]).where(cls.model.id == id_)
        return await db.fetch_one(query)

    @classmethod
    async def get_all(cls, db: Database) -> list[Record]:
        query = select([cls.model])
        return await db.fetch_all(query)

    @classmethod
    async def create(cls, data: dict, db: Database):
        query = insert(cls.model).values(**data)
        await db.execute(query)

    @classmethod
    async def update(cls, data: dict, condition: bool, db: Database):
        query = update(cls.model).where(condition).values(**data)
        await db.execute(query)

    @classmethod
    async def delete(cls, condition: bool, db: Database):
        query = delete(cls.model).where(condition)
        await db.execute(query)


class CarDAO(BaseDAO):
    model = Car


class BrandDAO(BaseDAO):
    model = Brand


class TransmissionDAO(BrandDAO):
    model = Transmission


class ColorDAO(BaseDAO):
    model = Color


class FuelTypeDAO(BaseDAO):
    model = FuelType


class CategoryDAO(BaseDAO):
    model = Category
