import math

from src.db.models import Incident
from src.dispatcher import Dispatcher
from src.schemas.incident import (
    RequestIncidentSchema,
    PaginatedIncidentSchema,
    UpdateIncidentSchema,
)
from src.utils.enums import IncidentStatus


class IncidentService:
    @classmethod
    async def get_incidents_by_status(
        cls,
        dispatcher: Dispatcher,
        page: int,
        size: int,
        status: IncidentStatus,
    ) -> PaginatedIncidentSchema:
        skip = (page - 1) * size
        async with dispatcher.transaction() as dispatcher:
            values, total = await dispatcher.incident.get_incidents_by_status(skip, size, status)
            total_pages = math.ceil(total / size)
            return PaginatedIncidentSchema(values=values, total_pages=total_pages)

    @classmethod
    async def create_incident(
        cls,
        dispatcher: Dispatcher,
        incident_schema: RequestIncidentSchema, 
    ) -> Incident | None:
        dict_data = incident_schema.model_dump()
        async with dispatcher.transaction() as dispatcher:
            incident = await dispatcher.incident.add(dict_data)
            return incident
    
    @classmethod
    async def update_incident_by_id(
        cls,
        dispatcher: Dispatcher,
        id: int,
        incident_schema: UpdateIncidentSchema,
    ) -> Incident | None:
        dict_data = incident_schema.model_dump(exclude_unset=True)
        async with dispatcher.transaction() as dispatcher:
            incident = await dispatcher.incident.update_by_id(id, dict_data)
            return incident
