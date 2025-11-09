from contextlib import asynccontextmanager
import logging
import traceback

from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.incident import IncidentRepository


class Dispatcher:
    def __init__(
        self, 
        session: AsyncSession
    ):
        self._session = session

    @asynccontextmanager
    async def transaction(self):
        try: 
            yield self
            await self._session.commit()
        except Exception as e:
            await self._session.rollback()
            error = ''.join(
                traceback.format_exception(type(e), e, e.__traceback__)
            )
            logging.exception(f"Database operation rolled back: {error}")
        finally:
            await self._session.close()

    @property
    def incident(self) -> IncidentRepository: 
        return IncidentRepository(self._session)
