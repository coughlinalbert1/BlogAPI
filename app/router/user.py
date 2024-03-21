from fastapi import APIRouter, Depends
from ..schemas import UserBase, UserDisplay
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db import db_user
from ..auth.oauth2 import get_current_user
from typing import List

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

# Create user
@router.post('/', response_model=UserDisplay, status_code=201)
def user(request: UserBase, db: Session = Depends(get_db)) -> UserDisplay:
    """
    Create a new user in the database.

    Args:
        request (UserBase): The user data to be created.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        User: The created user.
    """
    return db_user.create_user(db, request)

# Read user
@router.get('/', response_model=List[UserDisplay])
def all_users(db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    """
    Get all users from the database.

    Args:
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        list[User]: A list of all users.
    """
    return db_user.get_all_users(db)

@router.get('/{id}', response_model=UserDisplay)
def single_user(id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)) -> UserDisplay:
    """
    Get a single user from the database.

    Args:
        id (int): The user id.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        User: The user with the given id.
    """
    return db_user.get_user(db, id)

# Update user
@router.post('/{id}')
def update_user(id: int, request: UserBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    """
    Update a user in the database.

    Args:
        id (int): The user id.
        request (UserBase): The user data to be updated.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        User: The updated user.
    """
    return db_user.update_user(db, id, request)

# Delete user
@router.delete('/{id}')
def delete(id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    """
    Delete a user from the database.

    Args:
        id (int): The user id.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Returns:
        str: A message indicating the user was deleted.
    """
    return db_user.delete_user(db, id)