"""FoodPreference database model"""

from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import BaseModel  # noqa  # pylint: disable=unused-import
from app.models.common import AvailableTime


class FoodPreference(BaseModel):  # pylint: disable=too-few-public-methods
    """FoodPreference database model"""

    __tablename__ = "food_preferences"

    food_id = Column(String, ForeignKey("foods.id"), primary_key=True)
    price_min = Column(Integer, nullable=False)
    price_max = Column(Integer, nullable=False)
    calorie = Column(Integer, nullable=False)
    tags = Column(String, nullable=False, default="[]")  # Comma-separated tags
    spicy_level = Column(Integer, nullable=False, default=0)  # 0-10 scale
    restaurant = Column(Boolean, nullable=False, default=False)
    available_time = Column(
        Enum(AvailableTime), nullable=False, default=AvailableTime.ALLDAY
    )
    food = relationship("Food", back_populates="preference")
