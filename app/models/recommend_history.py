"""RecommendHistory model definition"""

from uuid import uuid4

from sqlalchemy import Column, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.base import BaseModel


class RecommendHistory(BaseModel):  # pylint: disable=too-few-public-methods
    """RecommendHistory model representing recommendation activity history."""

    __tablename__ = "recommend_histories"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    food_id = Column(String, ForeignKey("foods.id"), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, server_default=func.now())  # pylint: disable=not-callable

    # Relationship to User model (assuming a User model exists)
    user = relationship("User", back_populates="recommend_histories")
    # Relationship to Food model (assuming a Food model exists)
    food = relationship("Food", back_populates="recommend_histories")
