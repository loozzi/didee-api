from fastapi import APIRouter

from app.modules.auth import router as auth_router
from app.modules.users import router as users_router

api_router = APIRouter()
api_router.include_router(auth_router.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users_router.router, prefix="/users", tags=["users"])
