"""Common model enums and utilities"""

from enum import Enum


class UserProvider(str, Enum):
    """User authentication provider types"""

    EMAIL = "email"
    GOOGLE = "google"
    FACEBOOK = "facebook"
