"""
The schema models used by the ORM to store data in the database.
"""
# pylint: disable=too-few-public-methods

from sqlalchemy import Column, Integer, String

from .database import Base


class DBSecretKey(Base):
    """
    A secret key used to sign JWTs.
    """

    __tablename__ = "secrets"

    secret_key = Column(String, primary_key=True)


class DBUser(Base):
    """
    A user of the llama store.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)


class DBLlama(Base):
    """
    A llama, with details of it's name, age, color, and rating from 1 to 5.
    """

    __tablename__ = "llamas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    age = Column(Integer, index=False, nullable=False)
    color = Column(String, index=False, nullable=False)
    rating = Column(Integer, index=False, nullable=False)


class DBLlamaPicture(Base):
    """
    A picture of a llama. Pictures are stored in the file system, not in the database.
    The database records the location of the picture.
    """

    __tablename__ = "llama_picture_locations"

    id = Column(Integer, primary_key=True, index=True)
    llama_id = Column(Integer, index=True)
    image_file_location = Column(String, index=False, nullable=False)
