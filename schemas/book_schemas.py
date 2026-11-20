# schemas/book_schemas.py  -- the shape of data going IN and OUT of the API.
# (Models = database tables. Schemas = what the client sends / receives.)

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    """Body of POST /books"""
    title: str = Field(min_length=1, max_length=150)
    author: str = Field(min_length=1, max_length=100)
    published_year: Optional[int] = Field(default=None, ge=1000, le=2100)


class BookUpdate(BaseModel):
    """Body of PUT /books/{id} -- every field is optional, send only what changes."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=150)
    author: Optional[str] = Field(default=None, min_length=1, max_length=100)
    published_year: Optional[int] = Field(default=None, ge=1000, le=2100)
    is_active: Optional[bool] = None


class BookResponse(BaseModel):
    """What we send back to the client."""
    id: int
    title: str
    author: str
    published_year: Optional[int]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
