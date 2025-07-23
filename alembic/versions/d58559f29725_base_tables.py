"""base tables

Revision ID: d58559f29725
Revises: 
Create Date: 2025-07-23 11:16:31.667580

"""
from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'd58559f29725'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("hashed_password", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("email", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("full_name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("disabled", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(op.f("ix_user_email"), "user", ["username"], unique=True)

    op.create_table(
        "timespan",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("start_time", sa.DateTime, nullable=False),
        sa.Column("end_time", sa.DateTime, nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("note", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("tags", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("user")
