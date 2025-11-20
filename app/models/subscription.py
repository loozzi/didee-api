"""Subscription model definition"""

from uuid import uuid4

from sqlalchemy import Column, String, Boolean, ForeignKey, Enum, DateTime, Integer
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.models.common import SubscriptionStatus

class Subscription(BaseModel):  # pylint: disable=too-few-public-methods
    """Subscription database model"""

    __tablename__ = "subscriptions"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    plan_id = Column(String, ForeignKey("plans.id"), nullable=False)
    status = Column(Enum(SubscriptionStatus), nullable=False, default=SubscriptionStatus.PENDING)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    auto_renew = Column(Boolean, default=True, nullable=False)
    credit_remain = Column(Integer, default=0, nullable=False)

    user = relationship("User", back_populates="subscriptions")
    plan = relationship("Plan", back_populates="subscriptions")
