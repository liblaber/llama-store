"""
This file contains the functions that will be used to interact with llamas in the database.
"""

# pylint: disable=invalid-name

from typing import List
from sqlalchemy.orm import Session

from data.schema import DBLlama
from models.llama import Llama, LlamaCreate


def get_db_llama_by_id(db: Session, llama_id: int) -> DBLlama:
    """
    Get a llama from the database by ID.

    :param Session db: The database session.
    :param int llama_id: The ID of the llama to get.
    :return: The llama with the given ID.
    :rtype: DBLlama
    """
    return db.query(DBLlama).filter(DBLlama.llama_id == llama_id).first()


def get_llama_by_id(db: Session, llama_id: int) -> Llama:
    """
    Get a llama by ID.

    :param Session db: The database session.
    :param int llama_id: The ID of the llama to get.
    :return: The llama with the given ID.
    :rtype: LLama
    """
    db_llama = get_db_llama_by_id(db, llama_id)
    return None if db_llama is None else Llama.model_validate(db_llama)


def get_llama_by_name(db: Session, llama_name: str) -> Llama:
    """
    Get a llama by name. Llama names muct be unique

    :param Session db: The database session.
    :param int llama_name: The name of the llama to get.
    :return: The llama with the given name.
    :rtype: LLama
    """
    db_llama = db.query(DBLlama).filter(DBLlama.name == llama_name).first()
    return None if db_llama is None else Llama.model_validate(db_llama)


def get_all_llamas(db: Session) -> List[Llama]:
    """
    Get all llamas.

    :param Session db: The database session.
    :return: All llamas.
    :rtype: List[Llama]
    """
    return list(map(Llama.model_validate, db.query(DBLlama).all()))


def create_llama(db: Session, llama: LlamaCreate) -> Llama:
    """
    Create a new llama.

    :param Session db: The database session.
    :param LlamaCreate llama: The llama to create.
    :return: The created llama.
    :rtype: Llama
    """
    db_llama = DBLlama(name=llama.name, age=llama.age, color=llama.color, rating=llama.rating)
    db.add(db_llama)
    db.commit()
    db.refresh(db_llama)
    return Llama.model_validate(db_llama)


def update_llama(db: Session, llama: LlamaCreate, llama_id: int) -> Llama:
    """
    Update a llama.

    :param Session db: The database session.
    :param Llama llama: The llama to update.
    :return: The updated llama.
    :rtype: Llama
    """
    db_llama = get_db_llama_by_id(db, llama_id)
    db_llama.name = llama.name
    db_llama.age = llama.age
    db_llama.color = llama.color
    db_llama.rating = llama.rating
    db.commit()
    db.refresh(db_llama)
    return Llama.model_validate(db_llama)


def delete_llama(db: Session, llama_id: int) -> None:
    """
    Delete a llama.

    :param Session db: The database session.
    :param int llama_id: The ID of the llama to delete.
    """
    db_llama = get_db_llama_by_id(db, llama_id)
    db.delete(db_llama)
    db.commit()
