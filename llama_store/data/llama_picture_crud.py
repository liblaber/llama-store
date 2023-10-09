"""
This file contains the functions that will be used to interact with llamas in the database.
"""
# pylint: disable=invalid-name

from sqlalchemy.orm import Session

from data.schema import DBLlamaPicture
from models.llama_picture import LlamaPicture


def get_db_llama_picture_by_id(db: Session, llama_id: int) -> DBLlamaPicture:
    """
    Get a llama picture by ID from the database as a database record.

    :param Session db: The database session.
    :param int llama_picture_id: The ID of the llama picture to get.
    :return: The llama picture with the given ID.
    :rtype: DBLlamaPicture
    """
    return db.query(DBLlamaPicture).filter(DBLlamaPicture.llama_id == llama_id).first()


def get_llama_picture_by_id(db: Session, llama_id: int) -> LlamaPicture:
    """
    Get a llama picture by ID from the database.

    :param Session db: The database session.
    :param int llama_picture_id: The ID of the llama picture to get.
    :return: The llama picture with the given ID.
    :rtype: DBLlamaPicture
    """
    db_llama_picture = get_db_llama_picture_by_id(db, llama_id)
    return None if db_llama_picture is None else LlamaPicture.model_validate(db_llama_picture)


def create_or_update_llama_picture(db: Session, llama_id: int, file_path: str) -> LlamaPicture:
    """
    Create a new llama picture. If one already exists for this llama, overwrite it.

    :param Session db: The database session.
    :param int llama_id: The ID of the llama.
    :param str file_path: The path to the llama picture file.
    :return: The llama picture.
    :rtype: LlamaPicture
    """
    # Get the llama picture from the database
    db_llama_picture = get_db_llama_picture_by_id(db, llama_id)

    # If the llama picture does not exist, create it
    if db_llama_picture is None:
        db_llama_picture = DBLlamaPicture(llama_id=llama_id, image_file_location=file_path)
        db.add(db_llama_picture)
        db.commit()
    else:
        # If the llama picture does exist, update it
        db_llama_picture.image_file_location = file_path
        db.commit()

    # Refresh the llama picture from the database
    db.refresh(db_llama_picture)
    return LlamaPicture.model_validate(db_llama_picture)


def delete_llama_picture(db: Session, llama_picture_id: int) -> None:
    """
    Delete a llama picture.

    :param Session db: The database session.
    :param int llama_picture_id: The ID of the llama picture to delete.
    """
    db_llama_picture = get_db_llama_picture_by_id(db, llama_picture_id)
    db.delete(db_llama_picture)
    db.commit()
