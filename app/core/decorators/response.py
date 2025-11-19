import inspect
from functools import wraps
from typing import Any, Callable

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse


def response_handler(message: str = "Operation successful"):
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
                    "message": message,
                    "data": data,
                }
            except HTTPException as http_ex:
                return JSONResponse(
                    status_code=http_ex.status_code,
                    content={
                        "success": False,
                        "message": http_ex.detail,
                        "data": None,
                    },
                )
            except Exception as e:
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content={
                        "success": False,
                        "message": str(e),
                        "data": None,
                    },
                )

        return wrapper

    return decorator
