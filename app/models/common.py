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
