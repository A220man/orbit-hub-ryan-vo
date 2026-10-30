
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import engine, Base, async_session_maker
from app.main import app


@pytest_asyncio.fixture(scope="session", autouse=True)
async def init_test_db():
    """Initialize test database before running tests."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session() -> AsyncSession:
    """Create a new database session for each test."""
    async with async_session_maker() as session:
        yield session
        await session.rollback()
