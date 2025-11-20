"""Database base import for Alembic migrations"""
# pylint: disable=cyclic-import

# Import all models here for Alembic to detect them
from app.db.session import Base  # noqa  # pylint: disable=unused-import
from app.models.category import Category  # noqa  # pylint: disable=unused-import
from app.models.category_food import CategoryFood  # noqa  # pylint: disable=unused-import
from app.models.food import Food  # noqa  # pylint: disable=unused-import
from app.models.user import User  # noqa  # pylint: disable=unused-import

# Add other models here as you create them
__all__ = ["Base", "Category", "CategoryFood", "Food", "User"]
