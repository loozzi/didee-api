"""Firebase authentication dependency"""

import logging
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.firebase import FirebaseAuth
from app.db.session import get_db
from app.models.user import User
from app.modules.users import crud

logger = logging.getLogger(__name__)

security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """
    Dependency to get the current authenticated user from Firebase token

    Args:
        credentials: HTTP Authorization credentials (Bearer token)
        db: Database session

    Returns:
        User: The authenticated user object

    Raises:
        HTTPException: If authentication fails
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    # Verify Firebase token
    decoded_token = await FirebaseAuth.verify_token(token)

    # Get Firebase UID from token
    firebase_uid = decoded_token.get("uid")
    if not firebase_uid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: missing user ID",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get user from database
    user = crud.get_user_by_firebase_uid(db, firebase_uid)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found. Please verify your account first.",
        )

    return user


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db),
) -> Optional[User]:
    """
    Dependency to get the current user if authenticated, otherwise None
    Useful for endpoints that work with or without authentication

    Args:
        credentials: HTTP Authorization credentials (Bearer token)
        db: Database session

    Returns:
        Optional[User]: The authenticated user object or None
    """
    if not credentials:
        return None

    try:
        token = credentials.credentials
        decoded_token = await FirebaseAuth.verify_token(token)
        firebase_uid = decoded_token.get("uid")

        if firebase_uid:
            return crud.get_user_by_firebase_uid(db, firebase_uid)
    except HTTPException:
        # If token is invalid, just return None
        pass

    return None
