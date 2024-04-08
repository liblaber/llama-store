"""
User models. These are used by the user endpoints.
"""

# pylint: disable=duplicate-code

from pydantic import BaseModel, ConfigDict, Field
from models.user import UserRegistration


class APITokenRequest(UserRegistration):
    """
    A model to represent an API token request. The email and password must match an existing user.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "email": "noone@example.com",
                    "password": "Password123!",
                }
            ],
            "description": "A request to get an API token for a given user.",
        },
        from_attributes=True,
    )


class APIToken(BaseModel):
    """
    A model to represent a new API token returned by the /token endpoint.
    This token is used to authenticate requests, and expires after 30 minutes.
    """

    access_token: str = Field(
        description="The bearer token to use with the API. Pass this in the Authorization header as a bearer token.",
        examples=["Authorization: Bearer 1234567890abcdef"],
        alias="accessToken",
        title="Access Token",
    )

    token_type: str = Field(
        default="bearer",
        description="The type of token. This will always be bearer.",
        examples=["bearer"],
        alias="tokenType",
        title="Token Type",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "accessToken": "1234567890abcdef",
                    "tokenType": "bearer",
                }
            ],
            "description": "An API token to use for authentication.",
        },
        from_attributes=True,
        populate_by_name=True,
    )
