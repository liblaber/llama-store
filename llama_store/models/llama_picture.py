"""
Llama models. These are used by the llama endpoints.
"""

from pydantic import BaseModel


class LlamaPicture(BaseModel):
    """
    A link to a file containing a picture of a llama.
    """

    llama_picture_id: int
    llama_id: int
    image_file_location: str

    model_config = {
        "from_attributes": True,
    }
