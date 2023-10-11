"""seat_cursor

Revision ID: 7cf4cfb98216
Revises: b671ee08b4ec
Create Date: 2023-10-09 08:17:11.669909

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7cf4cfb98216"
down_revision: Union[str, None] = "b671ee08b4ec"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "seats",
        sa.Column(
            "row_col_cursor",
            sa.Integer(),
            sa.Computed(
                "(`row` * 10000) + `col`",
            ),
            nullable=False,
        ),
    )
    op.create_index(
        op.f("seats_row_col_cursor_idx"), "seats", ["row_col_cursor"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("seats_row_col_cursor_idx"), table_name="seats")
    op.drop_column("seats", "row_col_cursor")
    # ### end Alembic commands ###
