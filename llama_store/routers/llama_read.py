"""
The endpoints for reading llamas.
"""

# pylint: disable=invalid-name

from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from data import llama_crud
from data.database import get_db
from data.user_crud import get_current_user_from_api_token

from models.llama import Llama
from models.user import User

router = APIRouter(
    prefix="/llama",
    tags=["Llama"],
)


@router.get(
    path="",
    operation_id="GetLlamas",
    response_model=List[Llama],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": List[Llama], "description": "Llamas"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid API token"},
        status.HTTP_403_FORBIDDEN: {
            "description": "Not authenticated. Send a valid API token in the Authorization header."
        },
    },
)
def get_llamas(
    _: Annotated[User, Depends(get_current_user_from_api_token)], db: Session = Depends(get_db)
) -> List[Llama]:
    """
    Get all the llamas.
    """
    # Get all the llamas from the database
    return llama_crud.get_all_llamas(db)


@router.get(
    path="/{llama_id}",
    operation_id="GetLlamaByID",
    response_model=Llama,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": List[Llama], "description": "Llamas"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid API token"},
        status.HTTP_403_FORBIDDEN: {
            "description": "Not authenticated. Send a valid API token in the Authorization header."
        },
        status.HTTP_404_NOT_FOUND: {"description": "Llama not found"},
    },
)
def get_llama(
    llama_id: Annotated[int, Path(description="The llama's ID", examples=["1", "2"])],
    _: Annotated[User, Depends(get_current_user_from_api_token)],
    db: Session = Depends(get_db),
) -> Llama:
    """
    Get a llama by ID.
    """
    # Get the llama from the database by ID
    llama = llama_crud.get_llama_by_id(db, llama_id)
    if llama is None:
        # If the llama does not exist, return a 404
        raise HTTPException(status_code=404, detail="Llama not found")
    # Return the llama
    return llama
