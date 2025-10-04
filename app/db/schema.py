"""SQLAlchemy ORM schema definitions and database engine setup."""

from sqlalchemy import String, Text, create_engine, DateTime, func
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
    """Prompt table schema for AI prompt catalog."""
    __tablename__ = "prompts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    content: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())