"""Application configuration settings"""

from typing import List

from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""

    # Environment
    ENVIRONMENT: str = "development"  # development, staging, production

    # Project
    PROJECT_NAME: str = "FastAPI Application"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = "sqlite:///./app.db"

    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Firebase
    FIREBASE_CREDENTIALS_PATH: str = ""  # Path to Firebase service account JSON file

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # Routes that don't require authentication
    PUBLIC_ROUTES: List[str] = [
        "/",
        "/health",
        "/api/v1/docs",
        "/api/v1/redoc",
        "/api/v1/openapi.json",
        "/api/v1/users/verify",
    ]

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v: str, info) -> str:
        """Validate that SECRET_KEY is changed in production"""
        environment = info.data.get("ENVIRONMENT", "development")
        if (
            v == "your-secret-key-here-change-in-production"
            and environment == "production"
        ):
            raise ValueError("SECRET_KEY must be changed in production!")
        return v

    model_config = {"env_file": ".env", "case_sensitive": True}


settings = Settings()
