from contextlib import asynccontextmanager
from typing import AsyncIterator, Optional, Type

from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.src.app.config import settings


Base = declarative_base()

class InitPool:
    engine: AsyncEngine

    def __init__(self) -> None:
        self.uri: str = 'postgresql+asyncpg://{login}:{password}@{host}:{port}/{db}'.format(
            login=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            db=settings.POSTGRES_DB,
        )

    def create_pool(self, pool_size: int = 10) -> sessionmaker:
        self.engine = create_async_engine(
            url=make_url(self.uri),
            echo=settings.POSTGRES_ECHO,
            pool_size=3,
            max_overflow=pool_size,
            pool_pre_ping=True
        )
        return sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)


init_pool = InitPool()
async_session: sessionmaker = init_pool.create_pool()


class PoolConnector:
    _instance: Optional['PoolConnector'] = None

    def __new__(cls: Type['PoolConnector']) -> 'PoolConnector':
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self.async_session: sessionmaker = init_pool.create_pool()

    @classmethod
    async def get_session(cls) -> AsyncIterator[AsyncSession]:
        """
        Get a session to the database.

        :return: AsyncSession
        """
        async with cls.async_session() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    @classmethod
    @asynccontextmanager
    async def session(cls) -> AsyncIterator[AsyncSession]:
        async with cls.async_session() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()