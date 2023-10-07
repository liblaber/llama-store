"""
This file contains the functions that will be used to interact with users in the database.
"""
# pylint: disable=invalid-name

from typing import Annotated, List
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

from sqlalchemy.orm import Session

from data.schema import DBSecretKey, DBUser
from data.database import SessionLocal, get_db
from data.security import ALGORITHM, bearer_scheme, get_password_hash
from models.user import User


def get_user(db: Session, user_id: int) -> User | None:
    """
    Get a user by ID.

    :param Session db: The database session.
    :param int user_id: The ID of the user to get.
    :return: The user with the given ID.
    :rtype: User
    """
    # Get the user by ID. This field is unique, so there should only be one.
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    return None if db_user is None else User.model_validate(db_user)


def get_all_users(db: Session) -> List[User]:
    """
    Get all users.

    :param Session db: The database session.
    :return: All users.
    :rtype: List[User]
    """
    # Get all users. This should not be exposed to the API, but is useful for testing.
    return list(map(User.model_validate, db.query(DBUser).all()))


def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Get a user by email.

    :param Session db: The database session.
    :param str email: The email of the user to get.
    :return: The user with the given email.
    :rtype: User
    """
    # Get the first user that matches the email. This field is unique, so there should only be one.
    db_user = db.query(DBUser).filter(DBUser.email == email.lower()).first()
    return None if db_user is None else User.model_validate(db_user)


def get_user_password_by_email(db: Session, email: str) -> str | None:
    """
    Get the password for a user by email.

    :param Session db: The database session.
    :param str email: The email of the user to get.
    :return: The users password
    :rtype: str
    """
    # Get the first user that matches the email. This field is unique, so there should only be one.
    db_user = db.query(DBUser).filter(DBUser.email == email.lower()).first()
    return None if db_user is None else db_user.hashed_password


def create_user(db: Session, user: User) -> User:
    """
    Create a new user.

    :param Session db: The database session.
    :param User user: The user to create.
    :return: The created user.
    :rtype: User
    """
    # Hash the password
    hashed_password = get_password_hash(user.password)
    # Create the user with the hashed password
    db_user = DBUser(email=user.email.lower(), hashed_password=hashed_password)
    # Add the user to the database
    db.add(db_user)
    db.commit()
    # Refresh the user to get the ID
    db.refresh(db_user)
    # Return the user
    return User.model_validate(db_user)


# The maximum number of users to keep in the database
MAXIMUM_USERS = 1000


def delete_old_users(db: Session) -> None:
    """
    Delete users except the latest MAXIMUM_USERS. This will stop the database getting too large.

    :param Session db: The database session.
    """
    # Delete users with an ID less than the highest minus the MAXIMUM_USERS
    latest_user = db.query(DBUser).order_by(DBUser.id.desc()).first()

    # If we don't have any users, return
    if latest_user is None:
        return

    # Delete users with an ID less than the highest minus the MAXIMUM_USERS
    minimum_user_id = latest_user.id - MAXIMUM_USERS
    db.query(DBUser).filter(DBUser.id < minimum_user_id).delete()
    db.commit()


def get_secret_key(db: Session) -> str:
    """
    Get the secret key from the database.

    :param Session db: The database session.
    :return: The secret key.
    :rtype: str
    """
    # Get the first secret key. This field is unique, so there should only be one.
    db_secret_key = db.query(DBSecretKey).first()
    # Return the secret key
    return db_secret_key.secret_key


def get_current_user_from_api_token(
    token: Annotated[str, Depends(bearer_scheme)], db: SessionLocal = Depends(get_db)
) -> User:
    """
    Get the current user from the access token. If the user does not exist, raise an exception.

    :param str token: The access token.
    :param SessionLocal db: The database session.
    :return: The current user.
    :rtype: User
    """
    # Define an exception if the user is not valid for the token
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decode the token
        payload = jwt.decode(token.credentials, get_secret_key(db), algorithms=[ALGORITHM])
        # Get the user email from the token
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception  # pylint: disable=raise-missing-from

    # Load the user from the database
    user = get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception

    # Return the user
    return user
