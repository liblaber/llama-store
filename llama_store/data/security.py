"""
This file contains functions to help with API security. This includes password hashing, token creation
and token validation.
"""

# pylint: disable=invalid-name

from datetime import datetime, timedelta
from fastapi.security import HTTPBearer

from jose import jwt

from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from pydantic import BaseModel, constr

from models.user import EMAIL_REGEX

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# The password context to use for hashing and verifying passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# The bearer security scheme to use for authentication
bearer_scheme = HTTPBearer(scheme_name="Bearer", bearerFormat="JWT")


class TokenData(BaseModel):
    """
    A model to represent the data in a token.
    """

    email: constr(min_length=5, max_length=254, pattern=EMAIL_REGEX)


def verify_password(plain_password, hashed_password) -> bool:
    """
    Verify a password against the hashed password.

    :param str plain_password: The plain text password.
    :param str hashed_password: The hashed password.
    :return: Whether the password is correct.
    :rtype: bool
    """
    try:
        result = pwd_context.verify(plain_password, hashed_password)
        return result
    except UnknownHashError:
        return False


def get_password_hash(password) -> str:
    """
    Get the password hash for a password.

    :param str password: The password to hash.
    :return: The hashed password.
    :rtype: str
    """
    return pwd_context.hash(password)


def create_access_token(user_email: str, secret_key: str) -> str:
    """
    Create an access token for a user with an expiry time of 30 minutes.

    :param str user_email: The email of the user to create the token for.
    :param str secret_key: The secret key to use to sign the token.
    :return: The access token.
    :rtype: str
    """
    # The default token expiry time is 30 minutes
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Create the token with the user email and expiry time
    to_encode = {
        "sub": user_email,
        "exp": expire,
    }
    # Encode the token encoded with the secret key and algorithm
    return jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
