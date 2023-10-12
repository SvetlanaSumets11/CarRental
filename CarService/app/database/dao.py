from databases import Database
from databases.backends.postgres import Record
from sqlalchemy import delete, insert, select, update

from app.database.db import Base


async def get_by_id(model: Base, id_: int, db: Database) -> Record:
    query = select(model).where(model.id == id_)
    return await db.fetch_one(query)


async def get_all(model: Base, db: Database) -> list[Record]:
    query = select(model)
    return await db.fetch_all(query)


async def create(model: Base, data: dict, db: Database):
    query = insert(model).values(**data)
    await db.execute(query)


async def upgrade(model: Base, data: dict, condition: bool, db: Database):
    query = update(model).where(condition).values(**data)
    await db.execute(query)


async def remove(model: Base, condition: bool, db: Database):
    query = delete(model).where(condition)
    await db.execute(query)
