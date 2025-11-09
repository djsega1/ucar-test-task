from fastapi import APIRouter, Depends, Query
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.connection import get_session
from src.dispatcher import Dispatcher
from src.services import IncidentService
from src.schemas.incident import (
    ResponseIncidentSchema,
    RequestIncidentSchema,
    PaginatedIncidentSchema,
    UpdateIncidentSchema,
)
from src.utils.enums import IncidentStatus

api_router = APIRouter(prefix="/incidents", tags=["Incidents"])


@api_router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=PaginatedIncidentSchema,
)
async def get_incidents_by_status(
    page: int = Query(default=1),
    size: int = Query(default=4),
    order: IncidentStatus = Query(default=IncidentStatus.NEW),
    session: AsyncSession = Depends(get_session),
):
    dispatcher = Dispatcher(session)
    return await IncidentService.get_incidents_by_status(
        dispatcher, page, size, order
    )


@api_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseIncidentSchema,
)
async def create_incident(
    incident: RequestIncidentSchema,
    session: AsyncSession = Depends(get_session),
):
    dispatcher = Dispatcher(session)
    return await IncidentService.create_incident(
        dispatcher, incident
    )


@api_router.put(
    "/{incident_id}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Incident doesn't exist"},
    },
    response_model=RequestIncidentSchema,
)
async def update_incident_by_id(
    incident_id: int,
    incident_schema: UpdateIncidentSchema,
    session: AsyncSession = Depends(get_session),
):
    dispatcher = Dispatcher(session)
    return await IncidentService.update_incident_by_id(
        dispatcher, incident_id, incident_schema
    )
