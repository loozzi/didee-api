"""Common schema definitions"""

from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ResponseModel(BaseModel, Generic[T]):
    """Generic response model for API responses"""

    success: bool
    message: str
    data: Optional[T] = None
    error: Optional[str] = None
