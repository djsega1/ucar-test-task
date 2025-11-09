from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from src.config import get_settings


class SessionManager:
    def __init__(self) -> None:
        self.refresh()

    def __new__(cls) -> 'SessionManager':
        if not hasattr(cls, "instance"):
            cls.instance = super(SessionManager, cls).__new__(cls)
        return cls.instance

    def refresh(self) -> None:
        settings = get_settings()
        self.engine = create_async_engine(
            settings.database_uri,
            pool_size=settings.DB_POOL_SIZE,
            future=True,
            max_overflow=10,
            pool_pre_ping=True,
            pool_recycle=60,
            connect_args={'timeout': 5},
        )
        self.session_maker = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
            autoflush=False,
            close_resets_only=False,
        )


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    session_manager = SessionManager()
    async with session_manager.session_maker() as session:
        yield session
