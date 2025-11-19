from uuid import uuid4

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Food(BaseModel):
    __tablename__ = "foods"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    name = Column(String, nullable=False)
    image = Column(String, nullable=True)
    description = Column(String, nullable=True)
    locations = Column(String, nullable=False, default="[]")  # JSON string of locations
    slug = Column(String, unique=True, index=True, nullable=False)

    category_foods = relationship(
        "CategoryFood", back_populates="food", cascade="all, delete-orphan"
    )
    categories = relationship("Category", secondary="category_foods", viewonly=True)
