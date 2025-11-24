"""User CRUD operations"""

from typing import Optional

from sqlalchemy.orm import Session

from app.models.user import User
from app.modules.users.schemas import UserCreate, UserUpdate


def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_firebase_uid(db: Session, firebase_uid: str) -> Optional[User]:
    """Get user by Firebase UID"""
    return db.query(User).filter(User.firebase_uid == firebase_uid).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user_data: UserCreate) -> User:
    """Create a new user"""
    user = User(
        firebase_uid=user_data.firebase_uid,
        email=user_data.email,
        full_name=user_data.full_name,
        avatar_url=user_data.avatar_url,
        phone_number=user_data.phone_number,
        provider=user_data.provider,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user_id: str, user_data: UserUpdate) -> Optional[User]:
    """Update user information"""
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    update_data = user_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: str) -> bool:
    """Delete a user"""
    user = get_user_by_id(db, user_id)
    if not user:
        return False

    db.delete(user)
    db.commit()
    return True
