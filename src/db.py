from collections.abc import AsyncGenerator
import uuid

from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime

# SQLite database used by the app
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Base class for all SQLAlchemy models
class Base(DeclarativeBase):
    pass

# Database model for a post
class Post(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # Unique post ID
    caption = Column(Text)  # Optional post caption
    url = Column(String, nullable=False)  # File URL stored in the database
    file_type = Column(String, nullable=False)  # Type of uploaded file
    file_name = Column(String, nullable=False)  # Original file name
    created_at = Column(DateTime, default=datetime.utcnow)  # Time the post was created

# Async database engine
engine = create_async_engine(DATABASE_URL)

# Creates async sessions for database operations
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

# Creates tables if they do not exist
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # Create all model tables

# Dependency that gives a database session to routes
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session