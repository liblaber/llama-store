"""
Llama models. These are used by the llama endpoints.
"""

from enum import Enum

from pydantic import BaseModel, Field


class LlamaColor(str, Enum):
    """
    The color of a llama.
    """

    BROWN = "brown"
    WHITE = "white"
    BLACK = "black"
    GRAY = "gray"


class LlamaId(BaseModel):
    """
    A llama's ID. This is used as a response model when creating llama pictures.
    """

    llama_id: int = Field(description="The ID of the llama.", examples=[1])

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "llama_id": "1",
                }
            ],
            "description": "A llama id.",
        },
    }


class LlamaBase(BaseModel):
    """
    A base llama model, shared between create and get requests
    """

    name: str = Field(
        description="The name of the llama. This must be unique across all llamas.",
        examples=["libby the llama", "labby the llama"],
        max_length=100,
    )
    age: int = Field(
        description="The age of the llama in years.",
        examples=[5, 6, 7],
    )
    color: LlamaColor = Field(
        description="The color of the llama.",
        examples=["brown", "white", "black", "gray"],
    )
    rating: int = Field(
        description="The rating of the llama from 1 to 5.",
        examples=[1, 2, 3, 4, 5],
        ge=1,
        le=5,
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "libby the llama",
                    "age": 5,
                    "color": "brown",
                    "rating": 4,
                }
            ],
            "description": "A new llama for the llama store.",
        },
        "from_attributes": True,
    }


class LlamaCreate(LlamaBase):
    """
    A model to represent a llama creation request.
    """


class Llama(LlamaBase):
    """
    A llama, with details of it's name, age, color, and rating from 1 to 5.
    """

    llama_id: int = Field(description="The ID of the llama.", examples=[1])

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "llama_id": "1",
                    "name": "libby the llama",
                    "age": 5,
                    "color": "brown",
                    "rating": 4,
                }
            ],
            "description": "A llama, with details of its name, age, color, and rating from 1 to 5.",
        },
        "from_attributes": True,
    }
