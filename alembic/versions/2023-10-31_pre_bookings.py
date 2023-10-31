"""pre_bookings

Revision ID: a3d493eaca16
Revises: c4a20d3e43ff
Create Date: 2023-10-31 23:31:49.045837

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3d493eaca16'
down_revision: Union[str, None] = 'c4a20d3e43ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pre_bookings',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('schedule_id', sa.Uuid(), nullable=False),
    sa.Column('performance_id', sa.Uuid(), nullable=False),
    sa.Column('snowflake_id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['performance_id'], ['performances.id'], name=op.f('pre_bookings_performance_id_fkey')),
    sa.ForeignKeyConstraint(['schedule_id'], ['schedules.id'], name=op.f('pre_bookings_schedule_id_fkey')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('pre_bookings_user_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('pre_bookings_pkey'))
    )
    op.create_index(op.f('pre_bookings_id_idx'), 'pre_bookings', ['id'], unique=False)
    op.create_index(op.f('pre_bookings_snowflake_id_idx'), 'pre_bookings', ['snowflake_id'], unique=False)
    op.create_table('pre_booking_seat_association',
    sa.Column('pre_booking_id', sa.Uuid(), nullable=False),
    sa.Column('seat_id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['pre_booking_id'], ['pre_bookings.id'], name=op.f('pre_booking_seat_association_pre_booking_id_fkey')),
    sa.ForeignKeyConstraint(['seat_id'], ['seats.id'], name=op.f('pre_booking_seat_association_seat_id_fkey')),
    sa.PrimaryKeyConstraint('pre_booking_id', 'seat_id', name=op.f('pre_booking_seat_association_pkey'))
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pre_booking_seat_association')
    op.drop_index(op.f('pre_bookings_snowflake_id_idx'), table_name='pre_bookings')
    op.drop_index(op.f('pre_bookings_id_idx'), table_name='pre_bookings')
    op.drop_table('pre_bookings')
    # ### end Alembic commands ###
