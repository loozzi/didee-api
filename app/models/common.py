"""Common model enums and utilities"""

from enum import Enum


class UserProvider(str, Enum):
    """User authentication provider types"""

    EMAIL = "email"
    GOOGLE = "google"
    FACEBOOK = "facebook"


class AvailableTime(str, Enum):
    """Available time slots for scheduling"""

    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    NIGHT = "night"
    ALLDAY = "all_day"


class PlanType(str, Enum):
    """Types of subscription plans"""

    FREE = "free"
    CREDIT = "credit"
    SUBSCRIPTION = "subscription"


class BillingCycle(str, Enum):
    """Billing cycle options for subscription plans"""

    MONTHLY = "monthly"
    YEARLY = "yearly"


class SubscriptionStatus(str, Enum):
    """Subscription status options"""

    ACTIVE = "active"
    INACTIVE = "inactive"
    CANCELED = "canceled"
    PENDING = "pending"


class UserFoodPreferenceType(str, Enum):
    """Types of user food preferences"""

    LIKE = "like"
    DISLIKE = "dislike"
    ALLERGY = "allergy"
