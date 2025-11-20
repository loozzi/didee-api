"""Location database model"""

from uuid import uuid4

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Location(BaseModel):  # pylint: disable=too-few-public-methods
    """Location database model"""

    __tablename__ = "locations"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    name = Column(String, nullable=False)
    image = Column(String, nullable=True)
    description = Column(String, nullable=True)
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    order = Column(Integer, nullable=False, default=0)
    slug = Column(String, unique=True, index=True, nullable=False)

    food_locations = relationship(
        "FoodLocation", back_populates="location", cascade="all, delete-orphan"
    )
    foods = relationship("Food", secondary="food_locations", viewonly=True)
