# Import all models here for Alembic to detect them
from app.db.session import Base  # noqa
from app.models.category import Category  # noqa
from app.models.category_food import CategoryFood  # noqa
from app.models.food import Food  # noqa
from app.models.user import User  # noqa

# Add other models here as you create them
__all__ = ["Category", "CategoryFood", "Food", "User"]
