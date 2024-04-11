"""
The endpoints for accessing users.
"""

# pylint: disable=invalid-name

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from data import user_crud
from data.database import get_db
from models.user import User, EMAIL_REGEX

# Create the router
router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.get(
    path="/{email}",
    operation_id="GetUserByEmail",
    response_model=User,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": User, "description": "User"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid API token"},
        status.HTTP_403_FORBIDDEN: {
            "description": "Not authenticated. Send a valid API token in the Authorization header."
        },
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
    },
)
def get_user_by_email(
    email: Annotated[
        str, Path(min_length=5, max_length=254, pattern=EMAIL_REGEX, description="The user's email address")
    ],
    current_user: Annotated[User, Depends(user_crud.get_current_user_from_api_token)],
    db: Session = Depends(get_db),
) -> User:
    """
    Get a user by email.

    This endpoint will return a 404 if the user does not exist. Otherwise, it will return a 200.
    """
    # Check that we are requesting our own user
    if current_user.email.lower() != email.lower():
        # If we are not requesting our own user, return a 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Get the user by email
    user = user_crud.get_user_by_email(db, email)
    if user is None:
        # If the user does not exist, return a 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # If the user exists, return a 200 with the user
    return user.model_dump()
