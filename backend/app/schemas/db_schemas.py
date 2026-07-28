from typing import Optional, Literal
from pydantic import BaseModel, Field, ConfigDict, field_validator, HttpUrl

VECTOR_DIM = 512
MAX_STRING_LEN = 500  # generous ceiling for names/urls/notes
MAX_NOTES_PER_LAYER = 20  # sanity cap on note-list sizes
MAX_ACCORDS = 20


def _check_bson_safe_string(v: str, field_name: str) -> str:
    """Reject characters/patterns that break BSON encoding or Mongo field semantics."""
    if not isinstance(v, str):
        raise ValueError(f"{field_name} must be a string")

    # Null bytes are illegal in BSON strings and will raise on insert
    if "\x00" in v:
        raise ValueError(
            f"{field_name} contains a null byte, which is not valid in BSON"
        )

    # Guard against accidental operator injection if this value is ever
    # used as a dict key or interpolated into a query
    if v.startswith("$"):
        raise ValueError(
            f"{field_name} cannot start with '$' (reserved for Mongo operators)"
        )

    if len(v) > MAX_STRING_LEN:
        raise ValueError(
            f"{field_name} exceeds max length of {MAX_STRING_LEN} characters"
        )

    return v


class FragranceDoc(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str
    fragrantica_url: HttpUrl
    rating: float = Field(ge=0, le=5)
    rating_count: int = Field(ge=0, le=1_000_000)
    year: Optional[int] = Field(default=None, ge=1700, le=2100)
    brand: str
    gender: Literal["men", "women", "unisex"]
    country: Optional[str] = None
    popularity: Optional[int] = Field(default=None, ge=0)

    top_notes: list[str] = Field(default_factory=list, max_length=MAX_NOTES_PER_LAYER)
    mid_notes: list[str] = Field(default_factory=list, max_length=MAX_NOTES_PER_LAYER)
    base_notes: list[str] = Field(default_factory=list, max_length=MAX_NOTES_PER_LAYER)
    accords: list[str] = Field(default_factory=list, max_length=MAX_ACCORDS)

    top_notes_vector: Optional[list[float]] = None
    mid_notes_vector: Optional[list[float]] = None
    base_notes_vector: Optional[list[float]] = None
    accords_vector: Optional[list[float]] = None
    notes_vector: Optional[list[float]] = None
    fragrance_vector: Optional[list[float]] = None

    # --- string field safety ---

    @field_validator("name", "brand", "country")
    @classmethod
    def validate_plain_strings(cls, v, info):
        if v is None:
            return v
        v = _check_bson_safe_string(v, info.field_name)
        if not v:
            raise ValueError(f"{info.field_name} cannot be empty")
        return v

    @field_validator("top_notes", "mid_notes", "base_notes", "accords")
    @classmethod
    def validate_note_lists(cls, v, info):
        cleaned = []
        for item in v:
            item = _check_bson_safe_string(item, info.field_name)
            if not item:
                raise ValueError(f"{info.field_name} entries cannot be empty strings")
            cleaned.append(item)
        return cleaned

    # --- numeric safety (protect against NaN/Inf, which BSON can't encode safely) ---

    @field_validator("rating")
    @classmethod
    def validate_rating_finite(cls, v):
        if v != v or v in (float("inf"), float("-inf")):  # NaN check + inf check
            raise ValueError("rating must be a finite number")
        return v

    # --- vector safety ---

    @field_validator(
        "top_notes_vector",
        "mid_notes_vector",
        "base_notes_vector",
        "accords_vector",
        "notes_vector",
        "fragrance_vector",
    )
    @classmethod
    def check_vector(cls, v, info):
        if v is None:
            return v
        if len(v) != VECTOR_DIM:
            raise ValueError(
                f"{info.field_name} must have exactly {VECTOR_DIM} dimensions, got {len(v)}"
            )
        for x in v:
            if not isinstance(x, (int, float)):
                raise ValueError(f"{info.field_name} must contain only numeric values")
            if x != x or x in (float("inf"), float("-inf")):
                raise ValueError(
                    f"{info.field_name} contains NaN or Infinity, which BSON cannot encode"
                )
        return v


class DescriptorDoc(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str
    vector: list[float] = Field(min_length=VECTOR_DIM, max_length=VECTOR_DIM)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v, info):
        v = _check_bson_safe_string(v, info.field_name)
        if not v:
            raise ValueError("name cannot be empty")
        return v

    @field_validator("vector")
    @classmethod
    def validate_vector(cls, v):
        for x in v:
            if not isinstance(x, (int, float)):
                raise ValueError("vector must contain only numeric values")
            if x != x or x in (float("inf"), float("-inf")):
                raise ValueError(
                    "vector contains NaN or Infinity, which BSON cannot encode"
                )
        return v
