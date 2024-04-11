"""
The endpoints for accessing users.
"""

# pylint: disable=invalid-name

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from data import user_crud
from data.database import get_db
from data.security import create_access_token, verify_password
from models.token import APIToken, APITokenRequest

# Create the router
router = APIRouter(
    prefix="/token",
    tags=["Token"],
)


@router.post(
    path="",
    operation_id="CreateAPIToken",
    response_model=APIToken,
    status_code=201,
    responses={
        status.HTTP_201_CREATED: {"model": APIToken, "description": "A new API token for the user"},
        status.HTTP_404_NOT_FOUND: {"description": "User not found or the password is invalid"},
    },
)
def create_api_token(api_token_request: APITokenRequest, db: Session = Depends(get_db)) -> APIToken:
    """
    Create an API token for a user. These tokens expire after 30 minutes.

    Once you have this token, you need to pass it to other endpoints in the Authorization header as a Bearer token.
    """
    # Get the user by email
    user = user_crud.get_user_by_email(db, email=api_token_request.email)
    if user is None:
        # If the user does not exist, return a 404
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found or the password is invalid",
        )

    # If the user exists, verify the password
    if not verify_password(
        api_token_request.password,
        user_crud.get_user_password_by_email(db, email=api_token_request.email),
    ):
        # If the password is not correct, return a 404 - this way we are not susceptible to timing attacks
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found or the password is invalid",
        )

    # If the password is correct, return a 201 with the API token
    return APIToken(access_token=create_access_token(user.email, user_crud.get_secret_key(db)))
