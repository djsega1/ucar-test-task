from typing import Generic, Type, TypeVar, Tuple, Sequence, cast, Union

from sqlalchemy import delete, func, insert, select, update, Delete, Update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Base
from src.repositories.abstract import AbstractRepository

Model = TypeVar('Model', bound=Base)


class SQLAlchemyRepository(AbstractRepository, Generic[Model]):
    model: Type[Model]

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def add(self, data: dict) -> Model | None:
        stmt = insert(self.model).values(**data).returning(self.model)
        result = await self._session.scalar(stmt)
        return result

    async def get_by_id(self, id: int) -> Model | None:
        stmt = select(self.model).where(self.model.id == id)
        if hasattr(self.model, "is_active"):
            stmt = stmt.where(self.model.is_active)
        result = await self._session.scalar(stmt)
        return result

    async def get_range(self, skip: int = 0, limit: int = 10) -> Tuple[Sequence[Model], int]:
        count_stmt = select(func.count(self.model.id))
        values_stmt = select(self.model).offset(skip).limit(limit)
        if hasattr(self.model, "is_active"):
            values_stmt = values_stmt.where(self.model.is_active)
            count_stmt = count_stmt.where(self.model.is_active)
        values = (await self._session.scalars(values_stmt)).all()
        count = await self._session.scalar(count_stmt)
        return values, cast(int, count)

    async def get_all(self) -> Sequence[Model]:
        stmt = select(self.model)
        if hasattr(self.model, "is_active"):
            stmt = stmt.where(self.model.is_active)
        result = (await self._session.scalars(stmt)).all()
        return result

    async def update_by_id(self, id: int, data: dict) -> Model | None:
        stmt = update(self.model).where(self.model.id == id).values(**data).returning(self.model)
        if hasattr(self.model, "is_active"):
            stmt = stmt.where(self.model.is_active)
        result = await self._session.scalar(stmt)
        return result

    async def delete_by_id(self, id: int) -> Model | None:
        stmt: Union[Delete, Update] = delete(self.model)
        if hasattr(self.model, "is_active"):
            stmt = (
                update(self.model)
                .values(is_active=False)
            )
        stmt = stmt.where(self.model.id == id).returning(self.model)
        result = await self._session.scalar(stmt)
        return result
