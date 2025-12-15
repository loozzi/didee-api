"""Food model definition"""

from uuid import uuid4

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Food(BaseModel):  # pylint: disable=too-few-public-methods
    """Food database model"""

    __tablename__ = "foods"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    name = Column(String, nullable=False)
    image = Column(String, nullable=True)
    description = Column(String, nullable=True)
    slug = Column(String, unique=True, index=True, nullable=False)

    preference = relationship("FoodPreference", back_populates="food", uselist=False)
    category_foods = relationship(
        "CategoryFood", back_populates="food", cascade="all, delete-orphan"
    )
    categories = relationship("Category", secondary="category_foods", viewonly=True)
    food_locations = relationship(
        "FoodLocation", back_populates="food", cascade="all, delete-orphan"
    )
    locations = relationship("Location", secondary="food_locations", viewonly=True)
    recommend_histories = relationship(
        "RecommendHistory", back_populates="food", cascade="all, delete-orphan"
    )
    user_preferences = relationship(
        "UserFoodPreference", back_populates="food", cascade="all, delete-orphan"
    )
