"""
User models. These are used by the user endpoints.
"""
# pylint: disable=duplicate-code

import re
from typing import Annotated
from pydantic import BaseModel, StringConstraints, validator

EMAIL_REGEX = r".+\@.+\..+"
PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")


class UserBase(BaseModel):
    """
    A base user class, shared between create and get requests
    """

    email: Annotated[str, StringConstraints(min_length=5, max_length=254, pattern=EMAIL_REGEX)]


class UserRegistration(UserBase):
    """
    A model to represent a user registration request. This includes the password,
    a field not returned when you request the user.

    The password must be at least 8 characters long, and contain at least one letter,
    one number, and one special character.
    """

    password: Annotated[str, StringConstraints(min_length=8, max_length=254)]

    @validator("password")
    def passwords_match(cls, v, values, **kwargs):  # pylint: disable=unused-argument,no-self-argument,invalid-name
        """
        Validate that the password matches a regex - one uppercase, one lower, one number,
        one special character
        This is implemented here as a validator, not a regex, as Pydantic doesn't work with
        look forward/look back regexes (whatever those are)
        """
        assert PASSWORD_REGEX.match(v) is not None, (
            "Password must be at least 8 characters long, and contain at least "
            "one letter, one number, and one special character"
        )
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "noone@example.com",
                    "password": "Password123!",
                }
            ],
            "description": "A new user of the llama store.",
        },
        "from_attributes": True,
    }


class User(UserBase):
    """
    A user of the llama store. The password is not returned.
    """

    id: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "1",
                    "email": "noone@example.com",
                }
            ],
            "description": "A user of the llama store",
        },
        "from_attributes": True,
    }
