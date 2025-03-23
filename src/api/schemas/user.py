"""User module."""

from pydantic import BaseModel


class User(BaseModel):
    """User model."""

    username: str
    password: str
