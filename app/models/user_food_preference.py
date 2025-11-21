"""Model UserFoodPreference definition"""

from uuid import uuid4

from sqlalchemy import Column, Enum, ForeignKey, String
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.models.common import UserFoodPreferenceType


class UserFoodPreference(BaseModel):  # pylint: disable=too-few-public-methods
    """Model for user food preferences"""

    __tablename__ = "user_food_preferences"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    food_id = Column(String, ForeignKey("foods.id"), nullable=False)
    preference_type = Column(Enum(UserFoodPreferenceType), nullable=False)

    user = relationship("User", back_populates="food_preferences")
    food = relationship("Food", back_populates="user_preferences")
