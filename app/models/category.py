from uuid import uuid4

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class Category(BaseModel):
    __tablename__ = "categories"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    slug = Column(String, unique=True, index=True, nullable=False)

    category_foods = relationship(
        "CategoryFood", back_populates="category", cascade="all, delete-orphan"
    )
    foods = relationship("Food", secondary="category_foods", viewonly=True)
