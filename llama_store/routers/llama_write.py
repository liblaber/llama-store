"""
The endpoints for creating, updating and deleting llamas.
"""

# pylint: disable=invalid-name

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from data import llama_crud
from data.database import get_db
from data.user_crud import get_current_user_from_api_token

from models.llama import Llama, LlamaCreate
from models.user import User

router = APIRouter(
    prefix="/llama",
    tags=["llama"],
)


@router.post(
    path="",
    operation_id="create_llama",
    response_model=Llama,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": Llama, "description": "Llama created successfully"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid API token"},
        status.HTTP_403_FORBIDDEN: {
            "description": "Not authenticated. Send a valid API token in the Authorization header."
        },
        status.HTTP_409_CONFLICT: {"description": "Llama already exists"},
    },
)
def create_llama(
    llama: LlamaCreate,
    _: Annotated[User, Depends(get_current_user_from_api_token)],
    db: Session = Depends(get_db),
) -> Llama:
    """
    Create a new llama. Llama names must be unique.
    """
    # Check if the llama already exists
    existing_llama = llama_crud.get_llama_by_name(db, llama_name=llama.name)
    if existing_llama:
        # If the llama already exists, return a 409
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Llama named {llama.name} already exists")

    # Create the llama and return it
    return llama_crud.create_llama(db, llama)


@router.put(
    path="/{llama_id}",
    operation_id="update_llama",
    response_model=Llama,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_201_CREATED: {"model": Llama, "description": "New llama created successfully"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid API token"},
        status.HTTP_403_FORBIDDEN: {
            "description": "Not authenticated. Send a valid API token in the Authorization header."
        },
        status.HTTP_409_CONFLICT: {"description": "The llama name is already in use"},
    },
)
def update_llama(
    llama_id: Annotated[int, Path(description="The llama's ID", examples=["1", "2"])],
    llama: LlamaCreate,
    _: Annotated[User, Depends(get_current_user_from_api_token)],
    db: Session = Depends(get_db),
) -> Llama:
    """
    Update a llama. If the llama does not exist, create it.

    When updating a llama, the llama name must be unique. If the llama name is not unique, a 409 will be returned.
    """
    # Get the existing llama by name and Id
    existing_llama_by_id = llama_crud.get_llama_by_id(db, llama_id)
    existing_llama_by_name = llama_crud.get_llama_by_name(db, llama.name)

    # If neither exist, create a new llama and return it with a 201
    if existing_llama_by_id is None and existing_llama_by_name is None:
        return JSONResponse(status_code=201, content=llama_crud.create_llama(db, llama).model_dump())

    # If the llama doesn't exist by Id, and a different llama has the same name, return a 409
    if existing_llama_by_id is None and existing_llama_by_name is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Llama named {llama.name} already exists")

    # If the llama exists by Id, and a different llama has the same name, return a 409
    if (
        existing_llama_by_id is not None
        and existing_llama_by_name is not None
        and existing_llama_by_id.id != existing_llama_by_name.id
    ):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Llama named {llama.name} already exists")

    return llama_crud.update_llama(db, llama, llama_id)


@router.delete(
    path="/{llama_id}",
    operation_id="delete_llama",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Llama deleted successfully"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid API token"},
        status.HTTP_403_FORBIDDEN: {
            "description": "Not authenticated. Send a valid API token in the Authorization header."
        },
        status.HTTP_404_NOT_FOUND: {"description": "Llama not found"},
    },
)
def delete_llama(
    llama_id: Annotated[int, Path(description="The llama's ID", examples=["1", "2"])],
    _: Annotated[User, Depends(get_current_user_from_api_token)],
    db: Session = Depends(get_db),
) -> None:
    """
    Delete a llama. If the llama does not exist, this will return a 404.
    """
    # Get the llama by Id
    db_llama = llama_crud.get_llama_by_id(db, llama_id)

    # If the llama does not exist, return a 404
    if db_llama is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="LLama not found")

    # Delete the llama and return a 204
    llama_crud.delete_llama(db, llama_id)
