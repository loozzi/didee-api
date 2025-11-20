"""Plan model definition"""

from uuid import uuid4

from sqlalchemy import Boolean, Column, Enum, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.models.common import BillingCycle, PlanType


class Plan(BaseModel):  # pylint: disable=too-few-public-methods
    """Plan database model"""

    __tablename__ = "plans"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Integer, nullable=False)
    credit = Column(Integer, nullable=False)
    type = Column(Enum(PlanType), nullable=False)
    billing_cycle = Column(Enum(BillingCycle), nullable=False)
    is_active = Column(Boolean, default=True)

    subscriptions = relationship("Subscription", back_populates="plan")
    subscriptions = relationship("Subscription", back_populates="plan")
    subscriptions = relationship("Subscription", back_populates="plan")
