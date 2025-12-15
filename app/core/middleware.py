"""Custom middleware"""

import logging
import time

from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.firebase import FirebaseAuth

logger = logging.getLogger(__name__)


async def log_requests_middleware(request: Request, call_next):
    """Log all incoming requests and their processing time"""
    start_time = time.time()

    # Log request
    logger.info("Incoming request: %s %s", request.method, request.url.path)

    # Process request
    response = await call_next(request)

    # Calculate processing time
    process_time = time.time() - start_time

    # Log response
    logger.info(
        "Completed %s %s - Status: %s - Duration: %.3fs",
        request.method,
        request.url.path,
        response.status_code,
        process_time,
    )

    # Add custom header
    response.headers["X-Process-Time"] = str(process_time)

    return response


async def firebase_auth_middleware(request: Request, call_next):
    """
    Middleware to verify Firebase authentication token for protected routes

    Public routes (defined in settings.PUBLIC_ROUTES) are exempted from authentication
    """
    # Check if the route is public
    path = request.url.path

    # Check if path is in public routes
    is_public = any(path.startswith(public_route) for public_route in settings.PUBLIC_ROUTES)

    if is_public:
        # Skip authentication for public routes
        return await call_next(request)

    # For protected routes, check for Authorization header
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return JSONResponse(
            status_code=401,
            content={
                "detail": "Missing authentication token",
                "error": "unauthorized"
            },
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Extract token from "Bearer <token>"
    try:
        scheme, token = auth_header.split()
        if scheme.lower() != "bearer":
            return JSONResponse(
                status_code=401,
                content={
                    "detail": "Invalid authentication scheme. Expected Bearer token",
                    "error": "unauthorized"
                },
                headers={"WWW-Authenticate": "Bearer"},
            )
    except ValueError:
        return JSONResponse(
            status_code=401,
            content={
                "detail": "Invalid authorization header format",
                "error": "unauthorized"
            },
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify token
    try:
        decoded_token = await FirebaseAuth.verify_token(token)
        # Store decoded token in request state for later use
        request.state.firebase_token = decoded_token
        request.state.firebase_uid = decoded_token.get("uid")
    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error("Token verification failed in middleware: %s", str(e))
        return JSONResponse(
            status_code=401,
            content={
                "detail": "Invalid or expired authentication token",
                "error": "unauthorized"
            },
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Proceed with the request
    response = await call_next(request)
    return response
