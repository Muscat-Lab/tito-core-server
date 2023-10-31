"""content_info

Revision ID: 96c4d9e42e6e
Revises: 76fc2c4b1586
Create Date: 2023-10-23 06:44:20.109136

"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import mysql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "96c4d9e42e6e"
down_revision: Union[str, None] = "76fc2c4b1586"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "performance_contents", sa.Column("showtime_info", sa.Text(), nullable=True)
    )
    op.add_column(
        "performance_contents",
        sa.Column("casting_schedule", mysql.JSON(), nullable=True),
    )
    op.add_column(
        "performance_contents", sa.Column("discount_info", mysql.JSON(), nullable=True)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("performance_contents", "discount_info")
    op.drop_column("performance_contents", "casting_schedule")
    op.drop_column("performance_contents", "showtime_info")
    # ### end Alembic commands ###
