from typing import Optional, Literal
from pydantic import BaseModel, Field, ConfigDict, field_validator, HttpUrl
from app.config import settings


class SearchResults:
    pass


class FragranceResponse(BaseModel):
    name: str
    rating: float
    brand: str
    gender: str
    descriptors: list[str]
    score: float
