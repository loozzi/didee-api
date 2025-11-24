"""Firebase authentication utilities"""

import logging
import os

import firebase_admin
from firebase_admin import auth, credentials
from fastapi import HTTPException, status

from app.core.config import settings

logger = logging.getLogger(__name__)


class FirebaseAuth:
    """Firebase authentication handler"""

    _initialized = False

    @classmethod
    def initialize(cls):
        """Initialize Firebase Admin SDK"""
        if cls._initialized:
            return

        try:
            # Check if Firebase credentials path is set
            if not settings.FIREBASE_CREDENTIALS_PATH:
                logger.warning(
                    "FIREBASE_CREDENTIALS_PATH not set. Firebase authentication will not work."
                )
                return

            # Check if credentials file exists
            if not os.path.exists(settings.FIREBASE_CREDENTIALS_PATH):
                logger.warning(
                    "Firebase credentials file not found at: %s",
                    settings.FIREBASE_CREDENTIALS_PATH,
                )
                return

            # Initialize Firebase Admin SDK
            cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)
            cls._initialized = True
            logger.info("Firebase Admin SDK initialized successfully")

        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Failed to initialize Firebase Admin SDK: %s", str(e))

    @classmethod
    async def verify_token(cls, token: str) -> dict:
        """
        Verify Firebase ID token and return decoded token data

        Args:
            token: Firebase ID token

        Returns:
            dict: Decoded token containing user information

        Raises:
            HTTPException: If token is invalid or verification fails
        """
        if not cls._initialized:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Firebase authentication is not configured",
            )

        try:
            # Verify the token
            decoded_token = auth.verify_id_token(token)
            return decoded_token

        except auth.ExpiredIdTokenError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            ) from exc
        except auth.RevokedIdTokenError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication token has been revoked",
                headers={"WWW-Authenticate": "Bearer"},
            ) from exc
        except auth.InvalidIdTokenError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
                headers={"WWW-Authenticate": "Bearer"},
            ) from exc
        except auth.CertificateFetchError as exc:
            logger.error("Failed to fetch Firebase certificates")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Authentication service temporarily unavailable",
            ) from exc
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("Token verification failed: %s", str(e))
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
                headers={"WWW-Authenticate": "Bearer"},
            ) from e

    @classmethod
    def get_user_from_token(cls, decoded_token: dict) -> dict:
        """
        Extract user information from decoded token

        Args:
            decoded_token: Decoded Firebase token

        Returns:
            dict: User information including uid, email, name, etc.
        """
        return {
            "firebase_uid": decoded_token.get("uid"),
            "email": decoded_token.get("email"),
            "email_verified": decoded_token.get("email_verified", False),
            "full_name": decoded_token.get("name"),
            "avatar_url": decoded_token.get("picture"),
            "phone_number": decoded_token.get("phone_number"),
            "provider": cls._get_provider(decoded_token),
        }

    @classmethod
    def _get_provider(cls, decoded_token: dict) -> str:
        """Determine the authentication provider from token"""
        firebase_info = decoded_token.get("firebase", {})
        sign_in_provider = firebase_info.get("sign_in_provider", "")

        if "google.com" in sign_in_provider:
            return "GOOGLE"
        if "facebook.com" in sign_in_provider:
            return "FACEBOOK"
        if "apple.com" in sign_in_provider:
            return "APPLE"
        if "password" in sign_in_provider:
            return "EMAIL"
        return "EMAIL"  # Default to EMAIL


# Initialize Firebase on module load
FirebaseAuth.initialize()
