import uvicorn
from fastapi import FastAPI

from app.src.app.config import settings
from app.src.app.factory import create_app


app: FastAPI = create_app()

if __name__ == '__main__':
    uvicorn.run(
        app='app.src.app.factory.app',
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        log_level="debug" if settings.DEBUG else "info",
        reload=settings.RELOAD,
    )
