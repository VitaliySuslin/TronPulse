from fastapi import FastAPI

from app.src.app.api.rest.views import health


def add_rest_routers(app: FastAPI) -> None:
    app.include_router(health.router, prefix='')
