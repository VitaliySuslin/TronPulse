from fastapi import APIRouter
from sqlalchemy import text

from app.src.app.api.rest.schemas.responses.health import HealthSchema
from app.src.app.config import settings
from app.src.app.enums.tools import HealthStatusType
from app.src.app.extensions.logging import logger
from app.src.app.extensions.sqlalchemy import PoolConnector


router = APIRouter(
    tags=["The Tool Box"],
    prefix=settings.API_PATH_PREF
)

class HealthController:
    @classmethod
    async def _connect_sql(cls) -> None:
        async with PoolConnector.session() as session:
            await session.execute(text("SELECT 1"))

    @classmethod
    async def _check_sql(cls, health: HealthSchema) -> None:
        try:
            await cls._connect_sql()
        except Exception as exc:
            health.sql_status = HealthStatusType.error
            logger.error(f"SQL health error: {exc}")
        else:
            health.sql_status = HealthStatusType.ok

    @classmethod
    async def create(cls) -> HealthSchema:
        health = HealthSchema()
        await cls._check_sql(health)
        return health


@router.get(
    "/tools/health",
    response_model_exclude_none=True,
    response_model=HealthSchema,
)
async def health_check() -> HealthSchema:
    return await HealthController.create()


@router.get(
    "/tools/error-response",
    response_model_exclude_none=True,
    response_model=HealthSchema,
)
async def error_response() -> None:
    1 / 0 