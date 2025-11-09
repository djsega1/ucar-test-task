from datetime import datetime
from typing import TypeVar, Generic
from typing_extensions import Self

from pydantic import BaseModel, ConfigDict, model_validator

T = TypeVar('T', bound=BaseModel)


class TimestampSchema(BaseModel):
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class BasePagination(BaseModel, Generic[T]):
    values: list[T]
    total_pages: int


class UpdateBaseModel(BaseModel):
    @model_validator(mode="after")
    def check_for_any(self) -> Self:
        if not any(self.model_dump().values()):
            raise ValueError("At least one field must present")
        return self
