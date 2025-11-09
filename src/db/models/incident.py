from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.db.models import Base
from src.utils.enums import IncidentSource, IncidentStatus


class Incident(Base):
    description: Mapped[str] = mapped_column(nullable=False)
    source: Mapped[IncidentSource] = mapped_column(nullable=False)
    status: Mapped[IncidentStatus] = mapped_column(default=IncidentStatus.NEW, nullable=False)
