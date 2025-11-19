"""Exception handlers for the application"""

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError


async def integrity_error_handler(
    request: Request, exc: IntegrityError
) -> JSONResponse:
    """Handle database integrity errors"""
    error_msg = str(exc.orig)

    # Parse common integrity errors
    if "unique constraint" in error_msg.lower() or "duplicate" in error_msg.lower():
        detail = "A record with this value already exists"
        if "email" in error_msg.lower():
            detail = "Email already registered"
        elif "username" in error_msg.lower():
            detail = "Username already taken"

        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"success": False, "message": detail, "data": None},
        )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"success": False, "message": "Database error occurred", "data": None},
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.detail, "data": None},
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle all other exceptions"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "An unexpected error occurred",
            "data": None,
        },
    )
