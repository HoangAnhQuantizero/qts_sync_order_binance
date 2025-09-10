from contextlib import asynccontextmanager
from typing import AsyncGenerator, AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import text
from .config import settings

# Create Base class for declarative models
Base = declarative_base()

# Convert sync URL to async URL for asyncpg
async_database_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Create async engine for async DB access
async_engine = create_async_engine(
    async_database_url,
    pool_size=20,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=600,
    echo=False,  # Set to False in production
    pool_timeout=30,  # Add timeout
    pool_use_lifo=True,  # Use LIFO for better connection reuse
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)

# FastAPI dependency for request-scoped sessions
async def get_db() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# Context manager for explicit session management
@asynccontextmanager
async def get_db_context() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# For background tasks and workers
async def get_background_session() -> AsyncSession:
    return AsyncSessionLocal()

# Database health check
async def test_connection() -> bool:
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
            return True
    except Exception as e:
        print(f"Database connection error: {e}")
        return False

# Initialize database (create all tables)
async def init_db() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Cleanup database connection
async def close_db() -> None:
    await async_engine.dispose()