"""empty message

Revision ID: 8b0af4942743
Revises: 
Create Date: 2023-09-29 01:15:55.669005

"""
# pylint: disable=invalid-name,no-member
import secrets
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8b0af4942743"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


ALL_LLAMAS = [
    {
        "id": 1,
        "name": "Libby the Llama",
        "age": 3,
        "color": "white",
        "rating": 5,
    },
    {
        "id": 2,
        "name": "Labby the Llama",
        "age": 5,
        "color": "gray",
        "rating": 4,
    },
    {
        "id": 3,
        "name": "Sean the fake Llama",
        "age": 18,
        "color": "white",
        "rating": 1,
    },
    {
        "id": 4,
        "name": "Logo the Llama logo",
        "age": 2,
        "color": "black",
        "rating": 5,
    },
    {
        "id": 5,
        "name": "Barack O'Llama",
        "age": 4,
        "color": "black",
        "rating": 5,
    },
    {
        "id": 6,
        "name": "Llama Del Rey",
        "age": 9,
        "color": "white",
        "rating": 4,
    },
]


def upgrade() -> None:
    """
    Upgrade the database to the latest revision.
    """
    # Create the tables
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String, nullable=False, unique=True, index=True),
        sa.Column("hashed_password", sa.String, nullable=False),
    )

    op.create_table(
        "secrets",
        sa.Column("secret_key", sa.String, primary_key=True),
    )

    secret_key = secrets.token_hex(32)
    op.execute(f"INSERT INTO secrets VALUES ('{secret_key}')")

    llamas_table = op.create_table(
        "llamas",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False, unique=True, index=True),
        sa.Column("age", sa.Integer, nullable=False),
        sa.Column("color", sa.String, nullable=False),
        sa.Column("rating", sa.Integer, nullable=False),
    )

    llama_pictures_table = op.create_table(
        "llama_picture_locations",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("llama_id", sa.Integer, nullable=False, unique=True, index=True),
        sa.Column("image_file_location", sa.String, nullable=False),
    )

    # Create data
    op.bulk_insert(llamas_table, ALL_LLAMAS)

    root = ".appdata/llama_store_data/pictures"

    def get_llama_insert(llama_id: int) -> dict:
        return {
            "id": llama_id,
            "llama_id": llama_id,
            "image_file_location": f"{root}/{llama_id}.png",
        }

    op.bulk_insert(
        llama_pictures_table,
        [
            get_llama_insert(1),
            get_llama_insert(2),
            get_llama_insert(3),
            get_llama_insert(4),
            get_llama_insert(5),
            get_llama_insert(6),
        ],
    )


def downgrade() -> None:
    """
    Downgrade the database to the previous revision.
    """
