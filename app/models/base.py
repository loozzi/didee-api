from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func

from app.db.base import Base  # noqa: F401


class TimestampMixin:
    """Mixin to add created_at and updated_at timestamps to models"""

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class BaseModel(Base, TimestampMixin):
    __abstract__ = True
