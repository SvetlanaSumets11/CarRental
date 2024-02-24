from alembic.command import upgrade
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.api.routes import router
from app.core.config import get_settings
from app.core.database import get_alembic_config


def create_app() -> FastAPI:
    application = FastAPI(
        title=get_settings().PROJECT_NAME,
        root_path=get_settings().ROOT_PATH,
        version='0.1.0',
        openapi_url='/openapi.json',
    )
    application.include_router(router)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    application.add_middleware(SessionMiddleware, secret_key=get_settings().SESSION_SECRET_KEY)

    return application


app = create_app()


@app.on_event('startup')
async def startup():
    alembic_config = get_alembic_config(get_settings().DATABASE_URL)
    upgrade(alembic_config, 'head')
