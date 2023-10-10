"""
The endpoints for reading llama picturess.
"""
# pylint: disable=invalid-name

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from data import llama_picture_crud
from data.database import get_db
from data.user_crud import get_current_user_from_api_token

from models.user import User

router = APIRouter(
    prefix="/llama/{llama_id}/picture",
    tags=["llama-picture"],
)


@router.get(
    path="",
    operation_id="get_llama_picture_by_llama_id",
    response_class=FileResponse,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "content": {"image/png": {}},
            "description": "Llamas",
        },
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid API token"},
        status.HTTP_403_FORBIDDEN: {
            "description": "Not authenticated. Send a valid API token in the Authorization header."
        },
        status.HTTP_404_NOT_FOUND: {"description": "Llama or llama picture not found"},
    },
)
def get_llama_picture(
    llama_id: Annotated[int, Path(description="The ID of the llama to get the picture for", examples=["1", "2"])],
    _: Annotated[User, Depends(get_current_user_from_api_token)],
    db: Session = Depends(get_db),
) -> FileResponse:
    """
    Get a llama's picture by the llama ID. Pictures are in PNG format.
    """
    # Check the llama is valid
    db_picture = llama_picture_crud.get_llama_picture_by_id(db, llama_id)
    if db_picture is None:
        # If the llama does not exist, return a 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="LLama picture not found")

    # Return the llama picture from the file system
    return FileResponse(path=db_picture.image_file_location, media_type="image/png")
