"""Database base import for Alembic migrations"""

# pylint: disable=cyclic-import

# Import all models here for Alembic to detect them
from app.db.session import Base
from app.models.category import Category
from app.models.category_food import CategoryFood
from app.models.food import Food
from app.models.food_location import FoodLocation
from app.models.food_preference import FoodPreference
from app.models.location import Location
from app.models.plan import Plan
from app.models.subscription import Subscription
from app.models.user import User
from app.models.user_food_preference import UserFoodPreference

# Add other models here as you create them
__all__ = [
    "Base",
    "Category",
    "CategoryFood",
    "Food",
    "FoodLocation",
    "FoodPreference",
    "Location",
    "Plan",
    "Subscription",
    "User",
    "UserFoodPreference",
]
