from typing import Tuple, Sequence, cast

from sqlalchemy import select, func

from src.db.models import Incident
from src.repositories.base import SQLAlchemyRepository
from src.utils.enums import IncidentStatus


class IncidentRepository(SQLAlchemyRepository[Incident]):
    model = Incident

    async def get_incidents_by_status(
        self,
        skip: int = 0,
        limit: int = 10,
        status: IncidentStatus = IncidentStatus.NEW,
    ) -> Tuple[Sequence[Incident], int]:
        stmt = (
            select(self.model)
            .where(self.model.status == status)
            .where(self.model.is_active)
        )
        values_stmt = stmt.offset(skip).limit(limit)
        count_stmt = select(func.count()).select_from(stmt.subquery())
        values = (await self._session.scalars(values_stmt)).all()
        count = await self._session.scalar(count_stmt)
        return values, cast(int, count)
