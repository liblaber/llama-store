"""
Llama models. These are used by the llama endpoints.
"""
from enum import Enum

from pydantic import BaseModel


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

    id: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "1",
                }
            ],
            "description": "A llama id.",
        },
    }


class LlamaBase(BaseModel):
    """
    A base llama model, shared between create and get requests
    """

    name: str
    age: int
    color: LlamaColor
    rating: int

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

    id: int

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "1",
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
