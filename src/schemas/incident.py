from pydantic import BaseModel

from src.schemas.base import BasePagination, TimestampSchema, UpdateBaseModel
from src.utils.enums import IncidentSource, IncidentStatus


class BaseIncident(BaseModel):
    description: str
    source: IncidentSource
    status: IncidentStatus


class ResponseIncidentSchema(BaseIncident, TimestampSchema):
    id: int


class RequestIncidentSchema(BaseIncident):
    pass


class UpdateIncidentSchema(UpdateBaseModel):
    description: str | None = None
    source: IncidentSource | None = None
    status: IncidentStatus | None = None


class PaginatedIncidentSchema(BasePagination[ResponseIncidentSchema]):
    pass
