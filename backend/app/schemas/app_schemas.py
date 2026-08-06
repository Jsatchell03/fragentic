from typing import Optional, Literal
import numpy as np
from pydantic import BaseModel, Field, ConfigDict, PrivateAttr, model_validator
from app.config import settings

VECTOR_DIM = settings.openai.dimensions


class Descriptor(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str
    list_vector: list[float] = Field(min_length=VECTOR_DIM, max_length=VECTOR_DIM)

    _np_vector: np.ndarray = PrivateAttr(default=None)

    @model_validator(mode="after")
    def _build_np_vector(self) -> "Descriptor":
        self._np_vector = np.asarray(self.list_vector, dtype=np.float32)
        return self

    @property
    def np_vector(self) -> np.ndarray:
        return self._np_vector


class Fragrance(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str
    list_vector: list[float] = Field(min_length=VECTOR_DIM, max_length=VECTOR_DIM)

    _np_vector: np.ndarray = PrivateAttr(default=None)

    @model_validator(mode="after")
    def _build_np_vector(self) -> "Descriptor":
        self._np_vector = np.asarray(self.list_vector, dtype=np.float32)
        return self

    @property
    def np_vector(self) -> np.ndarray:
        return self._np_vector
