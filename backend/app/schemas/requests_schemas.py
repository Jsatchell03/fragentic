from typing import Optional, Literal
from pydantic import BaseModel, Field, ConfigDict, field_validator, HttpUrl
from app.config import settings

DESCRIPTOR_LIMIT = settings.query.descriptor_limit
LIST_QUERY_LIMIT = settings.query.list_query_limit


class _Query(BaseModel):
    brands: Optional[list[str]] = Field(default=None, max_length=LIST_QUERY_LIMIT)
    rating: Optional[float] = Field(default=None, ge=0, le=5)
    countries: Optional[list[str]] = Field(default=None, max_length=LIST_QUERY_LIMIT)
    popularity: Optional[list[Literal[1, 2, 3, 4, 5]]] = Field(
        default=None, max_length=5
    )
    excluded_descriptors: Optional[list[str]] = Field(
        default=None, max_length=LIST_QUERY_LIMIT
    )


class SearchQuery(_Query):
    descriptors: list[str] = Field(default_factory=list, max_length=DESCRIPTOR_LIMIT)


class MatchQuery(_Query):
    fragrance_id: str
