"""
The endpoints for creating, updating and deleting llamas.
"""
# pylint: disable=invalid-name

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from sqlalchemy.orm import Session

from data import llama_crud, llama_picture_crud
from data.database import get_db
from data.files import delete_llama_picture_file, write_llama_picture_to_file
from data.user_crud import get_current_user_from_api_token
from models.llama import LlamaId
from models.user import User

router = APIRouter(
    prefix="/llama/{llama_id}/picture",
    tags=["llama-picture"],
)


@router.post(
    path="",
    operation_id="create_llama_picture",
    status_code=status.HTTP_201_CREATED,
    response_model=LlamaId,
    responses={
        status.HTTP_201_CREATED: {"model": LlamaId, "description": "Llama picture created successfully"},
        status.HTTP_400_BAD_REQUEST: {"description": "The request body is empty"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid API token"},
        status.HTTP_403_FORBIDDEN: {
            "description": "Not authenticated. Send a valid API token in the Authorization header."
        },
        status.HTTP_404_NOT_FOUND: {"description": "Llama not found"},
        status.HTTP_409_CONFLICT: {"description": "Llama picture already exists"},
    },
    openapi_extra={
        "requestBody": {
            "content": {
                "image/png": {
                    "schema": {
                        "format": "binary",
                        "type": "string",
                    },
                },
            },
        },
    },
)
async def create_llama_picture(
    llama_id: Annotated[int, Path(description="The ID of the llama that this picture is for", examples=["1", "2"])],
    request: Request,
    _: Annotated[User, Depends(get_current_user_from_api_token)],
    db: Session = Depends(get_db),
) -> LlamaId:
    """
    Create a picture for a llama. The picture is sent as a PNG as binary data in the body of the request.
    """
    body = await request.body()

    # # If the request body is empty, return a 400
    if not body or len(body) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No llama picture sent")

    # Check the llama is valid
    db_llama = llama_crud.get_llama_by_id(db, llama_id)
    if db_llama is None:
        # If the llama does not exist, return a 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="LLama not found")

    # Check if the llama already has a picture
    db_picture = llama_picture_crud.get_llama_picture_by_id(db, llama_id)
    if db_picture is not None:
        # If the llama already has a picture, return a 409
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Llama already has a picture")

    # Write the bytes to a file
    try:
        file_path = write_llama_picture_to_file(llama_id, body)
    except Exception:  # pylint: disable=broad-except
        # pylint: disable=raise-missing-from
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Body is not a valid image")

    # Write the file path to the database
    llama_picture_crud.create_or_update_llama_picture(db, llama_id, file_path)

    return LlamaId(id=llama_id)


@router.put(
    path="",
    operation_id="update_llama_picture",
    status_code=status.HTTP_200_OK,
    response_model=LlamaId,
    responses={
        status.HTTP_200_OK: {"model": LlamaId, "description": "Llama picture created successfully"},
        status.HTTP_400_BAD_REQUEST: {"description": "The request body is empty"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid API token"},
        status.HTTP_403_FORBIDDEN: {
            "description": "Not authenticated. Send a valid API token in the Authorization header."
        },
        status.HTTP_404_NOT_FOUND: {"description": "Llama not found"},
    },
    openapi_extra={
        "requestBody": {
            "content": {
                "image/png": {
                    "schema": {
                        "format": "binary",
                        "type": "string",
                    },
                },
            },
        },
    },
)
async def update_llama_picture(
    llama_id: Annotated[int, Path(description="The ID of the llama that this picture is for", examples=["1", "2"])],
    request: Request,
    _: Annotated[User, Depends(get_current_user_from_api_token)],
    db: Session = Depends(get_db),
) -> LlamaId:
    """
    Update a picture for a llama. The picture is sent as a PNG as binary data in the body of the request.

    If the llama does not have a picture, one will be created. If the llama already has a picture,
     it will be overwritten.
    If the llama does not exist, a 404 will be returned.
    """
    body = await request.body()

    # # If the request body is empty, return a 400
    if not body or len(body) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No llama picture sent")

    # Check the llama is valid
    db_llama = llama_crud.get_llama_by_id(db, llama_id)
    if db_llama is None:
        # If the llama does not exist, return a 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="LLama not found")

    # Check if the llama already has a picture. If it does, delete it
    db_picture = llama_picture_crud.get_llama_picture_by_id(db, llama_id)
    if db_picture is not None:
        # If the llama already has a picture, delete it
        delete_llama_picture_file(db_picture.image_file_location)

    # Write the bytes to a file
    file_path = write_llama_picture_to_file(llama_id, body)

    # Write the file path to the database
    llama_picture_crud.create_or_update_llama_picture(db, llama_id, file_path)

    return LlamaId(id=llama_id)


@router.delete(
    path="",
    operation_id="delete_llama_picture",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Llama picture deleted successfully"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid API token"},
        status.HTTP_403_FORBIDDEN: {
            "description": "Not authenticated. Send a valid API token in the Authorization header."
        },
        status.HTTP_404_NOT_FOUND: {"description": "Llama or picture not found"},
    },
)
def delete_llama_picture(
    llama_id: Annotated[int, Path(description="The ID of the llama to delete the picture for", examples=["1", "2"])],
    _: Annotated[User, Depends(get_current_user_from_api_token)],
    db: Session = Depends(get_db),
) -> None:
    """
    Delete a llama's picture by ID.
    """
    # Check the llama is valid
    db_llama = llama_crud.get_llama_by_id(db, llama_id)
    if db_llama is None:
        # If the llama does not exist, return a 404
        raise HTTPException(status_code=404, detail="LLama not found")

    # Check the picture is valid
    db_picture = llama_picture_crud.get_llama_picture_by_id(db, llama_id)
    if db_picture is None:
        # If the picture does not exist, return a 404
        raise HTTPException(status_code=404, detail="Picture not found")

    # Delete the picture
    delete_llama_picture_file(db_picture.image_file_location)

    # Remove the picture from the database
    llama_picture_crud.delete_llama_picture(db, llama_id)
