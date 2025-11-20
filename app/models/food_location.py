"""FoodLocation database model"""

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import BaseModel

class FoodLocation(BaseModel):  # pylint: disable=too-few-public-methods
    """FoodLocation database model"""

    __tablename__ = "food_locations"

    food_id = Column(String, ForeignKey("foods.id"), primary_key=True, nullable=False)
    location_id = Column(String, ForeignKey("locations.id"), primary_key=True, nullable=False)

    food = relationship("Food", back_populates="food_locations")
    location = relationship("Location", back_populates="food_locations")
