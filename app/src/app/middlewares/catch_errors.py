from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


from app.src.app.middlewares.trace.traceback_handler import get_last_trace
from app.src.app.enums.services import BackendServicesNameEnum
from app.src.app.utils.pydantic.error_response import (
    DefaultErrorResponseSchema,
    DetailDefaultErrorResponseSchema,
)


class SendDefaultErrorResponseByExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
        except Exception as err:
            return JSONResponse(
                status_code=500,
                content=DefaultErrorResponseSchema(
                    code=500,
                    message="Ops! This is an error unrecognized by the server =(",
                    detail=DetailDefaultErrorResponseSchema(
                        context={
                            "err": str(err)[:500],
                            "trace": await get_last_trace(),
                        },
                        service=BackendServicesNameEnum.name,
                        description="An unknown error has occurred and we are already rushing to fix it!",
                    ),
                ).model_dump(),
            )
        return response
