from fastapi import FastAPI

from src.app.api.rest.routers import add_rest_routers


def init_routers(app: FastAPI) -> None:
    add_rest_routers(app)
