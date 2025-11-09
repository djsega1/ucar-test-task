import asyncio
import logging

from sqlalchemy import text

from src.db.connection import get_session


class Healthcheck:
    logger = logging.getLogger("Healthcheck")

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Healthcheck, cls).__new__(cls)
        return cls.instance  # noqa
    
    @classmethod
    async def _check_sql_database(cls):
        async for session in get_session():
            cls.logger.info(await session.execute(text("SELECT 1;")))

    @classmethod
    async def check_dependencies(cls):
        try:
            tasks = [
                cls._check_sql_database(),
            ]
            async with asyncio.timeout(5):
                await asyncio.gather(*tasks)
            cls.logger.info("Healthcheck passed!")
        except Exception as exc:
            raise exc
