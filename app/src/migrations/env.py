import asyncio

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.future import create_engine

from app.src.app.config import settings
from app.src.app.db.orm import *
from app.src.app.extensions.sqlalchemy import Base

config = context.config

uri = 'postgresql+asyncpg://{login}:{password}@{host}:{port}/{db}'.format(
    login=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    host=settings.POSTGRES_HOST,
    port=settings.POSTGRES_PORT,
    db=settings.POSTGRES_DB,
)
config.set_main_option('sqlalchemy.url', uri)

target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    connectable = AsyncEngine(
        create_engine(
            url=config.get_main_option('sqlalchemy.url'),
            poolclass=pool.NullPool,
            future=True,
        ),
    )

    async with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        await connection.run_sync(do_run_migrations)

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())