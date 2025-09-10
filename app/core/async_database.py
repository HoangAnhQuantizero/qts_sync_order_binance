from sqlalchemy import QueuePool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

# Convert sync URL to async URL for asyncpg
async_database_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Create async engine with high-performance connection pooling
async_engine = create_async_engine(
    async_database_url,
    echo=False,
    connect_args={
        "statement_cache_size": 0,
        "server_settings": {
            "jit": "off",  # Disable JIT for better performance with small queries
            "application_name": "qts_worker_sync_order",
            "tcp_keepalives_idle": "600",
            "tcp_keepalives_interval": "30",
            "tcp_keepalives_count": "3"
        }
    },
    poolclass=QueuePool,
    pool_size=50,  # Increased pool size for high throughput
    max_overflow=100,  # More overflow connections
    pool_pre_ping=False,  # Disable pre-ping for speed
    pool_recycle=1800,  # Recycle connections every 30 minutes
    pool_timeout=10,  # Faster timeout
    # Additional performance settings
    pool_reset_on_return="commit"
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()

async def get_async_db():
    """Async dependency to get database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close() 