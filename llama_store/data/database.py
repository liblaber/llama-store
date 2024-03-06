"""
Code to interact with the SQLite database
"""

# pylint: disable=invalid-name

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./.appdata/sql_app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> SessionLocal:
    """
    Get a database session.

    :return: A database session.
    :rtype: SessionLocal
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
