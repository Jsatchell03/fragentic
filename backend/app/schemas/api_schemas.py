from typing import Optional, Literal, TypeAlias, Annotated
from pydantic import BaseModel, Field, BeforeValidator, HttpUrl
from app.config import settings

DESCRIPTOR_LIMIT = settings.query.descriptor_limit
LIST_QUERY_LIMIT = settings.query.list_query_limit
VECTOR_DIM = settings.openai.dimensions

PopularityLiteral: TypeAlias = Annotated[
    Literal[1, 2, 3, 4, 5],
    BeforeValidator(lambda v: int(v) if isinstance(v, str) else v),
]

# Allowlist: letters, digits, spaces, hyphens, apostrophes only.
# Rejects injection-prone chars like : # $ % { } [ ] @ \ / & and MongoDB operators.
DescriptorStr: TypeAlias = Annotated[
    str,
    Field(
        min_length=1,
        max_length=100,
        pattern=r"^[a-zA-Z0-9 '\-]+$",
    ),
]


class _Query(BaseModel):
    brands: Optional[list[str]] = Field(default=None, max_length=LIST_QUERY_LIMIT)
    rating: Optional[float] = Field(default=None, ge=0, le=5)
    countries: Optional[list[str]] = Field(default=None, max_length=LIST_QUERY_LIMIT)
    popularity: Optional[list[PopularityLiteral]] = Field(default=None, max_length=5)
    excluded_descriptors: Optional[list[DescriptorStr]] = Field(
        default=None, max_length=LIST_QUERY_LIMIT
    )


class VectorQuery(_Query):
    search_vector: list[float] = Field(min_length=VECTOR_DIM, max_length=VECTOR_DIM)


class FragranceQuery(_Query):
    fragrance_id: str


class DescriptorQuery(_Query):
    descriptors: list[DescriptorStr] = Field(default_factory=list, max_length=DESCRIPTOR_LIMIT)


class FragranceResponse(BaseModel):
    name: str
    rating: float
    brand: str
    gender: str
    top_notes: list[str]
    mid_notes: list[str]
    base_notes: list[str]
    accords: list[str]
    score: float


class SearchResults(BaseModel):
    fragrances: list[FragranceResponse]
    search_vector: list[float] = Field(min_length=VECTOR_DIM, max_length=VECTOR_DIM)
