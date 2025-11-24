"""User schemas"""

from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base user schema"""

    email: EmailStr
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    phone_number: Optional[str] = None


class UserCreate(UserBase):
    """User creation schema"""

    firebase_uid: str
    provider: str


class UserUpdate(BaseModel):
    """User update schema"""

    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    phone_number: Optional[str] = None


class UserResponse(UserBase):
    """User response schema"""

    id: str
    firebase_uid: str
    provider: str
    created_at: str
    updated_at: str

    class Config:  # pylint: disable=too-few-public-methods
        """Pydantic config"""

        from_attributes = True


class TokenVerifyRequest(BaseModel):
    """Firebase token verification request"""

    firebase_token: str


class TokenVerifyResponse(BaseModel):
    """Firebase token verification response"""

    message: str
    user: Optional[UserResponse] = None
    is_new_user: bool = False
