"""performance_content

Revision ID: acfac32d3e3f
Revises: f1ddd4e65fc6
Create Date: 2023-10-04 07:18:09.860004

"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import mysql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "acfac32d3e3f"
down_revision: Union[str, None] = "f1ddd4e65fc6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "performance_contents",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("performance_id", sa.Uuid(), nullable=False),
        sa.Column("sequence", sa.Integer(), nullable=False),
        sa.Column("heading", sa.String(length=256), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["performance_id"],
            ["performances.id"],
            name=op.f("performance_contents_performance_id_fkey"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("performance_contents_pkey")),
        sa.UniqueConstraint(
            "performance_id",
            "sequence",
            name=op.f("performance_contents_performance_id_key"),
        ),
    )
    op.create_index(
        op.f("performance_contents_id_idx"),
        "performance_contents",
        ["id"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("permissions", mysql.JSON(), nullable=True))
    op.drop_index(
        op.f("performance_contents_id_idx"), table_name="performance_contents"
    )
    op.drop_table("performance_contents")
    # ### end Alembic commands ###
