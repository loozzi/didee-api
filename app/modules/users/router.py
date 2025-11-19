from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.decorators.response import response_handler
from app.core.schemas import ResponseModel
from app.modules.users import crud as crud_user
from app.db.session import get_db
from app.modules.users.schemas import User, UserCreate, UserUpdate

router = APIRouter()


@router.get("/", response_model=ResponseModel[List[User]])
@response_handler(message="Users retrieved successfully")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve users.
    """
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=ResponseModel[User], status_code=status.HTTP_201_CREATED)
@response_handler(message="User created successfully")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create new user.
    """
    # Check if user with email already exists
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Check if user with username already exists
    db_user = crud_user.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    return crud_user.create_user(db=db, user=user)


@router.get("/{user_id}", response_model=ResponseModel[User])
@response_handler(message="User retrieved successfully")
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get user by ID.
    """
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{user_id}", response_model=ResponseModel[User])
@response_handler(message="User updated successfully")
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    """
    Update a user.
    """
    db_user = crud_user.update_user(db, user_id=user_id, user_update=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/{user_id}", response_model=ResponseModel)
@response_handler(message="User deleted successfully")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user.
    """
    success = crud_user.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return None
