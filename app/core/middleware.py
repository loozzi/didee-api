"""Custom middleware"""

import logging
import time

from fastapi import Request

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
