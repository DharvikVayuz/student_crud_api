# database/database.py  -- the one place that knows how to connect to the database.

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import settings
from models.base import Base

# The engine is the actual connection to the database.
engine = create_async_engine(settings.DATABASE_URL, echo=False)

# A session is one "conversation" with the database (one per request).
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db() -> None:
    """Create all tables. Called once from main.py on startup."""
    # Importing the models makes sure Base knows about every table.
    import models.book_models  # noqa: F401

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency: gives each request its own session, closes it after."""
    async with AsyncSessionLocal() as session:
        yield session
