from contextlib import asynccontextmanager

from alembic.command import upgrade
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import get_settings
from app.core.database import get_alembic_config


@asynccontextmanager
async def lifespan(app: FastAPI):
    alembic_config = get_alembic_config(get_settings().DATABASE_URL)
    upgrade(alembic_config, 'head')
    yield


def create_app() -> FastAPI:
    application = FastAPI(
        title=get_settings().PROJECT_NAME,
        version='0.1.0',
        lifespan=lifespan,
    )
    application.include_router(router)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    return application


app = create_app()
