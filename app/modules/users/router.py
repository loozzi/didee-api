"""User routes"""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.core.firebase import FirebaseAuth
from app.db.session import get_db
from app.models.user import User
from app.modules.users import crud
from app.modules.users.schemas import (
    TokenVerifyRequest,
    TokenVerifyResponse,
    UserCreate,
    UserResponse,
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/verify", response_model=TokenVerifyResponse, status_code=status.HTTP_200_OK)
async def verify_firebase_token(
    request: TokenVerifyRequest,
    db: Session = Depends(get_db),
):
    """
    Verify Firebase token and create user if not exists

    This endpoint:
    - Verifies the Firebase authentication token
    - Creates a new user in the database if the user doesn't exist
    - Returns the user information
    """
    try:
        # Verify Firebase token
        decoded_token = await FirebaseAuth.verify_token(request.firebase_token)

        # Extract user information from token
        user_info = FirebaseAuth.get_user_from_token(decoded_token)
        firebase_uid = user_info["firebase_uid"]

        # Check if user already exists
        existing_user = crud.get_user_by_firebase_uid(db, firebase_uid)

        if existing_user:
            # User exists, return existing user
            return TokenVerifyResponse(
                message="User verified successfully",
                user=UserResponse.model_validate(existing_user),
                is_new_user=False,
            )

        # User doesn't exist, create new user
        user_create = UserCreate(
            firebase_uid=user_info["firebase_uid"],
            email=user_info["email"],
            full_name=user_info.get("full_name"),
            avatar_url=user_info.get("avatar_url"),
            phone_number=user_info.get("phone_number"),
            provider=user_info.get("provider", "EMAIL"),
        )

        new_user = crud.create_user(db, user_create)
        logger.info("Created new user with Firebase UID: %s", firebase_uid)

        return TokenVerifyResponse(
            message="User created successfully",
            user=UserResponse.model_validate(new_user),
            is_new_user=True,
        )

    except HTTPException:
        raise
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error("Error verifying token and creating user: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to verify token and process user",
        ) from e


@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    """
    Get current authenticated user information

    This endpoint requires a valid Firebase authentication token
    Returns the user information from the database
    """
    return UserResponse.model_validate(current_user)
