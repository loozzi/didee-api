import inspect
from functools import wraps
from typing import Any, Callable

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse


def response_handler(
    success_message: str = "Operation successful",
    error_message: str = "An error occurred",
):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            try:
                if inspect.iscoroutinefunction(func):
                    data = await func(*args, **kwargs)
                else:
                    data = func(*args, **kwargs)

                return {
                    "success": True,
                    "message": success_message,
                    "data": data,
                    "error": None,
                }
            except HTTPException as http_ex:
                return JSONResponse(
                    status_code=http_ex.status_code,
                    content={
                        "success": False,
                        "message": error_message,
                        "data": None,
                        "error": http_ex.detail,
                    },
                )
            except Exception as e:
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content={
                        "success": False,
                        "message": error_message,
                        "data": None,
                        "error": str(e),
                    },
                )

        return wrapper

    return decorator
