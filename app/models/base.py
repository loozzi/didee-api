"""Base model classes with common fields"""

from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func

from app.db.base import Base  # noqa: F401


class TimestampMixin:  # pylint: disable=too-few-public-methods
    """Mixin to add created_at and updated_at timestamps to models"""

    created_at = Column(DateTime(timezone=True), server_default=func.now())  # pylint: disable=not-callable
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),  # pylint: disable=not-callable
        onupdate=func.now(),  # pylint: disable=not-callable
    )


class BaseModel(Base, TimestampMixin):  # pylint: disable=too-few-public-methods
    """Base model class with timestamps"""

    __abstract__ = True
