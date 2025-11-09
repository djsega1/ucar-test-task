from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    def __init__(
        self, 
        session: AsyncSession
    ) -> None:
        self._session = session

    @abstractmethod
    async def add(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: int):
        raise NotImplementedError

    @abstractmethod
    async def get_range(self):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self):
        raise NotImplementedError

    @abstractmethod
    async def update_by_id(self, id: int, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(self, id: int):
        raise NotImplementedError
