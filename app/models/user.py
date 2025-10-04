"""Pydantic models for user API requests and responses."""

from pydantic import BaseModel


class UserCreate(BaseModel):
    """Model for creating a user."""
    name: str


class UserRead(BaseModel):
    """Model for reading user data."""
    id: int
    name: str