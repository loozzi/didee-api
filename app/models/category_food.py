from sqlalchemy import Column, ForeignKey, PrimaryKeyConstraint, String
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class CategoryFood(BaseModel):
    __tablename__ = "category_foods"

    category_id = Column(String, ForeignKey("categories.id"), nullable=False)
    food_id = Column(String, ForeignKey("foods.id"), nullable=False)

    category = relationship("Category", back_populates="category_foods")
    food = relationship("Food", back_populates="category_foods")

    __table_args__ = (PrimaryKeyConstraint("category_id", "food_id"),)
