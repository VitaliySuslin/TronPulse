from fastapi import FastAPI

from src.app.api.urls import init_routers
from src.app.config import settings
from src.app.extensions.sqlalchemy import PoolConnector
from src.app.middlewares.init_middlewares import add_middlewares


def create_app() -> FastAPI:
    app = FastAPI(
        title=f"{settings.NAME} API V1",
        debug=settings.DEBUG,
        docs_url=f"{settings.API_PATH_PREF}/docs",
        redoc_url=f"{settings.API_PATH_PREF}/redoc",
        openapi_url=f"{settings.API_PATH_PREF}/openapi.json",
    )

    add_middlewares(app)
    init_routers(app)
    PoolConnector()

    return app

app = create_app()
