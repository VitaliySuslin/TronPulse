from fastapi import FastAPI

from src.app.api.rest.views import health
from src.app.api.rest.views import wallet


def add_rest_routers(app: FastAPI) -> None:
    app.include_router(health.router, prefix='')
    app.include_router(wallet.router, prefix='')
