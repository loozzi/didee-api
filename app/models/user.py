"""User model definition"""

from uuid import uuid4

from sqlalchemy import Column, Enum, String
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.models.common import UserProvider


class User(BaseModel):  # pylint: disable=too-few-public-methods
    """User database model"""

    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, unique=True, index=True, nullable=True)
    provider = Column(Enum(UserProvider), nullable=False, default=UserProvider.EMAIL)

    subscriptions = relationship("Subscription", back_populates="user")
    food_preferences = relationship("UserFoodPreference", back_populates="user")
    recommend_histories = relationship("RecommendHistory", back_populates="user")
