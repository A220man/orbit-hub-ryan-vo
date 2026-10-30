
import uuid
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class ModelBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    framework: str = Field(..., min_length=1, max_length=100)
    version: str = Field(..., min_length=1, max_length=50)
    metadata_json: Optional[str] = None


class ModelCreate(ModelBase):
    pass


class ModelUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    framework: Optional[str] = Field(None, min_length=1, max_length=100)
    version: Optional[str] = Field(None, min_length=1, max_length=50)
    metadata_json: Optional[str] = None


class ModelResponse(ModelBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class ModelListResponse(BaseModel):
    items: list[ModelResponse]
    total: int
    page: int
    page_size: int
