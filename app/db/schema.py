"""SQLAlchemy ORM schema definitions and database engine setup."""

import sqlalchemy
from sqlalchemy import String, Text, create_engine, DateTime, func, Boolean, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from app.core.config import config

if config.db_url.startswith("sqlite"):
    engine = create_engine(config.db_url, connect_args={"check_same_thread": False})
else:
    engine = create_engine(config.db_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""
    pass


class User(Base):
    """User table schema."""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, index=True)


class Prompt(Base):
    """Prompt table schema for AI prompt catalog with versioning support."""
    __tablename__ = "prompts"

    id: Mapped[int] = mapped_column(primary_key=True)
    app_id: Mapped[str] = mapped_column(String(100), nullable=False)
    prompt_key: Mapped[str] = mapped_column(String(100), nullable=False)
    prompt_text: Mapped[str] = mapped_column(Text, nullable=False)
    version: Mapped[int] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_by: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    
    # Define unique constraints
    __table_args__ = (
        # Ensure version uniqueness for each (app_id, prompt_key) combination
        sqlalchemy.UniqueConstraint('app_id', 'prompt_key', 'version', name='uq_prompt_version'),
        
        # Create a partial index to ensure only one active version per prompt key
        sqlalchemy.Index('ix_active_prompt', 'app_id', 'prompt_key', 
                        unique=True, 
                        postgresql_where=sqlalchemy.text('is_active = true')),
    )