"""API v1 router configuration"""

from fastapi import APIRouter

from app.modules.users import router as users_router

api_router = APIRouter()
# Firebase authentication is now handled by middleware and /users/verify endpoint
api_router.include_router(users_router.router, prefix="/users", tags=["users"])
