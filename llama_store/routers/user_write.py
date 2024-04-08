"""
The endpoints for accessing users.
"""

# pylint: disable=invalid-name

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from data import user_crud
from data.database import get_db
from models.user import User, UserRegistration

# Create the router
router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.post(
    path="",
    operation_id="RegisterUser",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": User, "description": "User registered successfully"},
        status.HTTP_400_BAD_REQUEST: {"description": "User already registered"},
    },
)
def register_user(user_registration: UserRegistration, db: Session = Depends(get_db)) -> User:
    """
    Register a new user.

    This endpoint will return a 400 if the user already exists. Otherwise, it will return a 201.
    """
    # Check if the user already exists by getting the user by email
    existing_user = user_crud.get_user_by_email(db, email=user_registration.email)
    if existing_user:
        # If the user already exists, return a 400
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already registered")

    # Delete old users - this will stop the database from getting too big
    user_crud.delete_old_users(db)

    # If the user does not exist, create the user and return a 201 with the user
    return user_crud.create_user(db, user_registration)
