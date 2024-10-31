import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from bot.database.models import Base
from bot.settings import Settings

settings = Settings()

engine = create_async_engine(settings.DB_LITE)

session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)