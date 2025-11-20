"""Database base import for Alembic migrations"""
# pylint: disable=cyclic-import

# Import all models here for Alembic to detect them
from app.db.session import Base
from app.models.category import Category
from app.models.category_food import CategoryFood
from app.models.food import Food
from app.models.food_preference import FoodPreference
from app.models.user import User


# Add other models here as you create them
__all__ = ["Base", "Category", "CategoryFood", "Food", "FoodPreference", "User"]
