"""
The endpoints for accessing users for debug mode.
"""

# pylint: disable=invalid-name

from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from data import user_crud
from data.database import get_db
from models.user import User

# Create the router
router = APIRouter(
    prefix="/user",
    tags=["User"],
)


# If we are running in debug mode, add the get all users endpoint
@router.get(path="", operation_id="GetAllUsers", response_model=List[User], status_code=status.HTTP_200_OK)
def get_all_users(db: Session = Depends(get_db)) -> List[User]:
    """
    Get all users.

    This endpoint will return a 200 with a list of all users. This only works in debug mode.
    """
    # Get all users
    return user_crud.get_all_users(db)
